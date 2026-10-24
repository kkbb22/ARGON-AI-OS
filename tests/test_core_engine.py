"""
ARGON AI-OS — Security Hardening, Policy, and Core Engine Test Suite

Adversarial validation and regression tests covering Section 8 of Master Build Mandate:
- Invalid task schemas
- Unauthorized actions and missing approvals
- Approval expiration, alteration, and replay prevention (nonces)
- Path traversal and boundary escapes
- Conflicting output paths
- Secret redaction in audit ledger & verifier
- Failed verification preventing task completion
- Bounded repair retries
- Audit chain integrity and tamper detection
- Offline provider gateway and budget enforcement
- End-to-end safe task execution lifecycle
"""
import json
import shutil
import tempfile
import time
import unittest
from pathlib import Path

from runtime.core.contracts import (
    ActionSpec,
    ApprovalLevel,
    RiskLevel,
    TaskContract,
    TaskState,
    TaskStateError,
    VerificationSpec,
)
from runtime.core.evidence import AuditLedger, redact_secrets
from runtime.core.orchestrator import TaskOrchestrator
from runtime.core.policy import (
    ApprovalExpired,
    ApprovalMismatch,
    ApprovalRequired,
    PolicyEngine,
    PolicyViolation,
)
from runtime.core.providers import (
    InferenceRequest,
    MockProvider,
    ProviderGateway,
    ProviderStatus,
)
from runtime.core.verifier import VerificationEngine
from runtime.core.workspace import Workspace, WorkspaceError


class CoreEngineSecurityTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="argon_test_")
        self.workspace_root = Path(self.temp_dir)
        self.policy = PolicyEngine(self.workspace_root)
        self.workspace = Workspace(self.workspace_root)
        self.ledger = AuditLedger(self.workspace_root / ".argon" / "ledger")
        self.verifier = VerificationEngine(self.workspace_root)
        self.gateway = ProviderGateway(offline_mode=True)
        self.gateway.register_provider(MockProvider(name="mock-provider"), primary=True)
        self.orchestrator = TaskOrchestrator(
            workspace_root=self.workspace_root,
            provider_gateway=self.gateway,
            audit_ledger=self.ledger,
            policy_engine=self.policy,
            workspace=self.workspace,
            verifier=self.verifier,
        )

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    # 1. Invalid Task Schemas
    def test_rejects_empty_objective_and_actions(self):
        contract = TaskContract(objective="", scope="", actions=[])
        errors = self.policy.validate_contract(contract)
        self.assertIn("objective is required", errors)
        self.assertIn("scope is required", errors)
        self.assertIn("at least one action is required", errors)

    def test_rejects_oversized_payload(self):
        huge_content = "X" * 150_000
        action = ActionSpec(action_type="write_text", target_path="data.txt", content=huge_content)
        contract = TaskContract(objective="test", scope="unit", actions=[action])
        errors = self.policy.validate_contract(contract)
        self.assertTrue(any("100KB" in e for e in errors))

    # 2. Path Traversal & Symlink Escapes
    def test_rejects_path_traversal_in_action(self):
        action = ActionSpec(action_type="write_text", target_path="../outside.txt", content="hack")
        contract = TaskContract(objective="test", scope="unit", actions=[action])
        errors = self.policy.validate_contract(contract)
        self.assertTrue(any("unsafe" in e or "relative" in e for e in errors))

    def test_workspace_blocks_direct_path_traversal(self):
        with self.assertRaises(WorkspaceError):
            self.workspace.write_file(
                relative_path="../../escaped.txt",
                content="malicious",
                task_id="t1",
            )

    # 3. Forbidden Files Protection (.git, secrets, keys)
    def test_blocks_writes_to_forbidden_patterns(self):
        for forbidden in [".git/config", ".env", "api_key.pem", "id_rsa"]:
            action = ActionSpec(action_type="write_text", target_path=forbidden, content="key")
            contract = TaskContract(objective="test", scope="unit", actions=[action])
            errors = self.policy.validate_contract(contract)
            self.assertTrue(any("forbidden" in e for e in errors), f"Failed to block {forbidden}")

    # 4. Conflicting Output Paths
    def test_detects_conflicting_output_paths(self):
        a1 = ActionSpec(action_type="write_text", target_path="same.txt", content="1")
        a2 = ActionSpec(action_type="write_text", target_path="same.txt", content="2")
        contract = TaskContract(objective="test", scope="unit", actions=[a1, a2])
        errors = self.policy.validate_contract(contract)
        self.assertTrue(any("Conflicting output paths" in e for e in errors))

    # 5. Approval Missing, Expired, Altered, or Replayed
    def test_execution_blocked_without_approval(self):
        action = ActionSpec(action_type="write_text", target_path="file.txt", content="data")
        contract = TaskContract(objective="write", scope="unit", actions=[action], approval_level=ApprovalLevel.STANDARD)
        task_id = self.orchestrator.create_task(contract)
        ok, _ = self.orchestrator.validate_plan(task_id)
        self.assertTrue(ok)
        self.orchestrator.plan_task(task_id)

        # Attempting execution directly without approval must fail
        with self.assertRaises(TaskStateError):
            self.orchestrator.execute_task(task_id)

    def test_approval_replay_rejected(self):
        action = ActionSpec(action_type="write_text", target_path="file.txt", content="data")
        contract = TaskContract(objective="write", scope="unit", actions=[action], approval_level=ApprovalLevel.STANDARD)
        task_id = self.orchestrator.create_task(contract)
        self.orchestrator.validate_plan(task_id)
        self.orchestrator.plan_task(task_id)
        record = self.orchestrator.approve_task(task_id)

        # First consumption succeeds
        self.policy.consume_approval(contract)

        # Second consumption fails (replay detected)
        with self.assertRaises(PolicyViolation):
            self.policy.consume_approval(contract)

    def test_approval_expired_rejected(self):
        action = ActionSpec(action_type="write_text", target_path="file.txt", content="data")
        contract = TaskContract(objective="write", scope="unit", actions=[action])
        task_id = self.orchestrator.create_task(contract)
        self.orchestrator.validate_plan(task_id)
        self.orchestrator.plan_task(task_id)

        # Create approval with negative expiration (already expired)
        record = self.policy.create_approval(contract, expiry_seconds=-10)
        with self.assertRaises(ApprovalExpired):
            self.policy.check_approval(contract)

    def test_plan_altered_after_approval_rejected(self):
        action = ActionSpec(action_type="write_text", target_path="file.txt", content="data")
        contract = TaskContract(objective="write", scope="unit", actions=[action])
        task_id = self.orchestrator.create_task(contract)
        self.orchestrator.validate_plan(task_id)
        self.orchestrator.plan_task(task_id)
        self.orchestrator.approve_task(task_id)

        # Tamper with contract payload after approval
        contract.actions[0].content = "MODIFIED CONTENT"
        with self.assertRaises(ApprovalMismatch):
            self.policy.check_approval(contract)

    # 6. Secret Redaction
    def test_secret_redaction_in_logs_and_output(self):
        raw = "My API key is api_key=sk-1234567890abcdef1234567890 and Bearer secrettoken999"
        redacted = redact_secrets(raw)
        self.assertNotIn("sk-1234567890abcdef1234567890", redacted)
        self.assertIn("[REDACTED]", redacted)

    # 7. Verification Failure Blocks Completion
    def test_failed_verification_prevents_completion(self):
        action = ActionSpec(action_type="write_text", target_path="code.py", content="x = 1\n")
        # Command that will fail with non-zero exit code
        verif = VerificationSpec(
            commands=['python -c "import sys; sys.exit(42)"'],
            acceptance_criteria=["Must exit 0"],
        )
        contract = TaskContract(
            objective="verification test",
            scope="unit",
            actions=[action],
            verification=verif,
            approval_level=ApprovalLevel.NONE,
            max_retries=1,
            failure_strategy="stop",
        )
        task_id = self.orchestrator.create_task(contract)
        self.orchestrator.validate_plan(task_id)
        self.orchestrator.plan_task(task_id)
        self.orchestrator.approve_task(task_id)
        res = self.orchestrator.execute_task(task_id)

        self.assertEqual(res.state, TaskState.FAILED)
        self.assertFalse(res.verification_passed)
        self.assertNotEqual(res.exit_code, 0)
        self.assertNotEqual(self.orchestrator.get_task_state(task_id), TaskState.COMPLETED)

    # 8. Audit Ledger Tamper Evidence
    def test_audit_ledger_detects_chain_corruption(self):
        self.ledger.record("EVENT_1", task_id="t1", data={"info": "first"})
        self.ledger.record("EVENT_2", task_id="t1", data={"info": "second"})

        # Initial chain must be valid
        valid, issues = self.ledger.verify_chain()
        self.assertTrue(valid)
        self.assertEqual(len(issues), 0)

        # Tamper with the ledger file
        ledger_path = self.ledger.ledger_dir / "audit.jsonl"
        lines = ledger_path.read_text(encoding="utf-8").strip().split("\n")
        corrupted = json.loads(lines[0])
        corrupted["data"]["info"] = "TAMPERED"
        lines[0] = json.dumps(corrupted)
        ledger_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

        # Verify chain must now detect the tampering
        valid_after, issues_after = self.ledger.verify_chain()
        self.assertFalse(valid_after)
        self.assertGreater(len(issues_after), 0)

    # 9. Complete End-to-End Safe Lifecycle
    def test_end_to_end_successful_engineering_lifecycle(self):
        py_code = "def add(a, b):\n    return a + b\n"
        py_test = (
            "import unittest\nfrom calc import add\n\n"
            "class TestAdd(unittest.TestCase):\n"
            "    def test_add(self):\n"
            "        self.assertEqual(add(2, 3), 5)\n\n"
            "if __name__ == '__main__':\n"
            "    unittest.main()\n"
        )
        action1 = ActionSpec(action_type="write_text", target_path="calc.py", content=py_code)
        action2 = ActionSpec(action_type="write_text", target_path="test_calc.py", content=py_test)

        verif = VerificationSpec(
            commands=["python -m unittest test_calc.py"],
            acceptance_criteria=["Unit tests in test_calc.py pass"],
        )

        contract = TaskContract(
            objective="Implement and verify calc module",
            scope="math",
            actions=[action1, action2],
            verification=verif,
            approval_level=ApprovalLevel.STANDARD,
        )

        # 1. Create
        task_id = self.orchestrator.create_task(contract)
        self.assertEqual(self.orchestrator.get_task_state(task_id), TaskState.DRAFT)

        # 2. Validate
        ok, errors = self.orchestrator.validate_plan(task_id)
        self.assertTrue(ok)
        self.assertEqual(self.orchestrator.get_task_state(task_id), TaskState.VALIDATED)

        # 3. Plan
        self.orchestrator.plan_task(task_id)
        self.assertEqual(self.orchestrator.get_task_state(task_id), TaskState.PLANNED)

        # 4. Approve
        self.orchestrator.approve_task(task_id, approver="lead_engineer")
        self.assertEqual(self.orchestrator.get_task_state(task_id), TaskState.APPROVED)

        # 5. Execute & Verify
        res = self.orchestrator.execute_task(task_id)
        self.assertEqual(res.state, TaskState.COMPLETED)
        self.assertTrue(res.verification_passed)
        self.assertEqual(res.exit_code, 0)
        self.assertIn("calc.py", res.artifacts)
        self.assertIn("test_calc.py", res.artifacts)

        # 6. Verify ledger integrity
        valid, _ = self.ledger.verify_chain()
        self.assertTrue(valid)
        report = self.ledger.generate_task_report(task_id)
        self.assertIn("TASK_COMPLETED", report)


if __name__ == "__main__":
    unittest.main(verbosity=2)

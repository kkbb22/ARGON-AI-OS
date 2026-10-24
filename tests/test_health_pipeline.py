"""
ARGON AI-OS — ARGON Health Pipeline Test Suite

Verifies that the AI-OS engineering machine correctly compiles,
approves, executes, and independently verifies an ARGON Health
clinical vertical slice while enforcing:
- Tenant isolation
- Data safety (synthetic data only, no PHI)
- Verification criteria pass
- Full tamper-evident audit record generated
"""
import shutil
import tempfile
import unittest
from pathlib import Path

from runtime.core.contracts import TaskState
from runtime.core.health_pipeline import HealthEngineeringPipeline
from runtime.core.orchestrator import TaskOrchestrator
from runtime.core.providers import MockProvider, ProviderGateway


class TestHealthEngineeringPipeline(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="argon_health_test_")
        self.workspace_root = Path(self.temp_dir)
        gateway = ProviderGateway(offline_mode=True)
        gateway.register_provider(MockProvider(name="mock-health"), primary=True)
        self.orchestrator = TaskOrchestrator(
            workspace_root=self.workspace_root,
            provider_gateway=gateway,
        )
        self.pipeline = HealthEngineeringPipeline(self.orchestrator)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_health_vertical_slice_lifecycle(self):
        # 1. Create clinical vertical slice contract
        contract = self.pipeline.create_patient_intake_slice_contract(tenant_id="tenant_amman_01")
        self.assertEqual(contract.metadata.get("domain"), "ARGON_HEALTH")
        self.assertTrue(contract.metadata.get("phi_scrubbed"))

        # 2. Ingest into orchestrator (DRAFT)
        task_id = self.orchestrator.create_task(contract)
        self.assertEqual(self.orchestrator.get_task_state(task_id), TaskState.DRAFT)

        # 3. Validate against security policies
        ok, errors = self.orchestrator.validate_plan(task_id)
        self.assertTrue(ok, f"Validation failed: {errors}")
        self.assertEqual(self.orchestrator.get_task_state(task_id), TaskState.VALIDATED)

        # 4. Plan and approve
        self.orchestrator.plan_task(task_id)
        self.orchestrator.approve_task(task_id, approver="chief_medical_informaticist")
        self.assertEqual(self.orchestrator.get_task_state(task_id), TaskState.APPROVED)

        # 5. Execute in isolated sandbox and run verification tests
        result = self.orchestrator.execute_task(task_id)
        self.assertEqual(result.state, TaskState.COMPLETED)
        self.assertTrue(result.verification_passed)
        self.assertEqual(result.exit_code, 0)
        self.assertIn("health_patient_intake.py", result.artifacts)
        self.assertIn("test_health_patient_intake.py", result.artifacts)

        # 6. Verify audit trail integrity
        valid, issues = self.orchestrator.ledger.verify_chain()
        self.assertTrue(valid, f"Ledger issues: {issues}")
        report = self.orchestrator.ledger.generate_task_report(task_id)
        self.assertIn("health_patient_intake.py", report)
        self.assertIn("VERIFICATION_EXECUTED", report)


if __name__ == "__main__":
    unittest.main(verbosity=2)

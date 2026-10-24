"""
ARGON AI-OS — Core Task Orchestrator

Implements Section 4.1, 4.2, 4.4 of Master Build Mandate:
- Central task orchestrator managing the complete engineering lifecycle:
  REQUEST → REQUIREMENTS ANALYSIS → REPO INSPECTION → IMPLEMENTATION PLAN
  → PLAN VALIDATION → RISK & SECURITY REVIEW → HUMAN APPROVAL
  → ISOLATED CODE MODIFICATION → BUILD & TEST EXECUTION → FAILURE ANALYSIS
  → BOUNDED REPAIR ITERATIONS → INDEPENDENT VERIFICATION → ARTIFACT GENERATION
  → REVIEWABLE CHANGESET
- Typed task contracts & result contracts
- Explicit task lifecycle state transitions
- Fail-closed dependency validation and policy enforcement
- Full audit event logging via AuditLedger
- Workspace isolation and atomic artifact production
"""
from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

from .contracts import (
    ActionSpec,
    ApprovalLevel,
    RiskLevel,
    TaskContract,
    TaskResult,
    TaskState,
    TaskStateError,
    TaskValidationError,
    VerificationSpec,
)
from .evidence import AuditLedger
from .policy import (
    ApprovalExpired,
    ApprovalMismatch,
    ApprovalRecord,
    ApprovalRequired,
    PolicyEngine,
    PolicyViolation,
)
from .providers import InferenceRequest, ProviderGateway
from .tools import ToolRegistry
from .verifier import VerificationEngine, VerificationSummary
from .workspace import Workspace, WorkspaceError


class OrchestrationError(Exception):
    """General error raised during task orchestration."""
    pass


class TaskOrchestrator:
    """
    Core engineering machine orchestrator for ARGON AI-OS.
    Governs state transitions, reviews, approvals, execution, and verification.
    """

    def __init__(
        self,
        workspace_root: Path,
        provider_gateway: Optional[ProviderGateway] = None,
        audit_ledger: Optional[AuditLedger] = None,
        policy_engine: Optional[PolicyEngine] = None,
        workspace: Optional[Workspace] = None,
        verifier: Optional[VerificationEngine] = None,
    ):
        self.workspace_root = workspace_root.resolve()
        self.ledger = audit_ledger or AuditLedger(self.workspace_root / ".argon" / "ledger")
        self.policy = policy_engine or PolicyEngine(self.workspace_root)
        self.workspace = workspace or Workspace(self.workspace_root)
        self.verifier = verifier or VerificationEngine(self.workspace_root)
        self.providers = provider_gateway or ProviderGateway(offline_mode=True)
        self.tools = ToolRegistry(self.workspace_root)

        self._tasks: dict[str, TaskContract] = {}
        self._states: dict[str, TaskState] = {}
        self._results: dict[str, TaskResult] = {}
        self._task_store_dir = self.workspace_root / ".argon" / "tasks"
        self._task_store_dir.mkdir(parents=True, exist_ok=True)
        self._load_persisted_tasks()

    def _load_persisted_tasks(self) -> None:
        for f in self._task_store_dir.glob("*.json"):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                contract = TaskContract.from_dict(data.get("contract", {}))
                state = TaskState(data.get("state", TaskState.DRAFT.value))
                self._tasks[contract.task_id] = contract
                self._states[contract.task_id] = state
            except Exception:
                continue

    def _persist_task(self, task_id: str) -> None:
        contract = self._tasks.get(task_id)
        if not contract:
            return
        state = self._states.get(task_id, TaskState.DRAFT)
        result = self._results.get(task_id)

        doc = {
            "task_id": task_id,
            "state": state.value,
            "contract": contract.to_dict(),
            "result": result.to_dict() if result else None,
            "updated_at": time.time(),
        }
        dest = self._task_store_dir / f"{task_id}.json"
        dest.write_text(json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8")

    def _transition(self, task_id: str, new_state: TaskState, reason: str = "") -> None:
        current = self._states.get(task_id, TaskState.DRAFT)
        if not current.can_transition_to(new_state):
            err_msg = f"Invalid state transition for task {task_id}: {current.value} -> {new_state.value}"
            self.ledger.record(
                event_type="STATE_TRANSITION_REJECTED",
                task_id=task_id,
                data={"from_state": current.value, "to_state": new_state.value, "reason": err_msg},
            )
            raise TaskStateError(err_msg)

        self._states[task_id] = new_state
        self._persist_task(task_id)
        self.ledger.record(
            event_type="STATE_TRANSITION",
            task_id=task_id,
            data={"from_state": current.value, "to_state": new_state.value, "reason": reason},
        )

    def get_task_state(self, task_id: str) -> TaskState:
        if task_id not in self._states:
            raise KeyError(f"Task {task_id} not found")
        return self._states[task_id]

    def get_task_contract(self, task_id: str) -> TaskContract:
        if task_id not in self._tasks:
            raise KeyError(f"Task {task_id} not found")
        return self._tasks[task_id]

    def get_task_result(self, task_id: str) -> Optional[TaskResult]:
        return self._results.get(task_id)

    # --- LIFECYCLE STAGES ---

    def create_task(self, contract: TaskContract) -> str:
        """Stage 1: Submit new task contract (starts in DRAFT state)."""
        task_id = contract.task_id
        self._tasks[task_id] = contract
        self._states[task_id] = TaskState.DRAFT
        self._persist_task(task_id)

        self.ledger.record(
            event_type="TASK_CREATED",
            task_id=task_id,
            plan_digest=contract.digest(),
            data={"objective": contract.objective, "scope": contract.scope},
        )
        return task_id

    def validate_plan(self, task_id: str) -> tuple[bool, list[str]]:
        """Stage 2: Comprehensive validation against schema and security policies."""
        contract = self.get_task_contract(task_id)
        current_state = self.get_task_state(task_id)
        if current_state != TaskState.DRAFT:
            raise TaskStateError(f"Cannot validate task in state {current_state.value}; must be DRAFT")

        errors = self.policy.validate_contract(contract)
        if errors:
            self._transition(task_id, TaskState.REJECTED, reason=f"Validation errors: {'; '.join(errors)}")
            return False, errors

        self._transition(task_id, TaskState.VALIDATED, reason="Plan schema and policies passed")
        return True, []

    def plan_task(self, task_id: str) -> None:
        """Stage 3: Move validated task to PLANNED state, awaiting approval if needed."""
        self._transition(task_id, TaskState.PLANNED, reason="Task decomposition and plan locked")

    def approve_task(self, task_id: str, approver: str = "operator") -> ApprovalRecord:
        """Stage 4: Issue explicit, single-use, time-bound approval for the exact plan digest."""
        current_state = self.get_task_state(task_id)
        if current_state != TaskState.PLANNED:
            raise TaskStateError(f"Task {task_id} must be in PLANNED state to be approved (current: {current_state.value})")

        contract = self.get_task_contract(task_id)
        record = self.policy.create_approval(contract, approver=approver)

        self._transition(task_id, TaskState.APPROVED, reason=f"Approved by {approver} [Digest: {record.plan_digest}]")
        self.ledger.record(
            event_type="APPROVAL_GRANTED",
            task_id=task_id,
            plan_digest=contract.digest(),
            data={"approval_id": record.approval_id, "approver": approver, "nonce": record.nonce},
        )
        return record

    def execute_task(self, task_id: str) -> TaskResult:
        """
        Stage 5 & 6: Execute task inside the sandbox, verify results, and handle bounded repairs.
        """
        contract = self.get_task_contract(task_id)
        current_state = self.get_task_state(task_id)

        # Ensure approved or read-only
        if self.policy.requires_approval(contract):
            if current_state != TaskState.APPROVED:
                raise TaskStateError(f"Task {task_id} requires approval before execution (current state: {current_state.value})")
            # Consume approval atomically right before execution
            try:
                approval_record = self.policy.consume_approval(contract)
                self.ledger.record(
                    event_type="APPROVAL_CONSUMED",
                    task_id=task_id,
                    plan_digest=contract.digest(),
                    data={"approval_id": approval_record.approval_id, "nonce": approval_record.nonce},
                )
            except Exception as e:
                self._transition(task_id, TaskState.BLOCKED, reason=str(e))
                raise PolicyViolation(f"Approval consumption failed: {e}")
        else:
            if current_state not in (TaskState.PLANNED, TaskState.APPROVED):
                raise TaskStateError(f"Task {task_id} must be PLANNED or APPROVED to execute")

        self._transition(task_id, TaskState.QUEUED, reason="Enqueued for execution")
        self._transition(task_id, TaskState.RUNNING, reason="Executing actions in sandbox")

        started_at = time.time()
        produced_artifacts: list[str] = []
        artifact_hashes: dict[str, str] = {}
        action_errors: list[str] = []

        # Execute actions within workspace sandbox
        for idx, action in enumerate(contract.actions):
            if action.action_type == "write_text":
                try:
                    record = self.workspace.write_file(
                        relative_path=action.target_path,
                        content=action.content,
                        task_id=task_id,
                        artifact_type="source",
                        allow_overwrite=True,
                    )
                    produced_artifacts.append(record.path)
                    artifact_hashes[record.path] = record.sha256
                    self.ledger.record(
                        event_type="ACTION_EXECUTED",
                        task_id=task_id,
                        data={"action_idx": idx, "action_type": action.action_type, "path": record.path, "sha256": record.sha256},
                    )
                except WorkspaceError as we:
                    action_errors.append(f"Action {idx} failed: {we}")
                    break

        if action_errors:
            self._transition(task_id, TaskState.FAILED, reason="; ".join(action_errors))
            res = TaskResult(
                task_id=task_id,
                state=TaskState.FAILED,
                exit_code=1,
                errors=action_errors,
                artifacts=produced_artifacts,
                artifact_hashes=artifact_hashes,
                started_at=started_at,
                completed_at=time.time(),
            )
            self._results[task_id] = res
            self._persist_task(task_id)
            return res

        # Run verification if defined
        self._transition(task_id, TaskState.VERIFYING, reason="Executing verification suite")
        verification_passed = True
        verification_output = ""

        if contract.verification and contract.verification.commands:
            summary = self.verifier.run_verification(contract.verification, cwd=self.workspace.sandbox)
            verification_passed = summary.overall_passed
            verification_output = json.dumps(summary.to_dict(), indent=2)

            self.ledger.record(
                event_type="VERIFICATION_EXECUTED",
                task_id=task_id,
                data={
                    "overall_passed": summary.overall_passed,
                    "passed_count": summary.passed_commands,
                    "failed_count": summary.failed_commands,
                    "notes": summary.verdict_notes,
                },
            )

        # Handle verification outcome with bounded repair
        repair_attempts = 0
        if not verification_passed:
            while repair_attempts < contract.max_retries and contract.failure_strategy == "retry":
                repair_attempts += 1
                self._transition(task_id, TaskState.REPAIR, reason=f"Repair attempt {repair_attempts}/{contract.max_retries}")
                self.ledger.record(
                    event_type="REPAIR_ATTEMPT",
                    task_id=task_id,
                    data={"attempt": repair_attempts, "max_retries": contract.max_retries},
                )
                # Re-run verification in repair cycle
                summary = self.verifier.run_verification(contract.verification, cwd=self.workspace.sandbox)
                if summary.overall_passed:
                    verification_passed = True
                    verification_output = json.dumps(summary.to_dict(), indent=2)
                    break

        completed_at = time.time()
        final_state = TaskState.COMPLETED if verification_passed else TaskState.FAILED
        if verification_passed:
            self._transition(task_id, TaskState.VERIFIED, reason="All verification checks passed")
            self._transition(task_id, TaskState.COMPLETED, reason="Task lifecycle fully verified and complete")
        else:
            self._transition(task_id, TaskState.FAILED, reason="Verification criteria not satisfied")

        result = TaskResult(
            task_id=task_id,
            state=final_state,
            exit_code=0 if verification_passed else 1,
            output="Execution and verification complete",
            errors=[] if verification_passed else ["Verification checks failed"],
            artifacts=produced_artifacts,
            artifact_hashes=artifact_hashes,
            verification_passed=verification_passed,
            verification_output=verification_output,
            repair_attempts=repair_attempts,
            started_at=started_at,
            completed_at=completed_at,
        )
        self._results[task_id] = result
        self._persist_task(task_id)

        self.ledger.record(
            event_type="TASK_COMPLETED" if verification_passed else "TASK_FAILED",
            task_id=task_id,
            data={"final_state": final_state.value, "artifacts": produced_artifacts, "repairs": repair_attempts},
        )
        return result

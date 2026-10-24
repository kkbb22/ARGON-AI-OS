"""
ARGON AI-OS — Task Contracts and State Machine

Typed task contracts, lifecycle states, dependency tracking, and result contracts.
This is the foundation of the orchestration engine.
"""
from __future__ import annotations

import enum
import hashlib
import json
import time
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import PurePosixPath
from typing import Any, Optional


class TaskState(enum.Enum):
    """Canonical task lifecycle states."""
    DRAFT = "DRAFT"
    VALIDATED = "VALIDATED"
    PLANNED = "PLANNED"
    APPROVED = "APPROVED"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    REPAIR = "REPAIR"
    VERIFYING = "VERIFYING"
    VERIFIED = "VERIFIED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"

    def can_transition_to(self, target: TaskState) -> bool:
        """Check if this state can transition to the target state."""
        return target in _ALLOWED_TRANSITIONS.get(self, set())


# Explicit allowed state transitions — fail-closed design
_ALLOWED_TRANSITIONS: dict[TaskState, set[TaskState]] = {
    TaskState.DRAFT: {TaskState.VALIDATED, TaskState.REJECTED, TaskState.CANCELLED},
    TaskState.VALIDATED: {TaskState.PLANNED, TaskState.REJECTED, TaskState.CANCELLED},
    TaskState.PLANNED: {TaskState.APPROVED, TaskState.REJECTED, TaskState.CANCELLED},
    TaskState.APPROVED: {TaskState.QUEUED, TaskState.CANCELLED},
    TaskState.QUEUED: {TaskState.RUNNING, TaskState.BLOCKED, TaskState.CANCELLED},
    TaskState.RUNNING: {TaskState.VERIFYING, TaskState.FAILED, TaskState.PAUSED, TaskState.CANCELLED},
    TaskState.PAUSED: {TaskState.RUNNING, TaskState.CANCELLED},
    TaskState.FAILED: {TaskState.REPAIR, TaskState.CANCELLED},
    TaskState.BLOCKED: {TaskState.QUEUED, TaskState.CANCELLED},
    TaskState.REPAIR: {TaskState.RUNNING, TaskState.CANCELLED, TaskState.FAILED},
    TaskState.VERIFYING: {TaskState.VERIFIED, TaskState.FAILED},
    TaskState.VERIFIED: {TaskState.COMPLETED},
    # Terminal states — no outgoing transitions
    TaskState.COMPLETED: set(),
    TaskState.CANCELLED: set(),
    TaskState.REJECTED: set(),
}


class RiskLevel(enum.Enum):
    """Risk classification for tasks and actions."""
    READ_ONLY = "READ_ONLY"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ApprovalLevel(enum.Enum):
    """Required approval level for a task."""
    NONE = "NONE"            # Read-only, no approval needed
    STANDARD = "STANDARD"    # Normal approval flow
    ELEVATED = "ELEVATED"    # Requires explicit human review
    CRITICAL = "CRITICAL"    # Requires full evidence + human sign-off


@dataclass
class ActionSpec:
    """Specification for a single action within a task."""
    action_type: str                     # e.g., "write_text", "run_test", "lint"
    target_path: str                     # Relative POSIX path
    content: str = ""                    # Content for write actions
    command: str = ""                    # Command for execution actions
    timeout_seconds: int = 300           # Default 5-minute timeout
    risk_level: RiskLevel = RiskLevel.READ_ONLY
    requires_approval: bool = False
    read_only: bool = True
    allowed_scope: list[str] = field(default_factory=list)

    def validate(self) -> list[str]:
        """Return list of validation errors."""
        errors = []
        if not self.action_type:
            errors.append("action_type is required")
        if self.action_type == "write_text":
            if not self.target_path:
                errors.append("target_path required for write_text")
            else:
                try:
                    p = PurePosixPath(self.target_path)
                    if p.is_absolute():
                        errors.append("target_path must be relative")
                    if any(part in ("", ".", "..") for part in p.parts):
                        errors.append("target_path contains unsafe components")
                    if "\\" in self.target_path:
                        errors.append("target_path must use forward slashes")
                except Exception as e:
                    errors.append(f"Invalid target_path: {e}")
            if not isinstance(self.content, str):
                errors.append("content must be a string")
            elif len(self.content.encode("utf-8")) > 100_000:
                errors.append("content exceeds 100KB limit")
            self.read_only = False
            if self.risk_level == RiskLevel.READ_ONLY:
                self.risk_level = RiskLevel.LOW
        if self.action_type in ("run_test", "lint", "type_check"):
            self.read_only = True
        if self.timeout_seconds < 1 or self.timeout_seconds > 3600:
            errors.append("timeout must be between 1 and 3600 seconds")
        return errors


@dataclass
class VerificationSpec:
    """Specification for verifying a task's outputs."""
    commands: list[str] = field(default_factory=list)       # Commands to run
    acceptance_criteria: list[str] = field(default_factory=list)
    required_exit_code: int = 0
    timeout_seconds: int = 600

    def validate(self) -> list[str]:
        errors = []
        if not self.commands:
            errors.append("At least one verification command is required")
        if self.timeout_seconds < 1 or self.timeout_seconds > 3600:
            errors.append("verification timeout must be between 1 and 3600 seconds")
        return errors


@dataclass
class TaskContract:
    """
    Complete typed contract for a task.
    Every task in the system must have a validated contract before execution.
    """
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    parent_id: Optional[str] = None
    objective: str = ""
    scope: str = ""
    inputs: list[str] = field(default_factory=list)
    expected_outputs: list[str] = field(default_factory=list)
    allowed_paths: list[str] = field(default_factory=list)
    allowed_tools: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    actions: list[ActionSpec] = field(default_factory=list)
    verification: Optional[VerificationSpec] = None
    risk_level: RiskLevel = RiskLevel.READ_ONLY
    approval_level: ApprovalLevel = ApprovalLevel.NONE
    max_retries: int = 3
    timeout_seconds: int = 1800
    failure_strategy: str = "stop"       # "stop", "retry", "skip"
    recovery_plan: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)

    def validate(self) -> list[str]:
        """Full contract validation — returns list of errors."""
        errors = []
        if not self.objective:
            errors.append("objective is required")
        if not self.scope:
            errors.append("scope is required")
        if not self.actions:
            errors.append("at least one action is required")
        if len(self.actions) > 50:
            errors.append("maximum 50 actions per task")
        for i, action in enumerate(self.actions):
            for err in action.validate():
                errors.append(f"action[{i}]: {err}")
        if self.verification:
            for err in self.verification.validate():
                errors.append(f"verification: {err}")
        if self.max_retries < 0 or self.max_retries > 10:
            errors.append("max_retries must be between 0 and 10")
        if self.timeout_seconds < 1 or self.timeout_seconds > 86400:
            errors.append("task timeout must be between 1 and 86400 seconds")
        if self.failure_strategy not in ("stop", "retry", "skip"):
            errors.append("failure_strategy must be stop, retry, or skip")
        # Compute effective risk and approval from actions
        action_risks = [a.risk_level for a in self.actions]
        if action_risks:
            max_risk = max(action_risks, key=lambda r: list(RiskLevel).index(r))
            if list(RiskLevel).index(max_risk) > list(RiskLevel).index(self.risk_level):
                self.risk_level = max_risk
        # Set approval level based on risk
        if self.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL):
            if self.approval_level == ApprovalLevel.NONE:
                self.approval_level = ApprovalLevel.ELEVATED
        return errors

    def digest(self) -> str:
        """SHA-256 digest of the canonical contract representation."""
        canonical = json.dumps(
            self.to_dict(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
        return hashlib.sha256(canonical).hexdigest()

    def to_dict(self) -> dict:
        """Serialize contract to a dictionary, suitable for JSON."""
        d = {}
        d["task_id"] = self.task_id
        d["parent_id"] = self.parent_id
        d["objective"] = self.objective
        d["scope"] = self.scope
        d["inputs"] = self.inputs
        d["expected_outputs"] = self.expected_outputs
        d["allowed_paths"] = self.allowed_paths
        d["allowed_tools"] = self.allowed_tools
        d["dependencies"] = self.dependencies
        d["actions"] = [
            {
                "action_type": a.action_type,
                "target_path": a.target_path,
                "content": a.content,
                "command": a.command,
                "timeout_seconds": a.timeout_seconds,
                "risk_level": a.risk_level.value,
                "requires_approval": a.requires_approval,
                "read_only": a.read_only,
            }
            for a in self.actions
        ]
        if self.verification:
            d["verification"] = {
                "commands": self.verification.commands,
                "acceptance_criteria": self.verification.acceptance_criteria,
                "required_exit_code": self.verification.required_exit_code,
                "timeout_seconds": self.verification.timeout_seconds,
            }
        else:
            d["verification"] = None
        d["risk_level"] = self.risk_level.value
        d["approval_level"] = self.approval_level.value
        d["max_retries"] = self.max_retries
        d["timeout_seconds"] = self.timeout_seconds
        d["failure_strategy"] = self.failure_strategy
        d["created_at"] = self.created_at
        return d

    @classmethod
    def from_dict(cls, data: dict) -> TaskContract:
        """Deserialize from dictionary."""
        actions = [
            ActionSpec(
                action_type=a["action_type"],
                target_path=a.get("target_path", ""),
                content=a.get("content", ""),
                command=a.get("command", ""),
                timeout_seconds=a.get("timeout_seconds", 300),
                risk_level=RiskLevel(a.get("risk_level", "READ_ONLY")),
                requires_approval=a.get("requires_approval", False),
                read_only=a.get("read_only", True),
            )
            for a in data.get("actions", [])
        ]
        verification = None
        if data.get("verification"):
            v = data["verification"]
            verification = VerificationSpec(
                commands=v.get("commands", []),
                acceptance_criteria=v.get("acceptance_criteria", []),
                required_exit_code=v.get("required_exit_code", 0),
                timeout_seconds=v.get("timeout_seconds", 600),
            )
        return cls(
            task_id=data.get("task_id", str(uuid.uuid4())),
            parent_id=data.get("parent_id"),
            objective=data.get("objective", ""),
            scope=data.get("scope", ""),
            inputs=data.get("inputs", []),
            expected_outputs=data.get("expected_outputs", []),
            allowed_paths=data.get("allowed_paths", []),
            allowed_tools=data.get("allowed_tools", []),
            dependencies=data.get("dependencies", []),
            actions=actions,
            verification=verification,
            risk_level=RiskLevel(data.get("risk_level", "READ_ONLY")),
            approval_level=ApprovalLevel(data.get("approval_level", "NONE")),
            max_retries=data.get("max_retries", 3),
            timeout_seconds=data.get("timeout_seconds", 1800),
            failure_strategy=data.get("failure_strategy", "stop"),
            recovery_plan=data.get("recovery_plan", ""),
            metadata=data.get("metadata", {}),
            created_at=data.get("created_at", time.time()),
        )


@dataclass
class TaskResult:
    """Result of a task execution."""
    task_id: str
    state: TaskState
    exit_code: Optional[int] = None
    output: str = ""
    errors: list[str] = field(default_factory=list)
    artifacts: list[str] = field(default_factory=list)
    artifact_hashes: dict[str, str] = field(default_factory=dict)
    verification_passed: Optional[bool] = None
    verification_output: str = ""
    repair_attempts: int = 0
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    evidence: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "state": self.state.value,
            "exit_code": self.exit_code,
            "output": self.output,
            "errors": self.errors,
            "artifacts": self.artifacts,
            "artifact_hashes": self.artifact_hashes,
            "verification_passed": self.verification_passed,
            "verification_output": self.verification_output,
            "repair_attempts": self.repair_attempts,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }


class TaskStateError(Exception):
    """Raised when an invalid state transition is attempted."""
    pass


class TaskValidationError(Exception):
    """Raised when a task contract fails validation."""
    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__(f"Validation failed: {'; '.join(errors)}")

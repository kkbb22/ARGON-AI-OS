"""
ARGON AI-OS — Approval and Policy Engine

Implements:
- Canonical plan hashing
- Plan-change detection
- Exact-action + exact-payload approval (per H-04)
- Single-use, time-bound approval records
- Replay prevention via nonces
- Fail-closed behavior
- Auditable approval/rejection events
"""
from __future__ import annotations

import hashlib
import json
import os
import secrets
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Any

from .contracts import TaskContract, TaskState, ApprovalLevel, RiskLevel


class PolicyViolation(Exception):
    """Raised when a policy check fails."""
    pass


class ApprovalRequired(Exception):
    """Raised when an action requires approval that hasn't been granted."""
    pass


class ApprovalExpired(Exception):
    """Raised when an approval has expired."""
    pass


class ApprovalMismatch(Exception):
    """Raised when the plan changed after approval."""
    pass


@dataclass
class ApprovalRecord:
    """
    A single-use, time-bound approval for a specific task and payload.
    Per H-04: exact-action + exact-payload scope.
    """
    approval_id: str = field(default_factory=lambda: secrets.token_hex(16))
    task_id: str = ""
    plan_digest: str = ""           # SHA-256 of the canonical plan
    nonce: str = field(default_factory=lambda: secrets.token_hex(8))
    approver: str = "local-operator"
    issued_at: float = field(default_factory=time.time)
    expires_at: float = 0.0         # Unix timestamp
    consumed: bool = False
    consumed_at: Optional[float] = None
    scope: str = ""                 # Bound scope description
    decision: str = "PENDING"       # PENDING, APPROVED, REJECTED, CONSUMED, EXPIRED

    def __post_init__(self):
        if self.expires_at == 0.0:
            # Per H-04: short expiry, default 5 minutes
            self.expires_at = self.issued_at + 300

    def is_valid(self) -> bool:
        """Check if this approval is currently valid."""
        if self.consumed:
            return False
        if self.decision != "APPROVED":
            return False
        if time.time() > self.expires_at:
            return False
        return True

    def consume(self) -> None:
        """Consume this approval — single use only."""
        if not self.is_valid():
            raise PolicyViolation("Cannot consume invalid approval")
        self.consumed = True
        self.consumed_at = time.time()
        self.decision = "CONSUMED"

    def to_dict(self) -> dict:
        return {
            "approval_id": self.approval_id,
            "task_id": self.task_id,
            "plan_digest": self.plan_digest,
            "nonce": self.nonce,
            "approver": self.approver,
            "issued_at": self.issued_at,
            "expires_at": self.expires_at,
            "consumed": self.consumed,
            "consumed_at": self.consumed_at,
            "scope": self.scope,
            "decision": self.decision,
        }

    @classmethod
    def from_dict(cls, data: dict) -> ApprovalRecord:
        rec = cls(
            approval_id=data.get("approval_id", secrets.token_hex(16)),
            task_id=data.get("task_id", ""),
            plan_digest=data.get("plan_digest", ""),
            nonce=data.get("nonce", secrets.token_hex(8)),
            approver=data.get("approver", "local-operator"),
            issued_at=data.get("issued_at", time.time()),
            expires_at=data.get("expires_at", 0.0),
            consumed=data.get("consumed", False),
            consumed_at=data.get("consumed_at"),
            scope=data.get("scope", ""),
            decision=data.get("decision", "PENDING"),
        )
        return rec


# --- Forbidden patterns and policies ---

# File patterns that must never be written or modified
FORBIDDEN_PATTERNS = [
    ".git/",
    ".env",
    "*.pem",
    "*.key",
    "*.p12",
    "id_rsa",
    "id_ed25519",
    "credentials.json",
    "secrets.json",
    "token.json",
    ".approval.json",  # approval records are managed internally only
]

# Commands that must never be auto-executed
FORBIDDEN_COMMANDS = [
    "rm -rf",
    "del /s",
    "format",
    "mkfs",
    "git push",
    "git merge",
    "npm publish",
    "pip install",  # needs explicit approval
    "curl",         # network access needs approval
    "wget",
    "ssh",
    "scp",
]

# Action types classified by risk
ACTION_RISK_MAP = {
    "write_text": RiskLevel.LOW,
    "run_test": RiskLevel.READ_ONLY,
    "lint": RiskLevel.READ_ONLY,
    "type_check": RiskLevel.READ_ONLY,
    "run_build": RiskLevel.MEDIUM,
    "run_command": RiskLevel.HIGH,
    "git_commit": RiskLevel.HIGH,
    "deploy": RiskLevel.CRITICAL,
    "install_package": RiskLevel.HIGH,
    "network_request": RiskLevel.HIGH,
}


class PolicyEngine:
    """
    Central policy engine for ARGON AI-OS.
    Fail-closed: anything not explicitly allowed is denied.
    """

    def __init__(self, workspace_root: Path, approval_dir: Optional[Path] = None):
        self.workspace_root = workspace_root.resolve()
        self.approval_dir = (approval_dir or workspace_root / ".argon" / "approvals").resolve()
        self.approval_dir.mkdir(parents=True, exist_ok=True)
        self._consumed_nonces: set[str] = set()
        self._load_consumed_nonces()

    def _load_consumed_nonces(self) -> None:
        """Load previously consumed nonces for replay prevention."""
        nonce_file = self.approval_dir / ".consumed_nonces.json"
        if nonce_file.is_file():
            try:
                data = json.loads(nonce_file.read_text(encoding="utf-8"))
                self._consumed_nonces = set(data.get("nonces", []))
            except (json.JSONDecodeError, OSError):
                self._consumed_nonces = set()

    def _save_consumed_nonce(self, nonce: str) -> None:
        """Persist consumed nonce for replay prevention."""
        self._consumed_nonces.add(nonce)
        nonce_file = self.approval_dir / ".consumed_nonces.json"
        nonce_file.write_text(
            json.dumps({"nonces": list(self._consumed_nonces)}, indent=2),
            encoding="utf-8",
        )

    def validate_contract(self, contract: TaskContract) -> list[str]:
        """Validate a task contract against policies."""
        errors = contract.validate()

        # Check for forbidden paths
        for action in contract.actions:
            if action.target_path:
                for pattern in FORBIDDEN_PATTERNS:
                    if pattern.startswith("*"):
                        if action.target_path.endswith(pattern[1:]):
                            errors.append(
                                f"action target '{action.target_path}' matches "
                                f"forbidden pattern '{pattern}'"
                            )
                    elif pattern in action.target_path:
                        errors.append(
                            f"action target '{action.target_path}' matches "
                            f"forbidden pattern '{pattern}'"
                        )

            # Check for forbidden commands
            if action.command:
                for forbidden in FORBIDDEN_COMMANDS:
                    if forbidden in action.command.lower():
                        errors.append(
                            f"action command contains forbidden pattern '{forbidden}'"
                        )

        # Check for conflicting output paths
        output_paths = [a.target_path for a in contract.actions if a.target_path]
        if len(output_paths) != len(set(output_paths)):
            errors.append("Conflicting output paths detected — duplicate targets")

        return errors

    def check_approval(
        self, contract: TaskContract
    ) -> Optional[ApprovalRecord]:
        """
        Check if a valid approval exists for this task.
        Returns the approval record if valid, None if not found.
        Raises exceptions for specific failure modes.
        """
        approval_path = self.approval_dir / f"{contract.task_id}.json"
        if not approval_path.is_file():
            return None

        try:
            data = json.loads(approval_path.read_text(encoding="utf-8"))
            record = ApprovalRecord.from_dict(data)
        except (json.JSONDecodeError, OSError, KeyError) as e:
            raise PolicyViolation(f"Corrupted approval record: {e}")

        # Check nonce replay
        if record.nonce in self._consumed_nonces:
            raise PolicyViolation(
                f"Approval nonce '{record.nonce}' has already been consumed — "
                f"replay detected"
            )

        # Check expiry
        if time.time() > record.expires_at:
            raise ApprovalExpired(
                f"Approval expired at {record.expires_at}, "
                f"current time is {time.time()}"
            )

        # Check plan digest match
        current_digest = contract.digest()
        if record.plan_digest != current_digest:
            raise ApprovalMismatch(
                f"Plan changed after approval. "
                f"Approved digest: {record.plan_digest}, "
                f"Current digest: {current_digest}"
            )

        # Check consumed flag
        if record.consumed:
            raise PolicyViolation("Approval has already been consumed")

        # Check decision
        if record.decision != "APPROVED":
            raise PolicyViolation(f"Approval decision is '{record.decision}', not APPROVED")

        return record

    def create_approval(
        self,
        contract: TaskContract,
        approver: str = "local-operator",
        expiry_seconds: int = 300,
    ) -> ApprovalRecord:
        """Create an approval record for a validated contract."""
        # Validate contract first
        errors = self.validate_contract(contract)
        if errors:
            raise PolicyViolation(
                f"Cannot approve invalid contract: {'; '.join(errors)}"
            )

        record = ApprovalRecord(
            task_id=contract.task_id,
            plan_digest=contract.digest(),
            approver=approver,
            expires_at=time.time() + expiry_seconds,
            scope=contract.scope,
            decision="APPROVED",
        )

        # Persist approval
        approval_path = self.approval_dir / f"{contract.task_id}.json"
        approval_path.write_text(
            json.dumps(record.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return record

    def consume_approval(
        self, contract: TaskContract
    ) -> ApprovalRecord:
        """
        Consume an approval — single-use, atomic.
        Must be called at execution time, not planning time.
        """
        record = self.check_approval(contract)
        if record is None:
            raise ApprovalRequired(
                f"No approval found for task {contract.task_id}"
            )

        # Consume atomically
        record.consume()
        self._save_consumed_nonce(record.nonce)

        # Persist consumed state
        approval_path = self.approval_dir / f"{contract.task_id}.json"
        approval_path.write_text(
            json.dumps(record.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return record

    def requires_approval(self, contract: TaskContract) -> bool:
        """Check if a contract requires approval before execution."""
        if contract.approval_level != ApprovalLevel.NONE:
            return True
        # Any non-read-only action requires approval
        for action in contract.actions:
            if not action.read_only:
                return True
        return False

    def check_path_safety(self, path: str, sandbox: Path) -> list[str]:
        """Check if a path is safe to write to."""
        errors = []
        resolved = (sandbox / path).resolve()

        # Path traversal check
        try:
            resolved.relative_to(sandbox.resolve())
        except ValueError:
            errors.append(f"Path '{path}' escapes sandbox boundary")

        # Symlink check
        if resolved.is_symlink():
            errors.append(f"Path '{path}' is a symlink — denied")

        # Forbidden pattern check
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.startswith("*"):
                if str(resolved).endswith(pattern[1:]):
                    errors.append(f"Path matches forbidden pattern '{pattern}'")
            elif pattern in str(resolved):
                errors.append(f"Path matches forbidden pattern '{pattern}'")

        return errors

    def check_execution_preconditions(
        self, contract: TaskContract, sandbox: Path
    ) -> list[str]:
        """
        Full pre-execution policy check.
        Must pass before any action is executed.
        """
        errors = self.validate_contract(contract)

        # Check all write paths are safe
        for action in contract.actions:
            if action.action_type == "write_text" and action.target_path:
                errors.extend(self.check_path_safety(action.target_path, sandbox))

        # Check approval if required
        if self.requires_approval(contract):
            try:
                record = self.check_approval(contract)
                if record is None:
                    errors.append(
                        f"Approval required for task {contract.task_id} "
                        f"but none found"
                    )
            except (ApprovalExpired, ApprovalMismatch, PolicyViolation) as e:
                errors.append(str(e))

        return errors

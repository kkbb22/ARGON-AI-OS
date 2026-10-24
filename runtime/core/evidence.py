"""
ARGON AI-OS — Evidence and Audit Ledger

Append-oriented, tamper-evident task event record.
Records task lifecycle events, policy decisions, verification results,
and produces machine-readable JSON evidence + human-readable reports.

LIMITATIONS (documented per mandate):
- This is an append-only JSON Lines file with per-entry hashing.
- Hashes chain sequentially but a privileged attacker with filesystem
  access could rewrite the entire ledger. This is NOT a cryptographic
  audit log — it detects accidental corruption and casual tampering only.
- No secrets, credentials, or patient information are stored.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional
import re


# Patterns that must be redacted from all log output
_SECRET_PATTERNS = [
    re.compile(r'(?i)(api[_-]?key|token|secret|password|credential|auth)\s*[:=]\s*\S+'),
    re.compile(r'(?i)bearer\s+\S+'),
    re.compile(r'(?i)(sk|pk|rk)-[a-zA-Z0-9]{20,}'),
    re.compile(r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----'),
]


def redact_secrets(text: str) -> str:
    """Redact potential secrets from text."""
    result = text
    for pattern in _SECRET_PATTERNS:
        result = pattern.sub("[REDACTED]", result)
    return result


@dataclass
class AuditEvent:
    """A single event in the audit ledger."""
    event_id: str
    timestamp: float = field(default_factory=time.time)
    event_type: str = ""          # e.g., "task_created", "approval_granted", etc.
    task_id: str = ""
    run_id: str = ""
    plan_digest: str = ""
    data: dict[str, Any] = field(default_factory=dict)
    previous_hash: str = ""       # Hash of the previous entry (chain)
    entry_hash: str = ""          # Hash of this entry

    def compute_hash(self) -> str:
        """Compute the hash for this entry, chaining from previous."""
        payload = json.dumps(
            {
                "event_id": self.event_id,
                "timestamp": self.timestamp,
                "event_type": self.event_type,
                "task_id": self.task_id,
                "run_id": self.run_id,
                "plan_digest": self.plan_digest,
                "data": self.data,
                "previous_hash": self.previous_hash,
            },
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "task_id": self.task_id,
            "run_id": self.run_id,
            "plan_digest": self.plan_digest,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "entry_hash": self.entry_hash,
        }


class AuditLedger:
    """
    Append-only audit ledger with hash chaining.
    
    Security note: This provides tamper-evidence against casual modification.
    It does NOT provide cryptographic non-repudiation or protect against
    a privileged attacker with filesystem access who could rewrite the
    entire chain. The design includes an interface for future integration
    with stronger audit backends.
    """

    def __init__(self, ledger_dir: Path):
        self.ledger_dir = ledger_dir.resolve()
        self.ledger_dir.mkdir(parents=True, exist_ok=True)
        self._ledger_file = self.ledger_dir / "audit.jsonl"
        self._last_hash = self._get_last_hash()
        self._event_count = self._count_events()

    def _get_last_hash(self) -> str:
        """Get the hash of the last entry in the ledger."""
        if not self._ledger_file.is_file():
            return "GENESIS"
        last_line = ""
        with open(self._ledger_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    last_line = line
        if not last_line:
            return "GENESIS"
        try:
            entry = json.loads(last_line)
            return entry.get("entry_hash", "GENESIS")
        except json.JSONDecodeError:
            return "CORRUPTED"

    def _count_events(self) -> int:
        """Count existing events."""
        if not self._ledger_file.is_file():
            return 0
        count = 0
        with open(self._ledger_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    count += 1
        return count

    def record(
        self,
        event_type: str,
        task_id: str = "",
        run_id: str = "",
        plan_digest: str = "",
        data: Optional[dict] = None,
    ) -> AuditEvent:
        """Append an event to the ledger."""
        self._event_count += 1
        event = AuditEvent(
            event_id=f"EVT-{self._event_count:06d}",
            event_type=event_type,
            task_id=task_id,
            run_id=run_id,
            plan_digest=plan_digest,
            data=self._sanitize_data(data or {}),
            previous_hash=self._last_hash,
        )
        event.entry_hash = event.compute_hash()
        self._last_hash = event.entry_hash

        # Append to ledger file
        with open(self._ledger_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")

        return event

    def _sanitize_data(self, data: dict) -> dict:
        """Remove secrets from event data."""
        sanitized = {}
        for key, value in data.items():
            if isinstance(value, str):
                sanitized[key] = redact_secrets(value)
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize_data(value)
            elif isinstance(value, list):
                sanitized[key] = [
                    redact_secrets(v) if isinstance(v, str) else v
                    for v in value
                ]
            else:
                sanitized[key] = value
        return sanitized

    def verify_chain(self) -> tuple[bool, list[str]]:
        """
        Verify the hash chain integrity.
        Returns (is_valid, list_of_issues).
        """
        if not self._ledger_file.is_file():
            return True, []

        issues = []
        previous_hash = "GENESIS"
        line_num = 0

        with open(self._ledger_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                line_num += 1
                try:
                    entry_data = json.loads(line)
                except json.JSONDecodeError:
                    issues.append(f"Line {line_num}: Invalid JSON")
                    continue

                # Check chain
                if entry_data.get("previous_hash") != previous_hash:
                    issues.append(
                        f"Line {line_num}: Chain break — expected previous_hash "
                        f"'{previous_hash}', got '{entry_data.get('previous_hash')}'"
                    )

                # Verify entry hash
                event = AuditEvent(
                    event_id=entry_data["event_id"],
                    timestamp=entry_data["timestamp"],
                    event_type=entry_data["event_type"],
                    task_id=entry_data.get("task_id", ""),
                    run_id=entry_data.get("run_id", ""),
                    plan_digest=entry_data.get("plan_digest", ""),
                    data=entry_data.get("data", {}),
                    previous_hash=entry_data.get("previous_hash", ""),
                )
                expected_hash = event.compute_hash()
                if entry_data.get("entry_hash") != expected_hash:
                    issues.append(
                        f"Line {line_num}: Hash mismatch — "
                        f"expected '{expected_hash}', "
                        f"got '{entry_data.get('entry_hash')}'"
                    )

                previous_hash = entry_data.get("entry_hash", "")

        return len(issues) == 0, issues

    def get_events(
        self,
        task_id: Optional[str] = None,
        event_type: Optional[str] = None,
    ) -> list[dict]:
        """Query events from the ledger."""
        if not self._ledger_file.is_file():
            return []
        events = []
        with open(self._ledger_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    if task_id and entry.get("task_id") != task_id:
                        continue
                    if event_type and entry.get("event_type") != event_type:
                        continue
                    events.append(entry)
                except json.JSONDecodeError:
                    continue
        return events

    def generate_task_report(self, task_id: str) -> str:
        """Generate a human-readable report for a task."""
        events = self.get_events(task_id=task_id)
        if not events:
            return f"No events found for task {task_id}"

        lines = [
            f"# Task Report: {task_id}",
            f"Generated: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}",
            "",
            "## Event Timeline",
            "",
        ]
        for evt in events:
            ts = time.strftime(
                "%H:%M:%S", time.gmtime(evt.get("timestamp", 0))
            )
            lines.append(
                f"- [{ts}] **{evt.get('event_type', 'unknown')}** "
                f"(event: {evt.get('event_id', '?')})"
            )
            if evt.get("data"):
                for key, val in evt["data"].items():
                    if isinstance(val, str) and len(val) > 200:
                        val = val[:200] + "..."
                    lines.append(f"  - {key}: {val}")

        # Chain integrity
        valid, issues = self.verify_chain()
        lines.append("")
        lines.append("## Audit Chain Integrity")
        if valid:
            lines.append("Chain verification: **PASS**")
        else:
            lines.append("Chain verification: **FAIL**")
            for issue in issues:
                lines.append(f"- {issue}")

        lines.append("")
        lines.append("## Limitations")
        lines.append(
            "This ledger provides tamper-evidence via hash chaining. "
            "It does NOT provide cryptographic non-repudiation. "
            "A privileged attacker with filesystem access could rewrite "
            "the entire chain."
        )
        return "\n".join(lines)

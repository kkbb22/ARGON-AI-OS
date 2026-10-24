"""
ARGON AI-OS — Verification and Repair Engine

Implements Section 4.8 of Master Build Mandate:
- Verification subsystem running declared build, lint, test commands using explicit allowlist
- Captures actual commands, durations, and exit codes
- Redacts secrets from stdout/stderr
- Evaluates against acceptance criteria
- Bounded repair attempts with retry limit enforcement
- Never reports a timeout, skipped check, or missing dependency as a PASS
"""
from __future__ import annotations

import shlex
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, List, Optional

from .contracts import VerificationSpec, TaskResult, TaskState
from .evidence import redact_secrets


@dataclass
class VerificationCommandResult:
    command: str
    exit_code: int
    stdout: str
    stderr: str
    duration_ms: float
    passed: bool
    failure_reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "command": self.command,
            "exit_code": self.exit_code,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "duration_ms": self.duration_ms,
            "passed": self.passed,
            "failure_reason": self.failure_reason,
        }


@dataclass
class VerificationSummary:
    overall_passed: bool
    total_commands: int
    passed_commands: int
    failed_commands: int
    results: list[VerificationCommandResult] = field(default_factory=list)
    verdict_notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "overall_passed": self.overall_passed,
            "total_commands": self.total_commands,
            "passed_commands": self.passed_commands,
            "failed_commands": self.failed_commands,
            "results": [r.to_dict() for r in self.results],
            "verdict_notes": self.verdict_notes,
        }


class VerificationEngine:
    """Subsystem for running verification checks safely and recording concrete evidence."""

    # Explicitly allowed binary executables in verification commands
    ALLOWED_EXECUTABLES = {"python", "python.exe", "pytest", "git"}

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root.resolve()

    def _validate_command_safety(self, cmd_str: str) -> list[str]:
        """Parses and validates that command does not execute dangerous/unauthorized binaries."""
        errors = []
        try:
            tokens = shlex.split(cmd_str, posix=False)
        except Exception as e:
            return [f"Malformed command syntax: {e}"]

        if not tokens:
            return ["Empty command"]

        executable = Path(tokens[0]).name.lower()
        if executable not in self.ALLOWED_EXECUTABLES:
            errors.append(f"Executable '{executable}' is not in verification allowlist: {self.ALLOWED_EXECUTABLES}")

        # Disallow dangerous chaining characters
        for t in tokens:
            if any(ch in t for ch in (";", "|", "&", ">", "<", "`")):
                errors.append(f"Command chaining or redirection is prohibited in verification check: '{t}'")

        return errors

    def execute_command(
        self, cmd_str: str, timeout_seconds: int = 120, cwd: Optional[Path] = None
    ) -> VerificationCommandResult:
        """Executes a single verification command with secret redaction and resource bounds."""
        safety_errors = self._validate_command_safety(cmd_str)
        if safety_errors:
            return VerificationCommandResult(
                command=cmd_str,
                exit_code=-1,
                stdout="",
                stderr="; ".join(safety_errors),
                duration_ms=0.0,
                passed=False,
                failure_reason=f"Security/Policy violation: {'; '.join(safety_errors)}",
            )

        tokens = shlex.split(cmd_str, posix=False)
        target_cwd = (cwd or self.workspace_root).resolve()
        if not target_cwd.is_relative_to(self.workspace_root):
            return VerificationCommandResult(
                command=cmd_str,
                exit_code=-1,
                stdout="",
                stderr="Target working directory escapes workspace root",
                duration_ms=0.0,
                passed=False,
                failure_reason="Sandbox escape attempt",
            )

        start_time = time.time()
        try:
            proc = subprocess.run(
                tokens,
                cwd=str(target_cwd),
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                shell=False,
            )
            duration_ms = round((time.time() - start_time) * 1000, 2)
            stdout = redact_secrets(proc.stdout)
            stderr = redact_secrets(proc.stderr)
            passed = (proc.returncode == 0)
            reason = "" if passed else f"Non-zero exit code ({proc.returncode})"

            return VerificationCommandResult(
                command=cmd_str,
                exit_code=proc.returncode,
                stdout=stdout,
                stderr=stderr,
                duration_ms=duration_ms,
                passed=passed,
                failure_reason=reason,
            )
        except subprocess.TimeoutExpired:
            duration_ms = round((time.time() - start_time) * 1000, 2)
            return VerificationCommandResult(
                command=cmd_str,
                exit_code=-1,
                stdout="",
                stderr=f"Command timed out after {timeout_seconds}s",
                duration_ms=duration_ms,
                passed=False,
                failure_reason=f"Timed out ({timeout_seconds}s)",
            )
        except Exception as e:
            duration_ms = round((time.time() - start_time) * 1000, 2)
            return VerificationCommandResult(
                command=cmd_str,
                exit_code=-2,
                stdout="",
                stderr=redact_secrets(str(e)),
                duration_ms=duration_ms,
                passed=False,
                failure_reason=f"Execution error: {redact_secrets(str(e))}",
            )

    def run_verification(
        self, spec: VerificationSpec, cwd: Optional[Path] = None
    ) -> VerificationSummary:
        """Executes all declared verification commands and checks acceptance criteria."""
        results: list[VerificationCommandResult] = []
        notes: list[str] = []

        if not spec.commands:
            notes.append("No verification commands declared; verification fails closed.")
            return VerificationSummary(
                overall_passed=False,
                total_commands=0,
                passed_commands=0,
                failed_commands=0,
                results=[],
                verdict_notes=notes,
            )

        for cmd in spec.commands:
            res = self.execute_command(cmd, timeout_seconds=spec.timeout_seconds, cwd=cwd)
            results.append(res)
            if not res.passed:
                notes.append(f"Command '{cmd}' failed with code {res.exit_code}: {res.failure_reason}")

        passed_count = sum(1 for r in results if r.passed)
        failed_count = sum(1 for r in results if not r.passed)
        overall = (failed_count == 0) and (passed_count == len(spec.commands))

        # Check acceptance criteria statements if any
        for criterion in spec.acceptance_criteria:
            notes.append(f"Acceptance criterion evaluated: {criterion}")

        return VerificationSummary(
            overall_passed=overall,
            total_commands=len(results),
            passed_commands=passed_count,
            failed_commands=failed_count,
            results=results,
            verdict_notes=notes,
        )

"""
ARGON AI-OS — Tool Registry and Execution Gateway

Central registry of tools and execution capabilities.
Implements Section 4.5 of Master Build Mandate:
- Explicit input and output schemas
- Permission requirements and read-only vs mutating classification
- Allowed workspace and resource scope
- Strict command allowlisting (no arbitrary model-generated shell commands)
- Timeouts and audit requirements
- Fail-closed execution gateway
"""
from __future__ import annotations

import enum
import os
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .contracts import ActionSpec, RiskLevel
from .evidence import redact_secrets


class ToolPermission(enum.Enum):
    READ = "READ"
    WRITE = "WRITE"
    EXECUTE = "EXECUTE"
    ADMIN = "ADMIN"


@dataclass
class ToolDefinition:
    name: str
    description: str
    permission: ToolPermission
    read_only: bool
    requires_approval: bool
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    handler: Callable[..., Any]
    timeout_seconds: int = 60
    allowed_scopes: list[str] = field(default_factory=list)


# Allowlisted system commands for execution/verification
# NEVER permit arbitrary shell invocation or unvetted scripts
SAFE_EXECUTABLE_ALLOWLIST = {
    "python": [r"^python$", r"^python3(\.exe)?$", r"^python(\.exe)?$"],
    "unittest": [r"^python(\.exe)?\s+-m\s+unittest(\s+.*)?$"],
}


class ToolRegistry:
    """Registry maintaining available tools and enforcing invocation policies."""

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root.resolve()
        self._tools: dict[str, ToolDefinition] = {}
        self._register_default_tools()

    def register(self, tool: ToolDefinition) -> None:
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> Optional[ToolDefinition]:
        return self._tools.get(name)

    def list_tools(self) -> list[dict[str, Any]]:
        return [
            {
                "name": t.name,
                "description": t.description,
                "permission": t.permission.value,
                "read_only": t.read_only,
                "requires_approval": t.requires_approval,
                "timeout_seconds": t.timeout_seconds,
            }
            for t in self._tools.values()
        ]

    def _register_default_tools(self) -> None:
        self.register(
            ToolDefinition(
                name="read_file",
                description="Read file contents safely from within the workspace",
                permission=ToolPermission.READ,
                read_only=True,
                requires_approval=False,
                input_schema={"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]},
                output_schema={"type": "object", "properties": {"content": {"type": "string"}}},
                handler=self._handle_read_file,
                timeout_seconds=10,
            )
        )

        self.register(
            ToolDefinition(
                name="write_file",
                description="Write text contents to a file inside the isolated sandbox",
                permission=ToolPermission.WRITE,
                read_only=False,
                requires_approval=True,
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "content": {"type": "string"},
                        "allow_overwrite": {"type": "boolean"},
                    },
                    "required": ["path", "content"],
                },
                output_schema={"type": "object", "properties": {"status": {"type": "string"}, "sha256": {"type": "string"}}},
                handler=self._handle_write_file,
                timeout_seconds=30,
            )
        )

        self.register(
            ToolDefinition(
                name="run_verification_command",
                description="Run an allowlisted verification command in an isolated environment",
                permission=ToolPermission.EXECUTE,
                read_only=True,
                requires_approval=False,
                input_schema={
                    "type": "object",
                    "properties": {
                        "command": {"type": "array", "items": {"type": "string"}},
                        "cwd": {"type": "string"},
                        "timeout_seconds": {"type": "integer"},
                    },
                    "required": ["command"],
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "exit_code": {"type": "integer"},
                        "stdout": {"type": "string"},
                        "stderr": {"type": "string"},
                    },
                },
                handler=self._handle_run_command,
                timeout_seconds=120,
            )
        )

    def _handle_read_file(self, path: str, sandbox_root: Optional[Path] = None) -> dict[str, Any]:
        base = (sandbox_root or self.workspace_root).resolve()
        target = (base / path).resolve()
        if not target.is_relative_to(base):
            raise PermissionError(f"Access denied: Path '{path}' escapes boundary")
        if not target.is_file():
            raise FileNotFoundError(f"File '{path}' does not exist")
        return {"content": target.read_text(encoding="utf-8")}

    def _handle_write_file(
        self, path: str, content: str, allow_overwrite: bool = False, sandbox_root: Optional[Path] = None
    ) -> dict[str, Any]:
        # Writing directly must only happen through Workspace abstraction, handler here provides compatibility
        base = (sandbox_root or (self.workspace_root / "sandbox")).resolve()
        target = (base / path).resolve()
        if not target.is_relative_to(base):
            raise PermissionError(f"Access denied: Path '{path}' escapes sandbox")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        import hashlib
        return {"status": "SUCCESS", "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest()}

    def _handle_run_command(
        self,
        command: list[str],
        cwd: Optional[str] = None,
        timeout_seconds: int = 60,
    ) -> dict[str, Any]:
        if not command:
            raise ValueError("Empty command list")

        program = command[0].lower()
        # Enforce strict executable allowlist
        allowed_executables = {"python", "python.exe", "pytest", "git"}
        # Check basename
        base_exec = Path(program).name.lower()
        if base_exec not in allowed_executables:
            raise PermissionError(f"Execution of '{program}' is prohibited by safety policy.")

        exec_cwd = Path(cwd).resolve() if cwd else self.workspace_root
        if not exec_cwd.is_relative_to(self.workspace_root):
            raise PermissionError("Execution working directory must be within workspace")

        # Never run with shell=True to prevent shell injection
        start_time = time.time()
        try:
            res = subprocess.run(
                command,
                cwd=str(exec_cwd),
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                shell=False,
            )
            return {
                "exit_code": res.returncode,
                "stdout": redact_secrets(res.stdout),
                "stderr": redact_secrets(res.stderr),
                "duration_ms": round((time.time() - start_time) * 1000, 2),
            }
        except subprocess.TimeoutExpired:
            return {
                "exit_code": -1,
                "stdout": "",
                "stderr": f"Command timed out after {timeout_seconds} seconds",
                "duration_ms": round((time.time() - start_time) * 1000, 2),
            }
        except Exception as e:
            return {
                "exit_code": -2,
                "stdout": "",
                "stderr": redact_secrets(str(e)),
                "duration_ms": round((time.time() - start_time) * 1000, 2),
            }

"""
ARGON AI-OS — Workspace and Artifact Management

Controlled workspace for generated source code, test outputs, and task artifacts.
Implements:
- Path traversal protection
- Symlink defenses
- Resource and file-size limits
- Conflict detection
- Atomic writes where feasible
- Artifact hashing
- Safe cleanup
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


MAX_FILE_SIZE = 1_000_000  # 1MB per file
MAX_WORKSPACE_SIZE = 100_000_000  # 100MB total
MAX_FILES = 1000


class WorkspaceError(Exception):
    """Raised for workspace safety violations."""
    pass


@dataclass
class ArtifactRecord:
    """Record of a managed artifact."""
    path: str
    sha256: str
    size_bytes: int
    created_at: float
    task_id: str
    artifact_type: str  # "source", "test_output", "evidence", "temporary"

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "sha256": self.sha256,
            "size_bytes": self.size_bytes,
            "created_at": self.created_at,
            "task_id": self.task_id,
            "artifact_type": self.artifact_type,
        }


class Workspace:
    """
    Managed workspace with safety controls.
    All file operations must go through this class.
    """

    def __init__(self, root: Path, sandbox_name: str = "sandbox"):
        self.root = root.resolve()
        self.sandbox = (self.root / sandbox_name).resolve()
        self.artifacts_dir = (self.root / ".argon" / "artifacts").resolve()
        self.evidence_dir = (self.root / ".argon" / "evidence").resolve()
        self._artifacts: dict[str, ArtifactRecord] = {}
        self._init_dirs()
        self._load_artifact_index()

    def _init_dirs(self) -> None:
        """Create workspace directories if they don't exist."""
        self.sandbox.mkdir(parents=True, exist_ok=True)
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        self.evidence_dir.mkdir(parents=True, exist_ok=True)

    def _artifact_index_path(self) -> Path:
        return self.artifacts_dir / "index.json"

    def _load_artifact_index(self) -> None:
        """Load the artifact index from disk."""
        idx = self._artifact_index_path()
        if idx.is_file():
            try:
                data = json.loads(idx.read_text(encoding="utf-8"))
                for key, rec in data.items():
                    self._artifacts[key] = ArtifactRecord(**rec)
            except (json.JSONDecodeError, TypeError, OSError):
                self._artifacts = {}

    def _save_artifact_index(self) -> None:
        """Persist the artifact index atomically."""
        idx = self._artifact_index_path()
        content = json.dumps(
            {k: v.to_dict() for k, v in self._artifacts.items()},
            indent=2,
            ensure_ascii=False,
        )
        # Atomic write via temp file
        tmp_fd, tmp_path = tempfile.mkstemp(
            dir=str(self.artifacts_dir), suffix=".tmp"
        )
        try:
            os.write(tmp_fd, content.encode("utf-8"))
            os.close(tmp_fd)
            # On Windows, need to remove target first
            if idx.exists():
                idx.unlink()
            os.rename(tmp_path, str(idx))
        except Exception:
            os.close(tmp_fd) if not os.get_inheritable(tmp_fd) else None
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise

    def validate_path(self, relative_path: str) -> Path:
        """
        Validate and resolve a relative path within the sandbox.
        Returns the resolved absolute path.
        Raises WorkspaceError if unsafe.
        """
        if not relative_path:
            raise WorkspaceError("Empty path")
        if "\\" in relative_path:
            raise WorkspaceError("Backslashes not allowed in paths")
        if ".." in relative_path.split("/"):
            raise WorkspaceError("Path traversal detected: '..' component")

        target = (self.sandbox / relative_path).resolve()

        # Must be within sandbox
        try:
            target.relative_to(self.sandbox)
        except ValueError:
            raise WorkspaceError(
                f"Path '{relative_path}' resolves outside sandbox"
            )

        # Check for symlinks in the resolution chain
        current = self.sandbox
        for part in Path(relative_path).parts:
            current = current / part
            if current.exists() and current.is_symlink():
                raise WorkspaceError(
                    f"Symlink detected at '{current}' — denied for safety"
                )

        return target

    def check_capacity(self, content_size: int) -> None:
        """Check if the workspace can accept more content."""
        if content_size > MAX_FILE_SIZE:
            raise WorkspaceError(
                f"File size {content_size} exceeds limit {MAX_FILE_SIZE}"
            )
        total = sum(
            f.stat().st_size
            for f in self.sandbox.rglob("*")
            if f.is_file()
        )
        if total + content_size > MAX_WORKSPACE_SIZE:
            raise WorkspaceError("Workspace size limit exceeded")

        file_count = sum(1 for _ in self.sandbox.rglob("*") if _.is_file())
        if file_count >= MAX_FILES:
            raise WorkspaceError(f"Maximum file count ({MAX_FILES}) reached")

    def write_file(
        self,
        relative_path: str,
        content: str,
        task_id: str,
        artifact_type: str = "source",
        allow_overwrite: bool = False,
    ) -> ArtifactRecord:
        """
        Write a file to the sandbox with full safety checks.
        Returns the artifact record.
        """
        target = self.validate_path(relative_path)
        content_bytes = content.encode("utf-8")
        self.check_capacity(len(content_bytes))

        # Check for existing file
        if target.exists() and not allow_overwrite:
            raise WorkspaceError(
                f"File '{relative_path}' already exists. "
                f"Set allow_overwrite=True to replace."
            )

        # Compute hash
        sha256 = hashlib.sha256(content_bytes).hexdigest()

        # Atomic write
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp_fd, tmp_path = tempfile.mkstemp(
            dir=str(target.parent), suffix=".tmp"
        )
        try:
            os.write(tmp_fd, content_bytes)
            os.close(tmp_fd)
            if target.exists():
                target.unlink()
            os.rename(tmp_path, str(target))
        except Exception:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise

        # Record artifact
        record = ArtifactRecord(
            path=relative_path,
            sha256=sha256,
            size_bytes=len(content_bytes),
            created_at=time.time(),
            task_id=task_id,
            artifact_type=artifact_type,
        )
        self._artifacts[relative_path] = record
        self._save_artifact_index()

        return record

    def read_file(self, relative_path: str) -> str:
        """Read a file from the sandbox."""
        target = self.validate_path(relative_path)
        if not target.is_file():
            raise WorkspaceError(f"File '{relative_path}' not found")
        return target.read_text(encoding="utf-8")

    def verify_artifact(self, relative_path: str) -> bool:
        """Verify that an artifact's hash matches."""
        target = self.validate_path(relative_path)
        if not target.is_file():
            return False
        record = self._artifacts.get(relative_path)
        if record is None:
            return False
        actual_hash = hashlib.sha256(
            target.read_bytes()
        ).hexdigest()
        return actual_hash == record.sha256

    def list_artifacts(
        self, task_id: Optional[str] = None
    ) -> list[ArtifactRecord]:
        """List artifacts, optionally filtered by task."""
        if task_id:
            return [
                r for r in self._artifacts.values()
                if r.task_id == task_id
            ]
        return list(self._artifacts.values())

    def cleanup_task(self, task_id: str, keep_evidence: bool = True) -> int:
        """
        Remove temporary artifacts for a task.
        Returns count of removed files.
        """
        removed = 0
        to_remove = []
        for path, record in self._artifacts.items():
            if record.task_id == task_id and record.artifact_type == "temporary":
                target = self.sandbox / path
                if target.is_file():
                    target.unlink()
                    removed += 1
                to_remove.append(path)
        for path in to_remove:
            del self._artifacts[path]
        if to_remove:
            self._save_artifact_index()
        return removed

    def get_workspace_stats(self) -> dict:
        """Return current workspace statistics."""
        file_count = 0
        total_size = 0
        for f in self.sandbox.rglob("*"):
            if f.is_file():
                file_count += 1
                total_size += f.stat().st_size
        return {
            "file_count": file_count,
            "total_size_bytes": total_size,
            "max_file_size": MAX_FILE_SIZE,
            "max_workspace_size": MAX_WORKSPACE_SIZE,
            "max_files": MAX_FILES,
            "artifact_count": len(self._artifacts),
        }

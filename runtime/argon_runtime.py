import argparse
import hashlib
import json
import os
import time
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent
SANDBOX = (ROOT / "sandbox").resolve()
APPROVAL = ROOT / ".approval.json"
MAX_CONTENT = 100_000


def canonical_bytes(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def plan_digest(plan):
    return hashlib.sha256(canonical_bytes(plan)).hexdigest()


def validate_plan(plan):
    if not isinstance(plan, dict) or set(plan) != {"task", "actions"}:
        raise ValueError("Plan must contain exactly: task, actions")
    if not isinstance(plan["task"], str) or not plan["task"].strip():
        raise ValueError("task must be a non-empty string")
    actions = plan["actions"]
    if not isinstance(actions, list) or not actions or len(actions) > 20:
        raise ValueError("actions must contain 1 to 20 items")

    for action in actions:
        if not isinstance(action, dict):
            raise ValueError("Each action must be an object")
        if set(action) != {"type", "path", "content"}:
            raise ValueError("Action keys must be exactly type, path, content")
        if action["type"] != "write_text":
            raise ValueError("Only write_text actions are supported")
        rel = action["path"]
        content = action["content"]
        if not isinstance(rel, str) or not rel or "\\" in rel:
            raise ValueError("path must be a relative POSIX path")
        p = PurePosixPath(rel)
        if p.is_absolute() or any(part in ("", ".", "..") for part in p.parts):
            raise ValueError("Unsafe path")
        if not isinstance(content, str) or len(content.encode("utf-8")) > MAX_CONTENT:
            raise ValueError("content must be text no larger than 100 KB")

    return True


def load_plan(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        plan = json.load(f)
    validate_plan(plan)
    return plan


def approve(plan_path):
    plan = load_plan(plan_path)
    digest = plan_digest(plan)
    print("Plan SHA-256:", digest)
    print("Review the plan file before approving.")
    answer = input("Type APPROVE followed by the full SHA-256: ").strip()
    if answer != "APPROVE " + digest:
        raise ValueError("Approval text did not match; nothing was approved")
    record = {"digest": digest, "expires": time.time() + 600}
    APPROVAL.write_text(json.dumps(record), encoding="utf-8-sig")
    print("Approval recorded for this exact plan for 10 minutes.")


def apply_plan(plan_path):
    plan = load_plan(plan_path)
    if not APPROVAL.is_file():
        raise ValueError("No approval found; approve the plan first")
    record = json.loads(APPROVAL.read_text(encoding="utf-8-sig"))
    digest = plan_digest(plan)
    if record.get("digest") != digest:
        raise ValueError("Plan changed after approval; approval rejected")
    if not isinstance(record.get("expires"), (int, float)) or time.time() > record["expires"]:
        APPROVAL.unlink(missing_ok=True)
        raise ValueError("Approval expired; approve again")

    # Consume approval before any file mutation: one use only.
    APPROVAL.unlink()
    SANDBOX.mkdir(parents=True, exist_ok=True)
    results = []
    for action in plan["actions"]:
        target = (SANDBOX / action["path"]).resolve()
        if not target.is_relative_to(SANDBOX):
            raise ValueError("Resolved path escapes sandbox")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(action["content"], encoding="utf-8-sig")
        results.append(str(target.relative_to(SANDBOX)))
    print("Applied approved actions inside runtime/sandbox only:")
    for result in results:
        print(" -", result)


def main():
    parser = argparse.ArgumentParser(description="ARGON AI-OS minimal guarded runtime")
    parser.add_argument("command", choices=["validate", "approve", "apply"])
    parser.add_argument("plan", help="Path to a JSON plan")
    args = parser.parse_args()

    if args.command == "validate":
        plan = load_plan(args.plan)
        print("VALID: plan structure and action allowlist passed")
        print("SHA-256:", plan_digest(plan))
    elif args.command == "approve":
        approve(args.plan)
    else:
        apply_plan(args.plan)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit("BLOCKED: " + str(exc))


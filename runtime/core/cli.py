"""
ARGON AI-OS — Engineering Operations Interface (CLI)

Implements Section 5 of Master Build Mandate:
- Inspect system capabilities
- Validate task plans
- Review and approve tasks with cryptographic digest binding
- Execute approved tasks within isolated sandbox
- Run independent verification
- View task lifecycle status and inspect audit evidence
- Diagnose provider readiness without disclosing credentials
- Run offline self-tests
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from .contracts import (
    ActionSpec,
    ApprovalLevel,
    RiskLevel,
    TaskContract,
    TaskState,
    VerificationSpec,
)
from .evidence import AuditLedger
from .orchestrator import TaskOrchestrator
from .providers import MockProvider, ProviderGateway, ProviderStatus


def get_orchestrator(root: Optional[Path] = None) -> TaskOrchestrator:
    workspace_root = (root or Path(__file__).resolve().parents[2]).resolve()
    gateway = ProviderGateway(offline_mode=True)
    gateway.register_provider(MockProvider(name="mock-default"), primary=True)
    return TaskOrchestrator(workspace_root=workspace_root, provider_gateway=gateway)


def cmd_capabilities(args: argparse.Namespace) -> int:
    orch = get_orchestrator()
    print("==================================================")
    print("ARGON AI-OS - SYSTEM CAPABILITIES & STATUS")
    print("==================================================")
    print(f"Workspace Root: {orch.workspace_root}")
    print(f"Sandbox Root:   {orch.workspace.sandbox}")
    print(f"Ledger Path:    {orch.ledger.ledger_dir}")
    print("\n[Available Tools in Registry]")
    for tool in orch.tools.list_tools():
        perm = f"[{tool['permission']}]"
        read_only = "RO" if tool["read_only"] else "RW"
        req_appr = "NEEDS_APPROVAL" if tool["requires_approval"] else "AUTO"
        print(f" - {tool['name']:<25} {perm:<10} ({read_only}, {req_appr}) : {tool['description']}")

    print("\n[AI Provider Gateway]")
    for name, pinfo in orch.providers.get_provider_status().items():
        primary = " (PRIMARY)" if pinfo["is_primary"] else ""
        print(f" - {name:<15} : STATUS={pinfo['status']}{primary} - {pinfo['message']}")

    stats = orch.workspace.get_workspace_stats()
    print(f"\n[Sandbox Storage]")
    print(f" - Files: {stats['file_count']} / {stats['max_files']}")
    print(f" - Total Size: {stats['total_size_bytes']} bytes (limit: {stats['max_workspace_size']} bytes)")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    plan_path = Path(args.plan).resolve()
    if not plan_path.is_file():
        print(f"ERROR: Plan file '{plan_path}' does not exist.", file=sys.stderr)
        return 1

    try:
        data = json.loads(plan_path.read_text(encoding="utf-8"))
        contract = TaskContract.from_dict(data)
    except Exception as e:
        print(f"ERROR: Failed to parse contract: {e}", file=sys.stderr)
        return 1

    orch = get_orchestrator()
    task_id = orch.create_task(contract)
    ok, errors = orch.validate_plan(task_id)

    if ok:
        print("VALIDATION PASSED [OK]")
        print(f"Task ID:     {task_id}")
        print(f"Plan Digest: {contract.digest()}")
        print(f"Risk Level:  {contract.risk_level.value}")
        print(f"Approval:    {contract.approval_level.value}")
        return 0
    else:
        print("VALIDATION FAILED [FAIL]", file=sys.stderr)
        for err in errors:
            print(f" - {err}", file=sys.stderr)
        return 1


def cmd_approve(args: argparse.Namespace) -> int:
    task_id = args.task_id
    orch = get_orchestrator()
    try:
        contract = orch.get_task_contract(task_id)
    except KeyError:
        print(f"ERROR: Task '{task_id}' not found.", file=sys.stderr)
        return 1

    state = orch.get_task_state(task_id)
    if state == TaskState.DRAFT:
        ok, errors = orch.validate_plan(task_id)
        if not ok:
            print(f"ERROR: Cannot approve unvalidated task: {errors}", file=sys.stderr)
            return 1
        orch.plan_task(task_id)
    elif state == TaskState.VALIDATED:
        orch.plan_task(task_id)

    digest = contract.digest()
    print("==================================================")
    print("APPROVAL REQUEST")
    print("==================================================")
    print(f"Task ID:     {task_id}")
    print(f"Objective:   {contract.objective}")
    print(f"Actions ({len(contract.actions)}):")
    for a in contract.actions:
        print(f" - [{a.action_type}] target='{a.target_path}' (Risk: {a.risk_level.value})")
    print(f"Plan Digest: {digest}")
    print("--------------------------------------------------")

    approver = getattr(args, "approver", "operator") or "operator"
    record = orch.approve_task(task_id, approver=approver)
    print("APPROVED [OK]")
    print(f"Approval ID: {record.approval_id}")
    print(f"Expires at:  {record.expires_at} (valid for 5 minutes)")
    return 0


def cmd_execute(args: argparse.Namespace) -> int:
    task_id = args.task_id
    orch = get_orchestrator()
    try:
        print(f"Executing task {task_id}...")
        result = orch.execute_task(task_id)
        print(f"Execution complete! Final state: {result.state.value}")
        if result.state == TaskState.COMPLETED:
            print("Status: SUCCESS [OK]")
            print(f"Artifacts produced ({len(result.artifacts)}):")
            for art in result.artifacts:
                h = result.artifact_hashes.get(art, "")[:12]
                print(f" - {art} [sha256: {h}...]")
            return 0
        else:
            print("Status: FAILED [FAIL]", file=sys.stderr)
            for err in result.errors:
                print(f" - {err}", file=sys.stderr)
            return 2
    except Exception as e:
        print(f"ERROR during execution: {e}", file=sys.stderr)
        return 1


def cmd_status(args: argparse.Namespace) -> int:
    task_id = args.task_id
    orch = get_orchestrator()
    try:
        state = orch.get_task_state(task_id)
        contract = orch.get_task_contract(task_id)
        res = orch.get_task_result(task_id)

        print(f"Task ID:    {task_id}")
        print(f"Objective:  {contract.objective}")
        print(f"State:      {state.value}")
        print(f"Risk:       {contract.risk_level.value}")
        print(f"Approval:   {contract.approval_level.value}")
        if res:
            print(f"Exit Code:  {res.exit_code}")
            print(f"Verification Passed: {res.verification_passed}")
            print(f"Artifacts:  {res.artifacts}")
        return 0
    except KeyError:
        print(f"ERROR: Task '{task_id}' not found.", file=sys.stderr)
        return 1


def cmd_evidence(args: argparse.Namespace) -> int:
    task_id = args.task_id
    orch = get_orchestrator()
    report = orch.ledger.generate_task_report(task_id)
    print(report)
    return 0


def cmd_self_test(args: argparse.Namespace) -> int:
    print("Running ARGON AI-OS Offline Self-Tests...")
    orch = get_orchestrator()
    # 1. Test tool registry
    assert len(orch.tools.list_tools()) >= 3, "Missing core tools"
    # 2. Test policy engine
    assert orch.policy is not None, "Policy engine missing"
    # 3. Test workspace
    stats = orch.workspace.get_workspace_stats()
    assert "file_count" in stats, "Workspace stats failed"
    # 4. Test ledger chain
    valid, issues = orch.ledger.verify_chain()
    assert valid, f"Audit ledger chain invalid: {issues}"
    print("All offline self-test assertions PASSED [OK]")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ARGON AI-OS Engineering Operations CLI")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # capabilities
    subparsers.add_parser("capabilities", help="Inspect system capabilities and available tools")

    # validate
    p_val = subparsers.add_parser("validate", help="Validate a JSON task contract")
    p_val.add_argument("plan", help="Path to JSON task plan/contract")

    # approve
    p_app = subparsers.add_parser("approve", help="Approve a planned task contract")
    p_app.add_argument("task_id", help="Task ID to approve")
    p_app.add_argument("--approver", default="operator", help="Approver identity")

    # execute
    p_exe = subparsers.add_parser("execute", help="Execute an approved task")
    p_exe.add_argument("task_id", help="Task ID to execute")

    # status
    p_stat = subparsers.add_parser("status", help="Get state and details of a task")
    p_stat.add_argument("task_id", help="Task ID")

    # evidence
    p_evi = subparsers.add_parser("evidence", help="Generate task audit report & evidence")
    p_evi.add_argument("task_id", help="Task ID")

    # self-test
    subparsers.add_parser("self-test", help="Execute offline self-tests")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    commands = {
        "capabilities": cmd_capabilities,
        "validate": cmd_validate,
        "approve": cmd_approve,
        "execute": cmd_execute,
        "status": cmd_status,
        "evidence": cmd_evidence,
        "self-test": cmd_self_test,
    }

    cmd_fn = commands.get(args.subcommand)
    if not cmd_fn:
        parser.print_help()
        sys.exit(1)

    exit_code = cmd_fn(args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

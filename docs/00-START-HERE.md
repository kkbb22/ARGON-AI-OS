# 00 — START HERE: Reading Path & Onboarding Guide

Welcome to **ARGON AI-OS**. Whether you are an incoming human engineer or an autonomous Cloud persona (C1–C7), follow this sequential reading path to understand the system without making unsupported assumptions.

---

## Step 1: Understand Project Scope & Strict Separation
- **Read:** [`README.md`](../README.md)
- **Rule:** ARGON AI-OS is an autonomous engineering operating system. It is **not** ARGON-HEALTH. Do not reference clinical databases, medical standards, or hospital workflows.

## Step 2: Understand the Seven-Cloud Architecture
- **Read:** [`docs/SYSTEM-MAP.md`](SYSTEM-MAP.md)
- **Focus:** Observe the division of responsibilities:
  - C1: Orchestrator & Cross-Cloud Architecture
  - C2: Security & Trust
  - C3: Context & Token Economics
  - C4: Surgical Engineering & Mutation Defense
  - C5: Operator Control & Approval UX
  - C6: Evaluation & Verification
  - C7: Independent Forensic Auditor

## Step 3: Review Verified Forensic Baseline
- **Read:** [`assurance/audits/C7-FFA-003.md`](../assurance/audits/C7-FFA-003.md)
- **Takeaway:** Understand Gate 1 (Input Integrity: all 6 canonical files verified), Gate 3 (Source claim integrity), Gate 4 (Cross-cloud consistency), and Gate 9 (Reconciliation). Note the audit verdict: `CLEAN WITH OPEN EXPERIMENTS`.

## Step 4: Inspect Canonical Research
Read the six canonical research foundations in order:
1. [`clouds/C1/C1-CLOUD-HARNESS-ADAPTER-RESEARCH.md`](../clouds/C1/C1-CLOUD-HARNESS-ADAPTER-RESEARCH.md)
2. [`clouds/C2/C2-CLOUD-SECURITY-ADAPTER-RESEARCH.md`](../clouds/C2/C2-CLOUD-SECURITY-ADAPTER-RESEARCH.md)
3. [`clouds/C3/C3-CONTEXT-ENGINE-RESEARCH.md`](../clouds/C3/C3-CONTEXT-ENGINE-RESEARCH.md)
4. [`clouds/C4/C4-SURGICAL-ENGINEERING-PROTOCOL.md`](../clouds/C4/C4-SURGICAL-ENGINEERING-PROTOCOL.md)
5. [`clouds/C5/C5-OPERATOR-CONTROL-RESEARCH.md`](../clouds/C5/C5-OPERATOR-CONTROL-RESEARCH.md)
6. [`clouds/C6/C6-CLOUD-EVALUATION-ENGINE.md`](../clouds/C6/C6-CLOUD-EVALUATION-ENGINE.md)

## Step 5: Check Current Execution State & Handoff
- **Read:** [`docs/ARGON_AI_OS_MASTER_HANDOFF_AR.md`](ARGON_AI_OS_MASTER_HANDOFF_AR.md)
- **Read:** [`docs/CURRENT-STATE.md`](CURRENT-STATE.md)
- **Takeaway:** Understand C1's paused execution state (`C1-EXECUTION-STATE`) and why `ARGON-AI-OS-CROSS-CLOUD-SYNTHESIS.v2.md` is the immediate next deliverable.

## Step 6: Review Future Capability Packs (Designed Only)
- **Read:** [`capabilities/capability-index.md`](../capabilities/capability-index.md)
- **Remember:** These are `DESIGNED`, `NOT_IMPLEMENTED`, and `NO TEST EXECUTED`. Do not treat them as deployed features.

## Step 7: Review Open Questions and Next Actions
- **Read:** [`planning/OPEN-QUESTIONS.md`](../planning/OPEN-QUESTIONS.md)
- **Read:** [`planning/DEPENDENCY-REGISTER.md`](../planning/DEPENDENCY-REGISTER.md)
- **Read:** [`planning/NEXT-ACTIONS.md`](../planning/NEXT-ACTIONS.md)

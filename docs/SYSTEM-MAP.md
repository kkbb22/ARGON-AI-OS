# SYSTEM MAP — ARGON AI-OS Architecture & Cloud Collaboration

This document describes the seven Cloud roles, their verified dependencies, and boundaries grounded strictly in verified research artifacts.

---

## 1. Seven-Cloud Responsibility & Authority Model

```mermaid
flowchart TB
    subgraph Governance["Independent Assurance Layer"]
        C7["C7: Forensic Auditor<br/>• Verify / Classify / Cross-Check / Falsify<br/>• Independent Gate Audits (C7-FFA-003)<br/>• Verdict: CLEAN WITH OPEN EXPERIMENTS"]
    end

    subgraph Core["Architecture & Orchestration Core"]
        C1["C1: Architecture & Orchestrator<br/>• Multi-Cloud Harness Adapter<br/>• Delegation Depth = 1 Enforcement<br/>• Cross-Cloud Synthesis (v2 PENDING)"]
    end

    subgraph Pillars["Specialized Capability Pillars (DESIGNED / NOT IMPLEMENTED)"]
        C2["C2: Security & Trust<br/>• Plan/Act Mutation Firewall<br/>• Tool Authorization & Scoping<br/>• RP-1 to RP-13 Security Controls"]
        C3["C3: Context & Knowledge<br/>• Tiered Context Engine<br/>• Provenance & Token Economics<br/>• Semantic Graph & Memory Hierarchy"]
        C4["C4: Surgical Engineering<br/>• Plan/Act Execution Protocol<br/>• Adapter Boundaries & Reversion<br/>• Anti-Hallucination Diff Controls"]
        C5["C5: Human Operator Control<br/>• Operator Approval UX<br/>• Escalation Ladders<br/>• Human-in-the-Loop Override"]
        C6["C6: Evaluation Engine<br/>• Verification Matrix<br/>• Cost & Latency Benchmarks<br/>• Regression Detection"]
    end

    C1 -->|Orchestrates / Synthesizes| C2
    C1 -->|Orchestrates / Synthesizes| C3
    C1 -->|Orchestrates / Synthesizes| C4
    C1 -->|Orchestrates / Synthesizes| C5
    C1 -->|Orchestrates / Synthesizes| C6

    C7 -.->|Independently Audits| C1
    C7 -.->|Independently Audits| C2
    C7 -.->|Independently Audits| C3
    C7 -.->|Independently Audits| C4
    C7 -.->|Independently Audits| C5
    C7 -.->|Independently Audits| C6

    classDef verified fill:#e6f7ff,stroke:#1890ff,stroke-width:2px;
    classDef pending fill:#fffbe6,stroke:#faad14,stroke-width:2px;
    classDef auditor fill:#f6ffed,stroke:#52c41a,stroke-width:2px;
    class C1,C2,C3,C4,C5,C6 verified;
    class C7 auditor;
```

---

## 2. Artifact Provenance & Synthesis Flow

```mermaid
flowchart LR
    subgraph Inputs["Canonical Inputs (Hash-Verified Gate 1)"]
        I1["C1 Harness Research<br/>24e8cdb1...688f"]
        I2["C2 Security Research<br/>c6e95c26...0b99"]
        I3["C3 Context Research<br/>b48cbb0b...042c"]
        I4["C4 Surgical Protocol<br/>441007bc...1651"]
        I5["C5 Operator Control<br/>e70ea36b...e1a8"]
        I6["C6 Evaluation Engine<br/>a0d762ad...946a"]
    end

    subgraph Audit["Audit Gate"]
        FFA["C7-FFA-003 Audit<br/>Verified 6 of 6 Matches<br/>Verdict: CLEAN"]
    end

    subgraph Synthesis["Next Milestone (Phase D)"]
        SYN["ARGON-AI-OS-CROSS-CLOUD-SYNTHESIS.v2.md<br/>Status: PENDING<br/>Owner: C1"]
    end

    subgraph Wave4["Future Wave 4"]
        W4["Wave 4 Implementation & Runtime<br/>Status: BLOCKED ON SYNTHESIS"]
    end

    I1 & I2 & I3 & I4 & I5 & I6 --> FFA
    FFA -->|Authorizes Synthesis| SYN
    SYN -.->|Prerequisite For| W4

    classDef auditGate fill:#f6ffed,stroke:#52c41a,stroke-width:2px;
    classDef pending fill:#fff1f0,stroke:#f5222d,stroke-width:2px;
    classDef verified fill:#e6f7ff,stroke:#1890ff,stroke-width:2px;
    class I1,I2,I3,I4,I5,I6 verified;
    class FFA auditGate;
    class SYN,W4 pending;
```

---

## 3. Plan/Act 5-Vector Mutation Defense Convergence & Divergence

A critical architectural pattern across C1, C2, and C4 is the **5-Vector Mutation Test** for enforcing read-only plan phases:

| Vector # | Attack Vector Description | C1 Agreement | C2 Agreement | C4 Definition | Convergence Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Vector 1** | Direct file write tool call | Yes (E2) | Yes (RP-1) | Yes (Pattern F) | **CONFIRMED CONVERGENT** |
| **Vector 2** | Shell command writing to file | Yes (E2) | Yes (RP-1) | Yes (Pattern F) | **CONFIRMED CONVERGENT** |
| **Vector 3** | Interpreter write (python/node) | Yes (E2) | Yes (RP-1) | Yes (Pattern F) | **CONFIRMED CONVERGENT** |
| **Vector 4** | Wrapper / composite command | Yes (E2) | Yes (RP-1) | Yes (Pattern F) | **CONFIRMED CONVERGENT** |
| **Vector 5** | Indirect mutation | **Nested tool call** | **Nested tool call** | **Argument injection into read-only tool** | **MINOR TAXONOMY DIVERGENCE** (Non-blocking) |

*Resolution Note from C7-FFA-003:* Both interpretations represent genuine attack surfaces. C1 will reconcile the wording during Synthesis v2.

---

## 4. Delegation Depth Boundary

All clouds have converged on **Delegation Depth = 1**:
- C1 (Orchestrator) can spawn C2–C6 subagents.
- Subagents (C2–C6) cannot recursively spawn nested agents (`Depth <= 1`).
- Sourced from empirical vendor issue tracking (e.g., recursive spawning defects in nested multi-agent systems).

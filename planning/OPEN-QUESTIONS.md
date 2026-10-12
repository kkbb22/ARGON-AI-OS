# OPEN QUESTIONS REGISTER

This register tracks all unresolved architectural tensions, open experimental questions, and missing closure items identified in `C7-FFA-003.md` and cloud research documents.

---

## 1. High Priority Open Questions (Pre-Implementation)

### [OQ-01] RP-13 Cryptographic Binding Architecture
- **Origin:** C2 Research (§RP-13) & C7 Audit Gate 4 / Gate 9.
- **Description:** C2 identified six sub-questions regarding cryptographic binding between plan approval and action execution:
  1. Key custody: Where are private signing keys stored in a multi-cloud harness?
  2. Identity binding: How is a specific cloud persona's signature cryptographically validated?
  3. Replay prevention: What nonce/timestamp mechanism prevents plan replay attacks?
  4. Expiry: What is the maximum acceptable validity window for an approved plan token?
  5. Revocation: How does an operator revoke an in-flight approved plan token?
  6. Exact payload binding: How to sign non-deterministic LLM tool invocations without breaking execution?
- **Status:** `NEEDS EXPERIMENT` | Open by design.

### [OQ-02] Plan/Act 5-Vector Mutation Test Execution
- **Origin:** C1 Experiment E2, C2 RP-1, C4 Pattern F.
- **Description:** All three clouds specified a 5-vector mutation test to verify that the Plan phase cannot write to disk. However, this test has never been executed because the Wave 4 runtime environment does not exist.
- **Status:** `TEST SPECIFIED` | `NOT EXECUTED`.

### [OQ-03] 5th Mutation Vector Taxonomy Reconciliation
- **Origin:** C7 Audit Gate 4 (Finding Divergence).
- **Description:** C1 and C2 agree that the 5th mutation vector is "indirect mutation via a nested tool call". C4 defines it as "argument-injection into an ostensibly read-only tool".
- **Impact:** Minor wording/taxonomy divergence. Non-blocking for synthesis, but C1 must harmonize the definition in `ARGON-AI-OS-CROSS-CLOUD-SYNTHESIS.v2.md`.
- **Status:** `OPEN FOR C1 SYNTHESIS`.

### [OQ-04] SWE-bench Lite 10.7pp Citation Sourcing Note
- **Origin:** C7 Audit Gate 3 (Spot Check S2).
- **Description:** C1 removed a "+10.7 percentage points SWE-bench Lite" figure as unconfirmable, whereas C7 verified that the phrase appears verbatim in the primary NeurIPS paper. However, the paper's table shows a 7.0-point gap (18.00% vs 11.00%), creating an internal tension in the cited paper itself.
- **Status:** `MINOR SOURCING NOTE` for C1.

---

## 2. Infrastructure & Runtime Open Questions (Wave 4)

### [OQ-05] Delegation Depth = 1 Runtime Enforcement
- **Origin:** C1 Research & C7 Audit Gate 4.
- **Description:** How will the runtime harness intercept and block recursive subagent spawning attempts at the tool-definition layer vs the API-gateway layer?
- **Status:** `PENDING RUNTIME PROTOTYPE`.

### [OQ-06] Context Stale-State Resumption & Compaction
- **Origin:** C3 Context Engine (§3) & C1 Checkpoint Resumption.
- **Description:** When an agent halts due to platform rate limits or session timeouts, how does the context engine resume from partial checkpoint notes without re-reading the entire transcript?
- **Status:** `NEEDS EXPERIMENT`.

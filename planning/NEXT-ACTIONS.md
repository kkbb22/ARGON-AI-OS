# NEXT ACTIONS REGISTER

This document outlines the strictly sequenced next actions required to progress ARGON AI-OS, preventing premature implementation while unblocking canonical deliverables.

---

## Phase 1: Immediate Critical Path (Phase D — Cross-Cloud Synthesis)

1. **[ACTION-01] Resume C1 Cross-Cloud Synthesis v2**
   - **Owner:** C1 (Architecture Specialist)
   - **Target Deliverable:** `architecture/synthesis/ARGON-AI-OS-CROSS-CLOUD-SYNTHESIS.v2.md`
   - **Prerequisites:** Canonical C1–C6 research files + `C7-FFA-003.md` clearance (All available in repository).
   - **Instructions:**
     - Extract synthesis notes from canonical sources into working notes.
     - Reconcile C4's 5th mutation vector wording with C1/C2.
     - Note the SWE-bench Lite 10.7pp table vs prose tension.
     - Preserve the `NEEDS EXPERIMENT` status of RP-13 and delegation depth.
     - **Do NOT alter canonical research files.**

2. **[ACTION-02] Author C6 Future Capability Packs — COMPLETE (design deliverable only)**
   - **Owner:** C6 (Evaluation Specialist)
   - **Canonical Design Deliverable:** `capabilities/future/C6/C6-FUTURE-EVALUATION-CAPABILITY-PACKS.md` + companion manifest.
   - **Acceptance record:** `governance/decisions/C6-DESIGN-ONLY-ACCEPTANCE-2026-10-21.md`.
   - **Accepted boundary:** Documentation/design only. All five packs remain `DESIGNED` / `NOT_IMPLEMENTED` / `TEST SPECIFIED`; `TEST EXECUTED = 0`; `PASS WITH EVIDENCE = 0`.
   - **Remaining blockers:** C1 Synthesis v2 and its C7 audit remain prerequisites to Wave 4; the evaluation harness is only `DESIGNED`; interface contracts and `THRESHOLD NOT SET` items remain open.
   - **Authorization:** Closing this authoring action does not authorize runtime/Wave 4 execution or close DEP-06, DEP-09, or the security experiments.

---
## Phase 2: Post-Synthesis Assurance (Phase E)

3. **[ACTION-03] Independent Forensic Audit of Synthesis v2**
   - **Owner:** C7 (Independent Forensic Auditor)
   - **Target Deliverable:** `assurance/audits/C7-FFA-004.md`
   - **Scope:** Verify that Synthesis v2 strictly reflects canonical findings without unapproved architectural mutations.

---

## Phase 3: Wave 4 Prototyping & Runtime Implementation

4. **[ACTION-04] Wave 4 Runtime Scaffolding**
   - **Owner:** C4 (Engineering Specialist)
   - **Target Deliverable:** Minimal execution harness with Plan/Act tool sandboxing.
   - **Gate:** Must not begin until ACTION-03 is certified clean by C7.

5. **[ACTION-05] Execute the 5-Vector Mutation Test**
   - **Owner:** C2 / C4 / C6
   - **Target Deliverable:** Empirical test log for Vectors 1–5.

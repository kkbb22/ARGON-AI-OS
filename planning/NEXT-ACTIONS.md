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

2. **[ACTION-02] Author C6 Future Capability Packs**
   - **Owner:** C6 (Evaluation Specialist)
   - **Target Deliverable:** `capabilities/future/C6/C6-FUTURE-EVALUATION-CAPABILITY-PACKS.md`
   - **Prerequisites:** Canonical C6 Evaluation Engine (`clouds/C6/C6-CLOUD-EVALUATION-ENGINE.md`).

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

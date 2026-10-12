# DEPENDENCY REGISTER — Inter-Cloud Contracts & Dependencies

This register documents the operational and architectural dependencies among C1–C7 grounded in source artifacts.

---

| Dependency ID | Provider | Consumer | Required Capability / Contract | Evidence Source | Verification Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DEP-01** | C2, C3, C4, C5, C6 | C1 | Canonical Research Inputs for v2 Synthesis | `C7-FFA-003.md` (Gate 1) | **VERIFIED COMPLETE** (6 of 6 hashes match) |
| **DEP-02** | C7 | C1 | Forensic Audit Clearance for Synthesis | `C7-FFA-003.md` (Gate 9) | **VERIFIED COMPLETE** (`CLEAN`) |
| **DEP-03** | C1 | Program | `ARGON-AI-OS-CROSS-CLOUD-SYNTHESIS.v2.md` | Handoff & Phase D | **BLOCKED / PENDING C1** |
| **DEP-04** | C2 & C4 | C1 | Plan/Act Mutation Boundary Agreement | C1 E2, C2 RP-1, C4 Pattern F | **VERIFIED CONVERGENT** (Vectors 1–4 match; Vector 5 minor taxonomy) |
| **DEP-05** | C1 | C2–C6 | Delegation Depth = 1 Architectural Constraint | C1 Harness Research (§4) | **VERIFIED CONVERGENT** |
| **DEP-06** | C6 | C1–C5 | Evaluation & Verification Harness | C6 Evaluation Engine (§3) | `DESIGNED` |
| **DEP-07** | C6 | Program | C6 Future Capability Packs | Capability Portfolio | **MISSING / PENDING C6** |
| **DEP-08** | C5 | Program | C5 Future Capability Packs v1 Baseline | C5 Future Packs v2 Header | **MISSING SOURCE UPLOAD** |
| **DEP-09** | System Harness | C2 | Cryptographic Key Custody & Token Verifier | C2 Research RP-13 | `UNRESOLVED EXPERIMENT` |
| **DEP-10** | C1 Synthesis | Wave 4 | Master Architecture Blueprint for Implementation | Program Lifecycle | `BLOCKED ON DEP-03` |

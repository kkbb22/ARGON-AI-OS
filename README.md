# ARGON AI-OS — Forensic Repository Index & Knowledge Base

> **Independent Forensic Audit & Repository Intake Notice (C7)**  
> **Repository:** [kkbb22/ARGON-AI-OS](https://github.com/kkbb22/ARGON-AI-OS)  
> **Audit Status:** Verified by C7 (`C7-FFA-003.md`) — **CLEAN WITH OPEN EXPERIMENTS**  
> **Epistemological Status:** `DESIGNED_AND_AUDITED` | `NOT_IMPLEMENTED_IN_CODE` | `0_TESTS_EXECUTED_IN_RUNTIME`

---

## 1. Project Boundaries & Critical Separation

**ARGON AI-OS** is an autonomous engineering and orchestration operating system utilizing specialized Claude cloud personas (C1 through C7).

> [!IMPORTANT]
> **STRICT PROJECT SEPARATION:**  
> ARGON AI-OS is **strictly separate** from:
> 1. **ARGON-HEALTH** (the clinical healthcare platform repository).
> 2. **Legacy ARGON**.
>
> All legacy/healthcare artifacts accidentally uploaded during initial repository creation have been safely isolated into [`archive/external-health/`](archive/external-health/). Do **NOT** merge their requirements, architectures, clinical data models, or roadmaps into ARGON AI-OS.

---

## 2. The Seven Specialized Cloud Personas

| Cloud | Specialist Role | Focus Area | Canonical Artifact | Status |
| :--- | :--- | :--- | :--- | :--- |
| **C1** | Orchestrator & Cross-Cloud Architect | Harness adapter, orchestration flow, synthesis | [`clouds/C1/C1-CLOUD-HARNESS-ADAPTER-RESEARCH.md`](clouds/C1/C1-CLOUD-HARNESS-ADAPTER-RESEARCH.md) | Canonical Research Verified; v2 Synthesis **PENDING** |
| **C2** | Security & Trust Specialist | Authorization adapter, Plan/Act boundaries, trust | [`clouds/C2/C2-CLOUD-SECURITY-ADAPTER-RESEARCH.md`](clouds/C2/C2-CLOUD-SECURITY-ADAPTER-RESEARCH.md) | Canonical Research Verified; Future Packs Designed |
| **C3** | Context & Knowledge Specialist | Context engine, retrieval, token economics, provenance | [`clouds/C3/C3-CONTEXT-ENGINE-RESEARCH.md`](clouds/C3/C3-CONTEXT-ENGINE-RESEARCH.md) | Canonical Research Verified; Future Packs Designed |
| **C4** | Engineering & Execution Specialist | Surgical protocol, Plan/Act mutation defense, tools | [`clouds/C4/C4-SURGICAL-ENGINEERING-PROTOCOL.md`](clouds/C4/C4-SURGICAL-ENGINEERING-PROTOCOL.md) | Canonical Research Verified; Future Packs Designed |
| **C5** | Human Control & Operator Specialist | Approval UX, human-in-the-loop, overrides | [`clouds/C5/C5-OPERATOR-CONTROL-RESEARCH.md`](clouds/C5/C5-OPERATOR-CONTROL-RESEARCH.md) | Canonical Research Verified; Future Packs Designed |
| **C6** | Evaluation & Verification Specialist | Evaluation engine, benchmark validity, metrics | [`clouds/C6/C6-CLOUD-EVALUATION-ENGINE.md`](clouds/C6/C6-CLOUD-EVALUATION-ENGINE.md) | Canonical Research Verified; Future Packs **PENDING** |
| **C7** | Independent Forensic Auditor | Verification, falsification, provenance, gate audits | [`assurance/audits/C7-FFA-003.md`](assurance/audits/C7-FFA-003.md) | Final Audit Complete (`CLEAN WITH OPEN EXPERIMENTS`) |

---

## 3. Canonical Research Hashes (Independently Verified)

All canonical research documents match the reference hashes confirmed in `C7-FFA-003.md` (normalized to standard LF line endings):

| Cloud | Canonical File | Verified SHA-256 (LF Normalized) | Status |
| :--- | :--- | :--- | :--- |
| **C1** | `clouds/C1/C1-CLOUD-HARNESS-ADAPTER-RESEARCH.md` | `24e8cdb1cb8a088f146ff97265a484a329544b6a13d3bdfafea00de9f5dc688f` | **MATCH ✓** |
| **C2** | `clouds/C2/C2-CLOUD-SECURITY-ADAPTER-RESEARCH.md` | `c6e95c268aa6b065737933cbeff10761939d8f310cb11db8b9907fb03d000b99` | **MATCH ✓** |
| **C3** | `clouds/C3/C3-CONTEXT-ENGINE-RESEARCH.md` | `b48cbb0b6f1205e66eed9b738d7b5ff3fc6d4db1b10584739149577d2dc9042c` | **MATCH ✓** |
| **C4** | `clouds/C4/C4-SURGICAL-ENGINEERING-PROTOCOL.md` | `441007bcbdce318b212d7f166fb344e18e72d92e5d0090f75718b9bc9ec01651` | **MATCH ✓** |
| **C5** | `clouds/C5/C5-OPERATOR-CONTROL-RESEARCH.md` | `e70ea36bcab13b1abf76dbc386a82ca114a8c86c66f689d30224f1de71c9e1a8` | **MATCH ✓** |
| **C6** | `clouds/C6/C6-CLOUD-EVALUATION-ENGINE.md` | `a0d762ad472f0e5fb6a891495a943ca808ac642ab5b7d3b9eab42fd0e237946a` | **MATCH ✓** |

*(Note: The initial flat upload included an intermediate whitespace-reformatted copy of C6 (`d7924176...`), which has been preserved in `archive/superseded/`, while the canonical bytes matching manifest and audit have been established as the canonical C6 file).*

---

## 4. Epistemological Classification Standard

Every artifact in this repository adheres to strict truth boundaries:

- `CANONICAL`: Authoritative research baseline hash-verified against C7-FFA-003.
- `CURRENT_SUPPORTING`: Valid active context, handoffs, or future pack specifications.
- `DESIGNED`: Specified on paper; architecture exists as documentation.
- `NOT_IMPLEMENTED`: No executable software runtime or code exists.
- `TEST SPECIFIED`: Test scenarios or attack vectors described theoretically.
- `NO TEST EXECUTED`: Zero test scenarios have been run against a live system.
- `SUPERSEDED`: Historical drafts or earlier correction waves.
- `DUPLICATE`: Redundant byte copies safely tracked in archive.
- `EXTERNAL_CONTEXT`: Unrelated historical assets (e.g., ARGON-HEALTH platform).

---

## 5. Repository Directory Layout

```
ARGON-AI-OS/
├── README.md                              # This master index and forensic landing page
├── STATUS.md                              # Current project status and blocker tracker
├── docs/                                  # System maps, reading guides, catalogs
│   ├── 00-START-HERE.md                   # Step-by-step reading order
│   ├── SYSTEM-MAP.md                      # Source-grounded 7-Cloud system map & diagrams
│   ├── DOCUMENT-CATALOG.md                # Comprehensive catalog of all artifacts
│   ├── CURRENT-STATE.md                   # Forensic state analysis & intake history
│   ├── GLOSSARY.md                        # Standard terminology & concepts
│   └── ARGON_AI_OS_MASTER_HANDOFF_AR.md   # Handoff context document in Arabic
├── clouds/                                # Canonical C1–C6 research & manifests
│   ├── C1/                                # C1 Architecture & Harness Adapter
│   ├── C2/                                # C2 Security Adapter
│   ├── C3/                                # C3 Context Engine
│   ├── C4/                                # C4 Surgical Engineering Protocol
│   ├── C5/                                # C5 Operator Control & UX
│   ├── C6/                                # C6 Cloud Evaluation Engine
│   └── C7/                                # C7 Forensic Audit Links
├── capabilities/                          # Future Capability Packs (Designed only)
│   ├── capability-index.md                # Portfolio index & governance status
│   └── future/                            # C2, C3, C4, C5 Future Packs (C6 Pending)
├── assurance/                             # C7 audits, verification matrices, findings
│   └── audits/                            # C7-FFA-003 Final Forensic Audit
├── evidence/                              # Provenance manifests & intake registry
│   ├── MANIFEST.json                      # Machine-readable inventory of all files
│   ├── source_moves_registry.json         # Exact byte-level move verification log
│   └── handoff/                           # Original handoff zip packages
├── planning/                              # Open questions, dependencies, next actions
│   ├── OPEN-QUESTIONS.md                  # Unresolved architectural & test questions
│   ├── DEPENDENCY-REGISTER.md             # Provider/consumer dependency contracts
│   └── NEXT-ACTIONS.md                    # Prioritized next actions for C1 and team
└── archive/                               # Safely preserved non-canonical materials
    ├── duplicates/                        # Redundant numbered copies
    ├── superseded/                        # Whitespace variants and earlier revisions
    ├── historical/wave3.5/                # Predecessor Wave 3.5 correction files
    └── external-health/                   # Separated ARGON-HEALTH & medical docs
```

---

## 6. Where to Begin

1. **For New Engineers & Clouds:** Start with [`docs/00-START-HERE.md`](docs/00-START-HERE.md).
2. **For Immediate Architecture Next Action:** Review [`planning/NEXT-ACTIONS.md`](planning/NEXT-ACTIONS.md) and [`docs/ARGON_AI_OS_MASTER_HANDOFF_AR.md`](docs/ARGON_AI_OS_MASTER_HANDOFF_AR.md).
3. **For Verification & Audit History:** Review [`assurance/audits/C7-FFA-003.md`](assurance/audits/C7-FFA-003.md) and [`STATUS.md`](STATUS.md).

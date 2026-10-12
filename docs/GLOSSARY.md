# GLOSSARY — ARGON AI-OS Terminology

| Term | Definition in ARGON AI-OS | Sourcing / Owner |
| :--- | :--- | :--- |
| **ACI** | Agent-Computer Interface. Structured environment (tools, format constraints, execution boundaries) presented to an AI model. | C1 Research |
| **Canonical** | The single authoritative, verified version of an artifact matching the hash record in `C7-FFA-003.md`. | C7 Audit |
| **C1–C7** | The seven specialized cloud personas representing architecture, security, context, execution, operator UX, evaluation, and audit. | Master Architecture |
| **Delegation Depth = 1** | Architectural constraint preventing recursive agent spawning. The orchestrator may spawn subagents, but subagents cannot spawn further agents. | C1 / C7 Audit |
| **5-Vector Mutation Test** | Benchmark suite testing five file mutation vectors to ensure read-only plan phases cannot mutate disk state. | C1 / C2 / C4 |
| **Plan/Act Separation** | Protocol requiring distinct planning phases (strictly read-only tools) and execution phases (surgical, authorized write tools). | C2 / C4 Research |
| **RP-1 to RP-13** | Research propositions for cloud security adapters defined by C2. | C2 Research |
| **Surgical Engineering Protocol** | C4 execution standard requiring tight diffs, anti-hallucination syntax checks, and immediate rollback mechanisms. | C4 Research |
| **Epistemological Status** | Strict categorization of statements (`DESIGNED`, `NOT_IMPLEMENTED`, `TEST SPECIFIED`, `TEST EXECUTED`, `PASS WITH EVIDENCE`). | Program Standard |
| **External Context** | Files belonging to other repositories (such as the ARGON-HEALTH clinical platform) that are excluded from ARGON AI-OS. | Repository Boundary |

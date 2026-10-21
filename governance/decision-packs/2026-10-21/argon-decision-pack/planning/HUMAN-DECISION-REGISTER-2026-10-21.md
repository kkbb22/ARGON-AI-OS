# ARGON AI-OS — Delegated Architecture Decision Register

**Record ID:** ADR-HUMAN-DECISIONS-2026-10-21  
**Project baseline reviewed:** `71a3fa6d1fb1eed0e694886263710d4020e10341`  
**Decision date:** 2026-10-21  
**Authority:** The project owner explicitly delegated selection of the safest practical defaults in the ChatGPT conversation on 2026-10-21. These choices were made under that delegation.  
**Record state:** Decisions selected; this file has **not** been committed to or accepted by the canonical GitHub repository. The repo’s actual gates do not become passed merely because this file exists locally.

## Executive decision

Adopt a deny-by-default, human-controlled first release. Keep mutation-capable execution disabled until the required test, schema, security, and implementation gates pass. Prefer small, allowlisted interfaces; single-use approvals bound to one exact action and payload; no unattended mutations; and explicit evidence before any capability is promoted.

The selections below are ARGON governance decisions/recommendations, not claims that the canonical Cloud documents already implement them. Source-defined experiments remain `NOT EXECUTED` until real test evidence is recorded. No Wave 4 or runtime implementation is authorized by this record.

## Decisions H-01 through H-10

### H-01 — Delegation depth
**Selected:** Maximum delegation depth is **1** for the initial design/prototype. Deeper delegation is denied by default. Do not treat this as empirically validated or freeze it as a permanent Kernel rule until `C1-E1b` passes.

**Why:** A small, bounded delegation tree is easier to audit and limits recursive fan-out, context leakage, and runaway cost.  
**Reopen only when:** `C1-E1b` has a reproducible task set, recorded quality/cost results, and an independent review. Passing averages do not override a severe safety failure in an individual task.

### H-02 — Interface direction
**Selected:** Start with a **minimal, structured, allowlisted interface** (bounded ACI principles), not unrestricted CodeAct or arbitrary shell access. Use a narrow, explicit tool registry and separate read-only planning from mutation-capable execution. This is a prototype baseline, not a claim that the long-term interface question is experimentally settled.

**Why:** Smaller interfaces reduce the amount of authority the model can express and are easier to test.  
**Guardrail:** Keep concrete interface choice provisional until `C4-EXP7` is executed. Do not introduce raw shell or a wider tool surface merely for convenience; each added capability needs a named owner, permissions, test cases, and review.

### H-03 — Cryptographic binding
**Selected:** **Invest in cryptographic action-binding as the target for high-risk and live-write authorization.** Do not build or rely on an unverified signature/token design. `C2-RP13` and all six dimensions (key custody, identity binding, replay prevention, expiry, revocation, exact-payload binding) must be designed, independently tested, and recorded before any live write can rely on cryptographic approval.

**Why:** A non-cryptographic record can be misrepresented, replayed, substituted, or confused with UI confirmation.  
**Guardrail:** Until `C2-RP13` passes, any approval record is documentation/test data only. Do not claim that a hash field by itself provides authenticity, authorization, or replay prevention.

### H-04 — Approval baseline and scope
**Selected:** Use **exact-action + exact-payload approval**, with the narrowest scope: one action, one target, one execution attempt. Category/prefix matching (`A1`) may help filter or route requests but must never authorize a high-risk action by itself. The intended record must bind at minimum the approver identity, task/run, repository and target, exact operation, canonical payload/diff hash, a unique action identifier/nonce, issue and expiry times, and the decision/evidence reference.

**Scope policy:** No broad persisted approval and no approval inherited by a changed diff, branch, target, command, payload, session, or resumed state. The first prototype should use a short expiry (proposed maximum 5 minutes) and invalidate approval on any material state/payload change; failed canonicalization means deny and request a fresh approval. The expiry is an ARGON proposal to test, not a value reported by C1–C6.

**Why:** It minimizes scope and makes approval understandable and auditable.  
**Guardrail:** This decision selects the schema direction only. It does not pass `G-4`, create an enforced schema, or authorize ACT. Exact-payload and cryptographic properties remain unproven until their respective gates pass.

### H-05 — Third-party MCP scope
**Selected:** **Out of scope for the first stable release by default.** Permit only an explicitly allowlisted integration after a per-integration review of identity, permissions, provenance/version pinning, tool descriptions, prompt-injection/tool-poisoning risks, secrets handling, and runtime monitoring.

**Why:** Every external connector expands the attack surface and can introduce a confused-deputy path.  
**Guardrail:** No user- or model-added MCP server may become trusted automatically. Re-entry into scope requires a documented threat model and passing integration tests.

### H-06 — Deeper source coverage
**Selected:** **Yes, perform focused additional source review before freezing the implementation architecture**, prioritizing primary documentation, security advisories, and empirical evaluations for the components ARGON actually selects. This is a bounded review, not an indefinite research loop.

**Why:** The current source set explicitly omits several frameworks and benchmarks.  
**Guardrail:** Record which claims were checked, source date/version, limits, and unresolved conflicts. Vendor documentation is evidence of documented behavior, not proof of enforcement. Do not block safe documentation/schema work while literature coverage is improved; do block unverified performance/security claims.

### H-07 — Unattended runs
**Selected:** **No unattended mutation-capable runs in the initial release.** Keep a human in the loop for all repository writes, destructive operations, access/permission changes, releases, and high-risk actions. Automated read-only evaluation may be considered only in an isolated environment after sandbox boundaries and monitoring are verified.

**Why:** The current sources do not settle whether unattended operation exists or how its controls are enforced.  
**Guardrail:** No timeout, retry policy, score, confidence, or reversible action substitutes for explicit authorization. Any future unattended mode requires a separate decision and safety review.

### H-08 — Deployment-level enforcement feasibility
**Selected:** **Do not presume feasibility. Treat deployment enforcement as unproven and production-blocking until demonstrated.** Run a bounded feasibility spike for the host/container/runtime controls; verify that the policy boundary is enforced outside the model and cannot be bypassed by prompt instructions or alternate tools.

**Why:** A design statement is not enforcement, and container/deployment controls are still unresolved in the source baseline.  
**Guardrail:** If the chosen environment cannot demonstrate enforcement, production deployment remains blocked; select a stronger environment or reduce scope. This decision does not claim the infrastructure is feasible or infeasible today.

### H-09 — Mutation-surface taxonomy
**Selected:** **Accept MV-01 through MV-06 as the canonical planning taxonomy** for `C1-E2` and ACTION-05. Preserve the source-specific crosswalk, including C4 Pattern F’s argument-triggered side effect (MV-06) and wrapper/subprocess path (MV-04). Test nested tool-call mutation (MV-05) separately. Where one fixture overlaps surfaces, retain distinct independently reported probes rather than counting one pass twice.

**Why:** Six explicit stable IDs preserve all source-described attack surfaces without erasing the divergence between C1/C2 and C4.  
**Acceptance criterion:** Zero successful mutations on every surface, tested independently in a runnable harness; record logs and evidence for every attempt. The taxonomy decision closes the decision itself only; it does **not** mean `C1-E2` has run or passed.

### H-10 — C1-E1 before the context compiler
**Selected:** **Adopt G-3 as a binding precondition before Wave 4 implementation or activation of the context compiler.** Run `C1-E1` first and meet its source-defined promotion condition: at least 10 representative tasks per role and no `claim_status` outcome change for any task while the targeted token/context reduction is demonstrated.

**Allowed before G-3 passes:** Documentation, schema design, and an offline non-production experiment harness that cannot change repository or runtime state.  
**Blocked:** Building or activating the Wave 4 context compiler as an operational component, promoting context-sizing changes, or treating the proposed pipeline as validated. Any task that changes `claim_status` blocks promotion even if aggregate token savings look good.

**Why:** Prevents optimization from silently dropping evidence or changing conclusions.  
**Guardrail:** `G-0`, `G-11`, and all other applicable gates remain independently required; this decision does not authorize Wave 4 or Runtime implementation.

## Gate consequences

These selections do **not** mark implementation gates as passed:

- `G-0`: still requires an explicit governance authorization for Wave 4 design and a separate authorization for implementation.
- `G-1`: taxonomy choice is recorded here; canonical intake/acceptance remains pending.
- `G-2`: `C1-E2` still needs a runnable harness and successful six-surface results.
- `G-3`: selected as binding; `C1-E1` is still `NOT EXECUTED`.
- `G-4`: approval baseline direction is selected; the canonical approval schema still needs to be written, reviewed, and accepted.
- `G-5`: `C2-RP13` remains `NOT DESIGNED / NOT EXECUTED` and is required before live writes that rely on crypto.
- `G-6`: concrete interface remains provisional until `C4-EXP7` passes.
- `G-7`: do not freeze the delegation rule until `C1-E1b` passes.
- `G-8`: resumable ACT remains blocked until `C1-E4` and `XC-RESUME` semantics are designed and tested.
- `G-9`: no adapter-sufficiency claim until a second backend and `C1-E3` exist.
- `G-10a`/`G-10b`: schema documents still need acceptance; neither gate authorizes execution.
- `G-11`: a real implementation/test environment is still required.
- `G-12`: multi-task runtime remains blocked until `C3-E4` passes.

## C6 Future Capability Packs — corrected status wording

The project owner states that the C6 Future Capability Packs artifact already exists outside the repository and has not been uploaded. The pinned commit does not contain `capabilities/future/C6/C6-FUTURE-EVALUATION-CAPABILITY-PACKS.md`. Therefore the accurate status is:

> **Exists outside the pinned repository per owner statement; not yet received, hashed, reviewed, or accepted into the repository. Intake pending.**

Do not call the artifact nonexistent in the project, and do not mark `DEP-07` complete merely because it exists locally. After intake, verify its exact bytes and provenance, compare its claims against canonical C6, check the capability-pack schema/version and any security or promotion hooks, then update the dependency register and repository manifest. Do not edit the canonical `clouds/C6/C6-CLOUD-EVALUATION-ENGINE.md` to smuggle in new capability-pack content.

## Record and limitations

- Selected under the project owner's explicit delegation in the ChatGPT conversation on 2026-10-21; choices were authored by the assistant as the delegated decision drafter.
- This file is a proposed canonical record and has not yet been committed or accepted through the repository process.
- No source research artifact was changed; no experiment was run; no source-level hash is altered by this record.
- No Wave 4, production deployment, ACT flow, live write, or runtime implementation is authorized by this record.

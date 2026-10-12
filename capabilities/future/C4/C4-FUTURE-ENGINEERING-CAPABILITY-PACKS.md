# C4 — Future Engineering and Orchestration Capability Packs

**Project:** ARGON AI-OS (not ARGON Health, not Legacy ARGON)
**Author role:** C4 (Engineering and Execution Protocol specialist)
**Revision:** v3 — rebuilt against the C2, C3, C4, C5, C6 artifacts and the C7 final audit. Supersedes my own v1 and v2 drafts of this file (never canonical).
**Deliverable status:** `DESIGNED` · `NOT_IMPLEMENTED` · tests `TEST SPECIFIED` only · no `TEST EXECUTED` · no `PASS WITH EVIDENCE`
**Directory convention:** none verified (all manifests: `repository_target: none`, `execution_target: deliverable_output`); returned under the proposed name.

Status vocabulary: `DESIGNED` (specification written) · `NOT_IMPLEMENTED` · `TEST SPECIFIED` (written, not run) · `TEST EXECUTED` · `PASS WITH EVIDENCE`. Only the first three appear below. Nothing here has been executed.

---

## 1. Baseline verification

### 1.1 Inputs and what was verified

Uploaded names carry numeric prefixes and `__N_` suffixes; canonical names below come from each manifest.

| Input | Provided | Verification this run |
|---|---|---|
| `C4-SURGICAL-ENGINEERING-PROTOCOL.md` + manifest | Yes | SHA-256 `441007bc…` **matches** manifest; also matches the hash C7 lists |
| `C2-CLOUD-SECURITY-ADAPTER-RESEARCH.md` + manifest | Yes | SHA-256 `c6e95c26…` **matches** manifest |
| `C3-CONTEXT-ENGINE-RESEARCH.md` + manifest | Yes | SHA-256 `b48cbb0b…` **matches** `report_sha256_value` |
| `C5-OPERATOR-CONTROL-RESEARCH.md` + manifest | Yes | SHA-256 `e70ea36b…` **matches** manifest |
| `C6-CLOUD-EVALUATION-ENGINE.md` + manifest | Yes | SHA-256 `a0d762ad…` **matches** manifest |
| C7 audit (`C7-FFA-003`, uploaded twice under two names) | Yes | The two files are byte-different only in table padding; after whitespace normalization they are identical. Content created 2026-10-07T03:59:29Z. C7's own hashes for all six Clouds agree with the values I computed for C2–C6 |
| **C1** harness artifact (`c1-cloud-evolution-harness-v4-final`) | **No** | C7 lists its hash (`24e8cdb1…`) but the file was not supplied. Everything below about C1 is **second-hand via C7** |
| Wave 3.5 objects (Repository Snapshot, Approval, Task Packet, Verification Record, `execution_stage`) | Referenced, **not defined in a supplied file** | C3 describes the Repository Snapshot only as "write-once, referenced by Approval" (L135) |
| Standalone adapter-contract files, checkpoint files, test-vector files | **No** | — |

I have not re-fetched any external source; all vendor and paper citations are as the supplied artifacts cite them (accessed 2026-09-20).

### 1.2 What C7-FFA-003 actually says

- **Verdict:** `CLEAN WITH OPEN EXPERIMENTS`; next owner Cross-Cloud Synthesis (C1). It checked hashes, spot-checked three claims about **C1** (S1–S3), and cross-checked Plan/Act vectors and manifest vocabulary across Clouds.
- **Only C4-specific finding:** a **minor, non-blocking divergence** in Pattern F's fifth test vector. C7 reports C1 and C2 agree on five vectors (direct write tool, shell write, interpreter write, wrapper/composite command, indirect mutation via nested tool call), while C4 defines its items differently (Gate 4). I checked this against the text: C2 RP-1 lists those five (L190–L194); C4 Pattern F's test lists (a) dedicated write tool, (b) shell, (c) interpreter, (d) read-only tool invoked with side-effecting arguments, (e) permitted tool wrapping a write-capable subprocess (L323–L329). The divergence is real. Union = up to six distinct routes; C4(e) most closely matches C2(4), possibly also C2(5); C4(d) has no C2 counterpart.
- **Open items it lists** (all "need a real implementation environment"): RP-13's six cryptographic-binding sub-questions; the full Plan/Act five-vector test; delegation depth (E1b); adapter-boundary sufficiency (E3); checkpoint stale-state resumption; task-context isolation (C3 §3).
- C7 did **not** mention the cross-reference numbering and source-count inconsistencies I list in §1.3; they remain in the protocol text.

### 1.3 Observations on the C4 protocol (re-checked, unchanged from v2)

1. Experiments sit in §7 (L448) but are cited as "§6" at L380 (as "§6/§7"), L607, L674 and L722.
2. §0 says 6 sources (L47) and §8 "six systems" (L552); manifest and Appendix say 10.
3. The protocol's own C7 v3 matrix (D4, C4-F, C4-DG, C4-H, D4-citations) is present in the text; Pattern E's section pointer is the weakest.

### 1.4 Classification vocabulary

The brief names `NOW` / `ARCHITECTURE-READY` / `FUTURE TRIGGER` / `NOT NEEDED` / `BUSINESS DECISION` as "established". **None of those terms appears in any supplied artifact.** C2–C6 and the protocol use `ADOPT` / `ADAPT` / `REJECT` / `NEEDS EXPERIMENT` / `UNKNOWN`. I give the brief's label and a **proposed** program-vocabulary equivalent for each pack; the mapping is mine and unverified.

---

## 2. Known-questions register (evidence now inspected)

| # | Question | Evidence found | Status |
|---|---|---|---|
| Q1 | Missing or inadequate Plan/Act mutation test vectors? | **PLAN-side vectors exist in three places, none executed:** C2 RP-1 five vectors plus test matrix (L129–L200, L1055); C4 Pattern F (a)–(e); C1 E2 (per C7, not seen). **Act-side binding is covered by C2 and C5, not C4:** C2 RP-13 (exact-payload hash, single-use scope, expiry, nonce, signed identity; `NEEDS EXPERIMENT`, six sub-questions, L790–L880) and C5 P4/E3 (`approved_plan_ref`; backend must block mismatches independent of human detection, L147, L451). **My v2 claim that nobody covers the act side was wrong; only the C4 protocol lacks it.** Executor-side per-mutation precondition checks and execution records are not specified anywhere | PLAN vectors: `TEST SPECIFIED`, none run, taxonomy diverges (see §1.2). Act-side binding: `NEEDS EXPERIMENT` (C2). Executor-side record: **unspecified**, addressed by Pack 001 |
| Q2 | Previously reported C4 vector mismatches still current? | The only vector finding in the C7 audit is the fifth-vector divergence (§1.2): minor, non-blocking, assigned to Synthesis. Not fixed in any canonical file | **OPEN, minor.** Pack 001's test suite uses the union rather than choosing a winner |
| Q3 | Delegation-depth limits? | Not in the C4 protocol. Per C7 (C1 not supplied): C1 proposes depth = 1 as an ARGON design choice, no longer a "vendor fact", and cites three Claude Code GitHub issues showing nested delegation is bugged or uncontrolled (#80036, #61993, #68619); C7 says it verified them; I did not | **OPEN** (E1b). Second-hand only |
| Q4 | Adapter sufficiency and contract boundaries? | C2 uses **`Adapter`** as one of four rule-location tiers (`Runtime`, `Kernel`, `Adapter`, `Platform`): the MCP-specific integration layer (RP-11 L735; RP-12 L784), and distinguishes Model-Independent from Model Adapter (L1153). C2 RP-11 (`ADOPT`) requires re-validation on any tool-manifest change. No functional contract format, versioning or capability discovery exists in any supplied file. C1's E3 adapter-boundary experiment is open per C7 | **OPEN** (E3). Security re-validation is owned by C2; **functional contract/versioning is unspecified** |
| Q5 | Checkpoint / resumption behavior? | Protocol: revert checkpoints only (Pattern D L247). C3 P9 notes Cline's shadow-git checkpoint and defers it to C1 (L131–L138; Repository Snapshot at L135). C5 P10 adopts a LangGraph-style state-only checkpoint as the default shape (L633) and E5 sets the pass criterion: no duplicate side effect across resume, and "Resume" is offered only after that holds (L478). C5 says the dependency is **on C6**, "flagged in every C5 artifact since Wave 3.5 v1". **C6 contains zero checkpoint or resume content** (0 hits), and C2 has none either. C7 lists "checkpoint stale-state resumption" as open | **OPEN, with an ownership gap:** demand is clear (C5), no Cloud has specified it |
| Q6 | Context-isolation interface with C3? | C3 §3: isolation is **not assumed to exist**; "no direct external precedent"; `NEEDS EXPERIMENT` via E4 (two concurrent Task Packets must not leak Claims or Evidence) (L227–L237, L285). C3 §4: when to re-fetch or recompile is `UNKNOWN`; stale detection is `head` vs `origin_head` at task start (E3). No lease or concurrency primitive is defined | **OPEN.** C3 owns it; Pack 001 states what it needs from C3 |

Nothing here resolves any of these. A design proposal does not close any experiment.

---

## 3. Scope selection and overlap map

Idempotency, retry and compensation: **zero hits** for `idempot`, `compensat` and (outside one C3 line) `retry` across C2, C3, C5, C6 and the protocol. No existing Cloud covers effect semantics.

| Area (brief) | Already covered by | Residual gap | Disposition | Classification (brief / proposed program label) |
|---|---|---|---|---|
| 1. Plan/Act boundaries | C2 RP-1 (PLAN gating), C2 RP-13 (action binding), C5 P4/E3 (operator side), C4 Pattern F, C6 Pattern 3 (trajectory log) | Executor-side per-mutation preconditions and intent/outcome record | **Folded into Pack 001** | `FUTURE TRIGGER` / `NEEDS EXPERIMENT` |
| 2. Checkpoint and resume | C5 P10/E5 (requirement), C3 P9/E3 (snapshot, staleness) | The specification itself, executor-side | **Pack 001** (merged with area 1 to avoid two overlapping records) | `FUTURE TRIGGER` / `UNKNOWN` |
| 3. Idempotency, retry, compensation | Nothing (C5 P5 covers reversibility as a safety net, `REJECT` as default) | Whole area | **Pack 002** | `FUTURE TRIGGER` / `UNKNOWN` |
| 4. Versioned adapter contracts | C2 RP-11/RP-12 (trust, manifest re-review, secrets) | Functional compatibility, versioning, capability discovery | **Pack 003** | `FUTURE TRIGGER` / `UNKNOWN` |
| 5. Delegation depth | C1 (unsupplied): depth = 1; C7 open E1b | None demonstrated | **No pack** | `NOT NEEDED` / `UNKNOWN` |

**Why three packs, not four.** v2 had a separate Plan/Act record pack. Its authorization-binding half duplicated C2 RP-13 and C5 P4, so I removed that half; the remainder (execution record, preconditions) is the same artifact as the resume journal, so I merged them. v2 IDs map as: v2-001 + v2-002 → v3-001; v2-003 → v3-002; v2-004 → v3-003.

**Common prerequisite.** ARGON AI-OS is documentation-only (protocol Experiment 1, L461; every manifest: `NOT_IMPLEMENTED`; C7: "Wave 4 not started"). Every experiment below needs a sandbox that does not exist.

**Not designed:** a generic workflow engine. No evidence supports one.

---

## 4. Capability packs

Per-claim analysis: SOURCE → OBSERVED → WHY IT WORKS → GENERAL PRINCIPLE → ARGON ADAPTATION → TRADEOFF → REJECT IF → EXPERIMENT.

---

### FCP-C4-ENG-001 — Mutation Execution Record and Resume Journal (executor side)

**Status:** `DESIGNED` · `NOT_IMPLEMENTED` · tests `TEST SPECIFIED` · **Local evidence:** demand STRONG (C5 E5, C7 open item), specification NONE · **Classification:** `FUTURE TRIGGER` (proposed label `UNKNOWN`)

#### 4.1.1 Analysis block

- **SOURCE:** C5 P10 and E5 (L633, L478; LangGraph interrupt/checkpointer cited via C5, not re-fetched); C3 §4 and E3 (L239, L284); C2 RP-13 (L790); C6 Pattern 3 (L58); protocol Pattern D (L238). Background knowledge, unverified this run: write-ahead logging, event-sourced durable execution.
- **OBSERVED:** C5 wants "Resume" offered only if resume never duplicates a side effect, and treats checkpoint design as a C6 dependency; C6 never defines one. C3 detects staleness at **task start** and leaves later re-fetch triggers `UNKNOWN`. C2 leaves authorization binding `NEEDS EXPERIMENT`.
- **WHY IT WORKS:** recording intent before an action and outcome after it makes the crash window visible, separating "never started", "done", and "unknown".
- **GENERAL PRINCIPLE:** resume from structured state, not from a transcript; replay only what is provably safe; fail closed when a verification input is unavailable.
- **ARGON ADAPTATION:** a thin **control-plane** journal that *references* objects owned elsewhere instead of duplicating them: `approval_ref` (C2), `snapshot_ref` (C3), `trajectory_step_ref` (C6), `commit_ref` (protocol Pattern D). The journal is not a second evidence log.
- **TRADEOFF:** a journal write per mutating step; one more schema to version.
- **REJECT IF:** C6's trajectory schema plus C3's snapshot already record intent/outcome per mutation with unknown-outcome handling; or step granularity (C6 Pattern 3 TEST NEEDED, depends on C1) shows no per-mutation unit exists; or the operator Resume option is dropped.
- **EXPERIMENT:** EXP-001-A.

#### 4.1.2 Out of scope (owned elsewhere, not designed here)

Authorization binding and signing (C2 RP-13); approval display and operator mismatch detection (C5 P4/E3); PLAN-state capability gating (C2 RP-1, C4 Pattern F); evidence/trajectory content (C6); snapshot creation and task-start staleness check (C3); cross-task isolation (C3 §3/E4); storage location (unresolved, see §8).

#### 4.1.3 Activation trigger and prerequisites

**Trigger:** Wave 4 code exists **and** the operator Resume option (C5 E5) is to be offered, or a task must outlive a session with side effects. **Prerequisites:** Pack 002 step classes; C2's verify interface (`verify(approval_ref, mutation_digest)`); a C3 snapshot comparison callable at act time; a decision on where the journal lives (C3 or C6, §8).

#### 4.1.4 Lifecycle (specification only)

Task: `ACTIVE → PAUSED → RESUMING → ACTIVE → COMPLETED | ABANDONED`. Step: `INTENT_RECORDED → OUTCOME_RECORDED(SUCCEEDED | FAILED | UNKNOWN)`. One mutation = one patch = one revertible commit (protocol Pattern D).

#### 4.1.5 Proposed contract (unimplemented)

Entry: `seq`, `task_id`, `step_id`, `kind` (`INTENT` | `OUTCOME`), `step_class` (Pack 002), `approval_ref`, `snapshot_ref`, `trajectory_step_ref`, `commit_ref`, `mutation_digest` (content integrity digest, **not** a signature), `precondition_result`, `schema_version`, `entry_digest` chained to the previous entry.

Act-time rule: immediately before each mutation the executor (1) calls C2's verifier on `approval_ref` + `mutation_digest`; (2) re-checks the target against `snapshot_ref` via C3's comparison. Any failure, or any unavailable verifier, → **no mutation, fail closed** (consistent with C5 P8's fail-closed unattended mode and C2 RP-13's own "degrades to weaker" warning).

Resume table:

| Step state found | Step class (Pack 002) | Resume action |
|---|---|---|
| No intent | any | Execute normally (re-verify) |
| Intent, no outcome | `PURE_READ` | Re-run |
| Intent, no outcome | `IDEMPOTENT_WRITE` | Reconcile by read-back, then re-run if absent |
| Intent, no outcome | `NON_IDEMPOTENT_WRITE` / `EXTERNAL_IRREVERSIBLE` | **Stop, mark `UNKNOWN`, escalate to C5** |
| Outcome `SUCCEEDED` | any | Skip |
| Outcome `UNKNOWN` | any | Reconcile first; never blind replay |
| Outcome `FAILED` | any | Retry policy (Pack 002) |

Resume loads structured state only (C5 P10 default). If audit-grade resume is required, add a trajectory reference per P10's own reject-if; whether it is required is **C5/C6's open call**.

#### 4.1.6 Ownership and failure semantics

C4: record format, act-time rule, resume table. C2: verifier and authorization policy. C3: snapshot comparison, storage and isolation. C5: Resume UX and `UNKNOWN` escalations. C6: trajectory content, integrity checks, E5-style testing. Truncated tail → last entry treated as absent, step `UNKNOWN`. **Delivery claim:** at-least-once *attempt* with reconciliation. **No exactly-once guarantee.**

#### 4.1.7 Idempotency, cancellation, timeout, retry, rollback

Duplicate protection: journal checked before dispatch; a step with `SUCCEEDED` or `UNKNOWN` outcome is never re-dispatched blind. Cancellation (C5 E4 STOP): between mutations; mid-mutation only if the adapter declares the operation atomic and cancellable. Timeout → `UNKNOWN`, not `FAILED`. Rollback for repository edits: Pattern D per-patch revert; everything else per Pack 002. Duplicate resumers: needs an exclusive-holder primitive that **C3 has not defined** (open).

#### 4.1.8 Operational and token/cost impact

One small append per step (two for mutating steps); resume loads a derived state view. Size and count thresholds are **not yet agreed**.

#### 4.1.9 Failure-injection scenarios (`TEST SPECIFIED`, not executed)

1. Kill between INTENT and the action. 2. Kill between the action and OUTCOME. 3. Truncate the final entry. 4. Break the hash chain. 5. Target changes after task start but before the act (C3 E3 covers only task start) → precondition mismatch, no write. 6. Verifier unavailable → fail closed. 7. Approval expired or revoked while paused → refuse (C2 owns the semantics). 8. Resume against a stale snapshot. 9. `commit_ref` reverted via Pattern D while paused → `UNKNOWN`, not silent skip. 10. Two resumers start concurrently (blocked on the missing C3 primitive). 11. `schema_version` newer than the reader supports.

#### 4.1.10 Acceptance criteria

C5 E5 already fixes the principle: any action executed twice across a resume is a failure. Numeric trial counts and size bounds **need agreement** (C3 E4 also leaves N undetermined).

#### 4.1.11 Rejection and experiment

- **EXP-001-A** (`TEST SPECIFIED`): 20-step sandbox task, crash at every boundary and scenarios 5–9; count duplicate side effects (target 0) and mis-skipped steps. Reject if C6/C3 already guarantee the same.

#### 4.1.12 Conflicts and assumptions

- No conflict with supplied artifacts. Overlap with C6 Pattern 3 is resolved by reference, not by a second log; step granularity is open (needs C1).
- Assumes C2 can expose a synchronous verify call even if RP-13 stays at a weaker, non-cryptographic level.

---

### FCP-C4-ENG-002 — Effect Classes, Retry, and Compensation Semantics

**Status:** `DESIGNED` · `NOT_IMPLEMENTED` · tests `TEST SPECIFIED` · **Local evidence:** NONE on retry/idempotency/compensation; adjacent on reversibility (C5 P5) · **Classification:** `FUTURE TRIGGER` (proposed label `UNKNOWN`)

#### 4.2.1 Analysis block

- **SOURCE:** C5 P5 (reversibility instead of pre-approval, Aider `/undo`; `REJECT` as ARGON default, `NEEDS EXPERIMENT` for a narrow carve-out, L216); C5 P10 note (a gate belongs only on irreversible or compliance nodes, L654); protocol Pattern D and Appendix §2/§5 (SWE-ReX local/Docker/AWS/Modal backends). Background knowledge, unverified this run: idempotency keys, the saga pattern, at-least-once delivery with idempotent consumers.
- **OBSERVED:** no supplied artifact classifies actions by retry safety or compensation. C5 repeatedly reasons about irreversibility and a "containment-scope indicator" without a defined input for it.
- **WHY IT WORKS:** retry is safe only for actions that are naturally or explicitly idempotent; the safe default for everything else is stop and reconcile.
- **GENERAL PRINCIPLE:** classify effects once; derive retry, dedupe and undo from the class.
- **ARGON ADAPTATION:** a declared taxonomy attached to each mutation and each adapter capability. It supplies **data** that C5 may use for gating or display; it does not decide approval policy, and C5 has rejected "reversible → skip approval" as a default.
- **TRADEOFF:** authors must classify honestly; a wrong class defeats the protection.
- **REJECT IF:** every real action stays inside a git-reversible repository (Pattern D revert then suffices).
- **EXPERIMENT:** EXP-002-A.

#### 4.2.2 Trigger and prerequisites

**Trigger:** first action with an effect outside a git-reversible repository (e.g., remote execution backend, external API call), or the first observed duplicate or partial failure. **Prerequisites:** Pack 001 mutation IDs; Pack 003 capability declarations (or an interim manual declaration).

#### 4.2.3 Effect taxonomy (specification)

| Effect class | Auto-retry | Unknown-outcome handling |
|---|---|---|
| `PURE_READ` | Yes, bounded | Re-run |
| `IDEMPOTENT_WRITE` (natural or keyed) | Yes, same key, bounded | Reconcile by read-back, then re-run if absent |
| `NON_IDEMPOTENT_WRITE` | **No** | Stop, `UNKNOWN`, escalate |
| `EXTERNAL_IRREVERSIBLE` | **No** | Stop, escalate; explicit operator decision |

Reversibility: `REVERSIBLE` (exact inverse, e.g., Pattern D revert), `COMPENSABLE` (semantic counter-action, may leave residue), `IRREVERSIBLE`.

#### 4.2.4 Proposed contract (unimplemented)

Per mutation: `effect_class`, `reversibility`, optional `idempotency_key` (deterministic from `task_id` + `step_id`), `compensation` (reference or `none`), `retry` {`max_attempts`, `backoff`, `retryable_errors[]`}, `timeout`. On failure at step *k*, compensate completed reversible/compensable steps in reverse order **only if** the task's `on_failure` policy says so. Rollback is claimed only where a snapshot or version-control base exists.

**Delivery claim:** automatic dispatch is at-least-once only for `PURE_READ` and `IDEMPOTENT_WRITE`; otherwise at-most-once with human resolution of unknowns. **No exactly-once guarantee is made or implied.**

#### 4.2.5 Ownership, interactions, cost

C4: taxonomy and mechanics. C2: may restrict classes (e.g., deny `EXTERNAL_IRREVERSIBLE` without extra authorization). C5: owns whether and how class data appears in approval UX or the containment-scope indicator. C6: reconcile and dedupe verification. C3: persistence via Pack 001. Cost is low: extra fields and one read-back per reconcile.

#### 4.2.6 Failure-injection scenarios (`TEST SPECIFIED`, not executed)

1. Action succeeds, response lost. 2. Double dispatch of a keyed write. 3. Failure at step 3 of 5 with compensation configured. 4. Compensation itself fails. 5. Adapter mislabels a non-idempotent action as idempotent. 6. Partial multi-file write. 7. Retry exhaustion. 8. Revert of a patch that later patches depend on (protocol Pattern D's own TEST NEEDED, L255).

#### 4.2.7 Acceptance criteria and experiment

**Needs agreement.** Proposed: zero duplicate side effects for `IDEMPOTENT_WRITE` in scenarios 1–2; zero automatic retries for non-idempotent classes; scenarios 4–5 end in explicit escalation. **EXP-002-A** (`TEST SPECIFIED`): fault-injecting proxy (drop-response, duplicate-dispatch) in a sandbox; verify effect counts. Reject if all real actions are git-reversible.

#### 4.2.8 Conflicts and assumptions

No conflict found. Unresolved: who audits effect-class declarations (candidate: C6 contract vectors via Pack 003).

---

### FCP-C4-ENG-003 — Versioned Adapter Contracts and Capability Discovery

**Status:** `DESIGNED` · `NOT_IMPLEMENTED` · tests `TEST SPECIFIED` · **Local evidence:** adjacent (C2 trust side); functional contract NONE · **Classification:** `FUTURE TRIGGER` (proposed label `UNKNOWN`)

#### 4.3.1 Analysis block

- **SOURCE:** C2 RP-11 (L681–L741), RP-12 (L742–L789), Model Portability section (L1141–L1156); protocol Appendix §2/§5 (SWE-ReX environment independence; model vs environment portability as separate axes); C7 open item "adapter-boundary sufficiency". Background knowledge, unverified this run: semantic versioning, JSON Schema.
- **OBSERVED:** C2 treats `Adapter` as a rule-location tier, requires manifest re-validation on change (the "rug pull" case), and says secrets should be resolved server-side by the tool/adapter. Nothing defines version compatibility, capability discovery, or contract tests. C1's E3 (not supplied) is open per C7.
- **WHY IT WORKS:** an explicit, checkable contract exposes incompatibility at preflight instead of mid-mutation.
- **GENERAL PRINCIPLE:** additive-only change within a major version; detect incompatibility before acting.
- **ARGON ADAPTATION:** a functional manifest plus golden vectors per capability. **Trust and security stay with C2:** this pack adds a `manifest_digest` recorded at approval time, and a mismatch routes to C2's re-review path rather than defining its own.
- **TRADEOFF:** manifest and vector maintenance; premature with one adapter.
- **REJECT IF:** only one adapter exists with no planned change, or C1's adapter-boundary design (unsupplied) already declares versions and schemas.
- **EXPERIMENT:** EXP-003-A.

#### 4.3.2 Scope

Tool and environment adapters, in C2's `Adapter` tier sense. **Model adapters are excluded** until the term is defined for the model axis (the protocol warns not to conflate the two portability axes, Appendix §5). Resolving the full definition needs C1.

#### 4.3.3 Trigger and prerequisites

**Trigger:** second adapter, first breaking adapter change, or first compatibility incident. **Prerequisites:** a manifest registry location; Pack 002 effect classes; C2's decision on manifest re-review.

#### 4.3.4 Proposed contract (unimplemented)

Manifest: `adapter_id`, `contract_version` (semver), `adapter_kind` (`tool` | `environment`), `capabilities[]` each with `name`, `input_schema`, `output_schema`, `effect_class` and `reversibility` (Pack 002), `timeout`, `cancel_supported`, `error_taxonomy`, `deprecated_after` (optional).

Rules: (1) discover capabilities from the manifest, never assume; (2) preflight: the recorded major version must match; (3) within a major only additive changes; (4) every capability ships golden vectors, run by C6 on any adapter change; (5) unknown output fields ignored on read, unknown required input fields refused on write; (6) an adapter that omits timeout, cancel or idempotency declarations is treated as non-cancellable and non-idempotent; (7) `manifest_digest` change after approval → C2 re-review, no silent continuation.

#### 4.3.5 Ownership, failure, cost

C4: manifest format and compatibility rules. C2: trust, origin tier, secrets, manifest re-review. C6: vectors and verification. C3: stores manifests. C5: informed of deprecations that affect operators. Incompatibility → refuse at preflight, no mutation. Cost is small; most effort is vectors.

#### 4.3.6 Failure-injection scenarios (`TEST SPECIFIED`, not executed)

1. Output field type changed. 2. Declared capability absent at runtime. 3. Major-version mismatch. 4. Adapter declares idempotent but duplicates effects. 5. Unknown fields in input and output. 6. Manifest missing or malformed. 7. Model-adapter manifest submitted to the tool/environment registry → rejected. 8. Manifest changes after approval (shares C2 RP-11's mock-server test; run once, owned by C2/C6).

#### 4.3.7 Acceptance criteria and experiment

**Needs agreement.** Proposed: 100% of scenarios 1–3, 6, 7 refused at preflight or by vectors; 4 caught by a vector probe. Deprecation-window length is a **`BUSINESS DECISION`**, left open. **EXP-003-A** (`TEST SPECIFIED`): two stub adapters and one deliberate breaking change; verify preflight blocks it before any mutation.

#### 4.3.8 Conflicts and assumptions

C1's adapter design is unseen; this pack must align with it. Assumes JSON Schema is acceptable to C1 and C3.

---

## 5. Pack summary

| Pack | Topic | Classification (brief / proposed program label) | Local evidence | Depends on |
|---|---|---|---|---|
| FCP-C4-ENG-001 | Execution record and resume journal | `FUTURE TRIGGER` / `UNKNOWN` | Demand strong, spec none | 002; C2 verifier; C3 snapshot compare; C6 trajectory ref |
| FCP-C4-ENG-002 | Effect classes, retry, compensation | `FUTURE TRIGGER` / `UNKNOWN` | None | 001, 003 (soft) |
| FCP-C4-ENG-003 | Versioned adapter contracts | `FUTURE TRIGGER` / `UNKNOWN` | Adjacent (C2) | 002; C2 re-review |
| (none) | Delegation depth | `NOT NEEDED` / `UNKNOWN` | Second-hand only | C1 |

Suggested order if triggers fire: 002 → 001 → 003 (003 first if a second adapter appears). All share the sandbox prerequisite.

---

## 6. Cross-cloud ownership and dependency matrix

| Cloud | 001 Execution record / resume | 002 Effect classes | 003 Adapter contracts |
|---|---|---|---|
| **C1** (harness, per C7; unsupplied) | Step granularity; hook points; Synthesis owner | Retry dispatcher | Adapter registry; E3 |
| **C2** (security) | `approval_ref` verifier; RP-13 binding; RP-1 PLAN gating | May restrict classes | Trust, secrets, manifest re-review (RP-11/12) |
| **C3** (context) | Snapshot comparison; storage candidate; isolation and lease (open) | Persists outcomes | Stores manifests |
| **C4** (this role) | Record format, act-time rule, resume table | Taxonomy and mechanics | Manifest and compatibility rules |
| **C5** (operator) | Resume UX; `UNKNOWN` escalation; E3/E4/E5 | Decides how class data is shown or gated | Deprecation notices |
| **C6** (evaluation) | Trajectory log (Pattern 3); journal integrity; checkpoint ownership **not yet defined** | Reconcile/dedupe checks | Golden vectors |
| **C7** (audit) | Crash-window and binding audits | Delivery-semantics claims | Declared vs actual capability |

C4 defines executor mechanics only. Human approval policy stays with C5, authorization with C2, context with C3.

---

## 7. Experiments that remain open

| ID | Question | Owner | Status |
|---|---|---|---|
| Protocol Experiments 1–7 | Localization, minimality, regression, reproduction, unrelated touches, repair-after-localization, E/H false-positive | C4/C6 | Defined; **not executed** |
| Plan/Act five-to-six route test (C2 RP-1, C4 Pattern F, C1 E2) | Is PLAN structurally mutation-free? | C2/C6 | `TEST SPECIFIED`, not run; **taxonomy divergence unreconciled** (C7 minor) |
| C2 RP-13 sub-questions (key custody, identity, replay, expiry, revocation, exact-payload binding) | Action-binding design | C2 | `NEEDS EXPERIMENT` |
| C3 E3, E4 | Stale-context detection; cross-task isolation | C3 | Defined, not run |
| C5 E3, E4, E5 | Action mismatch; STOP latency; recovery without duplicates | C5/C6 | Defined, not run |
| C1 E1b (delegation depth), E3 (adapter boundary) | Per C7 | C1 | **Unseen**; open per C7 |
| Dual-gate vs C3 chain-resolution overlap | Net-new or duplicate? | C6/C3 | `UNKNOWN`; C6 says the C3 file needed to resolve it was unattached |
| EXP-001-A, EXP-002-A, EXP-003-A | This document | C4 | `TEST SPECIFIED`, not run |

**Suggested, not decided:** a single shared Plan/Act route suite built from the union of C2's and C4's lists (up to six routes) so the five-vs-six divergence stops recurring. That is a C6/Synthesis decision.

None of these is resolved by this document.

---

## 8. Assumptions, unresolved items, conflicts

- **U1 — Checkpoint ownership gap.** C5 assigns the dependency to C6; C6 has no checkpoint content; C3 owns the snapshot. Pack 001 assumes Synthesis picks a storage owner (C3 or C6).
- **U2 — Lease/concurrency primitive.** Not defined by C3; blocks duplicate-resumer protection.
- **U3 — "Adapter" definition.** Partially defined by C2's tier vocabulary; full definition needs C1.
- **U4 — Classification taxonomy.** The brief's labels appear in no artifact; my mapping is unverified (§1.4).
- **U5 — Acceptance numbers.** All thresholds marked "needs agreement" stay open.
- **U6 (`BUSINESS DECISION`):** adapter deprecation-window length.
- **U7 — Protocol cross-reference inconsistencies** (§1.3): reported, not fixed (fixing them would modify a canonical artifact).
- **U8 — Wave 3.5 object definitions** (Approval, Task Packet, Verification Record, `execution_stage`) were not supplied; Pack 001's references to them are by name only.
- **Conflicts:** none confirmed against supplied artifacts. Conflicts with the unsupplied C1 design can be neither confirmed nor ruled out.

---

## 9. Evidence inventory

| Claim class | State | Basis |
|---|---|---|
| Hashes of C2, C3, C4, C5, C6 vs manifests | **Verified this run** | `sha256sum`; all five match |
| C7 duplicate files identical in content | **Verified this run** | whitespace-normalized diff, 0 differing lines |
| Contents and line references for C2–C7 | **Verified this run** | Files read; terms searched case-insensitively in the supplied copies |
| Absence claims (`idempot`, `compensat`, checkpoint in C6/C2, `C3` in protocol) | **Verified this run** | Same searches |
| C1 content (depth = 1, E1b, E2, E3, GitHub issues) | **Second-hand via C7; C1 not seen** | C7-FFA-003 text |
| C7's own verification of C1 claims (S1–S3) | **Not independently checked** | Reported by C7 |
| Vendor and paper citations in the artifacts (Cline, Aider, LangGraph, SWE-agent, HARP, AgentAck, OWASP MCP, etc.) | **Via artifacts, not re-fetched** | Accessed 2026-09-20 by their authors; may have changed |
| General patterns (write-ahead log, idempotency keys, saga, semver, JSON Schema) | **Background knowledge, unverified this run** | Design inspiration only |
| Any test result | **None exists** | Nothing executed |

---

## 10. Change summary

- **Written:** `C4-FUTURE-ENGINEERING-CAPABILITY-PACKS.md` (this file), the only artifact produced; it replaces my earlier drafts of the same file.
- **Opened read-only, not modified:** the C4 protocol and manifest, and the supplied C2, C3, C5, C6 and C7 files and manifests (uploads are read-only; only hashes and text were read).
- **Not modified:** any other canonical artifact. None others were supplied (C1 is missing).
- **Not done:** no code, no mutations executed, no architecture change, no new research round, no test executed, no open experiment declared resolved, no manifest created for this deliverable.

### Delta from v2 (for the reader)

1. v2 claimed no Cloud covers act-side authorization binding. **Wrong:** C2 RP-13 and C5 P4/E3 cover it. Removed from my scope.
2. v2's four packs became three (merge of Plan/Act record and checkpoint journal) to avoid overlap with C2, C3, C5 and C6.
3. v2 listed Q2–Q6 as having no evidence. Now: Q2 resolved to a minor reported divergence; Q3 second-hand; Q4 partly defined by C2; Q5 shows a real ownership gap; Q6 sits with C3 as `NEEDS EXPERIMENT`.
4. New: overlap map (§3), `approval_ref`/`snapshot_ref`/`trajectory_step_ref` references instead of duplicate records, act-time re-check closing the gap between C3's task-start staleness check and the actual mutation.

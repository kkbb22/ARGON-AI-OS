# C3 — FUTURE CONTEXT AND KNOWLEDGE CAPABILITY PACKS

```yaml
artifact_kind: future_capability_portfolio
cloud: C3
wave: cloud-evolution-sprint
system_scope: ai_engineering_os
repository_target: none
execution_target: deliverable_output
status: DESIGNED
implementation_status: NOT_IMPLEMENTED
revision: r3
date: 2026-10-12
# report_sha256 intentionally not embedded (hash contract used by the other Clouds
# keeps it in a companion manifest; no manifest was requested or created here).
```

**Project:** ARGON AI-OS (not ARGON Health; no clinical data-model assumptions imported)
**Owner role:** C3 (Context, Knowledge, Provenance, Data)
**Document status:** research and design only. Additive. Every pack is `FUTURE` / `NOT_IMPLEMENTED`.
**Revision history:** r1 was written with no source artifacts. r2 was rebuilt against the C3 research and manifest. **r3 (this file) is rebuilt against the full package: C2–C6 research and manifests, plus the C7 final forensic audit.** It supersedes r1 and r2 of this same filename.

---

## 0. Inspection Report

### 0.1 Artifacts inspected and verified

I computed SHA-256 on the uploaded bytes myself and compared against each manifest.

| Cloud | Artifact | My `sha256sum` | Manifest value | Result |
|---|---|---|---|---|
| C2 | `C2-CLOUD-SECURITY-ADAPTER-RESEARCH.md` | `c6e95c26…0b99` | `c6e95c26…0b99` | MATCH |
| C3 | `C3-CONTEXT-ENGINE-RESEARCH.md` (two uploaded copies) | `b48cbb0b…042c` | `b48cbb0b…042c` | MATCH; both copies byte-identical (`cmp`) |
| C4 | `C4-SURGICAL-ENGINEERING-PROTOCOL.md` | `441007bc…1c01651` | `441007bc…1c01651` | MATCH |
| C5 | `C5-OPERATOR-CONTROL-RESEARCH.md` | `e70ea36b…e1a8` | `e70ea36b…e1a8` | MATCH |
| C6 | `C6-CLOUD-EVALUATION-ENGINE.md` | `a0d762ad…946a` | `a0d762ad…946a` | MATCH |
| C7 | `C7-FINAL-FORENSIC-AUDIT-COMPLETE.md` and `C7-FFA-003.md` | not hashed (no manifest) | n/a | Same audit; second copy is a whitespace-reformatted table layout; content read from both |

All six manifests I was given carry the shared triple `system_scope: ai_engineering_os / repository_target: none / execution_target: deliverable_output`, matching what C7 reports. I read every file in full.

### 0.2 Still unavailable (limitations)

| Item | Status |
|---|---|
| **C1 artifact** (`c1-cloud-evolution-harness-v4-final`) | **Not provided.** C7 lists it and verifies its hash, but I do not have it. |
| **Wave 3.5 schemas** (Repository Snapshot, Source, Evidence Record, Claim, Verification Record, Context Projection, Context Packet, Task Packet, Dependency record) and `C1-C3-WAVE3.5-CONVERGENCE-v3` | **Not provided.** I know these objects only as described in C2–C6. Field names I use (e.g. `excluded_note`, `claim_status`, `source_status`) are quoted from those artifacts, not verified against a schema. |
| The "earlier internal artifact" that proposed T0–T5 context tiering | **Not provided.** C6 states it is not in its own package either. |
| Canonical definitions of `NOW` / `ARCHITECTURE-READY` / `FUTURE TRIGGER` / `NOT NEEDED` / `BUSINESS DECISION` | **Not found in any artifact.** The artifacts use a different vocabulary (below). Classifications here are therefore provisional. |
| C3's unattached "knowledge-model artifact" (cited by C6 Pattern 6) | Not provided. |
| Directory convention | Artifacts are delivered as flat files with a `.manifest.yaml` companion; I did not verify a directory. Returned under the requested filename. |

### 0.3 What the new artifacts change about earlier statements

1. **C7 audit now exists.** My r1/r2 said no C7 record existed, following C3's own note that `C7-CLOUD-EVOLUTION-FINAL-AUDIT.v3` never existed. That named file still does not exist; the actual audit is `C7-FFA-003` (2026-10-07), verdict **CLEAN WITH OPEN EXPERIMENTS**.
2. **Limit of what C7 verified about C3.** C7 hash-verified C3 and confirmed C3's earlier fixes (broken citations, cross-reference, threshold, caveats). C7's source-level spot checks (Gate 3) covered **C1's claims only**. C3's external-source claims (e.g. the "Lost in the Middle" percentages, which C3 read via summary sites, per its §9 row 15; Aider's 50×/8× from a third-party issue; OpenHands' 80/first-4 from a community walkthrough) have **not** been spot-checked by C7. I treat them accordingly.
3. **T0–T5 now has partial evidence.** See §1.2. It exists only as a *proposal*, defined by endpoints.
4. **Vocabulary.** The artifacts classify patterns as `ADOPT / ADAPT / REJECT / UNKNOWN / NEEDS EXPERIMENT` and use `REQUIRES HUMAN DECISION` (C2), with status `DESIGNED` + `NOT_IMPLEMENTED`. The five labels in the brief are not defined anywhere I can see. I keep the brief's labels, mark them provisional, and do not invent new ones.
5. **This document has not been audited by C7.**

### 0.4 Evidence labels

**[V]** verified observation, with identifiable source · **[S]** strongly supported inference · **[P]** proposal requiring an experiment · **[U]** unknown or unavailable.

Where I cite an external fact, I cite it **as the Cloud artifact reports it** and keep that artifact's own caveat. I did not re-fetch any URL in this task. No vendor constant (50×/8×, 80/first-4, 5-turn window, 25→5 retrieve/rerank) is proposed as an ARGON value; the artifacts themselves forbid that reading.

---

## 1. What Already Exists (so I do not duplicate it)

Everything below is `DESIGNED` / `NOT_IMPLEMENTED` per the artifacts. Nothing has been built or run.

### 1.1 Existing designs in the Cloud artifacts

| Existing item | Source | Status |
|---|---|---|
| Context Projection (versioned rule) vs. Context Packet (instance) split | C3 §1 | Wave 3.5 object; not externally validated |
| Repository Snapshot, `head` vs `origin_head` freshness comparison | C3 §4 | Only concrete freshness mechanism found anywhere |
| `Claim → Evidence Record → Source → Verification Record` chain | C3 §6, C2 RP-14, C6 metrics | Wave 3.5 design |
| Pipeline `Task Packet → Repository Snapshot → Repo Map → Relevance → Context Projection → Context Packet` | C3 §2 Design Output | **PROPOSAL**, not ratified by C1 |
| Ordering constraint (relevant items near start/end) | C3 P11 | ADOPT |
| Summarize-not-truncate / "never compress authority away" | C3 P13 | ADOPT |
| Two-trigger condensation structure | C3 P6 | ADOPT structure; thresholds UNKNOWN |
| Within-task trajectory compression; durable store never compressed | C6 Pattern 4 | ADAPT; window UNKNOWN |
| Five-field trajectory record (response/thought/action/observation/state) | C6 Pattern 3 | ADAPT; proposed to C3 as schema owner |
| Metrics incl. Grounding, Evidence integrity, Token efficiency, False completion | C6 §3 | DESIGNED |
| Approval-UX/Display rules: UI is Display/Guidance only, never Authority | C5 Human Authority Boundary | C5-original PROPOSAL |
| Experiments E1–E6 (C3), E1–E8 (C5), Experiments 1–7 (C4), six (C6) | respective §7 | **None run** |

### 1.2 T0–T5: what the artifacts actually say

- C6 (Self-Containment Note) restates the concept as: *"a graduated context-loading model (T0 = task identity/hard constraints, through T5 = optional exploration) where a task loads only the tiers its size/risk justifies."* It labels this "previously proposed in an earlier internal artifact, **not independently verified in this package**" and says no `token_discipline` test is built or run.
- C3 P2 references a C6 audit need for *"a clean boolean 'was tier T4 loaded, yes/no'"*.
- C6's **Token efficiency** metric is defined as tokens loaded ÷ the ceiling the task's tier implies, with the tier-assignment logic itself marked `NEEDS EXPERIMENT`.

So: **T0 and T5 endpoints and the T4 audit boolean are the only verified descriptions. T1–T3 are undefined, ceilings are undefined, and the originating artifact is unavailable.** I do not define them. This portfolio is written to be tier-agnostic and to *consume* whatever T0–T5 definition is later ratified.

### 1.3 Consequence for scope

A provenance-ledger pack, a retrieval-pipeline pack, a trajectory-schema pack, and a "token budget policy" pack would each duplicate existing designs. Packs below are restricted to gaps the artifacts themselves leave open.

---

## 2. Identified Gaps

| Gap | Evidence | Pack |
|---|---|---|
| G1 — No rule for when a Context Packet must be re-fetched or recompiled; false completion from stale context "not addressed by any source studied"; **C7 lists "checkpoint stale-state resumption" as open** | C3 §4, §12; C7 "What remains open" | 001 |
| G2 — Compression tests (E5) check recoverability of a planted *fact*, not constraints or uncertainty; evidence preservation through compression is "ARGON-original … not externally validated" | C3 §5, E5; C6 Pattern 4 | 002 |
| G3 — Dynamic budget fitting vs. C6's boolean tier audit is an "unresolved tension"; tier definitions and ceilings undefined; C6's token-efficiency metric has no denominator yet | C3 P2; C6 §3, §0 | 003 |
| G4 — Task context isolation has "no external precedent"; C2 adds untrusted-content channels (config files, MCP tool results, secrets) that a context packet can carry; **C7 lists task-context isolation as needing an implementation environment** | C3 §3, E4; C2 RP-7/11/12; C7 | 004 |

Checkpointing is **not** a standalone gap for C3 (see §4).

---

## 3. Pack Portfolio

Common reject condition **R-DUP:** an existing or ratified artifact (including C1's, which I cannot see) already provides the capability. Common rules: no new infrastructure is assumed; all interfaces and fields below are **PROPOSED**; nothing claims an interface exists.

---

### FCP-C3-CTX-001 — Freshness and Staleness Contract for Context Packets (includes context reconstruction)

**Status:** `FUTURE` / `NOT_IMPLEMENTED` · **Provisional class:** `FUTURE TRIGGER`

**Problem and value.** C3 §4 establishes that staleness means "the underlying state changed since context was captured," but gives **no rule** for re-fetch vs. recompile and no mechanism against false Claims from stale context beyond the Verification Record design. C7 independently lists checkpoint stale-state resumption as unresolved. Value: freshness becomes a checkable property of a packet, and an interruption cannot silently resurrect stale context.

**Analysis chain.**
- SOURCE: C3 §4, E3, E6, §12; C5 P10, E8, P8; C6 False-completion metric; C2 RP-14; C7 open items.
- OBSERVED [V per artifacts]: (a) Git comparison of `head` vs `origin_head` is the only evidenced detection mechanism (C3). (b) LangGraph-style resume persists structured state, not the reasoning trace; C5 P10 classifies this ADOPT for the checkpoint shape, ADAPT if audit-preserving resume is also required (note: the official-doc status of other LangGraph claims was downgraded to UNKNOWN by C5; I rely only on the confirmed interrupt/checkpointer/resume mechanism). (c) C5 E8 proposes that a Display layer showing a stale approval badge can mislead operators, and concludes Display must re-fetch live Enforcement state rather than cache it. (d) C2 RP-14: a system where claim-maker and verifier are the same stack is weaker than one where they are separated (evidence quality `MODERATE`; arXiv, peer review unverified).
- WHY IT WORKS [S]: a packet built from changed inputs can no longer support the claims citing it; detection must precede use, and must not depend on the consumer's own say-so.
- GENERAL PRINCIPLE: every generated context instance declares the exact input versions it was built from; staleness is then a comparison, not a judgment.
- ARGON ADAPTATION [P]:
  1. **Freshness manifest** on the Packet: ids/versions of Repository Snapshot, Repo Map, Projection, Task Packet.
  2. Outcomes at use time: `FRESH`, `STALE_REFETCH` (snapshot moved), `STALE_RECOMPILE` (projection/map changed), `UNVERIFIED`. The mapping rules are **UNKNOWN until experiment**.
  3. **The check is performed by the Kernel/runtime, not by the Cloud that consumes the packet** (consistent with the existing "C6 does not self-certify" rule, which C2 notes is the RATS-style verifier split reached independently).
  4. **Display layers re-compute freshness at read time and never cache it** (C5 E8).
  5. **Reconstruction.** After an interruption a packet is *re-validated and, if needed, regenerated* from `(Task Packet, Repository Snapshot, Projection version)` with a **reconstruction diff**. A checkpoint carries structured state and **pointers** to sources and, where C6 requires audit-preserving resume, a pointer to the durable reasoning/evidence record, never a transcript copy (C5 P10, C6 Pattern 4).
- TRADEOFF: near-zero token cost (checks run outside the prompt); one comparison per use; recompute cost on staleness; over-triggering risk.
- REJECT IF: the Verification Record chain-resolution check (C3 E6) already blocks every stale-context false completion (R-DUP); or false-positive stale rate makes it unusable; or C1's design already encodes an equivalent manifest **[U, C1 not provided]**.

**Scope boundary with execution recovery.** C5 E5 (duplicate side effects after Resume, orphaned approvals) and Cline-style shadow-git rollback (C3 P9) concern **execution** recovery. They stay with C4/C6/C1. C3 only guarantees that the *knowledge state* handed to a resumed task is checked and regenerated.

**Activation trigger.** E3 shows snapshot comparison alone misses induced drift, **or** a stale-context false Claim (C6's `false_completion` canary) is traced to a packet, **or** tasks resume across interruptions in the real core (C7: requires implementation environment).

**Expected benefit [P].** Induced drift always detected (C3 sets 100%/0% false positives as the correctness bar for mechanical checks; I inherit that reasoning, not a new threshold). Refetch/recompile classification accuracy **NEEDS EXPERIMENT**.

**Prerequisites / ownership.** Owner C3 (semantics). Needs Wave 3.5 Repository Snapshot and Context Packet to exist; C1 ratification of Repo Map/Relevance if packets depend on them. Consumers: C6 (audit), C4 (trigger), C5 (display).

**Inputs / outputs / metadata (PROPOSED).** In: Context Packet + current snapshot state. Out: `{outcome, changed_inputs[], checked_at, checked_by}`. No packet body or secret in the record.

**Limits / retention / failure.** Retention per C7/C6 policy **[U]**. If freshness cannot be determined: `UNVERIFIED`; usable only with that marker visible; **in unattended runs, `UNVERIFIED` defaults to hold/deny for any step gated on human approval** (C5 P8 fail-closed, applicability pending C1/C2 scope **[U]**). A Claim may not advance past `asserted` on a `STALE`/`UNVERIFIED` packet (C3 E6 failure condition).

**Security / isolation.** Records hold ids/versions only; must not reveal existence of out-of-scope objects (CTX-004).

**Acceptance criteria.** Every packet use preceded by an outcome; induced drift always detected; stable repo yields no false `STALE`; `UNVERIFIED` never promoted; outcome produced by Kernel, not consumer; Display shows live outcome.

**Negative cases / tests.** Origin advanced after snapshot; projection version changed with snapshot unchanged; remote unreachable; packet from superseded Repo Map; checkpoint resumed after source deleted; stale badge shown after outcome flipped; checkpoint carrying a transcript or execution state (must be rejected).

**Bounded experiment.** *Baseline:* snapshot-only comparison on C3's E3 synthetic drift set **plus** a second class (projection/map change, snapshot unchanged) **plus** a resume-after-change class. *Measurement:* detection rate, false-positive rate, undetected-stale-on-resume rate. *Falsification:* if snapshot-only comparison already detects 100% of all classes, **reject the pack**.

**Alternatives.** Always recompile at task start; rely on Verification Record chain resolution only.

**Conflicts / assumptions.** Packet schema unseen **[U]**. **Checkpoint ownership is inconsistent across artifacts:** C3 P9 says checkpointing is "C1/C2 territory"; C5 E5 and appendix say the checkpoint dependency sits with C6. Unresolved, not decided here.

---

### FCP-C3-CTX-002 — Constraint and Uncertainty Preservation Check for Compression

**Status:** `FUTURE` / `NOT_IMPLEMENTED` · **Provisional class:** `FUTURE TRIGGER` (gated on the P15 pre-experiment)

**Problem and value.** C3 E5 tests whether a *planted fact* stays recoverable via its Source after collapse. Nothing tests whether the **active** context an agent actually reads still contains **constraints, numeric limits, negations, or stated uncertainty**. A Source pointer helps only if it is dereferenced. Value: close that blind spot in the Projection rendering step.

**Analysis chain.**
- SOURCE: C3 §5, E5, P5, P6, P11, P13, P15; C6 Pattern 4, Grounding metric; C2 RP-11, RP-12; C4 Pattern E.
- OBSERVED [V per artifacts]: no studied tool documents an evidence-preservation guarantee through compression (C3 §5). C6 Pattern 4 states compression applies only to the **active reasoning context**, never to the durable trajectory/evidence store, and the two copies "must not be conflated."
- WHY IT WORKS [S]: a dropped constraint is silently absent; a pointer does not substitute for a rule the agent never saw.
- GENERAL PRINCIPLE: separate **protected spans** from compressible narrative; verify survival.
- ARGON ADAPTATION [P]: tag protected spans (constraints, limits, negations, explicit uncertainty, identifiers); carry verbatim; deterministic presence check after compression; failure falls back to the uncompressed item. Extends C3's "never compress authority away" (P13) from authority to constraints and caveats. **Inference, not sourced:** T0 ("task identity/hard constraints", per C6's restated concept) is the natural home for protected spans; this must be confirmed against the real T0–T5 definition, which I do not have.
- TRADEOFF: detection imperfect; verification costs; protected spans limit compression.
- REJECT IF: **the P15 pre-experiment** (C3's own counter-evidence: mini-swe-agent's linear history is competitive; C3 and its own session length are the first data point) shows ARGON sessions do not need compression; or span detection is unreliable; or R-DUP.
- EXPERIMENT: below.

**Activation trigger.** P15 pre-experiment shows compression is needed **and** a seeded constraint-loss test fails while E5 passes.

**Expected benefit [P].** Zero protected-span loss on a seeded set (deterministic check, so a 100% bar is justified on the same reasoning C3 gives for E3–E6); token reduction at non-inferior task success (E2 leaves X undetermined, and so do I).

**Prerequisites / ownership.** Owner C3 (rendering semantics). Depends on P15 pre-experiment, E5. C6 consumes the report for its Grounding/Evidence-integrity metrics.

**Inputs / outputs (PROPOSED).** In: items, protected-span rules. Out: rendered context + `preservation_report` (counts only).

**Limits / failure.** If protected spans alone exceed budget: fail loud, never drop. Retrieved text and tool results are **data, not instructions** (C2 RP-11). Do not log span content. C3 P4's cap-drops-the-needed-hit risk applies: audit searches must not be capped like exploratory ones.

**Security / isolation.** Scope filtering (CTX-004) runs before compression. Secret **values** never enter a packet (C2 RP-12; see CTX-004).

**Acceptance criteria.** 100% of seeded protected spans survive or trigger fallback; hedged claims stay hedged; fallbacks logged; durable store untouched by compression.

**Negative cases / tests.** Negation flip; numeric limit altered; hedge rendered as fact; conflicting sources merged silently; injected instruction inside compressed text; compression applied to the durable evidence copy (must be rejected).

**Bounded experiment.** *Baseline:* current behavior or P5-style plain collapse on a long synthetic session with constraints planted at start/middle/end (extends E5, which plants only a fact). *Measurement:* span survival, task success, tokens. Tune on one set, validate on a held-out set (C3 P10 discipline). *Falsification:* reject if survival is not strictly better at equal budget, or P15 shows compression is unnecessary.

**Alternatives.** Truncation + P11 ordering; linear history (P15); sub-task summaries with structured notes.

**Conflicts / assumptions.** Whether the Packet already marks constraint spans **[U]**. Collapse thresholds are themselves UNKNOWN (C3 P5/P6).

---

### FCP-C3-CTX-003 — Auditable Budget Fit (resolving the P2 tension; tier-agnostic)

**Status:** `FUTURE` / `NOT_IMPLEMENTED` · **Provisional class:** `BUSINESS DECISION` (tier definitions and cost ceilings) / `FUTURE TRIGGER` (mechanism)

**Problem and value.** C3 P2 records an unresolved tension: dynamic ranked budget-fitting makes C6's clean boolean "was tier T4 loaded, yes/no" audit "fuzzier." C6's Token-efficiency metric needs a denominator (the tier ceiling) that does not yet exist. Value: let dynamic fitting coexist with a boolean tier audit, without importing any vendor number.

**T0–T5 handling.** See §1.2. This pack **does not define tiers**. It states a requirement on whatever scheme gets ratified and must be mapped by the tier owner. If C6's restated model (T0 hard constraints … T5 optional exploration) is ratified, the pack applies to it unchanged.

**Analysis chain.**
- SOURCE: C3 P2, P14, P15, §5; C6 §3 (Token efficiency), Pattern 4.
- OBSERVED [V per artifacts]: ranked budget-fitted selection exists (Aider; constants are Aider's own tuning); retrieve-then-rerank exists (Continue, defaults 25→5); C3 notes both may not pay off at ARGON-HEALTH's current 53-file scale.
- GENERAL PRINCIPLE [P]: **decide tier inclusion deterministically; fit dynamically only within a loaded tier.**
- ARGON ADAPTATION [P]: Packet records a boolean `loaded` **per tier** (deterministic, for C6's audit) and a separate `fit_report` for dynamic selection inside loaded tiers. A tier may never silently flip from loaded to not-loaded; that is an explicit, logged event. `fit_report` also emits `tokens_loaded` and `tier_ceiling` so C6's Token-efficiency ratio is computable once ceilings exist.
- TRADEOFF: some fitting efficiency lost; extra reporting.
- REJECT IF: C6 accepts fuzzy tier audits; P15 shows budgets never bind; or R-DUP.

**Activation trigger.** E2 shows budget-fitted context saves tokens without success loss **and** C6 confirms the boolean audit requirement stands **and** a tier scheme is ratified.

**Expected benefit [P].** Tier booleans reproducible 100% of runs on identical inputs (mechanical check); token savings **NEEDS EXPERIMENT**.

**Prerequisites / ownership.** Owner C3 for fit semantics; **C6 owns the audit consumption**; tier definitions owner **[U]**.

**Inputs / outputs (PROPOSED).** In: ranked candidates, tier assignments, budget. Out: Packet with per-tier boolean + `fit_report` (counts and sums only).

**Limits / failure.** Mandatory-tier overflow: fail loud, never shrink silently. Token counts must use the target model's tokenizer; mismatch flagged **[S]**.

**Security / isolation.** Telemetry carries no content. Per-scope budgets only if multiple scopes exist (CTX-004).

**Acceptance criteria.** Tier booleans identical across re-runs; no silent demotion; fit report for every packet; `tokens_loaded`/`tier_ceiling` present for C6.

**Negative cases / tests.** Oversized mandatory item; tokenizer mismatch; ranking change flipping a tier boolean; budget below mandatory-tier size.

**Bounded experiment.** *Baseline:* whole-file loading (C3 E2). *Measurement:* boolean reproducibility, tokens per successful task, success rate, on E1/E2's held-out Task Packets. *Falsification:* reject if reproducibility fails or savings cost success.

**Alternatives.** Fixed tier sizes with no dynamic fitting; whole-file loading (viable at current scale).

**Conflicts / assumptions.** P2 is classified UNKNOWN in C3; this pack only proposes a reconciliation for C1/C6 to accept or reject; it alters no canonical decision. Tier owner and definitions unknown.

---

### FCP-C3-CTX-004 — Task Context Isolation and Origin-Trust Labelling

**Status:** `FUTURE` / `NOT_IMPLEMENTED` · **Provisional class:** `ARCHITECTURE-READY` (design can be agreed now; enforcement requires the core)

**Problem and value.** Concurrent Clouds on related tasks must not leak Claims/Evidence into each other (C3 §3: "no direct external precedent", "closer to a distributed-systems/multi-tenant-security problem"). C2 adds that a packet can carry content from **untrusted channels**: repository config files that silently change behavior (RP-7), MCP tool results and manifests that "carry instructions" (RP-11), and secrets that must "never appear in the agent's context window" (RP-12). Value: one design that C3's E4 and C2's tests can both exercise.

**Analysis chain.**
- SOURCE: C3 §3, E4, P12; C2 RP-7, RP-9, RP-11, RP-12, RP-14; C7 open items.
- OBSERVED [V per artifacts]: no studied tool defends a boundary between concurrent related tasks; each gets isolation by construction (C3). C2 RP-7 documents a real tool (Aider) where a repo-committed config can silently remove all confirmation prompts, which is "the clearest documented real-world example" of repo content changing authority. C2 RP-11 and RP-12 evidence quality: `STRONG` (OWASP, SOC Prime) and `MODERATE` (single vendor blog) respectively; RP-12's source is a single blog, so I treat it as a design principle, not an established standard.
- WHY IT WORKS [S]: isolation enforced at assembly time is checkable; isolation by instruction is not.
- GENERAL PRINCIPLE: **default-deny, explicit-reference** across task scopes; **label origin, never infer trust from presence in context.**
- ARGON ADAPTATION [P]:
  1. Every Packet bound to its Task Packet scope; including anything from another task requires an explicit **Dependency record** (E4's own wording; shape unseen **[U]**). Shared immutable Source objects may be referenced across tasks (the useful half of Letta's shared blocks, P12); mutable cross-task state is not shared; derived items inherit the strictest scope; caches keyed by scope.
  2. **Origin label** on each packet item (e.g. repository content, tool result, third-party MCP, Cloud-authored). **C3 only carries and enforces the label; C2 owns the trust policy** (RP-11's origin-trust axis is a C2 proposal pending its own scope decision on third-party MCP **[U]**).
  3. **Secret values are excluded at assembly** as defense in depth; C2 owns the vault/adapter design that keeps them out of context in the first place (RP-12). Metadata *about* a secret may be included; RP-12's source does not address this distinction, so it is flagged for C2.
  4. Gate/approval configuration is never read from, or influenced by, packet content (RP-7, RP-9). C3 must not become a channel for that.
- TRADEOFF: less cross-task reuse; metadata discipline; over-strict scoping can starve legitimate work.
- REJECT IF: only one task runs per snapshot at a time; the core already enforces default-deny at assembly; or R-DUP with the Wave 3.5 Dependency design **[U]**.

**Activation trigger.** Concurrent related Task Packets share a snapshot, **or** E4's baseline leaks, **or** third-party MCP/tool results are admitted into packets.

**Expected benefit [P].** Zero unauthorized cross-task citations across N trials (N is **NEEDS EXPERIMENT** per E4; I do not set it).

**Prerequisites / ownership.** Owner C3 (context-scope semantics). C4 supplies task scope. **C2 owns trust and secret policy.** C6/C7 audit.

**Inputs / outputs (PROPOSED).** In: requesting scope, items with scope + origin labels, Dependency records. Out: filtered set + `isolation_report` (counts by reason; no content).

**Limits / failure.** Fail-closed: unlabeled or unknown-scope/origin items are excluded and logged.

**Security / isolation.** Addresses cross-task leakage, session contamination, stale cache, inherited context, scoped memory (C3 §3 list). Lineage/freshness queries must not reveal out-of-scope objects. Residual: model- or provider-side retention is outside C3's control **[U]**.

**Acceptance criteria.** Canary from Task A never in Task B's packet without a Dependency record; derived items inherit strictest scope; no cross-scope cache reuse; unlabeled items excluded; no secret canary in any packet; a tool result instructing a privileged action never alters packet authority labels.

**Negative cases / tests.** Canary in A queried from B; summary mixing A and B; scope label stripped by a transform; Dependency record revoked mid-task; stale cache from a prior task; repo config file attempting to weaken a gate (C2 RP-7 test); secret-shaped canary in a retrieved file; MCP tool result embedding an instruction.

**Bounded experiment.** C3's E4 as baseline (two adversarial concurrent tasks sharing scope) **extended with** C2's RP-7 and RP-12 canaries. *Measurement:* leakage count, legitimate-context miss rate. *Falsification:* any unauthorized citation or secret canary is a failure; reject if the miss rate exceeds a pre-registered tolerance (**NEEDS EXPERIMENT**).

**Alternatives.** Separate working copies per task (stronger, costlier); instruction-only isolation (rejected: unenforceable).

**Conflicts / assumptions.** Dependency record shape assumed from E4's wording. C2 has not decided whether third-party MCP is in scope (RP-11 adoption gate, UNKNOWN).

---

## 4. Candidates Considered and Not Proposed

| Candidate | Disposition | Reason |
|---|---|---|
| Provenance / source-lineage pack | **Rejected (R-DUP)** | Wave 3.5 chain exists as a design (C3 §6). Trust *tiers* of evidence (self-attested vs. independent) are C2 RP-14 / C6 territory and are a confirmed ARGON gap in the Evidence layer, not in context assembly. |
| Retrieve → rank → compress pipeline | **Rejected (R-DUP)** | Already proposed (C3 §2 pipeline, P14). Only the constraint-preservation residual remains (CTX-002). |
| Trajectory schema / `localization_correct` field | **Not a C3 pack** | C6 Patterns 3 and 5 hand these to C3 as "schema owner" for decision. They are evaluation/failure-analysis records, not context assembly. Left as C6↔C3 open items, listed in §7. |
| Standalone checkpoint pack | **`NOT NEEDED` standalone; folded into CTX-001** | A Packet is a regenerable instance. C7's open item "checkpoint stale-state resumption" is covered by CTX-001's reconstruction rules; execution recovery is C4/C6/C1. Revisit if C1's design shows checkpoints that cannot be regenerated from snapshot + projection. |
| Vector DB / graph DB / memory service | **Not proposed** | No identified gap; C3 doubts even reranking pays off at 53 files. |
| Self-editing / agent-rewritable memory | **Rejected** | Contradicts write-once evidence objects (C3 P12). |
| Majority-vote conflict resolution | **Rejected** | Already rejected (C3 P8b). |

Four packs delivered because only four are supported by an identified gap.

---

## 5. Evidence Base Actually Relied On

Taken from the artifacts' own source logs (C3 §9, C2, C5, C6). Not re-fetched.

| Used for | Source (as reported by artifact) | Strength | Limitation |
|---|---|---|---|
| Positional ordering | Liu et al., *Lost in the Middle*, arXiv:2307.03172 (C3 P11) | [V] tested models/tasks | C3 read it via summary sites; percentages not independently checked; **not spot-checked by C7** |
| History collapse, capped output | Yang et al., *SWE-agent*, arXiv:2405.15793 (C3 P4/P5, C6 P3/P4) | [V] ablation in paper | 5-turn window and 50-result cap tuned to its benchmark |
| Condensation structure | OpenHands docs + community walkthrough (C3 P6) | [V] structure | 80/first-4 numbers from a secondary source |
| Budgeted ranking | Aider blog; hermes-agent issue #535 (C3 P1/P2) | [V] method | 50×/8× from a third-party issue; Aider-specific |
| Retrieve-then-rerank | Continue docs (C3 P14) | [V] defaults | Defaults are not evidence of benefit |
| Shared, referenceable blocks | Letta docs (C3 P12) | [V] | Agent-editable by design (rejected for evidence objects) |
| Counter-evidence to compression | mini-swe-agent repo (C3 P15) | [V] design; reported >74% SWE-bench Verified | Single-benchmark score; benchmark caveat applies |
| Resume = structured state | LangGraph official docs: `interrupt()`, checkpointer, `Command(resume=…)` (C5 P10) | [V] per C5 (confirmed against official pages) | C5 downgraded its TTL/irreversible-nodes claims to UNKNOWN (Tier C only); I do not use them |
| Untrusted channels | OWASP MCP Tool Poisoning, SOC Prime (C2 RP-11); Aider config footgun (C2 RP-7) | `STRONG` | RP-7's severity framing is `MODERATE` (single-author write-up) |
| Secrets out of context | SuperTokens blog (C2 RP-12) | `MODERATE` single vendor blog | Not independently corroborated |
| Verifier/claimant separation | IETF RATS-derived arXiv paper, dev.to post, AIP arXiv paper (C2 RP-14) | `MODERATE` to `LOW/EMERGING` | arXiv peer review unverified; principle only, no mechanism adopted |

Benchmark-validity caveat (C3 §7, C4 §8.1, C6 §3): no cited score is proof of general quality. I cite none as ARGON evidence.

---

## 6. Compact Pack Catalog and Activation Triggers

| ID | Pack | Gap | Provisional class | Activation trigger |
|---|---|---|---|---|
| FCP-C3-CTX-001 | Freshness and Staleness Contract (+ reconstruction) | G1 | FUTURE TRIGGER | E3 shows snapshot comparison misses drift; stale-context false Claim; tasks resume across interruptions |
| FCP-C3-CTX-002 | Constraint and Uncertainty Preservation Check | G2 | FUTURE TRIGGER | P15 pre-experiment shows compression needed **and** seeded constraint-loss fails |
| FCP-C3-CTX-003 | Auditable Budget Fit (tier-agnostic) | G3 | BUSINESS DECISION / FUTURE TRIGGER | E2 shows savings without success loss **and** C6 confirms boolean audit **and** a tier scheme is ratified |
| FCP-C3-CTX-004 | Task Context Isolation and Origin-Trust Labelling | G4 | ARCHITECTURE-READY | Concurrent related tasks share a snapshot; E4 baseline leaks; third-party tool results admitted into packets |

All classes provisional. All packs `FUTURE` / `NOT_IMPLEMENTED`. Universal reject condition R-DUP. These labels are the brief's; the artifacts' own pattern vocabulary (`ADOPT/ADAPT/UNKNOWN/NEEDS EXPERIMENT/REQUIRES HUMAN DECISION`) is not mapped onto them because no mapping is defined.

---

## 7. Ownership and Dependency Table (C2, C4, C5, C6)

Roles below are **taken from what the artifacts themselves state**, not from a canonical role charter (none was provided). C1 (kernel/harness/synthesis, per C7's Phase D) is absent from my inputs, so every C1 dependency is `[U]`.

| Cloud (role per artifacts) | 001 Freshness | 002 Preservation | 003 Budget Fit | 004 Isolation / Origin-Trust |
|---|---|---|---|---|
| **C2** (security: approval authority, sandbox, secrets, MCP trust, evidence trust) | Verifier/claimant separation principle (RP-14): freshness checked by Kernel, not by consumer | Treat retrieved/tool text as data (RP-11) | Not primary | **Owns** trust policy, origin axis, secret/vault design (RP-11, RP-12); config-channel rule (RP-7) |
| **C4** (surgical engineering: localization → repair → validation) | Triggers refetch/recompile; owns resuming **execution** | Runs rendering/verification steps; owns bounded tool output (Pattern E) | Escalates overflow | Supplies task scope; owns concurrent execution |
| **C5** (operator control: UI is Display/Guidance, never Authority) | Display re-fetches live freshness, never caches (E8); unattended fail-closed (P8) | Not primary | May display tier-loaded boolean; never decides it | Display of isolation events only |
| **C6** (evaluation: metrics, failure analysis, verification) | Consumes outcomes; `false_completion` canary; checkpoint dependency per C5 | Consumes `preservation_report` for Grounding / Evidence integrity | **Owns tier-loaded audit boolean and Token-efficiency metric** | Audits isolation events; Scope-adherence metric |
| C1 (not provided) | **[U]** schemas, Packet/Snapshot, checkpoint ownership | **[U]** Projection rendering step | **[U]** tier definitions | **[U]** Dependency record |
| C7 | Independent audit of experiment results | idem | idem | idem |

**C3–C4 boundary.** C3 owns context snapshots, source selection, freshness, reconstruction semantics. C4 owns execution and orchestration. Proposed handshakes only (no interface exists): (1) C4 supplies task scope to assembly (CTX-004); (2) C4 requests a freshness outcome or regenerated packet and receives `FRESH | STALE_REFETCH | STALE_RECOMPILE | UNVERIFIED` plus a diff (CTX-001). C3 never starts, retries or reorders tasks; C4 never edits packets or freshness records.

**Cross-owner questions I found but cannot resolve:**
1. **Checkpoint ownership is inconsistent:** C3 P9 says C1/C2; C5 says C6. (CTX-001 does not depend on resolving it for context state, but execution-side resume does.)
2. **Who is "schema owner" for trajectory records:** C6 says C3; C3's own artifact does not claim it. C6 also flags a possible `localization_correct` field and a possible overlap between its dual-gate (Pattern 6) and C3's unattached knowledge-model work. All three need a C3/C6 joint review with the missing files present.
3. **C4's fifth Plan/Act mutation vector differs from C1/C2's** (C7 flagged, non-blocking). Not mine; noted because CTX-004's "tool result changes authority" tests reuse that surface.
4. **C6-vs-C7 verification-authority conflict** (Wave 3.5) remains open (C3 §12) and affects who consumes CTX-001/003 outputs.

---

## 8. Highest-Value Experiments When the Core Is Ready

None run. C7 states that isolation, checkpoint stale-state resumption, delegation depth and adapter sufficiency "require a real implementation environment that does not exist yet (Wave 4 not started)", so "core ready" means Wave 4. All follow C3 P10: tune on one set, validate on a held-out set. Thresholds, N and margins are **not set here**; the artifacts deliberately leave them NEEDS EXPERIMENT.

1. **P15 pre-experiment** (real session lengths vs. need for compression). Cheapest; gates CTX-002 and part of CTX-003; may eliminate packs.
2. **E3 extended** with a second drift class (projection/map change, snapshot unchanged) and a resume-after-change class. Decides CTX-001; reject it if snapshot comparison already catches all.
3. **E4 with canaries**, extended with C2's RP-7 (config-channel) and RP-12 (secret) canaries. Binary; decides CTX-004's enforcement design.
4. **E5 extended** with planted constraints and hedged statements. Decides CTX-002.
5. **E2 plus tier-boolean reproducibility**, once a tier scheme exists. Decides CTX-003 and informs the C6 conversation.

---

## 9. Change Summary

- **Created / replaced:** `C3-FUTURE-CONTEXT-CAPABILITY-PACKS.md` only. r3 supersedes my own r1 and r2 of this same file.
- **Not modified:** every uploaded artifact (C2–C7 research, manifests, audit) was opened read-only; SHA-256 values unchanged and matching their manifests. No canonical decision, Wave 3.5 object, schema, core implementation, checkpoint or audit record was touched. No ARGON-HEALTH or Legacy content was touched.
- **No infrastructure added.** No interface asserted as existing; every field and call is labelled PROPOSED.
- **Changes from r2:** C7 audit and C2/C4/C5/C6 now inspected; T0–T5 restated from C6's own description (partial, unverified) instead of "unavailable"; CTX-001 gained Kernel-side verification, no-cache Display, structured-state reconstruction and fail-closed unattended behavior; CTX-002 gained the durable-vs-active separation; CTX-003 gained the `tokens_loaded`/`tier_ceiling` outputs C6 needs; CTX-004 gained origin labels and secret exclusion and was renamed; ownership table rebuilt from artifact-stated roles; open cross-owner conflicts listed.
- **Open limitations:** C1 artifact and Wave 3.5 schemas unavailable; T1–T3 and tier ceilings undefined; the five status labels undefined; checkpoint ownership inconsistent across artifacts; C3's external-source claims not spot-checked by C7; no URL re-fetched; all classifications provisional; this document unaudited.

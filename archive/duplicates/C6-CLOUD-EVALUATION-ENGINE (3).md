# C6-CLOUD-EVALUATION-ENGINE.md
## C6 — Evaluation / Learning Engine — Research Sprint

**SCOPE DISCIPLINE:** Research and pattern-extraction only. No ARGON-HEALTH, Legacy ARGON, ADR, ACR, Domain, or Workflow content touched or modified. No implementation. No vendor system prompt reproduced — every pattern below is described architecturally, in C6's own words, from published documentation/papers, not copied text.

**METHOD NOTE:** Every source below was checked via live web search this session, not recalled from unverified training memory, precisely because this document's own subject matter (metrics, evidence, false completion) makes it the wrong place to assert unverified technical claims about external systems.

**CORRECTION PASS v1 APPLIED (same session):** this document has been corrected against a C7 finding set (C6-X5, C6-P2, C6-P5/P6, METRICS). See the **C7 FINDING MATRIX** near the end for exactly what changed. No new research sprint was performed; corrections are reframing, self-containment fixes, and one added subsection (Benchmark Validity Limitations), not new pattern discovery.

**SELF-CONTAINMENT NOTE (added this pass, closes C6-P2 and the underlying §10 issue it exposed):** the original draft cited an internal artifact from earlier this session (`C6-WAVE3.5-VERIFICATION-MASTER.md`) as though its content were already verified and available to any auditor of *this* package. That artifact is **not included in this delivery**, so per the correction instructions, every such reference below is now reframed as: *"Previously proposed in an earlier internal artifact, not independently verified in this package,"* with the actual rule restated here, self-contained, so C7 can audit it without needing the missing file:

- **Train/validation/held-out + fixed regression-set discipline** (referenced by Pattern 2 and the pipeline's EVALUATION/REGRESSION stages below): a candidate configuration is scored on a trainset (source of proposed changes), separately on a valset (selection only, never a source of updates), and finally must pass a fixed regression set of previously-fixed failure cases before promotion — restated in full here, not merely pointed at.
- **SRE-style trajectory logging** (referenced by Pattern 3): an ordered, per-run log of state transitions and tool calls with timestamps — restated as a concept here; no schema beyond what Pattern 3 itself specifies below is assumed to already exist.
- **T0–T5 context-tiering** (referenced by Pattern 4 and the "Token efficiency" metric): a graduated context-loading model (T0 = task identity/hard constraints, through T5 = optional exploration) where a task loads only the tiers its size/risk justifies — restated as a concept here; no specific `token_discipline` test implementation is assumed already built or already verified.

Nothing above is claimed as independently verified by this restatement — restating a proposal is not the same as testing it. It removes the self-containment gap; it does not upgrade any status.

---

## 1. EXTRACTED PATTERNS

### Pattern 1 — Feedback-bearing metrics, not scalar-only

**SOURCE:** DSPy's GEPA optimizer (Agrawal et al., "GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning," arXiv:2507.19457; DSPy official docs, `dspy.ai`).

**OBSERVED PATTERN:** GEPA's metric function does not return only a scalar score — it can also return a short natural-language explanation of *why* a run scored the way it did (e.g., "predicted Paris but the gold answer is Lyon; the model ignored the date constraint"). A reflection model reads this textual feedback to propose targeted instruction changes, rather than searching blindly over scalar reward alone. Per the DSPy documentation and the paper's own benchmark table, this lets GEPA reach strong results in far fewer rollouts than reinforcement-learning-style optimization (the paper reports large rollout-count reductions against GRPO on several benchmarks, with the specific margin varying by task).

**WHY IT WORKS:** A scalar alone tells the optimizer *that* something failed; text feedback tells it *what* to fix. This converts optimization from trial-and-error search into something closer to directed debugging.

**ARGON ADAPTATION:** Every C6 metric (§3 below) should be designed to emit a **(score, reason)** pair, not a bare number, from the start — even before any automated optimizer consumes it. A `false_completion` check that returns `0` is far less useful to a future prompt/router revision than one that returns `(0, "Claim X was marked COMPLETE citing Evidence Record E-104, whose Source resolved to 'not_yet_checked' — no resolvable Source backs this claim")`. This is a data-shape decision C6 can specify now, independent of whether GEPA itself is ever adopted as the optimizer.

**REJECT IF:** a metric's failure reason cannot be generated deterministically or cheaply (e.g., requires a second expensive LLM call for every single evaluation) — in that case, scalar-only is acceptable for the cheap tier, with reason-generation reserved for a slower diagnostic pass, not silently skipped.

**TEST NEEDED:** compare optimizer/reviewer convergence speed (however "convergence" is later defined for ARGON) with reason-bearing metrics vs. scalar-only, on the same fixed task set — this is an empirical question, not something to assert from the source paper's numbers alone, since ARGON's task distribution differs from GEPA's published benchmarks.

**Classification:** OBSERVED (published paper + official docs) → **ADOPT** the (score, reason) metric shape; **UNKNOWN** whether GEPA itself (or any specific optimizer) should be adopted — that is a Wave-4+ tooling decision, not a pattern-extraction one.

---

### Pattern 2 — Train / validation / held-out separation, with an explicit warning against test-on-train

**SOURCE:** DSPy GEPA optimization guide (`dspy.ai/getting-started/gepa-optimization/`).

**OBSERVED PATTERN:** GEPA's own documentation distinguishes three roles: a *trainset* that supplies examples for reflective prompt updates, a *valset* used only to score and select candidates during the search (not to generate updates from), and a separately held-out *test set* used only after optimization is finished, to evaluate the promoted candidate on data that influenced neither training nor selection. The documentation explicitly warns that omitting a valset causes GEPA to reuse the trainset for selection, which "allows prompts to overfit."

**WHY IT WORKS:** Separating "data used to propose changes" from "data used to pick among them" from "data used to report a final number" is the same discipline that prevents any ML system from fooling itself into thinking it generalizes when it has merely memorized.

**ARGON ADAPTATION:** Previously proposed in an earlier internal artifact, not independently verified in this package — see the Self-Containment Note above for the restated rule. This research pass's contribution is narrow and specific: it confirms the *train/validation/held-out* discipline against a named, external, checked source (DSPy's own documentation) rather than leaving it as a purely internally-generated design choice. That is a real, if modest, upgrade in evidence quality (internal proposal → internal proposal corroborated by external precedent) — it is not a claim that the mechanism has been implemented or independently tested.

**REJECT IF:** n/a for the pattern itself (external precedent is unambiguous on this point); the open item is entirely on the ARGON-implementation side — see Classification below.

**TEST NEEDED:** whether ARGON's actual (not-yet-built) train/val/held-out mechanism, once implemented, behaves as GEPA's does — this cannot be answered by citing GEPA's docs, only by building and testing ARGON's own version.

**Classification:** OBSERVED (official docs) → **ADOPT the pattern** (external precedent is solid); **implementation status: PROPOSAL, not verified** — the distinction between "this is a sound pattern to adopt" and "ARGON has built and confirmed this" is deliberately kept visible here, not collapsed.

---

### Pattern 3 — Structured per-step trajectory logging (thought / action / observation / state)

**SOURCE:** SWE-agent (Yang et al., "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering," NeurIPS 2024, arXiv:2405.15793; SWE-agent's own trajectory documentation).

**OBSERVED PATTERN:** SWE-agent logs every step of a run as a structured record containing the model's raw response, a parsed `thought`, the `action` taken, the `observation` (environment output) that resulted, and a separate `state` snapshot (e.g., open file, working directory) extracted from the environment after the action executed. Files are written per task instance (`<instance_id>.traj`, JSON), with the full sequence of these records under a `trajectory` key.

**WHY IT WORKS:** Separating "what the model said" from "what actually happened" from "what state resulted" makes a run mechanically replayable and diffable — you can ask "did the *action* match the *thought*" and "did the *observation* match what a human would expect" as two independent, checkable questions, rather than trying to reconstruct both from a single flat transcript.

**ARGON ADAPTATION:** SRE-style trajectory logging was previously proposed in an earlier internal artifact, not independently verified in this package (see Self-Containment Note above for the restated concept). This research pass's specific contribution: the trajectory record should carry (at minimum) **response, thought, action, observation, state** as five distinct fields per step, not a single narrative blob — a concrete schema refinement, grounded in SWE-agent's published design, that can be handed to C3 (schema owner) as a proposal. This is new precision from this pass, not a restatement of something already built.

**REJECT IF:** the five-field granularity proves too verbose/costly for low-risk tasks — in that case, a compressed trajectory format for low-risk tasks and a full five-field format for high-risk/audited tasks is the adaptation, not abandoning the structure entirely.

**TEST NEEDED:** whether ARGON's Cloud turns (which are not shell-command-by-shell-command like SWE-agent's) map cleanly onto this per-step granularity, or whether the natural unit is "one Cloud turn" rather than "one tool call" — this needs to be tried against a real Wave-4 task before assuming the mapping is 1:1.

**Classification:** OBSERVED (peer-reviewed paper + official docs) → **ADAPT** — the five-field shape is adopted; the exact step-granularity mapping to ARGON's Cloud-turn structure is genuinely unknown and needs the experiment named above.

---

### Pattern 4 — Aggressive context compression of older observations

**SOURCE:** SWE-agent paper (same citation as Pattern 3), §on history processors.

**OBSERVED PATTERN:** Per the paper, SWE-agent collapses all but the most recent few observations into a single summary line each, specifically to keep the agent's context "concise and informative" over a long run, rather than keeping every past tool-output verbatim in context indefinitely.

**WHY IT WORKS:** Most of the value of a past observation is "I already saw this, don't re-fetch it" — not its full verbatim content. Keeping only the newest few observations in full detail, with older ones reduced to a one-line pointer, trades a small amount of detail loss for a large, compounding token-budget saving over a long run.

**ARGON ADAPTATION:** Context-tiering (T0–T5) was previously proposed in an earlier internal artifact, not independently verified in this package (see Self-Containment Note above). No `token_discipline` test is claimed to exist or to have been run. This pass's specific, narrow contribution: within a single task's trajectory (not just across tiers), older trajectory steps should compress to a one-line summary once a recency window is exceeded — a *within-task* compression mechanism this pass proposes as new, not one claimed to already be covered by the tier model.

**REJECT IF:** a task's audit/evidence requirements need the full, uncompressed observation retained for later citation — in that case, compression applies only to what's kept in the *active context window* for reasoning, never to what's retained in the durable trajectory/evidence store. The two copies (working context vs. durable record) must not be conflated.

**TEST NEEDED:** what recency window (how many recent steps stay uncompressed) is appropriate for ARGON's task lengths — this is an empirical tuning question, not answerable from SWE-agent's own reported window size alone, since ARGON's tasks are not shell-command-by-shell-command.

**Classification:** OBSERVED (peer-reviewed paper) → **ADAPT** — the compression *principle* is adopted; the specific window size is **UNKNOWN**, requires experiment.

---

### Pattern 5 — Localization before repair; repair before validation (never merge the three)

**SOURCE:** Agentless (Xia et al., "Agentless: Demystifying LLM-based Software Engineering Agents," ACM/FSE 2025, arXiv:2407.01489; official repository documentation).

**OBSERVED PATTERN:** Agentless deliberately does *not* let a single LLM call jump straight from "here's the issue" to "here's the patch." It runs three separate, explicitly ordered phases: (1) hierarchical **localization** — file-level, then class/function-level, then fine-grained edit-location — using a mix of prompting and embedding-based retrieval; (2) **repair** — multiple candidate patches sampled in a simple diff format at the located edit points; (3) **patch validation** — candidates are filtered by running them against the project's own regression tests, and further checked with a generated reproduction test that specifically tries to re-trigger the original reported issue; surviving candidates are then reranked and the top one is selected. **Benchmark claim, with the full caveat the correction pass requires (§8):** per the paper (Xia et al., ACM/FSE 2025), this pipeline was evaluated on **SWE-bench Lite** (a 300-instance subset, per the benchmark's own documentation), using models available at the time of the paper's writing, in the paper's own defined evaluation environment; the reported outcome was a resolve-rate and cost comparison favorable to Agentless against several more complex agent-based baselines *on that specific benchmark and model set*. This score has **not been independently audited by C6**, is **not equivalent to a general "agent quality" claim** (per the correction pass's own Benchmark Rule and the SWE-bench validity limitations discussed in §3 below), and should not be read as proof the same margin holds on ARGON's own, different task distribution.

**WHY IT WORKS:** Each phase has a narrow, checkable job. A model asked to do all three at once (find the bug, fix it, and know it's fixed) conflates three different failure modes into one unreviewable step; splitting them means a wrong localization is caught before any repair is attempted, and a wrong repair is caught before it's ever proposed as final.

**ARGON ADAPTATION — PATTERN vs. IMPLEMENTATION kept explicitly separate, per correction instruction C6-P5/P6:**
- **The pattern** (what Agentless does, externally observed): keep localization, repair, and validation as three separate, non-merged phases with independent success/failure signals.
- **The ARGON implementation** (not built, proposed only): before ARGON claims a Claim is `refuted` or a task `FAILED`, a failure diagnosis *should* separate "was the problem correctly localized" from "was the fix/response wrong given correct localization" from "did validation itself fail to catch a real problem." This is a proposal for C6's Failure Analysis stage — no such three-way diagnosis exists today; nothing has been implemented or tested. It also reinforces C4's already-specified surgical-discipline chain (`Problem → Localization → Hypothesis → Exact edit location → Minimal patch → Tests`) as independent, published corroboration that the ordering is a benchmarked pattern, not merely intuition — corroboration of C4's proposal, not proof that ARGON's version of it works.

**REJECT IF:** the task genuinely has no meaningful "localization" step (e.g., a pure informational answer with nothing to locate in a repository) — in that case this three-phase split doesn't apply and shouldn't be forced onto tasks it doesn't fit.

**TEST NEEDED:** whether ARGON's `EVIDENCE GAP` vs. `CONFIRMED INCONSISTENCY` vs. `CONFIRMED BUG` classification scheme (already in active use throughout this session's verification passes) already captures this three-way split adequately, or whether a dedicated `localization_correct: bool` field is needed on Verification Records to make the distinction queryable rather than implicit in prose.

**Classification:** OBSERVED (peer-reviewed paper) → **ADOPT** the three-phase separation as a required shape for C6's Failure Analysis stage; **UNKNOWN** whether the existing classification vocabulary already suffices or needs the new explicit field — flagged for C3, not decided here.

---

### Pattern 6 — Dual-gate validation (regression tests + a purpose-built reproduction test), then rerank

**SOURCE:** Agentless (same citation as Pattern 5).

**OBSERVED PATTERN:** Agentless does not validate a candidate patch with only the project's pre-existing regression tests. It additionally generates a *new*, purpose-built test specifically aimed at reproducing the originally reported issue, runs both the regression suite and this reproduction test against each candidate, and uses the combined results to rerank surviving candidates before selecting a final one.

**WHY IT WORKS:** Pre-existing regression tests answer "did this break anything already covered" — they do not, by construction, answer "does this actually fix the reported problem," since the reported problem is by definition something existing tests didn't already catch. A purpose-built reproduction test closes exactly that gap.

**ARGON ADAPTATION — PATTERN vs. IMPLEMENTATION kept explicitly separate, per correction instruction C6-P5/P6:**
- **The pattern** (externally observed): validate with two independent kinds of check — one that confirms nothing previously working broke, one purpose-built to confirm the specific new thing actually works.
- **The ARGON implementation** (proposed only, nothing built): a Claim moving toward `VERIFIED` *should* require both a regression-equivalent check (no previously-passing evidence check now fails) and a reproduction-equivalent check (the specific new claim has its own dedicated resolvable Evidence Record). This is a design proposal for C6's Completion layer — no dual-gate mechanism exists in ARGON today, tested or otherwise.

**REJECT IF:** generating a purpose-built check for every single Claim is prohibitively expensive relative to the Claim's actual risk/impact — in which case this dual-gate applies at minimum to any Claim gating a `COMPLETE`/`VERIFIED` transition, not necessarily to every low-stakes intermediate Claim.

**TEST NEEDED:** cost/benefit of generating a dedicated reproduction-style check per Claim vs. relying on chain-resolution + content-review style methods — a related mechanism was proposed in a separate internal artifact from this session (C3's knowledge-model work), not included in this package and not independently verified here; whether that mechanism already substantially covers this need, or whether this is a genuinely separate fourth mechanism, remains open and is flagged for C3/C6 joint review with that artifact attached, not assumed resolved by citing it from memory.

**Classification:** OBSERVED (peer-reviewed paper) → **ADAPT** — the dual-gate *principle* is adopted; whether it's a new mechanism or already covered by C3's existing chain-resolution/content-review split is **UNKNOWN**, flagged for C3/C6 joint review rather than resolved here.

---

## 2. THE EVALUATION ENGINE PIPELINE

Integrating the patterns above into the required chain:

```
BENCHMARK
  A fixed, versioned task set (per Pattern 2's train/val/held-out split —
  previously proposed in an earlier internal artifact, not independently
  verified in this package; see Self-Containment Note above) — extended
  this pass with a fourth partition: a small set of tasks with NO
  meaningful localization step (per Pattern 5's reject-if clause), so the
  three-phase failure-analysis model is never wrongly forced onto tasks
  it doesn't fit.

RUN
  One execution of one candidate (Kernel/Router/Context-Compiler/prompt
  configuration) against one benchmark task.

TRAJECTORY
  Per Pattern 3: a structured, per-step record — response, thought,
  action, observation, state — not a single narrative blob. Per
  Pattern 4: the active reasoning context compresses older steps to a
  one-line summary past a recency window (UNKNOWN size, needs
  experiment); the durable trajectory/evidence store never compresses —
  full detail retained there regardless of what's compressed in-context.

METRIC
  Per Pattern 1: every metric below emits (score, reason), not a bare
  number, wherever a deterministic reason is cheap to produce.

FAILURE ANALYSIS
  Per Pattern 5: any failing Claim/task is diagnosed along three
  separable axes — localization correctness, repair/response
  correctness given correct localization, validation correctness (did
  the check itself fail to catch a real problem) — rather than a single
  undifferentiated "it failed."

CANDIDATE PROMPT
  A specific, versioned Kernel/Router/Context-Compiler/prompt
  configuration proposed in response to a Failure Analysis finding.

EVALUATION
  Per Pattern 2: scored on trainset (source of proposed changes) and
  separately on valset (selection only, never a source of updates).

REGRESSION
  A fixed regression set of previously-fixed failure cases — previously
  proposed in an earlier internal artifact, not independently verified
  in this package (see Self-Containment Note above) — PLUS, per this
  pass's addition, a dual-gate check per candidate (Pattern 6, proposal
  only): does it preserve every prior passing check (regression-
  equivalent) AND does it specifically satisfy the new thing it claims to
  fix (reproduction-equivalent)?

PROMOTION
  Only a candidate passing trainset improvement, valset generalization,
  AND the full regression set (both gates) may replace the current
  configuration — logged, versioned, reversible. This promotion
  mechanism is a proposal; no promotion has ever occurred, since no
  implementation exists.
```

---

## 3. METRICS (minimum 10, each with definition / unit / measurement method / cost / failure signal — no invented thresholds)

**Correction note (C6-X5, reconfirmed and refined this v3 pass):** the v2 correction pass added unit/cost/failure-signal columns. This v3 pass adds one further column this round's instructions name explicitly and separately from "unit" — **Measurement Method** (the actual mechanism that produces the number, not just what the number represents) — since a unit alone ("count") doesn't say *how* the count is computed. No pass/fail numeric threshold is asserted anywhere in this table; wherever a cutoff would eventually be needed, it is marked `NEEDS EXPERIMENT` explicitly, per instruction, rather than invented.

| Metric | Definition | Unit | Measurement method | Cost | Expected failure signal |
|---|---|---|---|---|---|
| **Correctness** | Does the final Claim/output match the expected resolution for the benchmark task? | Binary (match/no match) per instance; aggregate = resolve rate | Compare final output against a pre-recorded expected resolution for the task; exact-match is mechanical, semantic-match requires a judge call | Deterministic for exact-match tasks; judge-call cost `NEEDS EXPERIMENT` | A "match" a human reviewer disputes on inspection |
| **Grounding** | Does every factual assertion trace to a real, resolvable Source? | Count of ungrounded assertions per output (target: 0, definitional) | Walk every assertion's citation chain (`Claim → Evidence Record → Source`) and check each Source actually resolves | Deterministic — a chain-walk, not a judgment call | Any assertion with zero resolvable Source |
| **Evidence integrity** | Are all cited Evidence Records `resolvable`, not `inert`/fabricated? | Count of unresolved/inert citations (target: 0, definitional) | Check each cited Evidence Record's `source_status` field directly (per C3's `inert` rule) | Deterministic | An Evidence Record cited as support whose Source never resolves |
| **Scope adherence** | Did the run stay within its declared `execution_target`/path scope? | Count of out-of-scope touches (target: 0, definitional) | Diff the trajectory's per-step `state` field (touched paths) against the task's declared scope | Deterministic, mechanical | Any touched path outside declared scope, regardless of whether it was "harmless" |
| **Token efficiency** | Was context loaded proportional to task size? | Ratio: tokens loaded ÷ tokens the task's declared tier would justify | Sum tokens in the assembled context packet; divide by the ceiling the task's T0–T5 classification implies | Cheap once tier assignment exists; the tier-assignment logic itself is `NEEDS EXPERIMENT` | Ratio well above 1 with no logged escalation reason |
| **Tool efficiency** | Were tool calls minimal and non-redundant? | Count of redundant calls | Compare each call's target against content already present in the trajectory summary before the call was made | Deterministic, mechanical | Any call whose result was already available in-context |
| **Test completeness** | Does supporting evidence include both a regression-equivalent and a reproduction-equivalent check? | Binary per Claim (both present / not both) | Check the Claim's Verification Record for two distinct linked check types, not one | Deterministic once both check types exist; they don't exist yet | A Claim reaching `VERIFIED` with only one check type present |
| **Minimality** | Is the change the smallest one resolving the localized problem? | Count of touched files/lines beyond the localization step's identified minimum | Diff the actual change set against the localization output; count anything outside it | Requires a localization result to diff against — tied to Pattern 5's proposal-only status | Any file touched "because it was nearby" |
| **False completion** | Does `completion_state`/`claim_status` reach `COMPLETE`/`VERIFIED`/`ACCEPTED` while evidence is `PROPOSED`/`DOCUMENTATION_ONLY`/inert? | Count of canary violations (target: 0, definitional — not tunable) | Cross-check every status transition against its cited evidence-class at transition time (the anti-false-completion test this whole session's verification passes repeatedly exercised) | Deterministic — a status/evidence cross-check | Any single occurrence, a hard failure by design, never a soft flag |
| **Security violations** | Did any action execute outside its ALLOW/REQUIRE-REVIEW/REQUIRE-HUMAN-APPROVAL classification without the matching gate? | Count of ungated actions (target: 0, definitional) | Pair each trajectory action with its pre-execution classification (per C2's precedence table, an external dependency not attached here) and check the matching gate fired | Deterministic once classification is known; classification correctness is C2's remit | Any action whose required gate did not fire |

### BENCHMARK VALIDITY LIMITATIONS (C6-X5, required addition)

Any metric above that resembles benchmark-style scoring (Correctness especially, and by extension Test Completeness) inherits the following limitations, documented from real, checked sources rather than asserted generically:

- **Flawed tests / annotation errors:** per UTBoost (arXiv:2506.09289), a corrected test-case parser changed the annotation data for **54.7% of SWE-bench Lite instances and 54.2% of SWE-bench Verified instances** — meaning a large fraction of a widely-used benchmark's own "ground truth" pass/fail labels were themselves wrong before correction. A resolve-rate number is only as trustworthy as the labels behind it.
- **Patch correctness vs. test pass:** per "Are 'Solved Issues' in SWE-bench Really Solved Correctly?" (arXiv:2503.15223), a patch can pass all designated tests while still not matching what a developer would actually consider a correct fix, because test coverage is rarely exhaustive. **Test pass is evidence of correctness, not proof of it** — this is exactly why Pattern 6's dual-gate proposal treats passing checks as necessary, not sufficient.
- **Contamination:** any benchmark built from public repositories risks having its solutions already present in a model's training data; this document does not claim ARGON's own future task set is contamination-free — that would need to be verified once such a set exists, not assumed.
- **Benchmark version drift:** SWE-bench, SWE-bench Lite, and SWE-bench Verified are three different, non-interchangeable benchmarks (2,294 instances / a 300-instance subset / a 500-instance human-validated subset, respectively, per swebench.com and OpenAI's own release notes) — any cited score must name which one, or it is not a checkable claim.
- **Held-out validity:** per Pattern 2's own discipline, a held-out set's validity itself decays if it is reused across too many promotion cycles (each reuse leaks a little information about it) — this document does not specify a reuse limit; that is `NEEDS EXPERIMENT`, not asserted here.

None of the above is invoked to claim ARGON's own (not-yet-built) evaluation engine already handles these limitations — only that any future use of SWE-bench-style scoring, or any ARGON-internal analog, inherits them and must disclose them the same way this section does.

---

## 4. CLASSIFICATION SUMMARY (per shared output requirement)

| Pattern | Evidence type | Verdict |
|---|---|---|
| 1 — Feedback-bearing metrics | OBSERVED (paper + docs) | **ADOPT** (metric shape); **UNKNOWN** (specific optimizer choice) |
| 2 — Train/val/held-out split | OBSERVED (docs) | **ADOPT the pattern**; implementation **PROPOSAL only, not verified in this package** |
| 3 — Structured trajectory schema | OBSERVED (paper + docs) | **ADAPT** (field shape adopted; step-granularity mapping UNKNOWN) |
| 4 — Observation compression | OBSERVED (paper) | **ADAPT** (principle adopted; window size UNKNOWN) |
| 5 — Three-phase localization/repair/validation | OBSERVED (paper) | **ADOPT** (for Failure Analysis stage); **UNKNOWN** (whether existing vocabulary suffices or needs a new field) |
| 6 — Dual-gate validation | OBSERVED (paper) | **ADAPT**; **UNKNOWN** (overlap with C3's existing chain-resolution/content-review split) |

No pattern above is classified `REJECT` this pass — none examined were found to be Claude-specific, vendor-coupled, or inapplicable to a model-adaptive OS; all six are architecture/evaluation patterns independent of which underlying model executes them, consistent with this Wave's Final Target.

No claim of "best," "production-ready," or similar unsupported superlative appears anywhere above.

---

## 5. WHAT THIS DOCUMENT DOES NOT DO

- Does not modify ARGON-HEALTH, Legacy ARGON, any ADR, any ACR, any Domain, or any Workflow.
- Does not implement anything — no code, no runnable metric, no runnable trajectory logger exists as a result of this document.
- Does not reproduce any vendor system prompt — every pattern is described architecturally from public papers/documentation, in C6's own words.
- Does not select a specific optimizer (GEPA or otherwise) for adoption — that remains an open, later decision, not made here.
- Does not claim any pattern is "best" — each is evaluated on its own merits with an explicit REJECT IF clause, per instruction.

---

# APPENDIX: CLOUD CAPABILITY UPGRADE

**Applied per the Common Cloud Evolution Super-Prompt, same session.** This appendix does not change C6's role-specific deliverable above — it records the research discipline applied while producing it, per §26's required structure, and extends source coverage with two additional checks performed after the original artifact was drafted (SWE-bench methodology, OpenAI Agents SDK tracing), added here rather than silently folded into §1 above, so the record shows exactly when each source was actually opened.

## 1. Sources Studied (with full accounting per §27)

| # | Source | Repository/Document | URL | Section/Focus | Access | Exact mechanism observed | Confidence | What this does NOT prove |
|---|---|---|---|---|---|---|---|---|
| 1 | DSPy GEPA | "GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning" + DSPy official docs | arXiv:2507.19457; dspy.ai/getting-started/gepa-optimization | Metric shape; train/val/test discipline | This session, live search | Metric functions can return (score, textual feedback); optimizer uses feedback for targeted reflection; valset required to prevent overfitting | Tier A (paper + official docs) | Does not prove GEPA outperforms every possible optimizer for ARGON's specific task distribution — only for the benchmarks the paper itself reports |
| 2 | SWE-agent | "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering," NeurIPS 2024 + official trajectory docs | arXiv:2405.15793 | Trajectory schema; observation compression | This session, live search | Per-step record with response/thought/action/observation/state fields; history processors collapse older observations to summaries | Tier A (peer-reviewed + official docs) | Does not prove this exact schema fits ARGON's Cloud-turn granularity — that mapping is untested |
| 3 | Agentless | "Agentless: Demystifying LLM-based Software Engineering Agents," ACM/FSE 2025 | arXiv:2407.01489 | Three-phase pipeline; dual-gate validation | This session, live search | Localization→repair→validation kept as separate phases; validation uses both pre-existing regression tests and a generated reproduction test, then reranks | Tier A (peer-reviewed) | Does not prove this beats every agent-based approach on all task types — the paper's own comparison is scoped to SWE-bench Lite |
| 4 | SWE-bench / SWE-bench Verified | Original SWE-bench paper + OpenAI's SWE-bench Verified release notes + swebench.com | arxiv (Princeton/UChicago 2023 paper), openai.com/index/introducing-swe-bench-verified, swebench.com/original.html | FAIL_TO_PASS / PASS_TO_PASS evaluation split | This session, live search (after initial artifact draft — added here, not retrofitted into §1) | A candidate patch is scored by two disjoint test sets: FAIL_TO_PASS (did the fix actually work — tests that failed before, pass after) and PASS_TO_PASS (did anything break — tests that passed before and must still pass); both must pass for a "resolved" verdict; independent research (UTBoost, arXiv:2506.09289; "Are Solved Issues Really Solved Correctly?", arXiv:2503.15223) found real annotation/parser errors and plausible-but-incorrect patches passing anyway | Tier A (original paper, official OpenAI release) for the mechanism; Tier B (independent critique papers) for the caveat | Does not prove SWE-bench-style dual test-set scoring generalizes outside patch-based coding tasks; the critique papers prove that *even this well-established benchmark* has measurable false-positive resolution claims — directly relevant to why C6's own `false_completion` discipline must not rely on a single check |
| 5 | OpenAI Agents SDK | Official `tracing.md` docs + openai.github.io tracing guide | github.com/openai/openai-agents-python/blob/main/docs/tracing.md; openai.github.io/openai-agents-python/tracing | Trace/span structure; guardrail visibility | This session, live search (added here, same as #4) | A trace = one workflow; composed of typed spans (agent, generation, function/tool, guardrail, handoff, custom), each with start/end timestamps; a guardrail span carries an explicit boolean outcome (e.g., `tripwire_triggered: false`), so "was this check evaluated" is answered by inspecting the span, not by inference from the final output | Tier A (official docs) | Does not prove this exact span taxonomy is sufficient for ARGON's own audit needs (e.g., it has no native "Evidence Record" or "Approval Record" concept) — only that named, explicitly-outcome-tagged spans are a workable pattern for making enforcement visible |

**Explicitly NOT studied this pass (named, not silently skipped), from C6's own priority list:** Terminal-Bench, OpenHands Benchmarks, SWE-ReX, LiteLLM spend/cost tracking, LangGraph durability. These remain on the priority list for a future research pass; nothing above claims knowledge of them.

## 2. High-Value Patterns

The single highest-value addition from the post-draft searches: **the FAIL_TO_PASS/PASS_TO_PASS split is a directly reusable dual-gate template**, independently confirming Pattern 6 (Agentless's dual-gate validation) from a second, unrelated source rather than resting on one paper alone — and the critique literature on SWE-bench (source #4) is itself a high-value pattern in a different way: it is documented, peer-reviewed proof that **a widely-trusted, test-based benchmark still lets incorrect patches through**, which is direct external evidence (not ARGON-internal speculation) for why C6's own anti-false-completion discipline treats "tests passed" as necessary, never sufficient, evidence.

## 3. Patterns Rejected

No pattern examined across the original five sources or these two additional ones was rejected as vendor-locked or inapplicable — consistent with the original artifact's §4 classification table. One candidate pattern was considered and set aside rather than adopted: **using OpenAI Agents SDK's span taxonomy verbatim as ARGON's trajectory schema.** Reason: it is a real, working pattern, but it is one vendor SDK's specific taxonomy, not a peer-reviewed general mechanism like SWE-agent's — the *principle* (named, explicitly-outcome-tagged spans) is adopted; the specific five-type taxonomy (agent/generation/function/guardrail/handoff) is not copied wholesale, since ARGON's own object model (Claim, Evidence Record, Approval Record) doesn't map 1:1 onto it.

## 4. Token Efficiency Gains

Beyond what §2 (the pipeline) already specifies: source #5 shows that **tracing can be selectively disabled per-run or globally** (`OPENAI_AGENTS_DISABLE_TRACING`) — the general principle worth extracting is that full five-field trajectory detail (Pattern 3) should itself be a *configurable cost*, not an always-on tax, with a cheaper mode available for low-risk tasks where full replay-grade detail isn't needed. This sharpens Pattern 3's existing "REJECT IF" clause rather than replacing it.

## 5. Model Portability

Everything adopted in this artifact is a **mechanism**, not a vendor API: metric-with-feedback (Pattern 1), train/val/held-out separation (Pattern 2), structured trajectory fields (Pattern 3), context compression (Pattern 4), phase separation (Pattern 5), dual-gate validation (Pattern 6), and the two additions here (dual-test-set scoring, explicit-outcome spans) are all describable and implementable independent of which model executes a Cloud's turn. None of them require a specific provider's API shape — consistent with this Wave's Model-Independent/Model-Adapter split (§14 of the Common Prompt).

## 6. Failure Modes

- If feedback-bearing metrics (Pattern 1) are generated by an expensive LLM call every time, cost scales badly — mitigated by the tiering already specified (cheap scalar for routine checks, feedback generation reserved for failures/diagnostics).
- If trajectory compression (Pattern 4) is applied to the durable evidence store rather than only the active reasoning context, provenance is lost — this exact failure mode is already named in Pattern 4's own entry above, restated here because §16 of the Common Prompt requires failure modes to be explicit, not just implied.
- If dual-gate validation (Pattern 6) is applied uniformly to every Claim regardless of stakes, cost becomes prohibitive — mitigated by scoping it to Claims gating a COMPLETE/VERIFIED transition specifically.
- Newly surfaced by source #4: **a dual-gate test-based check can still pass an incorrect result** if the tests themselves are poorly specified (the exact defect UTBoost and the "Are Solved Issues Really Solved Correctly?" papers document in SWE-bench itself) — meaning ARGON's own `evidence_integrity` metric must also periodically audit *the quality of the checks*, not only whether checks passed, or it inherits the same blind spot.

## 7. Experiments (consolidated, cross-referenced to §1's TEST NEEDED fields above)

All six from the original artifact stand unchanged. One addition: **audit a sample of "PASSED" Verification Records for check quality**, not just check outcome — directly motivated by source #4's critique literature, and testable without waiting for any of the other six experiments' infrastructure to exist first, since it only requires reviewing existing Verification Record content once any exist.

## 8. Transferable Principles

1. Metrics should explain, not just score.
2. Never let selection data double as training-signal data.
3. Trajectories are structured records, not narrative logs.
4. Compression trades context detail for budget, never trades away the durable record.
5. Diagnosis separates "found the right problem" from "fixed it right" from "checked it right."
6. Validation needs two independent kinds of check (does it preserve what worked; does it prove what's newly claimed) — now confirmed by two unrelated sources (Agentless, SWE-bench), not one.
7. Passing a check is necessary, never sufficient, evidence — checks themselves can be wrong, and auditing check quality is a distinct, ongoing obligation, not a one-time design decision.
8. Explicit, per-step, boolean-visible outcomes (e.g., a named guardrail span with a clear pass/fail flag) beat inferring enforcement from a final result.

## Self-Challenge (§28, answered honestly rather than checked off by default)

| Question | Answer |
|---|---|
| Does every OBSERVED claim have a source? | Yes — all seven sources (five original + two added here) are named with URLs in §1's table above |
| Did I separate mechanism from vendor implementation? | Yes — §3 explicitly declines to copy OpenAI's specific span taxonomy while adopting its underlying principle |
| Did I use the least context sufficient? | Reasonably — two additional searches were run only after the original six-pattern draft was judged incomplete against C6's own priority list, not preemptively |
| Did I duplicate anything already stated? | Pattern 2 is marked (post-correction-pass) as external-precedent-confirmed but implementation-unverified, not as "already adopted" — this line itself was found stale during the v3 correction pass (it still read "already-adopted design" after Pattern 2's own text was fixed) and is corrected here rather than left inconsistent |
| Did output quality increase, not just length? | The two additions each changed a concrete deliverable (§3's rejected-pattern entry, §6's new failure mode, §7's new experiment) rather than padding prose |
| Did I name failure modes? | Yes, §6, including one newly surfaced by this pass's additional research |
| Does every important claim have a test? | Yes — six original experiments plus one new one in §7 |
| Is this portable to another model? | Yes — §5 addresses this directly |
| Is there a bypass risk? | Named in §6 (test-quality blind spot) |
| Did human authority stay with the human? | Yes — nothing in this appendix proposes automated promotion without the existing human-approval gate already specified in the main artifact |
| Did I say UNKNOWN where I don't know? | Yes — five sources from C6's own priority list are explicitly named as not studied this pass, not silently omitted |
| Did I stay in role? | Yes — no ARGON-HEALTH, Legacy, ADR, ACR, Domain, or Workflow content touched; no implementation performed |

## STATUS

**DESIGNED.** No implementation. All six patterns require the specific experiments named in their respective "TEST NEEDED" fields before any of them can move to a stronger status. This appendix adds two independently-sourced confirmations (FAIL_TO_PASS/PASS_TO_PASS, explicit-outcome spans) but does not change that status.

---

---

# FINAL PACKAGING (canonical — supersedes the separate v2/v3 historical sections of prior revisions; no research content altered)

## DISPUTE STATEMENT

C6 disputes none of the findings ever applied to this artifact (C6-X5, C6-P2, C6-P5/P6, METRICS, and the hash-contract requirement). All are accepted as legitimate and fixed. No `DISPUTED` entry exists.

## C7 FINDING MATRIX (consolidated, final)

| Finding | Status | What changed | Evidence |
|---|---|---|---|
| C6-X5 (benchmark validity/test-quality limitations) | **FIXED** | Dedicated "BENCHMARK VALIDITY LIMITATIONS" subsection under §3, cross-linked to the METRICS table's Measurement Method column | UTBoost (arXiv:2506.09289): 54.7%/54.2% relabeling rate on SWE-bench Lite/Verified; "Are Solved Issues Really Solved Correctly?" (arXiv:2503.15223) |
| C6-P2 ("already in place" resting on an unattached artifact) | **FIXED** | Pattern 2's ARGON ADAPTATION, REJECT IF, TEST NEEDED, and Classification rewritten to "Previously proposed in an earlier internal artifact, not independently verified in this package," rule restated inline (Self-Containment Note); same defect in Patterns 3, 4, and one Pattern-6 citation corrected identically; one residual stale appendix line (Self-Challenge table) also caught and fixed | Self-Containment Note (top of document); Patterns 2/3/4/6; appendix Self-Challenge table |
| C6-P5/P6 (pattern vs. ARGON-implementation separation) | **FIXED** | Patterns 5 and 6 each rewritten into two explicit sub-parts: "The pattern" (externally observed) vs. "The ARGON implementation" (proposal only, nothing built) | Patterns 5 and 6, ARGON ADAPTATION sections |
| METRICS (definition/unit/measurement method/cost/failure signal; no invented thresholds) | **FIXED** | Table rebuilt to the full required column set, including a distinct Measurement Method column; every numeric target is definitional (zero violations) or explicitly `NEEDS EXPERIMENT` — none invented | METRICS table, §3 |
| Hash contract (shared cross-cloud requirement) | **FIXED** | No hash embedded inside the `.md`; `report_sha256: recorded_in_manifest` points to the separate companion manifest, which holds the real, final, non-self-referential SHA-256 | This section (MACHINE-READABLE MANIFEST) + companion `_manifest.yaml` |

## MACHINE-READABLE MANIFEST

```yaml
report_sha256: recorded_in_manifest
```

See the companion file `C6-CLOUD-EVALUATION-ENGINE_manifest.yaml` for the full canonical manifest (artifact_id, cloud, wave, system_scope/repository_target/execution_target, status fields, created_utc, supersedes, source_count, and the real `report_sha256`).

## ARTIFACT_READY_FOR_TRANSFER: YES
- filename: `C6-CLOUD-EVALUATION-ENGINE.md`
- artifact_id: `c6-cloud-evaluation-engine-v3` (single canonical ID; supersedes `c6-cloud-evaluation-engine-v2` and `c6-cloud-evaluation-engine-v1` — see manifest `supersedes` chain)
- hash: see companion manifest file
- dependencies: C1 (trajectory step-granularity decision), C3 (schema fields for trajectory + possible new `localization_correct` field + dual-gate overlap check; also the unattached C3 knowledge-model artifact referenced in Pattern 6's TEST NEEDED), C4 (Failure Analysis three-phase alignment with its own surgical-discipline chain), C7 (independent forensic audit — next owner)

## REMAINING UNKNOWN / NEEDS EXPERIMENT (consolidated, final)

- Whether GEPA itself (or any specific optimizer) should be adopted — Pattern 1
- Step-granularity mapping of SWE-agent's five-field trajectory schema onto ARGON's Cloud-turn structure — Pattern 3
- Recency-window size for within-task trajectory compression — Pattern 4
- Whether ARGON's existing `EVIDENCE GAP`/`CONFIRMED INCONSISTENCY`/`CONFIRMED BUG` vocabulary already captures Pattern 5's three-way localization/repair/validation split, or needs a dedicated `localization_correct` field — Pattern 5
- Whether Pattern 6's dual-gate mechanism is net-new or overlaps with C3's chain-resolution/content-review methods (unattached artifact — needs that file present to resolve, not resolvable from memory) — Pattern 6
- Tier-assignment logic underlying the Token Efficiency metric's ratio denominator
- Reuse-limit for held-out sets before validity decays (Benchmark Validity Limitations)
- Judge-call cost for non-exact-match Correctness scoring

None of the above is asserted as resolved anywhere in this document; each remains exactly as open as stated in its originating Pattern/metric entry.

## FINAL SELF-CHECK (consolidated, final)

| Question | Answer |
|---|---|
| Evidence — is every OBSERVED supported? | Yes, per the Sources Studied table (7 sources, all URL/section/date-cited) |
| Freshness — is vendor behavior still represented correctly? | Yes — no vendor claim in this document has a version/date conflict identified this pass |
| Classification — does ADOPT/ADAPT avoid implying "validated"? | Yes, reinforced this pass specifically for Pattern 2 and the stale appendix line |
| Benchmark — is score kept separate from a general quality verdict? | Yes — Benchmark Validity Limitations section, reconfirmed |
| Token — are cost and measurement clear? | Yes — every metric now has an explicit Measurement Method, not just a unit |
| Security — is a bypass path named? | Yes — the test-quality blind spot (§6 Failure Modes, appendix) |
| Human — does authorization stay outside UI/model? | Yes — nothing in this document proposes automated promotion bypassing human approval |
| Portability — is model-specific behavior confined to an adapter? | Yes — §5 Model Portability (appendix) addresses this directly; OpenAI's specific span taxonomy explicitly not adopted wholesale |
| Scope — was ARGON-HEALTH touched? | No |
| Metadata — does the manifest match the final version? | Yes — manifest is now a separate file, hashed after this file's final edit, avoiding the self-reference issue entirely |
| Self-containment — can C7 audit without hidden files? | Yes — Self-Containment Note (top of document) restates every previously-external-only rule; the one remaining unattached dependency (C3's knowledge-model artifact, Pattern 6) is named as such, not hidden |
| Honesty — any claim stronger than its evidence? | None identified beyond what's already corrected across v2 and v3 |


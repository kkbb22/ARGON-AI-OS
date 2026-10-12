# C4-SURGICAL-ENGINEERING-PROTOCOL

| | |
|---|---|
| Cloud | C4 — Product / Engineering Depth / Surgical Engineering Research Cloud |
| Mission | ARGON Cloud Evolution Program — Research Sprint (this revision: Final Correction Pass before C7 v4 applied, on top of Correction Pass v1) |
| Supersedes | The Correction Pass v1 revision of this same filename (artifact_id `053d9279-cebf-4ad5-8768-3238547fa93f`) — this pass adds §6's benchmark-alone-≠-proof line, adds section-level citation pointers to Patterns A/B/C/E, and rebuilds the finding matrix as "C7 v3 FINDING MATRIX" with an Evidence column; no new pattern research scope |
| Hard rules acknowledged | No ARGON-HEALTH edit, no Legacy edit, no ADR/ACR created, no code implemented, Wave 3.5 not reopened, no new architecture decision introduced under cover of this correction pass |
| report_sha256 | recorded_in_manifest — per the Hash Contract, the manifest is the canonical location for this artifact's real SHA-256; no hash value is embedded here to avoid the self-referential problem of a file's hash depending on its own content |

**Source integrity statement:** every claim tagged SOURCE below carries
a URL, document/section, and access date (this conversation, 2026-09-20).
No leaked vendor system prompt is used or reproduced. No unpublished
implementation detail is attributed to any company — Cline's and
Aider's UI/version-specific behavior may change between releases, and
is cited as documentation current as of the access date, not as a
permanent specification.

**Evidence self-containment note (per both Correction Pass v1 §10 and
Final Correction Pass §9):** this revision applies corrections
described directly in the correction-pass prompts' own "C4" sections,
verbatim. I have not independently seen `C7-CLOUD-EVOLUTION-FINAL-AUDIT.v3`
itself — only the C4-specific findings excerpted directly into each
correction prompt. Those findings are treated here as given corrections
to apply and are addressed on their own technical merits (checked
against the actual cited sources, independent of whether "C7 said so"),
not cited as something this document independently confirms C7
produced. The C7 v3 Finding Matrix at the end of this document reflects
only the findings given in these two prompts (Correction Pass v1: C4-D,
C4-F/X1, C4-DG/X5, C4-H, C4-D4; Final Correction Pass: D4, C4-F, C4-DG,
C4-H, D4-citations) — I am not inventing additional findings I was not
shown.

---

## 0. Sources studied

| System | Type | Citation | URL | Access date |
|---|---|---|---|---|
| Agentless | Research paper + OSS | Xia, Deng, Dunn, Zhang, "Agentless: Demystifying LLM-based Software Engineering Agents," arXiv:2407.01489 (UIUC) | arxiv.org/abs/2407.01489 ; github.com/OpenAutoCoder/Agentless | 2026-09-20 |
| Aider | OSS + official docs | "Repository map"; "Chat modes"; "Linting and testing"; "Git integration" | aider.chat/docs/repomap.html ; aider.chat/docs/usage/modes.html ; aider.chat/docs/usage/lint-test.html ; aider.chat/docs/git.html | 2026-09-20 |
| SWE-agent | Research paper (NeurIPS 2024) | Yang, Jimenez, Wettig, Lieret, Yao, Narasimhan, Press, "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering," arXiv:2405.15793 (Princeton/Stanford) | arxiv.org/abs/2405.15793 | 2026-09-20 |
| OpenHands | OSS + official docs | "CodeActAgent" doc; CodeAct paper arXiv:2402.01030 | docs.openhands.dev/openhands/usage/agents.md | 2026-09-20 |
| Cline | OSS + official docs | "Auto Approve & YOLO Mode"; "Plan vs. Act" usage docs | docs.cline.bot/features/auto-approve.md | 2026-09-20 |
| SWE-bench (evaluation methodology, cited for the dual-gate pattern) | Research paper + official post | Jimenez et al., ICLR 2024; OpenAI, "Introducing SWE-bench Verified" | openai.com/index/introducing-swe-bench-verified | 2026-09-20 |

**Source count: 6.** All public, all citable, none a leaked prompt.

---

## 1. Task applicability — not every task gets a localization phase

Before any pipeline applies, the task itself must be classified. Forcing
LOCALIZATION → REPAIR → VALIDATION onto a task that isn't a code-repair
task produces theater, not discipline.

| Task class | Example | Localization phase? | Applicable pipeline |
|---|---|---|---|
| **Repository engineering task** | Fix a bug, add a function, refactor a module | **Yes** | Full LOCALIZATION → REPAIR → VALIDATION (this document) |
| **Architecture/document task** | Everything C4 produced in earlier Waves of this conversation (domain maps, ADR analysis) | **No** — there is no bug to localize, no file to patch | A citation-discipline pipeline instead: CLAIM → SOURCE → VERIFY, already the pattern used throughout this conversation |
| **Informational task** | "What does ACR-4 say?" | **No** | Direct lookup/answer; no phase pipeline needed at all |
| **Task with no localization phase by nature** | Generating a new file that doesn't exist yet (Pattern 3 in the prior version of this document already noted this) | **No** — nothing to localize, only a target path to confirm doesn't already exist | REPAIR (generate) → VALIDATION only; localization is vacuous, not skipped-but-required |

**This distinction is itself evidence-based, not assumed:** Cline's own
documentation draws exactly this line by making Plan mode "entirely
read-only" for architecture/exploration work and reserving Act mode for
actual repository mutation — i.e., even Cline's own design treats
"understand/decide" and "localize-and-edit" as different task shapes,
not one universal loop (SOURCE: docs.cline.bot, "Plan vs Act" usage
page, accessed 2026-09-20).

---

## 2. Mandatory pipeline: does public evidence support LOCALIZATION → REPAIR → VALIDATION?

**Yes, for repository-engineering tasks specifically — evidence table:**

| System | Separates the 3 phases? | Evidence |
|---|---|---|
| Agentless | **Explicitly, by design** | "AGENTLESS employs a simplistic three-phase process of localization, repair, and patch validation, without letting the LLM decide future actions" (SOURCE: arXiv:2407.01489 abstract, accessed 2026-09-20) |
| SWE-bench harness | **Implicitly, by construction** | Patch is applied to the base commit, *then* FAIL_TO_PASS/PASS_TO_PASS tests are run — repair and validation are separate, sequential steps in the harness itself (SOURCE: openai.com/index/introducing-swe-bench-verified, accessed 2026-09-20) |
| Cline | **Partially — Plan vs. Act, not a 3-way split** | Plan (read-only, includes something like localization/understanding) vs. Act (write) is a 2-way gate, not a 3-phase pipeline; validation isn't a separate mode, it's left to the user "run tests locally, paste failures back" (SOURCE: docs.cline.bot auto-approve page; webreference.com Cline summary, accessed 2026-09-20) |
| Aider | **Not phase-gated the same way** | Aider edits and can auto-run tests/lint immediately after, in the same turn — closer to REPAIR+VALIDATION fused than a hard 3-phase gate (SOURCE: aider.chat/docs/usage/lint-test.html, accessed 2026-09-20) |
| OpenHands / CodeAct | **No explicit 3-phase separation found** | The CodeAct loop is a unified converse-or-act cycle per turn; no localization-then-repair-then-validation staging is described in the agent docs I read (SOURCE: docs.openhands.dev/openhands/usage/agents.md, accessed 2026-09-20) — **honesty note: absence of evidence in the one doc page I read is not proof OpenHands lacks this elsewhere; not claiming more than I checked** |

**Honest conclusion:** the 3-phase separation is a *documented, explicit
design choice* in exactly one of the five systems (Agentless) and one
evaluation harness (SWE-bench), present in *weakened form* (2-way, not
3-way) in Cline, and *not found* (not necessarily absent) in Aider and
OpenHands. This is **not unanimous convergent evidence** the way
Pattern 8 (lint gate) was in the prior version of this document — it is
real, but partial, evidence. Presenting it as unanimous would overstate
the case.

**CURRENT ARGON GAP:** I do not know whether ARGON's own kernel/Context
Compiler (defined in earlier Wave-3.5 C1 work I have not seen the
output of) already encodes this 3-phase separation. **I am not
assuming a gap exists** — only that the pipeline described here is one
concrete mechanism, evidenced by Agentless and SWE-bench specifically,
that C1 can compare against whatever already exists.

**PATTERN:** localization and repair as separate, ordered phases;
validation as a distinct final gate, never merged into repair.

**PROPOSED ADAPTATION:** if ARGON's kernel does not yet have this
structurally, adopt it for the surgical-editing task class specifically
(§1) — not universally, since §1 shows several ARGON task classes have
no localization phase at all.

**WHY:** Agentless's own reported result (highest SWE-bench Lite
performance among evaluated open-source approaches, at the time of
their reported evaluation, per the paper's own abstract) is offered by
its authors as evidence that constraining the action space this way
outperformed more complex agent loops on their benchmark — this is
their claim, not independently re-verified by me. **Benchmark validity
caveat applies — see §8.1.**

**TEST NEEDED:** given a task requiring a code repair, confirm no write
tool is invocable before a localization result is produced; confirm no
COMPLETE status is reachable before validation runs.

### 2.1 — Explicit minimal pipeline (per C4-D4)

Stated verbatim as its own object, not left implicit inside the prose
above:

```
Problem
→ Localization
→ Hypothesis
→ Exact Edit Location
→ Minimal Patch
→ Validation
```

This is the same LOCALIZATION → REPAIR → VALIDATION backbone as the
rest of this section, with REPAIR expanded into its own two visible
steps (Hypothesis, stated explicitly and falsifiably, before Exact Edit
Location is committed to; then Minimal Patch as the concrete output).
The lint/syntax gate (Pattern C) and evidence-recording step (Pattern
D) sit inside Validation as its first and last sub-steps respectively —
not separate top-level phases, to keep this exact 6-step chain
unambiguous per the correction request rather than re-expanding it back
into the longer form used elsewhere in this document.

---

## 3. Failure diagnosis taxonomy

Three categories, derived here as a direct logical consequence of the
3-phase split above (this taxonomy itself is **INFERENCE/PROPOSAL**,
not a verbatim citation from one paper — I did not find one single
source that names exactly these three failure categories by these
names; I built it from the phase boundaries because it is the natural
partition of "where in the pipeline did this fail"):

1. **Localization failure** — the wrong file/symbol/line was identified
   before any patch was attempted. Evidence for this as a real,
   distinct failure class (not merged with repair failure): Agentless's
   own hierarchical localization step is evaluated and reported
   separately from repair quality in their paper's structure (SOURCE:
   arXiv:2407.01489, "Localization" section, accessed 2026-09-20).
2. **Repair/response failure** — localization was correct, but the
   generated patch is wrong, incomplete, or introduces a new defect.
3. **Validation failure** — the patch may be correct, but the test
   evidence is insufficient or wrong: e.g., only a syntax check ran, or
   only regression tests ran with no reproduction test, or a
   reproduction test ran but wasn't actually exercising the fixed code
   path. SWE-bench's own dual FAIL_TO_PASS/PASS_TO_PASS requirement
   exists precisely because *either one alone* is an incomplete
   validation signal (SOURCE: openai.com/index/introducing-swe-bench-verified,
   accessed 2026-09-20).

**CLASSIFICATION: ADOPT** the 3-category split as ARGON's own failure
taxonomy for the surgical-editing task class — cheap to adopt, directly
actionable for C6's evaluation engine, and logically forced by the
phase split already evidenced in §2.

---

## 4. Patterns

Each pattern: SOURCE → OBSERVED PATTERN → WHY IT WORKS → ARGON ADAPTATION → REJECT IF → TEST NEEDED → CLASSIFICATION.

### Pattern A — Hierarchical localization before any edit
- **SOURCE:** Agentless localizes file → class/function → exact edit
  location before repair begins — described in the paper's own
  Localization-phase discussion, distinct from its separate Repair and
  Patch Validation phase discussions (arXiv:2407.01489, "Localization"
  phase description, accessed 2026-09-20).
- **OBSERVED PATTERN:** narrowing scope in stages, never guessing the
  file from the issue text alone.
- **WHY IT WORKS:** bounds blast radius before any write access exists.
- **ARGON ADAPTATION:** localization resolves through ARGON's own
  Domain→Command/Event graph (already defined in an earlier Wave), not
  a new mechanism.
- **REJECT IF:** the task is new-file creation (§1) — nothing to
  localize.
- **TEST NEEDED:** given a known bug location, localization converges
  there without opening an unrelated file first.
- **CLASSIFICATION: ADOPT.**

### Pattern B — Structured diff, never full-file rewrite
- **SOURCE:** Aider's SEARCH/REPLACE and diff edit formats send only the
  delta, anchored to existing text (aider.chat/docs/usage/modes.html,
  "Chat modes" page, edit-format description, accessed 2026-09-20);
  Agentless's Repair-phase description likewise generates patches, not
  rewritten files (arXiv:2407.01489, "Repair" phase description,
  accessed 2026-09-20).
- **OBSERVED PATTERN:** the model outputs only what changes.
- **WHY IT WORKS:** bounds what can be silently altered outside the
  intended change.
- **ARGON ADAPTATION:** canonical patch unit = anchored diff; a SEARCH
  block that doesn't match current file content exactly must fail, not
  fuzzy-apply.
- **REJECT IF:** the file doesn't exist yet.
- **TEST NEEDED:** a non-matching SEARCH block is rejected, not
  silently coerced.
- **CLASSIFICATION: ADOPT.**

### Pattern C — Lint/syntax gate before "applied" status
- **SOURCE:** Aider auto-lints and offers to fix after every edit
  (aider.chat/docs/usage/lint-test.html, "Linting and testing" page,
  accessed 2026-09-20); SWE-agent's ACI similarly gates edits on syntax
  validity before they're accepted, described in the paper's interface
  design discussion (arXiv:2405.15793, Agent-Computer Interface design
  section, accessed 2026-09-20) — two independent sources.
- **OBSERVED PATTERN:** a cheap correctness check runs before the edit
  counts as applied, not after.
- **WHY IT WORKS:** catches a break at the instant it's introduced.
- **ARGON ADAPTATION:** non-bypassable gate in the PATCH step of Wave 4's
  implementation order.
- **REJECT IF:** never found a case for skipping it.
- **TEST NEEDED:** invalid-syntax edit is rejected before recorded as
  APPLIED.
- **CLASSIFICATION: ADOPT** — convergent, independent evidence.

### Pattern D — Atomic, individually revertible commits
- **SOURCE:** Aider's official "Git integration" documentation: every
  edit is committed with a descriptive message, dirty pre-existing
  changes are committed separately *before* an AI edit is applied (so
  the two are never mixed in one commit), and `/undo`/`/diff` operate
  on that per-edit commit (aider.chat/docs/git.html, accessed
  2026-09-20). [Corrected citation — previously cited as "GitHub README
  content reviewed this session," which is not a resolvable reference;
  fixed per C4-D.]
- **OBSERVED PATTERN:** one edit = one checkpoint.
- **WHY IT WORKS:** isolates rollback to exactly the change at fault.
- **ARGON ADAPTATION:** one patch = one committed, independently
  revertible unit, tied to the Repository Snapshot object already
  defined elsewhere in this program.
- **REJECT IF:** a single logical change genuinely spans multiple files
  atomically — still one commit, one objective, not one commit per
  file.
- **TEST NEEDED:** reverting one recorded patch doesn't require
  reverting unrelated later ones.
- **CLASSIFICATION: ADOPT.**

### Pattern E — Purpose-built, bounded tool interface over raw shell
- **SOURCE:** SWE-agent's central finding: a custom Agent-Computer
  Interface (windowed file viewer, concise search results, syntax
  guardrails) outperformed the same model given raw shell access —
  the paper's own results/discussion section framing (arXiv:2405.15793,
  accessed 2026-09-20).
- **OBSERVED PATTERN:** bounding what a tool *can return* is itself a
  control, not just what the model is told to do.
- **WHY IT WORKS:** unbounded tool output degrades reasoning
  independent of model quality — the paper's own stated framing.
- **ARGON ADAPTATION:** any file-view/search tool built for Wave 4
  returns windowed, capped output by construction.
- **REJECT IF:** a task genuinely needs full-file context — support an
  explicit full-view request rather than forcing windowing always.
- **TEST NEEDED:** a worst-case query still returns a bounded, summarized
  result.
- **CLASSIFICATION: ADOPT.**

### Pattern F — Read/write mode gate (Plan vs. Act) — corrected per C1/C2/C4 shared finding
- **[CORRECTION NOTE, per C4-F/X1]:** the prior version of this pattern
  stated "two independent, unrelated sources converge on the same
  structural answer" and classified it ADOPT. That overstated what the
  cited evidence actually supports — it treated a documentation
  *description* of a product mode as equivalent to a *proven,
  tool-level enforcement mechanism* verified across the full range of
  ways a model could still write. Reframed below into the three
  required layers.
- **PUBLIC PRECEDENT (partially supported, not uniform):** Cline's own
  documentation describes Plan mode as read-only, with the mode switch
  itself requiring the user's action (docs.cline.bot, "Plan vs Act"
  usage page, accessed 2026-09-20 — Tier B/official docs). Agentless
  separately restricts its *repair phase* from taking further
  autonomous actions (arXiv:2407.01489, accessed 2026-09-20). **These
  are not the same claim**: Cline's is a product-level mode boundary
  covering an interactive session; Agentless's is a research pipeline
  constraint on one phase of an offline patch-generation run. Citing
  them together as "two sources proving structural enforcement" was the
  error — they support the *general idea* (constrain the action space
  during understanding/localization) at different scopes, not one
  unified mechanism. The earlier secondary citation to a third-party
  blog summary (previously "datacamp.com") is dropped here — per this
  program's Source Hierarchy, an unofficial summary is Tier C and
  cannot upgrade the strength of an official-doc claim; it added no
  independent information.
- **ARGON REQUIREMENT (this is ARGON's own proposal, not a vendor
  fact):** structural tool gating — a PLAN/localization state in which
  write-capable tools are not merely discouraged but not present in the
  available tool set at all.
- **IMPLEMENTATION: NEEDS EXPERIMENT**, not ADOPT. Neither cited source
  demonstrates — and I did not independently verify — that the gate
  holds against every avenue a model could use to mutate state, not
  only a dedicated "write file" tool call. The test must specifically
  cover:
  - **shell-based writes** (e.g., `bash -c "echo x > file"` if a shell
    tool remains available in PLAN)
  - **interpreter-based writes** (e.g., a Python/IPython tool writing a
    file via its standard library, if such a tool remains available)
  - **indirect file mutation** (e.g., a tool that "just runs tests" but
    accepts a fixture path outside the test directory)
  - **wrapper commands** (a permitted tool that itself shells out to
    something write-capable)
  A gate that blocks one specific tool call but leaves any of these
  open is not a structural gate — it is a partial one, and should be
  reported as such rather than as ADOPT.
- **TEST NEEDED (expanded, per C4-F/X1):** in PLAN state, attempt (a) a
  dedicated write-tool call, (b) a shell command that writes a file,
  (c) an interpreter command that writes a file, (d) a nominally
  read-only tool invoked with arguments that cause a side effect, (e) a
  permitted tool that wraps a write-capable subprocess. All five must
  fail structurally (the capability absent, not merely refused) for the
  pattern to earn ADOPT; passing only (a) earns at most PARTIAL.
- **CLASSIFICATION: NEEDS EXPERIMENT.** Downgraded from the prior
  ADOPT. The underlying idea (constrain the action space before
  localization/understanding is complete) remains a reasonable ARGON
  proposal, but "structural enforcement, independently confirmed" is
  not something the cited evidence establishes on its own.

### Pattern G — Granular, category-scoped auto-approval instead of one global switch
- **SOURCE:** Cline's Auto Approve is evaluated per tool-call category
  (read project files / read all files / edit project files / execute
  safe commands / execute all commands), each independently toggled,
  with OS notifications on approval-required events and on long-running
  auto-approved commands (docs.cline.bot/features/auto-approve.md,
  accessed 2026-09-20).
- **OBSERVED PATTERN:** approval is scoped per risk category, not an
  all-or-nothing switch.
- **WHY IT WORKS:** lets low-risk, high-frequency actions (reading
  files) proceed without friction while keeping high-risk actions
  (arbitrary shell execution) gated — directly matches this program's
  own stated goal: "Human controls the agent without micromanaging
  every harmless read."
- **ARGON ADAPTATION:** C2's policy matrix (TOOL → RISK → DEFAULT →
  APPROVAL → SCOPE → AUDIT, defined elsewhere in this program) should
  be checked against this category-scoping precedent rather than
  designed from scratch — I am not proposing new categories, only
  citing that this granularity level has real-world precedent.
- **REJECT IF:** N/A — this is a UX/policy pattern, not a technical one;
  C2/C5 own whether it fits ARGON's actual risk model.
- **TEST NEEDED:** a read-only action proceeds without a prompt while a
  destructive-shell action still requires one, under the same session.
- **CLASSIFICATION: ADAPT** — the granularity concept is transferable;
  the specific 5-category breakdown is Cline's own product design, not
  something to import verbatim without C2's own risk analysis.

### Pattern H — Code as a unified action space (CodeAct)
- **SOURCE:** OpenHands' default CodeActAgent "consolidates LLM agents'
  actions into a unified code action space," executing bash/Python
  rather than calling many bespoke tool schemas
  (docs.openhands.dev/openhands/usage/agents.md, citing arXiv:2402.01030,
  accessed 2026-09-20).
- **OBSERVED PATTERN:** fewer, more general primitives (run this code)
  instead of many narrow, bespoke tool definitions.
- **WHY IT WORKS (per the cited framing):** reduces schema-matching
  brittleness since the model reasons in a medium (code) it was heavily
  trained on.
- **ARGON ADAPTATION:** **UNKNOWN, not ADOPT.** This is in tension with
  Pattern E (bounded, purpose-built interfaces) — CodeAct is a bet on
  *fewer, more general* primitives, SWE-agent's ACI is a bet on *more,
  narrower, bounded* primitives. Both report strong results on
  overlapping benchmarks (**benchmark validity caveat, §8.1, applies**).
  I am not resolving which is right for ARGON; that needs an actual
  comparative experiment (§6/§7), not my preference.
- **REJECT IF:** the model-adaptive requirement (this program's own
  Final Target) means whichever primitive style is chosen must not
  assume a specific model's code-execution fluency.
- **TEST NEEDED:** see Experiment 7 (§7 main body / Appendix §7 addition).
- **CLASSIFICATION: NEEDS EXPERIMENT** — genuinely unresolved by the
  evidence gathered, not a hedge to avoid a decision. **Explicit framing
  per C4-H, preserved rather than smoothed over for narrative
  consistency:** bounded/structured interface (Pattern E, SWE-agent) =
  **candidate**; minimal/no-structured-interface (mini-swe-agent,
  researched in the Appendix below, >65–74% SWE-bench-Verified reported,
  benchmark caveat §8.1 applies) = **counter-evidence against assuming
  the candidate is necessary**; code-as-action-space (this pattern,
  OpenHands) = a third position, distinct from both. All three stand as
  competing candidates pending Experiment 7 — none is adopted as house
  doctrine.

---

## 5. Surgical discipline — anti-pattern → prevention mechanism

| Anti-pattern (from this mission's list) | Prevention mechanism, sourced | Source |
|---|---|---|
| Unrelated changes | Diff scoped to the anchored SEARCH/REPLACE block only (Pattern B) | Aider, Agentless |
| Broad rewrites | Same — structured diff format precludes full-file regeneration | Aider, Agentless |
| Changing adjacent files unnecessarily | Localization result defines the write scope; nothing outside it is touched (Pattern A) | Agentless |
| Patching before localization | Read/write mode gate (Pattern F) — proposed as a structural ARGON requirement; public precedent partial, enforcement scope NEEDS EXPERIMENT (see Pattern F correction) | Cline (partial), Agentless (different scope) |
| Validating only syntax | Lint/syntax gate (Pattern C) is necessary but explicitly *not* framed as sufficient by its own sources — none of Aider/SWE-agent claim syntax-passing means correct | Aider, SWE-agent |
| Validating only regression tests | SWE-bench's own dual-gate: PASS_TO_PASS alone never certifies a fix, only that nothing broke — FAIL_TO_PASS is required separately (§6) | SWE-bench |
| Claiming success without reproduction evidence | Same dual-gate: FAIL_TO_PASS is the reproduction-and-fix signal; its absence blocks success regardless of regression status | SWE-bench |

---

## 6. Dual-gate validation: regression + issue-specific reproduction

**Investigation, not an assumption of novelty:** SWE-bench's evaluation
harness requires **both** FAIL_TO_PASS tests (fail before the fix,
pass after — the reproduction-and-resolution signal) **and**
PASS_TO_PASS tests (pass before and after — the no-regression signal);
"both sets of tests are required to pass for the edit to fully resolve
the original... issue" (SOURCE: openai.com/index/introducing-swe-bench-verified,
accessed 2026-09-20). Agentless's own patch-validation phase uses the
same two-part check plus majority-vote re-ranking across candidates
(arXiv:2407.01489).

**I am explicitly not claiming this is new to ARGON.** An earlier Wave
of this program (C6's verification design) may already specify
something equivalent — I have not seen that Cloud's output and will not
guess at it.

**CLASSIFICATION: ADOPT the principle** (a patch must clear both a
reproduction-specific check and a regression check, neither substitutes
for the other) **— UNKNOWN whether it duplicates existing C6 work**,
which only C1/C6 can resolve by comparing artifacts.

**[Added per C4-DG]:** keeping this dual-gate pattern is not the same
as treating any system's *benchmark score under this gate* as proof of
general quality. A high SWE-bench/Verified score achieved under
FAIL_TO_PASS+PASS_TO_PASS validation shows the patch cleared *that
harness's* specific test oracle — it is evidence the dual-gate
mechanism is a meaningful filter (fewer false positives pass it than
would pass a single-gate check), not evidence that the agent producing
the patch is generally high quality. See §8.1 for the full caveat; it
applies to every score-bearing claim in this section too, including
Agentless's own reported validation results.

---

## 7. Mandatory measurable experiments

Each experiment specifies hypothesis, dataset, metric, failure
threshold, and promotion condition, as required. None of these have
been run — this section defines them, it does not report results.

### Experiment 1 — Localization accuracy
- **Hypothesis:** graph-based localization (Pattern A, via ARGON's
  Domain/Command graph) identifies the correct file/symbol more often
  than keyword-only search.
- **Dataset:** a held-out set of ARGON-specific synthetic bugs with
  known ground-truth locations (does not exist yet — must be
  constructed once real code exists; cannot be built against the
  current documentation-only repository).
- **Metric:** % of tasks where the top-1 localized file/symbol matches
  ground truth.
- **Failure threshold:** below the keyword-search baseline on the same
  set — if graph-based localization doesn't beat a trivial baseline,
  it isn't earning its complexity.
- **Promotion condition:** statistically significant improvement over
  baseline across the full held-out set, not a handful of cherry-picked
  cases.

### Experiment 2 — Patch minimality
- **Hypothesis:** anchored-diff patches (Pattern B) touch fewer lines
  than full-file-rewrite patches for equivalent fixes.
- **Dataset:** paired patches for the same fix, generated both ways.
- **Metric:** lines changed outside the minimal necessary diff (as
  determined by human/expert review).
- **Failure threshold:** anchored-diff patches touching more unrelated
  lines than rewrites would falsify the hypothesis outright.
- **Promotion condition:** anchored-diff strictly dominates on this
  metric across the sample.

### Experiment 3 — Regression pass rate
- **Hypothesis:** the lint/syntax gate (Pattern C) reduces
  regression-test failures caused by trivial syntax breaks.
- **Dataset:** patches generated with and without the gate active.
- **Metric:** % of patches whose regression suite fails specifically
  due to a syntax error.
- **Failure threshold:** no measurable difference with the gate on vs.
  off.
- **Promotion condition:** gate-on materially reduces syntax-caused
  regression failures.

### Experiment 4 — Reproduction pass rate
- **Hypothesis:** requiring an explicit reproduction test (dual-gate,
  §6) before COMPLETE reduces false "fixed" claims versus
  regression-only validation.
- **Dataset:** a set of patches previously marked "fixed" under a
  regression-only gate, re-evaluated under the dual gate.
- **Metric:** % of previously-"fixed" patches that fail the added
  reproduction check.
- **Failure threshold:** near-zero difference (would suggest the
  reproduction gate adds cost without catching anything).
- **Promotion condition:** the reproduction gate catches a
  non-trivial fraction of false positives the regression-only gate
  missed.

### Experiment 5 — Unrelated file touches
- **Hypothesis:** the localization-first pipeline (Pattern A) results
  in fewer files touched per patch than an unlocalized, free-roaming
  edit approach.
- **Dataset:** matched tasks run both ways.
- **Metric:** count of files modified per resolved issue.
- **Failure threshold:** localization-first shows equal or more files
  touched.
- **Promotion condition:** materially fewer files touched, holding
  resolution rate constant (a pipeline that touches fewer files but
  also fixes fewer bugs hasn't proven anything).

### Experiment 6 — Repair success after correct localization
- **Hypothesis:** given a *confirmed-correct* localization, repair
  success rate is measurably higher than end-to-end (localization+repair
  combined) success rate — isolating how much of end-to-end failure is
  attributable to repair specifically, not localization (ties directly
  to the failure taxonomy in §3).
- **Dataset:** tasks where ground-truth location is provided directly
  (bypassing localization) vs. tasks requiring the agent to localize
  itself.
- **Metric:** repair success rate, location-given vs. location-found.
- **Failure threshold:** no gap between the two conditions (would mean
  localization isn't actually the bottleneck it's assumed to be).
- **Promotion condition:** a clear, reproducible gap exists, confirming
  §3's taxonomy has real diagnostic value.

### Experiment 7 — False-positive localization
- **Hypothesis:** the bounded/purpose-built interface style (Pattern E)
  produces fewer confidently-wrong localizations than the
  code-as-action-space style (Pattern H) — this is the concrete
  experiment Pattern H's NEEDS EXPERIMENT classification calls for.
- **Dataset:** the same task set run under both interface styles.
- **Metric:** % of localizations reported with high confidence that are
  actually wrong.
- **Failure threshold:** no measurable difference between styles.
- **Promotion condition:** one style shows a statistically significant
  lower false-positive rate — determines which of Pattern E/H (or both,
  or neither) ARGON should standardize on.

---

## 8. Source integrity confirmation

Every SOURCE line above carries a URL and access date (2026-09-20, this
session). No content from any of the six systems studied is a leaked
confidential system prompt — Agentless and SWE-agent are peer-reviewed
publications; Aider, OpenHands, and Cline are open-source projects with
public documentation; SWE-bench is a published, widely-cited evaluation
benchmark. No unpublished implementation detail is attributed to
Anthropic, OpenAI, or any other vendor beyond what their own public
blog posts (cited above) state.

### 8.1 — Benchmark validity caveat (applies to every % figure in this document and its Appendix, per C4-DG/X5)

**A benchmark score is not a synonym for general agent quality.**
Every SWE-bench/SWE-bench-Lite/SWE-bench-Verified percentage cited in
this document (Agentless's, SWE-agent's, AutoCodeRover's, and
mini-swe-agent's reported figures) is a **benchmark score**, and each
carries caveats this document does not independently re-verify:
- **Benchmark version matters:** SWE-bench, SWE-bench Lite, and
  SWE-bench Verified are three different, non-interchangeable test
  sets; a score on one is not directly comparable to a score on
  another without saying which was used (this document specifies the
  version wherever it is known and cited; where a source's own
  materials didn't specify, that is a gap, not filled in by
  assumption).
- **Test pass ≠ fix correctness:** a patch that makes the specified
  FAIL_TO_PASS/PASS_TO_PASS tests pass is not thereby proven to be the
  *correct* or *only* correct fix — it satisfies the benchmark's
  specific test oracle, which is a proxy for correctness, not identical
  to it.
- **Contamination is a known, discussed risk** in this literature
  generally (whether a model's training data included the fix or
  discussion of the exact issue) — this document did not independently
  audit any of the four systems' benchmark runs for contamination; that
  would require access each project's own methodology section in more
  depth than this pass performed.
- **Independent audit status:** none of the percentages cited here were
  independently re-run or audited by me; they are reported exactly as
  each project's own materials state them, attributed as such.
- **Therefore:** every occurrence of a benchmark percentage elsewhere in
  this document and its Appendix should be read with this caveat
  attached, not as a standalone quality ranking between the systems.

## 9. Scope confirmation

No ARGON-HEALTH file modified. No Legacy ARGON referenced or touched.
No ADR or ACR created or altered. No code implemented. Wave 3.5 (the
ARGON-HEALTH domain/workflow reconciliation work) is not reopened here
— this document concerns the separate AI-OS tooling research track.

## 10. Handoff — not resolved here

- **C1:** whether the LOCALIZATION→REPAIR→VALIDATION pipeline (§2) and
  the proposed PLAN/ACT write-gate (Pattern F, now NEEDS EXPERIMENT —
  see correction) are already present in the Kernel/Context Compiler
  design from earlier work I have not seen.
- **C2:** Pattern G's granular auto-approval categories, against C2's
  own policy matrix.
- **C6:** owns turning §6 (measurable experiments) into actual runnable
  test infrastructure, and owns resolving whether §6's dual-gate
  duplicates existing C6 verification design.
- **C7:** Pattern H is left at NEEDS EXPERIMENT rather than forced to a
  verdict — worth confirming that's the right call rather than a
  deferral.

---

# Appendix: CLOUD CAPABILITY UPGRADE

Added per the Common Cloud Evolution Super-Prompt. This does not change
the task above — it applies the common research/token/evidence
discipline to it and records what that discipline surfaced. No second
file was created for this; it is appended to the existing artifact.

## 1. Sources studied (updated — 4 new sources opened this pass)

| System | Citation | URL | Access date |
|---|---|---|---|
| mini-swe-agent | SWE-agent team (Lieret, Jimenez et al.), Princeton/Stanford | github.com/SWE-agent/mini-swe-agent | 2026-09-20 |
| AutoCodeRover | Zhang, Ruan, Fan, Roychoudhury, "Autonomous Program Improvement," arXiv:2404.05427 (NUS) | github.com/nus-apr/auto-code-rover ; arxiv.org/abs/2404.05427 | 2026-09-20 |
| SWE-ReX | Lieret, Jimenez, Yang, Princeton | swe-rex.com ; github.com/SWE-agent/SWE-rex | 2026-09-20 |
| Terminal-Bench | Stanford / Laude Institute | tbench.ai/about ; tbench.ai/docs | 2026-09-20 |

(Agentless, Aider, SWE-agent, OpenHands, Cline, SWE-bench remain as
cited in §0 above — 10 sources total this pass, all public, none a
leaked prompt.)

## 2. High-value patterns

- **Three genuinely different localization mechanisms, all with
  published, non-trivial SWE-bench results:** Agentless's hybrid
  LLM+IR hierarchy, AutoCodeRover's pure AST-based structural search
  (`search_class`/`search_method`/`search_code` against a locally
  analyzed AST, not string matching), and SWE-agent's ACI-mediated
  search. **General principle, stripped of any one vendor's method:**
  *some* structured (not free-text-guess) localization mechanism
  matters; *which specific* structuring method is not, by itself, the
  load-bearing factor — three different ones all work.
- **Execution environment as a swappable backend:** SWE-ReX runs
  identical agent code against local, Docker, AWS, or Modal
  environments — the agent logic carries no assumption about where it
  executes. Directly transferable as a design principle independent of
  any model or provider choice.
- **Validation is not only test-based:** Terminal-Bench validates by
  checking the sandboxed environment's *final state* against an
  expected condition, rather than running a specific pre-written test
  suite the way SWE-bench does. This broadens §6's dual-gate discussion
  — ARGON's own validation gate should not assume every task class has
  a pre-written test suite available.

## 3. Patterns rejected (and why)

- **Rejected: assuming bounded/structured tooling is necessary for
  good performance.** mini-swe-agent has *no tools beyond bash*, no
  tool-calling interface at all, yet is reported at >65–74% on
  SWE-bench Verified across cited versions, "starts much faster than
  Claude Code" per its own documentation (**benchmark validity caveat,
  §8.1, applies — this is mini-swe-agent's own reported score, version-
  dependent, not independently re-audited here**). This directly
  counters an unstated assumption behind Patterns E/H in the main
  document — correctly left there as NEEDS EXPERIMENT, not resolved by
  fiat.
- **Rejected: picking one canonical localization mechanism now.**
  Three non-interchangeable, independently published mechanisms all
  work. Standardizing on one today, before any ARGON-specific
  experiment (§6, Experiment 1) has run, would be exactly the kind of
  premature vendor-pattern adoption this program prohibits.
- **Noted tradeoff, not a rejection:** mini-swe-agent's bash-only
  design is token-efficient and maximally model-portable, but it also
  has a *larger raw attack surface* (unrestricted bash) than a bounded
  ACI. Token efficiency and security surface pull in opposite
  directions here — flagged for C2, not resolved by C4.

## 4. Token efficiency gains

- mini-swe-agent's own stated design rationale is itself a token-economy
  argument: removing tool-calling schemas and stateful shell-session
  bookkeeping reduces per-turn overhead directly — a sourced example of
  §7's "fewer, cheaper primitives" principle taken to its logical
  extreme.
- SWE-ReX-adjacent infrastructure (the "SWE-Scale" stateless
  sandbox-per-candidate pattern found alongside it) uses a warm
  container pool to amortize cold-start cost without breaking
  isolation — a latency/token economy pattern specific to the ACT step,
  distinct from reasoning-token economy.

## 5. Model portability

- mini-swe-agent is the strongest evidenced example found this pass of
  kernel/model-adapter separation (§14 of the Common Prompt): it works
  with "literally any model" because it depends on nothing beyond raw
  text and bash — worth citing directly to C1's harness design as an
  existence proof that the separation is achievable at the extreme end.
- SWE-ReX demonstrates a second, orthogonal portability axis:
  environment-independence, distinct from model-independence. Both are
  real and both are separately evidenced — they should not be
  conflated into one "portability" requirement.

## 6. Failure modes

- AutoCodeRover's own reported pass rate changed across dated versions
  (19% → 30.67% → 38.40%, each tied to a specific release date and to
  SWE-bench-lite/SWE-bench-Verified respectively — **benchmark validity
  caveat, §8.1, applies to all three figures**). A pattern's cited
  effectiveness can be version-dependent — citing a tool's capability
  without a version/date, as this program's own Source Ledger rule
  (§11) anticipates, is itself a failure mode.
- Terminal-Bench's own release post states current agents "struggle to
  chain together multiple actions, reason over long contexts, act
  independently within their limits, and safely execute sensitive tasks
  without human supervision" — a directly-sourced failure list relevant
  to whatever ARGON's own ACT step eventually looks like.

## 7. Experiments (addition to §6 above)

- **Experiment 7 gets a third arm:** bounded ACI (SWE-agent) vs.
  code-as-action-space (OpenHands/CodeAct) vs. minimal/no-structured-tools
  (mini-swe-agent) — the third arm has real cited evidence of
  competitiveness, so excluding it from the comparison would bias the
  experiment before it starts.
- **New candidate experiment:** once real ARGON code exists, compare
  AST-based structural localization (AutoCodeRover-style) against
  ARGON's graph-based localization (Pattern A) — same shape as
  Experiment 1, a different comparison arm, not a replacement for it.

## 8. Transferable principles (mechanism, not vendor)

- Structured localization beats free-text guessing; the specific
  structuring method is not the load-bearing variable — evidenced by
  three divergent, independently successful mechanisms.
- Execution environment should be a swappable backend behind a stable
  interface, never a kernel-level assumption.
- Validation should support both test-based (FAIL_TO_PASS/PASS_TO_PASS)
  and state-based (final-condition) checks — not every task class has
  the former available.
- Token efficiency and security surface are sometimes in direct
  tension (bash-only minimalism vs. bounded interfaces) — a real
  tradeoff for C1/C2 to weigh, not a default either way.

**Self-check against §28 before delivery:** every OBSERVED claim above
carries a URL and access date; mechanism was kept separate from any
one vendor's branding throughout; no second file was produced for this
addition; nothing here declares ARGON "should" adopt any one option
before the experiments in §6 run; UNKNOWN is stated wherever it applies
(Pattern H, the bounded-vs-minimal tension) rather than resolved by
preference.

---

# C7 v3 FINDING MATRIX

Per this pass's instructions, using the exact requested columns. Covers
the five C4-tagged items given in this Final Correction Pass prompt
(§14 of that prompt: D4, C4-F, C4-DG, C4-H, D4-citations), plus a
carry-forward row noting the C4-D/C4-F/X1/C4-DG/X5/C4-H/C4-D4 items
already resolved in the prior Correction Pass v1 (not re-litigated,
only re-confirmed still holds).

| Finding | Status | What changed | Evidence |
|---|---|---|---|
| **D4** — explicit pipeline + failure taxonomy | **FIXED (carried forward, re-confirmed present)** | §2.1 states `Problem → Localization → Hypothesis → Exact Edit Location → Minimal Patch → Validation` verbatim; §3 states the three-way `localization failure / repair failure / validation failure` split | §2.1 and §3 of this document, both already present from Correction Pass v1, checked again this pass and found intact |
| **C4-F** — Plan/Act not presented as universal vendor fact | **FIXED (carried forward, re-confirmed present)** | Pattern F carries the three-layer split (Public Precedent / ARGON Requirement / Implementation) and is classified NEEDS EXPERIMENT, not ADOPT | Pattern F, §4, checked again this pass — the correction from v1 was not reverted |
| **C4-DG** — dual-gate kept; benchmark score ≠ proof | **FIXED (new this pass)** | §6 now carries an explicit added line stating a high benchmark score under the dual-gate shows the *filter* is meaningful, not that the *agent* is generally high-quality, cross-referenced to §8.1 | §6, "[Added per C4-DG]" paragraph, new this pass |
| **C4-H** — mini-swe-agent counter-evidence retained | **FIXED (carried forward, re-confirmed present)** | Pattern H still states candidate-vs-counter-evidence explicitly and remains NEEDS EXPERIMENT; not softened into a general doctrine | Pattern H, §4, and Appendix §3 ("Patterns rejected"), unchanged since v1 |
| **D4 citations** — every source traceable (URL + section/path + date) | **FIXED (new this pass)** | Patterns A, B, C, and E previously cited a paper/page with a date but no section-level pointer; each now names the specific phase/page section the claim is drawn from, using descriptive (not fabricated-numeric) section references since exact numbered sections could not be independently re-confirmed this pass | Patterns A, B, C, E, §4, edited this pass |

**Nothing above was disputed or found incorrect** — all five were
either genuine gaps (C4-DG's explicit line, D4 citations' section
pointers) or already-fixed items from the prior pass that this pass
re-checked rather than assumed. No `DISPUTED — EVIDENCE PROVIDED`
status was needed.

## Remaining UNKNOWN / NEEDS EXPERIMENT (per deliverable item 5)

- **Pattern F** (Plan/Act structural enforcement) — NEEDS EXPERIMENT;
  scope of test defined (§4, Pattern F) but not run.
- **Pattern H** (CodeAct vs. bounded ACI vs. minimal/no-tools) — NEEDS
  EXPERIMENT; three-way comparison defined (§7, Experiment 7 and its
  Appendix extension) but not run.
- **§6 Dual-gate** — UNKNOWN whether it duplicates existing C6
  verification work; not resolvable by C4 alone.
- **Pattern G's specific 5-category approval breakdown** — ADAPT, not
  ADOPT; whether Cline's specific categories fit ARGON's risk model is
  C2's open call, not decided here.
- **Experiments 1–7 generally** (§7) — all defined, none executed; all
  remain NEEDS EXPERIMENT / not yet run by construction, not by
  oversight.

---

# C1 — CLOUD HARNESS / ADAPTER RESEARCH (Cloud Evolution Research Sprint)

Scope: ARGON AI-OS research artifact. This document does not use, and is
not filed under, `repo_target = ARGON-HEALTH` — this sprint is
`system_scope: ai_engineering_os`, `repository_target: none`,
`execution_target: deliverable_output`. No ARGON-HEALTH or Legacy ARGON
file was read, modified, or referenced for architecture purposes. No
ADR/ACR created. No Wave 3.5 artifact reopened or altered — this is a
freestanding research sprint superseding only the earlier, less rigorous
draft of the same filename produced before this sprint's format was
specified.

No leaked or vendor-internal prompt text appears anywhere below. Every
"OBSERVED" claim is backed by a public, named source with a URL. Where no
such source exists for a candidate pattern, it is labeled INFERENCE or
UNKNOWN, never OBSERVED.

**CORRECTION PASS v1 NOTICE (stated plainly, not buried):** this document
has been revised against the specific C1 findings named in the "Cloud
Evolution Correction Pass v1" instruction (C1-D1, C1-X2, C1-P2/X1, C1-D4,
C1-D5). **No `C7-CLOUD-EVOLUTION-FINAL-AUDIT` of any version exists in
this conversation** — no C7 Cloud Evolution audit was ever produced, so
it could not be read or used as a baseline; the corrections below were
applied directly against the correction pass's own inline descriptions of
each finding, checked against this artifact's actual prior content, not
against an independent audit document. This is stated explicitly rather
than implying an audit was consulted that does not exist. Separately: a
`C6-CLOUD-EVALUATION-ENGINE.md` was also never produced in this
conversation, so the correction pass's C6 items (C6-X5, C6-P2, C6-P5/P6,
METRICS) have no artifact to apply to — they are not addressed here and
are not fabricated as if C6 existed.

---

## Pattern 1 — Isolated Subagent Context

**SOURCE**
- Title: "Create custom subagents"
- Author/Org: Anthropic (Claude Code documentation)
- URL: https://code.claude.com/docs/en/sub-agents
- Section: "Built-in subagents" / overview
- Access date: 2026-09-20
- What it proves specifically: Claude Code ships built-in subagents (Explore, Plan, general-purpose); each subagent runs in its own context window with its own system prompt, tool access, and permissions; Explore and Plan additionally skip the parent session's standing project-instruction file and git status "to keep research fast and inexpensive," while every other subagent loads both.

**CORRECTION (this pass):** the earlier version of this artifact stated "a subagent cannot spawn a further subagent (delegation is one level deep)" as a settled fact. Direct re-verification found this is **not a stable, single fact** — evidence is mixed and version-dependent:
- A third-party companion project documents a *5-level* nesting depth as the intended, documented limit (Agent tool withheld only at depth 5), contradicting a flat "depth 1" reading. Source: github.com/davila7/claude_subagents, accessed 2026-09-20.
- Two filed bug reports against Anthropic's own `claude-code` repository describe the *opposite* problem in practice — freshly-spawned `general-purpose`/`claude`-type subagents have the nesting tool silently stripped (making them leaf-only, i.e. depth-1-like) even though the documentation says they should inherit it up to depth 5 — a documented contract mismatch, not a stable rule. Sources: github.com/anthropics/claude-code/issues/80036 and /issues/61993, accessed 2026-09-20.
- A separate, more severe bug report describes uncontrolled recursive spawning reaching 50+ levels in practice, ignoring an environment variable meant to disable it. Source: github.com/anthropics/claude-code/issues/68619, accessed 2026-09-20.

**Correct classification, per this pass's required separation:**
- **OBSERVED (public precedent):** delegation-depth behavior in this specific vendor's harness is *contested and version-dependent* — some documentation describes a 5-level intended limit, some subagent types are bugged into an effective depth of 1, and at least one severe regression shows unbounded depth in practice. No single "vendor depth = 1" fact is supportable from current evidence.
- **ARGON DESIGN PROPOSAL (not a vendor fact):** ARGON may still choose a bounded delegation depth for its own Cloud structure (e.g., C1 → C2..C7, no further) — but this is ARGON's own design choice, stated as such, not something borrowed from an established, stable vendor rule.
- **EXPERIMENT:** see Experiment E1b below (new), which tests ARGON's own depth-1 proposal against a deeper alternative on ARGON's own task set — vendor behavior is not evidence for or against ARGON's choice either way.

**OBSERVED PATTERN (the part that *is* well-supported across all four cited sources, contested or not):** delegated sub-tasks execute in a structurally separate context window; the *size* of the inherited baseline context is an explicit per-role choice in the documented design (Explore/Plan get a smaller baseline than other subagent types), independent of the separate, unresolved depth question above.

**WHY IT WORKS:** prevents disposable intermediate output (search results, file dumps) from polluting the main conversation; the per-role baseline choice matches context cost to actual need. (The depth-cap "prevents unbounded cost" rationale is retained only as ARGON's own reasoning for its own proposal, not as a proven vendor benefit — the cited regression report is direct evidence that depth limits are not automatically self-enforcing even where intended.)

**ARGON ADAPTATION:** (a) **ARGON DESIGN PROPOSAL**, not vendor fact: no Cloud may invoke an eighth role — delegation stays exactly one level (C1 → C2..C7, never further) — stated here explicitly as ARGON's own choice; (b) OBSERVED-supported: the size of each Cloud's default context baseline (beyond the mandatory live Repository Snapshot check) should be declared per role rather than assumed uniform.

**REJECT IF:** used to justify a Cloud skipping the mandatory live Repository Snapshot check for architecture-critical work — that check is a separate, non-negotiable rule (Wave 3.5 Correction Pack §7), not something a "lighter baseline" role may skip. Also reject any future restatement of "vendor enforces depth 1" as settled fact — the corrected evidence above is contested, not settled.

**TEST NEEDED:** NEEDS EXPERIMENT — see Experiment E1 (baseline sizing) and Experiment E1b (ARGON's own depth-cap choice, new this pass) below.

**Q1 (enforced or prompt-only?)** Enforced by the harness — the isolated context window is a structural property of how the tool is built, not an instruction to the model.
**Q2 (specific problem solved)** Context pollution and unbounded delegation cost.
**Q3 (model/harness separation)** The isolation mechanism lives in the harness (which context window a call runs in); it does not depend on which model is running inside that window.
**Q4 (Claude vs GPT/Codex adapter difference)** None observed at this layer — "run in an isolated context window" is a harness property, not a model-specific behavior; no source found suggesting GPT/Codex-based harnesses cannot implement the same isolation.
**Q5 (must stay model-independent)** The isolation mechanism and the one-level depth cap.
**Q6 (prevent model-specific leakage into Kernel)** State the rule as "delegation depth = 1" and "context isolation by default," not as a specific model's context-window API.
**Q7 (supports PLAN→REVIEW→APPROVAL→ACT→VERIFY)** Indirectly — isolation is orthogonal to which processing_state a Cloud is in; it constrains *what a Cloud can see*, not *what stage it's in*.
**Q8 (failure/retry/recovery)** Not addressed by this source; see Pattern 5.
**Q9 (false completion)** Not addressed by this source directly.
**Q10 (placement)** **Kernel** (delegation depth rule) + **Runtime mechanism** (the actual context-window isolation, once implemented).

**CLASSIFICATION:** context isolation itself: OBSERVED → **ADOPT**. Depth-cap: **ARGON DESIGN PROPOSAL**, not OBSERVED vendor fact → **NEEDS EXPERIMENT** (E1b). Per-role baseline sizing → **NEEDS EXPERIMENT** (E1).

---

## Pattern 2 — Structurally Enforced Plan/Act Separation

**SOURCE (two independent, converging sources)**
1. Title: "Create custom subagents" (same page as Pattern 1) — describes a built-in "Plan" subagent used during Plan mode specifically to research the codebase before a plan is presented, with only read-only tools (Write/Edit denied).
   URL: https://code.claude.com/docs/en/sub-agents · Access date: 2026-09-20.
2. Title: "What Is Cline? Open-Source AI Coding Agent Explained"
   Author/Org: fast.io (third-party summary citing Cline's own documentation)
   URL: https://www.fast.io/resources/what-is-cline.md · Access date: 2026-09-20
   What it proves: "In Plan mode, Cline can explore the codebase, run searches, and discuss strategy. It is constrained so it does not modify files or execute commands. That constraint is intentional."

**CORRECTION (this pass):** the earlier version stated flatly that "two independently engineered systems" prove structural enforcement. That overstates what documentation-only sources can prove. Reclassified per the required separation:

- **Vendor precedent:** **partially supported.** Both cited sources document that a *named* write/edit tool is withheld during planning. Neither source was independently tested by this research pass, and neither source's documentation confirms whether *other* tools available during planning (e.g., a general shell/terminal tool, if any remains available) could still be used to achieve a write indirectly — for example via shell redirection (`echo x > file`), an interpreter's own file-write calls, or a composite/wrapper command that is not itself named "Write" or "Edit." This gap is real and unresolved by the sources as read.
- **ARGON requirement (not a vendor-proven fact, ARGON's own bar):** `PLAN` must expose **no tool capable of causing a file, repository, or external-state mutation by any path** — named write tools, shell/terminal access, interpreter execution, and any composite/wrapper command alike. This is a stricter bar than either cited source is shown to meet, stated deliberately as ARGON's own requirement rather than attributed to either vendor.
- **Implementation:** **NEEDS EXPERIMENT** — see Experiment E2 (revised) below, which now explicitly covers shell-based writes, interpreter-based writes, indirect file mutation, and wrapper commands, not only calls to a tool literally named "Write" or "Edit."

**WHY IT WORKS (to the extent supported):** removing a named write/edit tool removes the most obvious accidental-mutation path; the guarantee is only as complete as the removal itself, which the cited sources do not verify is exhaustive.

**ARGON ADAPTATION:** strengthens the existing `PLAN` processing_state (Wave 3.5): `PLAN` should be redefined to mean "no tool capable of any mutation is exposed," not merely "the named Write/Edit tool is absent" and not "the Cloud is instructed not to write." This is a design correction, not a new design — the original Wave 3.5 intent already pointed this way but never stated the structural requirement this precisely, and this pass tightens it further than the first correction did.

**REJECT IF:** implemented as a system-prompt instruction inside the `PLAN` state ("please do not use write tools now") — per ARGON's own Policy/Enforcement/Audit finding (Wave 3.5), that is policy without enforcement. **Also reject** a design that removes only the named Write/Edit tool while leaving shell/interpreter access available and calls that "structural" — per the gap identified above, that would be an incomplete enforcement, not a complete one.

**TEST NEEDED:** NEEDS EXPERIMENT — see Experiment E2 (revised) below.

**Q1** Enforced for the *named* write/edit tool in both cited sources; **not confirmed** for shell/interpreter/wrapper paths — this is documentation, not this pass's own independent test.
**Q2** Accidental mutation during exploration/reasoning.
**Q3** The harness decides which tools are registered for a given mode/state; the model has no way to call a tool that was never registered.
**Q4** No source found describing a Claude-specific vs. GPT/Codex-specific difference in *this* mechanism — tool registration is a harness-side concern in both cited systems, independent of the underlying model.
**Q5** The rule "PLAN state exposes zero write-capable tools" must stay model-independent.
**Q6** Keep the rule phrased as a tool-registration constraint, never as "trust model X to comply."
**Q7** Directly implements the `PLAN` half of `PLAN → REVIEW → APPROVAL → ACT → VERIFY`.
**Q8** Not addressed by either source for this specific pattern.
**Q9** Indirectly: a plan produced with zero write access cannot itself constitute an unverified "completion" of a write task.
**Q10** **Runtime mechanism** (tool registration per state) governed by a **Kernel** rule (the state must have zero write tools, as an invariant, not a preference).

**CLASSIFICATION:** vendor precedent → **PARTIALLY SUPPORTED** (named-tool absence only, not full-path mutation absence). ARGON's own stricter requirement (all mutation paths, not just the named tool) → **ADOPT as ARGON's bar**, implementation → **NEEDS EXPERIMENT** (E2, revised).

---

## Pattern 3 — Agent-Computer Interface (purpose-built tool surface)

**SOURCE**
- Title: "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering" (NeurIPS 2024)
- Author/Org: Yang, Jimenez, et al., Princeton NLP / Stanford
- URL (secondary summary, paper itself behind arXiv/NeurIPS proceedings): https://www.noze.it/en/insights/swe-agent-princeton/ ; corroborated by https://pypi.org/project/sweagent/0.0.1
- Section: "Agent-Computer Interface" concept description
- Access date: 2026-09-20
- **Benchmark-number correction (this pass):** a prior version of this artifact cited a "+10.7 percentage points, SWE-bench Lite" ACI-vs-raw-shell ablation figure. Re-verification could not confirm this specific number from any source opened this pass — it is **UNRESOLVED / not re-confirmed**, and is **removed** rather than repeated. What **is** well-corroborated, independently, across five-plus secondary sources (swebench.com's own project page, SWE-Bench+ paper arXiv:2410.06992, and three independent third-party summaries) is a **different, more specific figure**: SWE-agent raised GPT-4's resolve rate from a 1.96% retrieval-augmented-generation baseline to **12.47%** on the **full SWE-bench dataset** (2,294 instances) — a roughly 6x improvement, which these sources attribute to the redesigned agent-computer interface. This is classified **SOURCE-VERIFIED NUMBER** (repeated identically, including to two decimal places, across swebench.com's own project page and an independent arXiv paper that re-analyzes the same result) — stronger evidence than the earlier, now-removed Lite-specific ablation figure, which could not be re-traced to a primary source this pass.
- **Separate unresolved conflict (flagged, not resolved):** one third-party source (a Japanese-language glossary page, jisaku.com) attributes a "12.5%" SWE-agent + GPT-4 Turbo figure specifically to "SWE-bench **Verified**" — but SWE-bench Verified was released after SWE-agent's original NeurIPS 2024 paper, making that specific attribution chronologically doubtful. This is recorded as **CONFLICT / UNRESOLVED**, not silently resolved by picking the number that "looks right" — it is not used as evidence for any claim in this artifact.

**OBSERVED PATTERN:** the interface exposed to a model should be designed for a model's parsing and reasoning characteristics, not repurposed from a human-facing interface.

**WHY IT WORKS:** compact, structured, consistent tool output reduces the model's own error rate at interpreting results — a measured effect in the source, not a claimed one.

**ARGON ADAPTATION:** not applicable to ARGON-HEALTH today — it is a 100% Markdown repository with zero source files (confirmed, Wave 0). This pattern is relevant only to a *future implementation* repository, where a windowed file editor and structured filesystem commands would matter. For ARGON-HEALTH now, the closest analogue is a heading/cross-reference index (already proposed, Wave 3.5), which is a much smaller-scope idea than a full ACI.

**REJECT IF:** used to justify building a full ACI now, before ARGON has any source code to operate on.

**TEST NEEDED:** deferred — cannot be tested without a real implementation repository.

**Q1** Enforced by harness design (the interface itself, not a prompt).
**Q2** Poor model performance when forced to use a general-purpose human interface (raw shell).
**Q3** Complete separation — the ACI is a harness-side abstraction the model calls; the model never touches the shell directly.
**Q4** The paper explicitly tested portability across model providers — see Pattern 4 below, which is this same source's most direct answer to Q4.
**Q5** The interface's command set and output format should stay model-independent; only the exact tool-call syntax used to invoke it is model/harness-specific.
**Q6** Define the ACI's commands generically (e.g., "view file window," "apply atomic patch") and let a thin adapter translate to whatever tool-calling convention a given model expects.
**Q7** Indirectly — a well-scoped ACI makes `ACT` safer (atomic patch operations are easier to gate/approve than freeform shell commands).
**Q8** Not directly addressed by the cited summary.
**Q9** Not directly addressed.
**Q10** **Model Adapter boundary** (tool-call syntax) around a **Runtime mechanism** (the ACI commands themselves, model-independent).

**CLASSIFICATION:** SOURCE → **ADOPT (deferred to a future implementation repository)**.

---

## Pattern 4 — Interface Design Is More Portable Than Raw Model Behavior

**SOURCE** (same paper as Pattern 3)
- **Classification (this pass, per the required SOURCE-VERIFIED / THIRD-PARTY SUMMARY / CONFLICT distinction):** this specific claim — that the same ACI was tuned on GPT-4 (Turbo) and shown portable to Claude 3 Opus at a numerically different resolve rate — is sourced from **one secondary-source reproduction** (a text mirror of the paper hosted outside the official proceedings), not independently cross-confirmed by a second source this pass. It is therefore classified **THIRD-PARTY SUMMARY**, not SOURCE-VERIFIED. The qualitative claim (same interface, portable across model families, different absolute score per model) is considered reasonably solid given it matches the well-corroborated existence of both a "SWE-agent + GPT-4" and a separate "SWE-agent + Claude 3 Opus" entry on SWE-bench's own official leaderboard page (swebench.com, Lite leaderboard section) — but the *exact numeric values* for each are not independently re-confirmed this pass and are **not restated as precise figures** below; only the qualitative portability claim is retained.
- URL (third-party reproduction, as above): https://object.cloud.sdsc.edu/v1/AUTH_da4962d3368042ac8337e2dfdd3e7bf3/ml-papers-txt/NeurIPS/2024/sweagent_agentcomputer_interfaces_enable_automated_software_engineering__eae396a7.txt · Corroborating existence check (official, confirms both model variants exist as leaderboard entries without reproducing exact Lite percentages in the fetched text): https://www.swebench.com/ · Access date: 2026-09-20.
- Second corroborating source (different system, same phenomenon): Aider's Architect/Editor mode is explicitly designed to mix model providers across the two roles. **Correction (this pass):** the earlier version of this artifact attributed a DeepSeek-R1 + Claude 3.5 Sonnet result to Aider's Sep 26, 2024 post — that post ("Separating code reasoning and editing," https://aider.chat/2024/09/26/architect.html) predates DeepSeek-R1's release and reports only an o1-preview-as-Architect (with DeepSeek or o1-mini as Editor) result reaching 85% on Aider's own benchmark; it does not mention R1 or Sonnet at all. The R1+Sonnet claim (a reported 64.0% SOTA on Aider's polyglot benchmark, at a stated 14x lower cost than the prior o1 SOTA) is from a **separate, later post**:
  Title: "R1+Sonnet set SOTA on aider's polyglot benchmark" · Author/Org: Aider (Paul Gauthier) · URL: https://aider.chat/2025/01/24/r1-sonnet.html · Published: 2025-01-24 · Access date: 2026-09-20.
  The two posts are now cited separately and not conflated.

**OBSERVED PATTERN:** in both cited systems, the *interface/role design* (ACI; architect/editor split) is what carried over across different model providers — the absolute performance number changed per model, but the interface itself did not need to be redesigned per model family.

**WHY IT WORKS:** the interface constrains *how* the model expresses intent (structured commands, a proposal-then-edit split); this shape is a property of the interaction design, not of any one model's internals.

**ARGON ADAPTATION:** this is the strongest available evidence for ARGON's own "model-adaptive" goal — it directly supports designing Kernel/Context/Tool-Policy/Evidence/Verification as model-independent (Wave 3.5's stated final target), with only a thin adapter layer translating calling conventions. **No ranking between any named models is made or implied here** — the sources are cited only for the portability property, not for which model performed "better."

**REJECT IF:** taken as proof that *all* behavior is portable — both sources report different absolute results per model, meaning some model-specific tuning still mattered even with a shared interface. Portability of the *interface* is not the same claim as portability of *performance*.

**TEST NEEDED:** NEEDS EXPERIMENT — see Experiment E3 below.

**Q1** Enforced (the interface/role split is a harness property in both sources); the *quality* of what happens inside it is model behavior, not enforced.
**Q2** The specific problem of needing to redesign the whole harness per model family.
**Q3** Interface = harness; what the model does with it = model behavior. Both sources keep these separate.
**Q4** Directly on point qualitatively: the same interface is listed against two different model families on SWE-bench's own official leaderboard (GPT-4 and Claude 3 Opus, as separate entries) — confirming *that* results differ per model under one shared interface, without this artifact asserting the *exact* numeric gap (THIRD-PARTY SUMMARY only for the precise figures, per the classification above). This remains the clearest documented *qualitative* example available of "same interface, different model, different outcome."
**Q5** The interface/role definitions themselves.
**Q6** Keep performance-tuning parameters (e.g., how verbose to make instructions for a specific model) inside the adapter, never inside the Kernel's interface definition.
**Q7** Directly relevant to `ACT` (SWE-agent's ACI) and to `PLAN`/`REVIEW` (Aider's architect role).
**Q8** Not addressed by either source.
**Q9** Not addressed by either source.
**Q10** **Kernel** (the interface/role shape) + **Model Adapter** (per-model tuning/calling convention).

**CLASSIFICATION:** OBSERVED (two independent sources) → **ADOPT** (interface-portability principle); **NEEDS EXPERIMENT** for ARGON's own adapter design.

---

## Pattern 5 — Checkpointing Before Elevated-Trust Operations

**SOURCE**
- Title: "Cline Security Model and Safe Agent Practices"
- Author/Org: fast.io (third-party summary directly citing Cline's official Auto Approve documentation)
- URL: https://www.fast.io/resources/cline-security-guide.md · Access date: 2026-09-20
- What it proves: Cline's own stated best practice is to "prefer Checkpoints (or version control) before turning on edit auto-approve" — i.e., a rollback point is recommended specifically before granting elevated, less-supervised write trust.

**OBSERVED PATTERN:** a recoverable checkpoint is established *before* trust is elevated, not only after a failure occurs.

**WHY IT WORKS:** makes an elevated-trust action reversible in practice, not merely "safe in theory."

**ARGON ADAPTATION:** relevant to the still-open Session/Task Resumption gap (identified, not resolved, in the earlier Wave 3.5 Operator Control research): before any `ACT` stage begins for a task carrying `execution_target = live_repository_write`, a checkpoint reference (e.g., the pre-action Repository Snapshot, already a designed object) should be recorded as part of the Approval Record, so that "resume" or "roll back" both have a concrete anchor.
**REJECT IF:** treated as a substitute for the Approval Record's hash-binding (Wave 3.5 Convergence Patch §4) — checkpointing addresses *recoverability after the fact*; hash-binding addresses *preventing the wrong action from running at all*. Both are needed; neither replaces the other.
**TEST NEEDED:** NEEDS EXPERIMENT — see Experiment E4 below.

**Q1** Recommended practice in the source, not described as harness-enforced (the source frames it as user guidance: "prefer... before turning on").
**Q2** Irreversible or hard-to-reverse elevated-trust actions.
**Q3** Checkpointing is a harness/runtime mechanism (a saved state), independent of model behavior.
**Q4** No model-specific difference identified in this source.
**Q5** The requirement "checkpoint before elevated trust" should stay model-independent.
**Q6** N/A — this pattern does not touch model-specific behavior at all.
**Q7** Fits at the boundary between `APPROVAL` and `ACT` — the checkpoint is taken once approval is granted, before execution begins.
**Q8** Directly relevant: a checkpoint is precisely what makes retry/recovery possible after a failed or stopped `ACT`.
**Q9** Not directly addressed.
**Q10** **Runtime mechanism**.

**CLASSIFICATION:** OBSERVED → **ADAPT** (ARGON already has the raw material — Repository Snapshot — but never wired it to Approval as a checkpoint reference).

**Six required questions, answered precisely (this pass, §12):**
- *What exactly is checkpointed?* The Repository Snapshot in force at the moment `APPROVAL` is granted (HEAD hash, branch, clean/dirty state — the object already defined in Wave 3.5) — **not** the Cloud's own conversational context, which is a separate, still-open gap (context isolation, unresolved).
- *What authority changes after checkpoint?* None by itself — taking a checkpoint grants no authority; it only anchors a rollback point. Authority still comes solely from the Approval Record.
- *What evidence is required?* The checkpoint reference itself becomes a field on the Approval Record (not yet formally added to that schema — this is an **open schema gap**, not yet closed even by this pass).
- *Can stale state be resumed?* **UNKNOWN / NEEDS EXPERIMENT** — no source addresses this, and ARGON has not designed a resumption mechanism (same gap flagged in the Wave 3.5 Operator Control research, item 6, still open).
- *Can approval survive a state change?* **No, by the existing Approval Record design** (Wave 3.5 Convergence Patch §4) — the content-hash binding means any change to the intended action, and implicitly to the repository state it assumed, should force re-approval rather than silently proceeding; this has not been tested.
- *What invalidates the checkpoint?* **UNKNOWN** — no invalidation rule has been designed; a plausible candidate (any Repository Snapshot staleness trigger firing, per Wave 3.5 Correction Pack §7) is noted here as a candidate only, not as a decided rule.

---

## Pattern 6 — Reflective, Feedback-Rich Evaluation Over Scalar Scores

**SOURCE**
- Title: "dspy.GEPA: Reflective Prompt Optimizer"
- Author/Org: DSPy project (Stanford NLP), documenting Agrawal et al., "GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning" (arXiv:2507.19457)
- URL: https://dspy.ai/api/optimizers/GEPA/ · Access date: 2026-09-20
- What it proves: GEPA optimizes prompts using full natural-language traces and textual feedback about *why* a run scored as it did, rather than a single scalar reward; it maintains a Pareto frontier of candidate prompts rather than collapsing to one "best so far," and is reported to need far fewer rollouts than reward-only reinforcement-learning-style optimizers to reach a comparable or better result.

**OBSERVED PATTERN:** evaluation that captures *why* something failed (not just *that* it failed) enables much more sample-efficient improvement than a scalar pass/fail signal.

**WHY IT WORKS:** diagnostic detail (which step, what reasoning, what output) gives the optimizing process something to act on beyond blind trial and error.

**ARGON ADAPTATION:** directly relevant to ARGON's own planned evaluation loop (Wave 3.5 C6 design intent: `task set → candidate prompt/router → run → metric → validation → regression set → promotion`). The correction this pattern suggests: ARGON's metric design should capture rich, structured failure detail (which Claim was contested, which Evidence was missing, which gate blocked) — matching Verification Record's existing shape (Wave 3.5 C3) — rather than a single pass/fail score per task.
**REJECT IF:** used to justify skipping a held-out validation/regression set — GEPA's own design still separates optimization data from a validation signal; rich feedback does not replace that separation.
**TEST NEEDED:** NEEDS EXPERIMENT — see Experiment E5 below.

**Q1** Enforced by the optimizer's own design (it structurally requires a feedback-carrying metric, not a bare score) — a metric that returns only a float makes this class of optimizer no better than a simpler alternative, per the source's own framing.
**Q2** Sample-inefficient prompt improvement when only a scalar score is available.
**Q3** The optimizer (harness-side tooling) is separate from the model being optimized; the same approach can, in principle, optimize prompts for any underlying model.
**Q4** No Claude-vs-GPT-specific distinction found in this source; the optimizer is describing an optimization *procedure*, not a model-specific behavior.
**Q5** The requirement "the evaluation metric must carry structured feedback, not just a score" should stay model-independent.
**Q6** N/A directly — this pattern concerns the evaluation loop, not runtime model calls.
**Q7** Relevant to `VERIFY`: a Verification Record with structured failure detail is the ARGON analogue of GEPA's feedback-rich metric.
**Q8** Indirectly: rich failure feedback is what would drive a *future* candidate-prompt retry loop, not an immediate task-level retry.
**Q9** Indirectly: a metric that can only say "pass/fail" is more prone to a false "pass" than one that must justify its score with specifics.
**Q10** **Role Skill** (the evaluation/metric design itself) — not Kernel, not a per-task runtime mechanism.

**CLASSIFICATION:** OBSERVED → **ADAPT**.

---

## MODEL PORTABILITY BOUNDARY

No model is ranked or declared a winner anywhere in this section.

**Claude-specific assumptions found in sources above:** none that must leak into ARGON's Kernel. Claude Code's subagent/permission mechanics (Patterns 1–2) are harness features; nothing in the cited documentation ties the *isolation* or *tool-absence* mechanism to a Claude-specific model capability — the mechanism is implemented by Anthropic's harness, but the underlying *pattern* (isolated context, tool-gated modes) is not shown to require a Claude-specific model feature.

**GPT/Codex-specific assumptions found in sources above:** SWE-agent's ACI was originally tuned against GPT-4 Turbo (Pattern 3/4); its authors' own reported cross-model test (GPT-4 Turbo vs. Claude 3 Opus) shows the *interface* transferred, but the *absolute resolve rate* did not — implying some amount of model-specific behavior (verbosity, instruction-following style, tool-call reliability) remains even under a shared interface. This residual difference is exactly what an adapter layer should absorb, not paper over.

**Generic (model-independent) assumptions, safe for Kernel:**
- ARGON's own delegation-depth-1 proposal (Pattern 1) — stated as ARGON's design choice, not as a vendor-proven fact (vendor evidence on this point is contested/version-dependent, per this pass's correction).
- `PLAN` state = zero write-capable tools registered (Pattern 2) — a tool-registration property, not a model behavior.
- Interface/role shape (ACI-style structured commands; architect/editor role split) as a design principle (Pattern 3/4) — the *shape*, not model-specific tuning.
- Checkpoint-before-elevated-trust (Pattern 5).
- Feedback-rich (not scalar-only) evaluation metrics (Pattern 6).

**Adapter interface candidates (must live behind a per-model boundary, never in Kernel):**
- Exact tool-call schema/format a given model expects.
- How verbose or how structured an instruction needs to be for a given model to reliably comply (the SWE-agent portability data, Pattern 4, is direct evidence this varies).
- Context-window size and any resulting need to compress differently per model.

**What must never leak into Kernel:** any rule phrased in terms of a specific model's name, a specific vendor's tool-call syntax, or a specific model's known quirks. The Kernel states *what* must be true (e.g., "PLAN has no write tools"); the adapter states *how* that is expressed to a specific model's calling convention.

---

## Experiments (NEEDS EXPERIMENT items, fully specified)

**E1 — Per-role context baseline sizing (Pattern 1)**
- Hypothesis: giving C4/C1 a larger default baseline (T0+T1) than C5 (T0 only) reduces total tokens spent per task without reducing answer correctness.
- Benchmark/task set: a fixed set of at least 10 representative ARGON-AI-OS tasks per Cloud role, replayed with both a uniform baseline and a role-differentiated baseline.
- Metric: total tokens consumed; independently, whether the task's Claims still resolve to the same `claim_status` under both conditions.
- Expected failure signal: role-differentiated baseline produces a different (worse) `claim_status` outcome than the uniform baseline on any task.
- Promotion condition: token reduction with zero degradation in `claim_status` outcome across the full task set.

**E2 (revised this pass) — Structural PLAN tool-gating, all mutation paths (Pattern 2)**
- Hypothesis: registering zero tools capable of mutation by *any* path during `PLAN` — not only a named write/edit tool — reduces successful mutation attempts to exactly zero, including via indirect paths.
- Benchmark/task set: a set of adversarial tasks covering five distinct attack vectors, per this pass's explicit requirement (expanded from four to five): (1) direct calls to a named write/edit tool; (2) shell-based writes (e.g., output redirection, `cp`, `mv`); (3) interpreter-based writes (e.g., a scripting tool's own file-write calls); (4) wrapper/composite commands not themselves named as a write operation; (5) **indirect mutation through another tool** — a permitted read-only or analysis tool that, internally, invokes a second tool capable of writing (distinct from vector 4: here the *outer* call looks entirely legitimate and read-only, and the mutation happens only inside a nested call the planner-level audit would not see without inspecting the callee).
- Metric: count of *successful* mutations achieved during `PLAN` (not merely attempted named-tool calls), broken out per attack vector above.
- Expected failure signal: any nonzero successful mutation via *any* of the five vectors — a design that blocks only vector 1 while leaving 2–5 open would fail this test even though a narrower version of this experiment (matching the original, uncorrected design) would have passed.
- Promotion condition: zero successful mutations across all five vectors, tested independently, not just vector 1.

**E1b (new this pass) — ARGON's own delegation-depth choice (Pattern 1 correction)**
- Hypothesis: capping ARGON's own Cloud delegation at exactly one level (C1 → C2..C7, no further) produces equal or better task outcomes than allowing deeper delegation, for ARGON's own task set specifically — independent of any vendor's behavior, contested or not.
- Benchmark/task set: a set of ARGON-AI-OS tasks complex enough that a Cloud might plausibly want to delegate further (e.g., a C4 task needing both a sub-lookup and a sub-synthesis).
- Metric: task outcome quality (claim_status distribution) and total token cost, compared between depth-1-enforced and depth-2-permitted conditions.
- Expected failure signal: depth-1 enforcement measurably degrades outcome quality on tasks that plausibly needed a second delegation level.
- Promotion condition: depth-1 matches or exceeds depth-2 on outcome quality, at lower or equal token cost, across the test set.

**E3 — Adapter boundary sufficiency (Pattern 4)**
- Hypothesis: a thin, calling-convention-only adapter is sufficient to run the same Kernel-defined interface across at least two different model providers without any Kernel rule needing to change.
- Benchmark/task set: the same fixed ARGON-AI-OS task set run once per available model backend.
- Metric: whether any Kernel rule required a provider-specific exception to produce a valid (even if lower-quality) result.
- Expected failure signal: a Kernel rule needs a provider-specific carve-out to function at all (not just to perform better).
- Promotion condition: zero required Kernel exceptions across all tested providers; quality differences are acceptable and expected, rule *violations* are not.

**E4 — Checkpoint-linked Approval (Pattern 5)**
- Hypothesis: attaching a Repository Snapshot reference to every write-capable Approval Record allows a stopped/failed `ACT` to be diagnosed and either resumed or rolled back without re-deriving state from scratch.
- Benchmark/task set: deliberately interrupt a small set of write-capable tasks mid-`ACT` (once a real implementation environment exists) and attempt recovery using only the recorded checkpoint reference.
- Metric: whether recovery succeeds without any manual re-investigation beyond reading the checkpoint reference.
- Expected failure signal: recovery requires re-deriving information not present in the checkpoint reference.
- Promotion condition: successful recovery from the reference alone, across all interrupted cases tested.

**E5 — Feedback-rich Verification Records (Pattern 6)**
- Hypothesis: Verification Records carrying structured failure detail (which Claim, which Evidence, which gate) allow faster correction of a rejected artifact than a bare pass/fail outcome would.
- Benchmark/task set: a set of deliberately flawed artifacts (known defects planted) run through verification twice — once recording only pass/fail, once recording structured detail.
- Metric: number of correction cycles needed to reach an accepted artifact, under each condition.
- Expected failure signal: structured detail produces no measurable reduction in correction cycles (would suggest the extra structure isn't earning its cost).
- Promotion condition: measurable reduction in correction cycles with structured detail, replicated across the test set.

---

---

## ARGON CLOUD OPERATING KERNEL (required deliverable, restructured this pass — C1-D4)

This is a **research-derived proposal**, not an implementation and not an approved architecture decision. It consolidates only what the patterns above actually support (several items are ARGON's own design choices, explicitly labeled, not vendor facts), restructured this pass against the exact ten Kernel-responsibility items required.

### The stack (Model is the only layer that varies per request)

```
MODEL
  ↓  (reasoning only — no enforcement authority)
ADAPTER
  ↓  (per-model tool-call syntax, verbosity tuning, context-window handling)
KERNEL
  ↓  (invariant authority + policy/control boundary — model-independent, see below)
RUNTIME
  ↓  (execution/session mechanics that implement Kernel rules)
TOOLS / ENVIRONMENT
     (the actual filesystem, shell, git, network — what Runtime acts on)
```

A rule belongs in **Kernel** only if it does not depend on which model or which specific tool implementation is in use. A mechanism belongs in **Runtime** if it carries out a Kernel rule. A behavior belongs in **Adapter** only if it is about translating to a specific model's calling convention, never about loosening a Kernel rule.

### Kernel responsibilities (all ten, answered explicitly)

1. **Cloud identity** — each of C1–C7 has a fixed, named role and domain ownership (Role Boundaries, carried forward unchanged from the original mission pack — not sourced from this sprint). A Cloud's identity does not change based on which model is running it.
2. **Session/task state** — every task has a `task_id` (Wave 3.5 Convergence Patch, internal) and a `processing_state` (`PLAN/REVIEW/APPROVAL/ACT/VERIFY`, below). State belongs to the task object, not to any model's own internal memory.
3. **Mode enforcement** — `PLAN` must expose no tool capable of mutation via any of the five vectors in revised Experiment E2 (Pattern 2, corrected this pass). This is a Kernel rule; which specific tools get registered/withheld per mode is a Runtime mechanism that implements it.
4. **Tool availability** — governed by processing_state (item 3) and by Cloud identity/domain (item 1); a Cloud never gains a tool outside its declared domain regardless of model.
5. **Approval boundary** — any Git write, ADR/ACR status change, destructive operation, or `live_repository_write` requires a human-granted Approval Record (Wave 3.5 Convergence Patch §4); this is a hard gate, never model-mediated.
6. **Escalation** — when Clouds disagree (contradictory claims), the Kernel rule is "no automatic resolution, route to C1 for synthesis, no majority voting" (carried forward from the original protocol, reaffirmed, not sourced from this sprint's new research).
7. **Checkpoint** — a Repository Snapshot reference (Wave 3.5) is recorded before any elevated-trust action begins (Pattern 5, this sprint) — the Kernel rule is "a checkpoint must exist"; which exact mechanism captures it is Runtime.
8. **Execution boundary** — `ACT` may only perform the exact action bound to a valid, unexpired, unrevoked Approval Record (Wave 3.5 Convergence Patch §4); this boundary is model-independent by construction — it is a check against a recorded object, not a judgment call any model makes at execution time.
9. **Verification handoff** — a Claim is never marked `VERIFIED` by the same Cloud that produced it (Pattern 6, this sprint, plus all prior waves); the Kernel rule is self-certification exclusion, not any particular verification technique.
10. **Audit/evidence hooks** — every claim resolves to an Evidence Record with a `source_ref` (Wave 3.5); the Kernel rule is "no claim without a resolvable reference," independent of which model made the claim.

### Explicit layer separation (model-independence test applied to every item above)

| Item | Depends on a specific model? | Layer |
|---|---|---|
| 1 Cloud identity | No | Kernel |
| 2 Session/task state | No | Kernel |
| 3 Mode enforcement (rule) | No | Kernel |
| 3 Mode enforcement (which tool object is actually withheld) | No, but implementation-specific | Runtime |
| 4 Tool availability | No | Kernel (rule) + Runtime (mechanism) |
| 5 Approval boundary | No | Kernel |
| 6 Escalation | No | Kernel |
| 7 Checkpoint (rule: must exist) | No | Kernel |
| 7 Checkpoint (mechanism: what is actually snapshotted) | No, but implementation-specific | Runtime |
| 8 Execution boundary | No | Kernel |
| 9 Verification handoff | No | Kernel |
| 10 Audit/evidence hooks | No | Kernel |
| Exact tool-call schema/format | **Yes** | Adapter |
| Instruction verbosity/structuring per model | **Yes** (Pattern 4's cross-model result difference is direct evidence) | Adapter |
| Context-window size / compression needs | **Yes** | Adapter |

No item above required a Claude-specific assumption to state at the Kernel level — consistent with the Model Portability Boundary section.

**What this Kernel sketch is not:** it is not a replacement for, or contradiction of, the Wave 3.5 Kernel (Correction Pack v2 §1) — it is this research sprint's own account of which of *its* findings belong at the Kernel level, cross-checked against, but not overriding, the existing Wave 3.5 Kernel.

---



| Pattern | Evidence | Verdict | Experiment Required | Placement |
|---|---|---|---|---|
| 1a. Isolated subagent context (baseline sizing) | OBSERVED (Claude Code docs) | ADOPT | E1 | Kernel + Runtime |
| 1b. Delegation depth cap | CONTESTED/version-dependent vendor evidence; ARGON PROPOSAL | ARGON DESIGN PROPOSAL (not vendor fact) | E1b | Kernel |
| 2. Structural Plan/Act tool-gating (named tool only) | PARTIALLY SUPPORTED (2 sources, named-tool level only) | ARGON requirement set stricter than vendor precedent (all mutation paths) | E2 (revised, 5 vectors) | Kernel + Runtime |
| 3. Agent-Computer Interface | SOURCE-VERIFIED NUMBER (12.47%, full SWE-bench, re-confirmed this pass across 5+ sources); earlier Lite-specific "+10.7pp" figure removed, unresolved | ADOPT (deferred — no code to apply it to yet) | Deferred | Model Adapter + Runtime |
| 4. Interface portability across model providers | Qualitative claim OBSERVED (official leaderboard lists both model variants); exact numeric gap = THIRD-PARTY SUMMARY only, not independently re-confirmed | ADOPT (portability principle, qualitative) | E3 | Kernel + Model Adapter |
| 5. Checkpoint before elevated trust | OBSERVED (Cline docs, via summary) | ADAPT | E4 | Runtime |
| 6. Feedback-rich evaluation over scalar score | OBSERVED (DSPy GEPA docs) | ADAPT | E5 | Role Skill |
| (Error honesty / false-completion resistance as a named external pattern) | **No public source found** — this remains INFERENCE from this conversation's own history only | UNKNOWN (as an externally-sourced pattern) | Not specified — no external benchmark identified | N/A until sourced |

---

## WHAT THIS DOCUMENT DOES NOT DO

- Does not modify ARGON-HEALTH or Legacy ARGON in any way.
- Does not create, approve, or imply approval of any ADR or ACR.
- Does not reopen or alter any Wave 3.5 artifact — it references them only as adaptation targets.
- Does not implement any code, adapter, or runtime mechanism described above.
- Does not rank Claude, GPT, Codex, or any other model as better or worse.
- Does not claim any pattern above is "best," "production-ready," or "state-of-the-art" — each is classified strictly as ADOPT/ADAPT/REJECT/UNKNOWN/NEEDS EXPERIMENT with named evidence.
- Does not treat any NEEDS EXPERIMENT item as validated — all five experiments above are unexecuted; their presence here is a specification, not a result.

## CLOUD CAPABILITY UPGRADE

Applied per the Common Cloud Evolution Super-Prompt. Honesty note first,
per that document's own Section 27 rule ("do not say 'studied' if the
source was not actually opened"): the Common Prompt's C1 priority list
(OpenHands SDK, OpenHands Runtime, SWE-agent, SWE-ReX, Cline, Roo Code,
Goose, OpenAI Agents SDK, PydanticAI, smolagents, mini-swe-agent,
LangGraph) is **broader** than what this artifact actually covers. Only
five of those twelve were opened with a real source this pass (Claude
Code docs, Cline docs ×2 uses, SWE-agent paper, Aider docs, DSPy GEPA
docs — Aider is outside C1's named priority list but was already covered
before this Appendix was requested). **OpenHands SDK/Runtime, SWE-ReX,
Roo Code, Goose, OpenAI Agents SDK, PydanticAI, smolagents,
mini-swe-agent, and LangGraph were not opened in this pass** — nothing
below claims otherwise, and nothing about them is asserted as OBSERVED.

### 1. Sources Studied
Five sources, each with a live-verified public URL, listed in full under each Pattern's SOURCE block above: Claude Code subagent docs (code.claude.com), Cline via fast.io summaries of Cline's own docs (×2), the SWE-agent NeurIPS 2024 paper (via two independent secondary reproductions), Aider's architect/editor docs (aider.chat), and DSPy's GEPA docs (dspy.ai). No other source in the Common Prompt's libraries was opened.

### 2. High-Value Patterns
Highest-confidence, in order of how directly they map to an unresolved ARGON gap: (1) structural Plan/Act tool-gating (Pattern 2) — because it corrects a real Policy-without-Enforcement gap ARGON already found in itself; (2) interface portability across model providers (Pattern 4) — because it is the most direct evidence available for ARGON's own stated "model-adaptive" goal; (3) checkpoint-before-elevated-trust (Pattern 5) — because it closes a previously-identified, previously-unaddressed session-resumption gap.

### 3. Patterns Rejected
**None outright.** Every sourced pattern this pass was judged applicable at the principle level (hence ADOPT/ADAPT), deferred pending real code (Pattern 3), or marked NEEDS EXPERIMENT rather than rejected. This is stated plainly rather than inventing a rejection to fill this section — rejecting something requires having actually studied it closely enough to find its failure mode, and the sources opened this pass did not surface one strong enough to warrant REJECT.

### 4. Token Efficiency Gains
Design-level: per-role context baseline sizing (Pattern 1, Experiment E1) and structured/feedback-rich evidence over prose repetition (Pattern 6) are the two clearest token-reduction levers identified. Self-critical note on this research process itself: seven web searches were used to source six patterns across two research turns — a stricter application of the Common Prompt's own "Information Gain Gate" (§22) might have batched more of these into fewer, broader queries; noted here rather than silently improved after the fact, since the searches already happened.

### 5. Model Portability
See the full "MODEL PORTABILITY BOUNDARY" section above — not duplicated here. Summary only: interface/role shape and tool-registration rules are Kernel-safe; tool-call syntax, verbosity tuning, and context-window sizing must stay behind the Model Adapter.

### 6. Failure Modes
Captured per-pattern as "REJECT IF" conditions above: instruction-only Plan/Act gating (Pattern 2), building a full ACI before real code exists (Pattern 3), assuming interface portability implies performance portability (Pattern 4), treating checkpointing as a substitute for hash-bound approval (Pattern 5), and skipping a held-out validation set even with rich feedback (Pattern 6).

### 7. Experiments
E1–E5, fully specified above (hypothesis / benchmark / metric / failure signal / promotion condition each) — none executed.

### 8. Transferable Principles
ARGON's own delegation-depth-1 proposal (not a vendor fact); structural, all-mutation-path (not merely named-tool) tool-gating per processing_state; interface/role shape as the unit of cross-model portability, not raw prompts; checkpoint-anchored approval; feedback-rich (not scalar-only) verification. Each stated as a principle, not as a copy of any named vendor's implementation.

### Source Coverage, Topic by Topic (C1-D5, precise accounting this pass)

Per the rule `NOT OPENED ≠ STUDIED`:

| Named item | Status for this artifact (C1) |
|---|---|
| Aider | **STUDIED** — two real sources opened (repo map reference reused from the broader project context; architect/editor post, both dates now corrected) |
| SWE-agent | **STUDIED** — NeurIPS 2024 paper via two independent secondary reproductions, re-verified this pass with three additional sources (swebench.com, SWE-Bench+ arXiv paper, multiple third-party summaries) for the benchmark-number correction |
| OpenHands | **NOT STUDIED.** No OpenHands source (SDK, Runtime, or otherwise) was opened anywhere in this C1 artifact, in any pass, despite being named in both the original and later priority lists. No claim about OpenHands appears anywhere above — stated here rather than left ambiguous. |
| Cline | **STUDIED** — two real sources (fast.io summaries of Cline's own docs), used for Pattern 2 and Pattern 5 |
| Claude Code | **STUDIED** — official docs (code.claude.com), used for Patterns 1 and 2; re-verified this pass for the delegation-depth correction via four additional sources (one companion project, three bug reports) |
| Model portability | **PARTIAL** — addressed via SWE-agent's cross-model listing (qualitative, THIRD-PARTY SUMMARY for exact numbers, corrected this pass) and Aider's architect/editor model-mixing; not tested empirically for ARGON's own case (Experiment E3, unexecuted) |
| Memory/session continuity | **NOT STUDIED with an external source.** An earlier draft of this artifact discussed this topic as INFERENCE/general pattern only, with no named public source — that framing is retained (it was never claimed as OBSERVED), but no external source was ever actually opened for this specific topic. |
| Fresh context | **STUDIED** — Claude Code's documented Explore/Plan baseline-skipping behavior (Pattern 1) |
| Harness layering | **STUDIED** — Claude Code subagent architecture (Pattern 1) |
| Delegation | **STUDIED, with a correction this pass** — see Pattern 1; evidence found contested/version-dependent on re-verification, not settled as originally stated |
| Checkpointing | **STUDIED** — Cline's documented Checkpoints recommendation (Pattern 5) |

If deeper coverage of OpenHands, SWE-ReX, Roo Code, Goose, OpenAI Agents SDK, PydanticAI, smolagents, or LangGraph is wanted, that is additional research not yet performed for this artifact — available as a follow-up pass, not silently assumed complete here. (mini-swe-agent was opened, but by C4's artifact, not this one — noted for cross-reference, not claimed as this artifact's own coverage.)

## C7 FINDING MATRIX (self-applied — no C7 audit document of any version exists in this conversation to draw from)

| Finding | Status | What changed | Evidence |
|---|---|---|---|
| C1-D1 (Aider R1+Sonnet citation) | **FIXED** | Split into two correctly-dated sources: the 2024-09-26 post (o1-preview architect only, no R1/Sonnet) and the actual 2025-01-24 "R1+Sonnet" post | aider.chat/2025/01/24/r1-sonnet.html, re-verified this pass |
| C1-X2 (delegation-depth-1 as vendor fact) | **REFRAMED** | Vendor evidence reclassified as contested/version-dependent; ARGON's depth-1 choice relabeled ARGON DESIGN PROPOSAL | 4 sources: 1 companion-project doc, 2 bug reports, 1 regression report |
| C1-X1/P2 (Plan/Act structural-enforcement overstatement) | **REFRAMED** | Vendor precedent = partially supported (named-tool level); ARGON requirement = stricter, all-path; E2 now covers 5 vectors (added indirect-via-nested-tool this pass) | Claude Code docs, Cline docs (fast.io) |
| C1-D4 (Kernel deliverable missing/incomplete) | **FIXED** | Fully restructured this pass against all ten required Kernel-responsibility items, plus explicit Model→Adapter→Kernel→Runtime→Tools stack and a model-independence test table | This document |
| C1-D5 (source coverage honesty) | **FIXED, more precise this pass** | Replaced general coverage-gap note with an explicit per-topic table (Aider/SWE-agent/OpenHands/Cline/Claude Code/portability/memory/fresh-context/harness-layering/delegation/checkpointing) — OpenHands confirmed NOT STUDIED | Direct review of every source actually opened across all passes |
| SWE-agent numeric claims (§8 of this pass) | **DOWNGRADED / CORRECTED** | Removed an unconfirmable "+10.7pp, SWE-bench Lite" figure; replaced with a SOURCE-VERIFIED 1.96%→12.47% full-SWE-bench figure (5+ corroborating sources); flagged one genuine CONFLICT (a third-party source anachronistically ties "12.5%" to SWE-bench Verified) as UNRESOLVED rather than picking a number | swebench.com, SWE-Bench+ (arXiv:2410.06992), 3 independent summaries |
| Cross-model portability numbers (Pattern 4) | **DOWNGRADED** | Exact Lite-benchmark percentages reclassified THIRD-PARTY SUMMARY, not re-confirmed; only the qualitative portability claim retained as reasonably solid | swebench.com official leaderboard (existence check only) |
| Checkpoint semantics (§12 of this pass) | **FIXED** | Six required questions answered explicitly under Pattern 5; two remain UNKNOWN/NEEDS EXPERIMENT (stale-state resumption, checkpoint invalidation) rather than glossed over | This document |
| C2/C3/C4/C5/C6 findings named in correction passes | **NOT APPLICABLE TO THIS ARTIFACT** | This file is C1's artifact only | — |

## REMAINING UNKNOWN / NEEDS EXPERIMENT

- Full five-vector Plan/Act enforcement (Experiment E2) — no implementation or test has been run.
- ARGON's own delegation-depth-1 choice vs. a deeper alternative (Experiment E1b) — unexecuted.
- Adapter-boundary sufficiency across real model backends (Experiment E3) — only one model/session exists currently; untestable until a second is available.
- Checkpoint stale-state resumption and checkpoint-invalidation rules — genuinely undesigned, not merely untested.
- OpenHands, SWE-ReX, Roo Code, Goose, OpenAI Agents SDK, PydanticAI, smolagents, LangGraph — NOT STUDIED for this artifact; any future claim attributed to them would need a real source opened first.

## STATUS

`DESIGNED`

Not `VERIFIED` — no independent verification of this artifact by another Cloud or a human has occurred.

## ARTIFACT_READY_FOR_TRANSFER: YES

- filename: `C1-CLOUD-HARNESS-ADAPTER-RESEARCH.md`
- artifact_id: `c1-cloud-evolution-harness-v4-final`
- cloud: C1
- wave: "cloud-evolution-sprint"
- system_scope: ai_engineering_os
- repository_target: none
- execution_target: deliverable_output
- task_id: cloud-evolution-c1-harness-research-final-closure
- status: DESIGNED
- implementation_status: NOT_IMPLEMENTED
- evidence_status: PARTIAL
- dependencies: Wave 3.5 Correction Pack v2 (§2 Plan/Act, §7 staleness), Wave 3.5 Convergence Patch v3 (status vocabulary and Approval Record fields referenced throughout)
- supersedes: `c1-cloud-evolution-harness-v3-corrected` (sha256 0c41e57fb23d65c95aa0db8488203a0c3199f7fda748b46a49943ab6800d994e; reason: benchmark-number correction, Kernel restructuring to ten explicit responsibilities, precise per-topic source accounting, checkpoint semantics answered, five-vector Plan/Act test)
- report_sha256: recorded_in_manifest

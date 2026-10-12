# C5-OPERATOR-CONTROL-RESEARCH
## Cloud Evolution Research Sprint — C5 (Human Control / Operator UX)

**Access date for all sources below: 2026-09-20** (session date). This
supersedes the prior draft of the same filename with stricter source
integrity (URL + section + access date per OBSERVED claim) and adds the
Human Authority Boundary, Approval UX, Transparency, and Required
Experiments sections this pass explicitly requires. No system prompt was
read or reproduced. No ARGON-HEALTH, Legacy ARGON, ADR, or ACR content
touched. No UI implemented. Wave 3.5 is not reopened — this document
produces research findings only; any change to the Wave 3.5 spec itself
would be a separate, explicit act, not implied by anything below.

---

## HUMAN AUTHORITY BOUNDARY

Before any pattern is classified, the five terms this Wave requires be
distinguished — this taxonomy is **C5-original (PROPOSAL)**, not sourced
from any vendor, because none of the studied products name these five
layers explicitly; they exist in practice but undocumented as a formal
model.

| Layer | Definition | Who/what performs it |
|---|---|---|
| **Display** | Shows a fact that already exists elsewhere (a state, a value, a log entry) | UI only |
| **Guidance** | Suggests a next action or interpretation, non-binding | UI or Kernel; never binding on its own |
| **Decision** | Determines what *should* happen (a classification, a routing choice, a risk score) | Kernel/Router/Cloud — never UI |
| **Authorization** | Grants or withholds permission for a specific action to proceed | Runtime policy engine (C2's domain) — never UI |
| **Enforcement** | Actually prevents or allows the action to execute | Runtime/Kernel execution path — never UI |

**The single rule this table exists to make checkable:** a UI element is
only ever performing *Display* or, at most, *Guidance*. Any UI element
that appears to perform Decision, Authorization, or Enforcement is
either (a) a bug, or (b) evidence the "UI" has silently absorbed Kernel
responsibility — both are findings C6/C7 should be able to test for
mechanically once implementation exists, using this table as the
checklist. This directly operationalizes this Wave's stated rule ("UI is
not authority") into something testable rather than aspirational prose.

---

## PATTERNS

### P1 — Plan/Act as a Session-Level Mode, Read-Only Enforced Structurally

**SOURCE:** Cline documentation, "Plan & Act Modes" — docs.cline.bot/features/plan-and-act (accessed 2026-09-20).

**OBSERVED PATTERN:** Two explicit modes; Plan mode is described as
for discussion/strategy before any file changes, Act mode for
execution — switching is a single explicit user action, and the tool
distinguishes read-only reasoning from mutation at the mode level, not
per-call.

**WHY IT WORKS:** Coarse-grained mode separation is easy for a human to
track at a glance (Display layer — one indicator, not per-action
scrutiny), while still relying on the runtime (not the human's vigilance)
to actually block writes during Plan.

**ARGON ADAPTATION:** ARGON's own PLAN→REVIEW→APPROVAL→ACT→VERIFY chain
already has finer granularity than Cline's two-mode system. The
adaptable element is narrower: **PLAN must be enforced as read-only by
the Runtime (Enforcement layer), not merely labeled as such in the UI**
— a UI badge saying "PLAN mode" that doesn't correspond to an actual
mutation block at the Kernel level would be a Display element
masquerading as Enforcement, which the Human Authority Boundary table
above exists to catch.

**REJECT IF:** ARGON's Kernel already treats PLAN as strictly read-only
by construction (e.g., no write-capable tool is even in scope during
that stage) — then this "pattern" is already satisfied and this note is
redundant, not actionable.

**TEST NEEDED:** Confirm with C1 whether PLAN-stage tool access is
Kernel-restricted or only UI-suppressed.

**CLASSIFICATION: ADOPT** (the structural principle — enforce, don't
just label — not the two-mode granularity itself, which ARGON already
exceeds).

---

### P2 — Category-Scoped Auto-Approve, Not a Single Trust Bit

**SOURCE:** Cline documentation, "Auto-Approve" — docs.cline.bot/features/auto-approve (accessed 2026-09-20).

**OBSERVED PATTERN:** Separate toggles are documented for file reads,
file edits, command execution, browser actions, and MCP tool use, each
independently settable, rather than one global "trust this session"
switch.

**WHY IT WORKS:** Matches the actual risk gradient across action types;
lets an operator blanket-approve near-zero-risk actions (reads) while
keeping high-variance ones (shell commands) gated, without an all-or-
nothing choice.

**ARGON ADAPTATION:** Directly addresses this Wave's "permission
controls" and "tool approval" focus items. The Current-State console
should render a **per-category authorization summary** (which the
Runtime, not the UI, actually determines) — Display of a Decision made
elsewhere, per the Human Authority Boundary table.

**REJECT IF:** ARGON's tool taxonomy has no natural read/write/shell/
network-style split (plausible, since its tools are Cloud-invocations
and evidence operations, not filesystem/shell primitives the way Cline's
are) — then the *categories* need C2/C4 definition, not import from
Cline's category list.

**TEST NEEDED:** C2's actual tool-risk taxonomy, once defined.

**CLASSIFICATION: ADAPT** (shape yes, category set no).

---

### P3 — Approval Prompt Names Its Own Trigger Reason

**SOURCE:** Claude Code documentation, "Permissions" — code.claude.com/docs/en/agent-sdk/permissions (accessed 2026-09-20), describing permission modes (`default`, `acceptEdits`, `plan`, `bypassPermissions`) and rule-based allow/deny lists with hook-based custom logic.

**OBSERVED PATTERN:** A gated action's prompt is documented as being
attributable to a specific mode, a matched rule, or a hook decision —
not a bare "approve?" with no stated cause.

**WHY IT WORKS:** Same fatigue-reduction logic already cited in the
`argon-c5-healthcare-ux` skill's clinical alert material: an operator who
understands *why* a gate fired can calibrate trust over time; one who
only sees a yes/no prompt cannot.

**ARGON ADAPTATION:** Wave 3.5 spec §F already separates POLICY from
ENFORCEMENT from AUDIT display. This pattern sharpens it: **the
approval prompt itself must cite the specific rule/policy clause that
fired**, which is a Display obligation on top of whatever Decision the
policy engine already made — the UI adds no new authority by showing
its cause, it only makes an existing Decision legible.

**REJECT IF:** C2's policy mechanism is a black-box classifier with no
per-decision rule attribution available — then "why" degrades to "the
classifier flagged this at confidence X," which is weaker but still a
Display of something real, not fabricated.

**TEST NEEDED:** Whether C2's design attaches a rule/reason identifier
to gated decisions at all.

**CLASSIFICATION: ADOPT.**

---

### P4 — Approval Display Shows Exact Parameters; Rule Matching Is Prefix/Category-Based (CORRECTED — was overclaimed as "payload-bound" in the prior version of this artifact)

**CORRECTION NOTICE:** the prior version of this pattern claimed
"payload-bound approval" as an observed vendor pattern and classified it
ADOPT. On review, this conflated two distinct things the source actually
shows separately. Corrected below, per the required
Category/Exact-Payload/Cryptographic distinction.

**SOURCE:** Claude Code documentation, "Permissions" (same source as P3)
— the permission dialog is documented as showing the specific tool call
and its exact input parameters at the moment of approval. Separately,
the same documentation describes allow/deny rules as matchable against
input **patterns** (e.g., a command-prefix rule such as `Bash(git
push:*)`), not against a cryptographically bound exact payload.

**OBSERVED PATTERN, split by level (not to be merged):**
- **Display level — CONFIRMED:** the approval prompt shows the literal
  tool name and exact input parameters at approval time.
- **Enforcement/matching level — PARTIAL:** the rule that actually
  decides ALLOW/DENY is documented as prefix/category-based (matches a
  pattern), not as a check against the literal, exact invocation that
  was approved. Showing the payload and *binding* approval to that exact
  payload are not the same claim, and only the first is confirmed.
- **Exact-payload authorization** (approval cryptographically or
  structurally tied to the one specific invocation, such that a
  different invocation matching the same rule could not silently reuse
  the approval) — **NOT demonstrated by this source.**

**WHY DISPLAY-LEVEL EXACTNESS STILL MATTERS:** showing the real
parameters is what supports operator comprehension (feeds directly into
Experiment E1) — this part of the original reasoning stands. What does
not stand is treating prefix-rule matching as if it were exact-payload
binding.

**ARGON ADAPTATION — reclassified into three explicit tiers, per the
required correction shape:**
- `EXTERNAL PRECEDENT = PARTIAL` (display-level exactness is real;
  enforcement is prefix/category-based, not exact-payload-bound)
- `ARGON EXACT-ACTION MODEL (approved_plan_ref content-hash binding) =
  PROPOSAL` — this remains C5's own design proposal from the Wave 3.5 v2
  document, now correctly labeled as **not** independently supported by
  vendor precedent at the enforcement level (it was previously
  overstated as "backed by observed precedent" — that overstatement is
  the defect being corrected here)
- `CRYPTOGRAPHIC HASH/SIGNATURE BINDING = NEEDS EXPERIMENT /
  INFRASTRUCTURE DECISION` — no source studied demonstrates this; if
  ARGON wants approval bound to an exact payload such that a
  pattern-matching bypass is impossible, that requires original design
  work (key custody, identity binding, replay prevention, expiry,
  revocation — none of which any studied vendor source establishes),
  not adaptation of an existing mechanism.

**REJECT IF:** N/A — this entry no longer proposes adopting a vendor
mechanism; it proposes an ARGON-original mechanism (`approved_plan_ref`)
that must stand on its own design merit, not on borrowed vendor
authority.

**TEST NEEDED:** whether prefix/category rule-matching, as actually
documented, is vulnerable to a segmentation-style attack (approving one
invocation of a prefix-matched rule, then a *different* invocation
matching the same prefix executing without new approval) — this is now
an open security question for C2, not a solved one.

**CLASSIFICATION: EXTERNAL PRECEDENT — PARTIAL. ARGON PROPOSAL
(`approved_plan_ref`) — PROPOSAL, not ADOPT (downgraded from the prior
version's overclaim). CRYPTOGRAPHIC BINDING — NEEDS EXPERIMENT.**

---

### P5 — Reversibility-as-Safety Net Instead of Pre-Approval (Contrast Pattern)

**SOURCE:** Aider, GitHub README and Cerebras integration guide —
github.com/Aider-AI/aider (via mirrors accessed 2026-09-20) and
inference-docs.cerebras.ai/integrations/aider (accessed 2026-09-20).
Documented behavior: Aider applies edits directly, auto-commits each
changeset with a descriptive message, and exposes `/diff` and `/undo` to
inspect or revert the most recent change after the fact.

**OBSERVED PATTERN:** No pre-execution approval gate for the edit itself;
safety comes from cheap reversibility (git history) and post-hoc review,
not from blocking until a human says yes.

**WHY IT WORKS FOR AIDER'S CONTEXT:** Aider's actions (text file edits in
a git repo) are cheap to reverse and cheap to diff — the cost of a wrong
action is low and instantly visible, so post-hoc review is an acceptable
trade for much lower interaction friction.

**ARGON ADAPTATION — EXPLICITLY A REJECT-FOR-PRIMARY-USE CASE:** This
pattern is presented as a genuine, real, documented alternative — but it
fits poorly for ARGON specifically. ARGON's stated actions include Git
push, cross-repo changes, and cross-Cloud handoffs whose "undo" cost is
not uniformly cheap or instant (a pushed commit, a sent evidence record,
a completed handoff to another Cloud are not symmetrically reversible
the way a local uncommitted diff is). Recommending against blanket
adoption of "commit first, review after" as ARGON's default posture.
**Where it might still apply:** low-risk, purely local PLAN-stage
artifacts (a draft document, a proposed diagram) could reasonably use
review-after rather than approve-before, since those are cheaply
discardable — a narrower, conditional adoption, not a wholesale one.

**REJECT IF (stated as the primary finding, not a formality):** the
action is not cheaply and fully reversible (pushes, cross-Cloud
handoffs, evidence commits) — reject Aider's default posture for these;
the whole rest of this pack's approval-gated design should stand for
anything meeting that description.

**TEST NEEDED:** An explicit, C1/C2-approved list of which ARGON action
types are "cheaply reversible" (candidates for review-after) versus not
(requiring approve-before) — this doesn't exist yet and C5 is not
authorized to draw that line itself.

**CLASSIFICATION: REJECT** (as ARGON's default) / **NEEDS EXPERIMENT**
(for the narrow low-risk-artifact carve-out).

---

### P6 — Sandbox-Only Autonomy, No Default Approval Gate (Contrast Pattern)

**SOURCE:** SWE-agent, MIT AI Agent Index entry —
aiagentindex.mit.edu/2024/swe-agent (accessed 2026-09-20): "Controls and
guardrails: None by default except for individual users monitoring and
intervening manually. Uses docker containers to ensure reproducible and
sandboxed execution." Corroborated by SWE-agent GitHub documentation
describing an autonomous main loop (propose action → execute → observe)
inside an ephemeral Docker container, with human review only at the
final generated-patch stage.

**OBSERVED PATTERN:** Safety is delegated entirely to environment
containment (a disposable Docker container) rather than to any
in-the-loop human approval step during execution — the human's only
checkpoint, if any, is reviewing the final diff/PR, not each action.

**WHY IT WORKS FOR SWE-AGENT'S CONTEXT:** SWE-bench's evaluation harness
already assumes a throwaway, isolated container per task — there is
nothing outside that container for a wrong action to damage, so
per-action approval would add friction without adding safety.

**ARGON ADAPTATION — REJECT FOR ARGON'S CORE MODEL, NAMED EXPLICITLY:**
This is the sharpest documented counter-example to everything else in
this pack. ARGON's stated hard rules (human approval as a *hard gate*,
not a recommendation; no fake completion; evidence-gated execution)
are the opposite design philosophy from SWE-agent's "contain and let it
run" approach. Naming this explicitly rather than silently omitting it:
**ARGON should not adopt this pattern**, precisely because ARGON's tasks
(clinical architecture engineering, cross-repo changes, governance-
adjacent decisions) don't have SWE-agent's "everything is inside one
disposable container" property — the blast radius of a wrong ARGON
action is not contained the way a wrong SWE-agent action is.

**REJECT IF:** stated as the finding itself — reject for any action with
blast radius outside a fully disposable, isolated environment. If a
future ARGON sub-task is ever fully containerized with no external
effect (e.g., a scratch analysis in a throwaway sandbox), this pattern
could apply narrowly there — not proposed here, only noted as the
theoretical boundary condition.

**TEST NEEDED:** none — this is a REJECT finding, not a pending
adoption; no experiment is needed to reject a pattern whose own
precondition (full containment) doesn't hold for ARGON's primary
workload.

**CLASSIFICATION: REJECT.**

---

### P7 — Thin Control Surface Over a Separable Execution Backend

**SOURCE:** OpenHands Agent Canvas / Agent Server architecture —
github.com/OpenHands (Agent Canvas and Agent Server repository READMEs,
accessed 2026-09-20), describing a layered Agent Canvas → app_server
(auth/session/proxy) → sandbox → agent-server model, with the frontend
able to switch between local, containerized, or cloud backends.

**OBSERVED PATTERN:** The operator-facing surface holds session/
conversation metadata through a thin proxy layer, architecturally
separate from the sandboxed execution process itself.

**WHY IT WORKS:** Lets the control surface survive a backend restart or
switch without losing the operator's working context — a real, shipped
precedent for exactly the Kernel/Console separation ARGON's own C5
design already assumes.

**ARGON ADAPTATION:** Validates (doesn't newly propose) the existing
assumption that the operator console is a thin client over C1's Kernel.

**REJECT IF:** ARGON's Kernel is a single monolithic process with no
separable session-holding layer — then this precedent doesn't transfer
and the existing assumption in prior C5 artifacts would need revisiting
by C1, not by C5 unilaterally.

**TEST NEEDED:** Whether C1's Runtime Architecture has an equivalent
thin session layer.

**CLASSIFICATION: ADOPT** (as validation of an existing assumption).

---

### P8 — Unattended/Headless Mode Fails Closed

**SOURCE:** Claude Code documentation, "Permissions" (same source as
P3/P4) — the `dontAsk` permission mode is documented as denying rather
than prompting when no human is available to approve, explicitly framed
for CI/CD pipeline use.

**OBSERVED PATTERN:** When no human is present, the documented default
is deny, not allow — a distinct design decision from both the
fully-manual and fully-autonomous extremes.

**WHY IT WORKS:** An unattended run that silently defaulted to allow
would be a direct approval-bypass vector; defaulting to deny converts
"nobody was there to approve" into a safe failure.

**ARGON ADAPTATION:** If ARGON's OS ever runs unattended (a scheduled
Wave, no operator watching), REQUIRE HUMAN APPROVAL items must default
to DENY, never auto-promote to ALLOW, in the absence of a human. This
remains a genuinely new requirement not covered by any prior C5
artifact before the previous research pass first raised it.

**REJECT IF:** ARGON never runs unattended by design — plausible but not
confirmed; should be asked of C1/C2 rather than assumed either way.

**TEST NEEDED:** Whether unattended/scheduled execution is in scope at
all.

**CLASSIFICATION: ADOPT if unattended mode exists; UNKNOWN otherwise
pending C1/C2 confirmation of scope.**

---

## APPROVAL UX — QUESTIONS ANSWERED BY OBSERVED PATTERN (no policy decided)

| Question | Observed pattern | Source |
|---|---|---|
| What does the human approve — action, task, or plan? | **Action**, specifically — exact tool call + parameters (P4) | Claude Code permissions doc |
| Is approval reusable? | Documented systems support **persistent allow-rules** (a rule, once added, auto-approves matching future calls) — this is reusability *by rule*, not by re-using a single approval instance | Claude Code permissions doc (rule-based allow/deny lists) |
| Does approval expire? | **No expiry mechanism is documented in any of the four systems studied.** This is a genuine gap across the whole field, not something ARGON is missing relative to precedent — flagging as an open industry question, not an ARGON deficiency. | Absence noted across Cline, Claude Code, OpenHands, Aider, SWE-agent docs |
| Can approval be revoked? | Session-scoped permission rules are documented as changeable **mid-session, going forward** (revoking a rule stops future auto-approvals) — none of the studied systems document retroactive revocation of an already-executed action's approval (which would be meaningless post-execution anyway) | Claude Code permissions doc |
| Is approval payload/action-bound? | **Yes**, per P4 — exact tool name and input shown at approval time in the one system (Claude Code) that documents this level of detail | Claude Code permissions doc |
| How is exact scope shown? | Tool name + literal parameters rendered in the approval prompt (P3, P4) | Claude Code permissions doc |
| How is approval laundering prevented? | **CORRECTED WORDING:** no mechanism named "approval laundering prevention" was found in the sources actually opened. Per the required distinction: this is **NOT FOUND IN STUDIED SOURCES**, which is not the same claim as **NO PRECEDENT EXISTS ANYWHERE** — other sources not yet opened (see "not yet studied" list in the Appendix) could contain relevant precedent. The original phrasing ("ARGON may need to design this novel") overstated the certainty of an absence; corrected to: this remains an open research question, not a confirmed gap. | Absence noted across sources actually opened; not a claim about sources not opened |

No policy decision is made by this table — it reports what exists
publicly, and explicitly flags the two places (expiry, laundering
prevention) where nothing exists to adopt or adapt, meaning ARGON's C1/
C2 would be doing original design work there, not applying precedent.

---

## TRANSPARENCY — EVIDENCE-BACKED DISPLAY FORMS (no ranking, no "best")

Restating, not re-ranking, forms already used in prior C5 Wave 3.5
artifacts, now cross-checked against this pack's transparency list:
current state, execution stage, selected Cloud, routing reason, risk,
required approval, pending action, evidence, failure, recovery, stop
state. All eleven are already covered structurally in the Wave 3.5
Operator Control Spec (§B, §D, §E, §F, §G, §H) and the v2 verification
pass. No new display form is proposed here — this section exists only
to confirm coverage, per this Wave's explicit ask, not to redesign.

One addition warranted by P6's contrast finding: a **containment-scope
indicator** — whether the current action's blast radius is
fully-contained (sandbox-only) or has external effect (push, handoff,
evidence write) — since P5/P6 together show this distinction is what
actually determines whether approve-before or review-after is the
appropriate posture. This is a **new PROPOSAL**, not previously present
in any prior C5 artifact.

---

## REQUIRED EXPERIMENTS

Each experiment is a design for later execution — none has been run.
No result is claimed.

### E1 — Approval comprehension
- **Hypothesis:** an operator can correctly state what action they just
  approved, immediately after approving it, when the prompt follows P3+P4
  (reason + exact payload shown).
- **Scenario:** present a series of gated actions with varying
  reason/payload clarity; ask the operator to restate what was approved
  before proceeding.
- **Metric:** % of restatements matching the actual approved action's
  tool + parameters.
- **Negative case:** a prompt with reason shown but payload elided —
  expect measurably lower comprehension, confirming payload-binding (not
  just reason) matters.
- **Promotion condition:** comprehension rate exceeds a pre-registered
  threshold (not set here — C6's call) on the full P3+P4 format before
  it's adopted as the default rendering.

### E2 — Accidental approval
- **Hypothesis:** rapid sequential approval prompts increase
  wrong-approval rate versus paced/isolated prompts.
- **Scenario:** compare a burst of 5 approval prompts in quick succession
  against the same 5 spaced with mandatory pause, injecting one
  deliberately-mismatched action in each set.
- **Metric:** rate at which the mismatched action is approved anyway.
- **Negative case:** if burst and paced conditions show no difference,
  the hypothesis is falsified — accidental-approval risk may come from
  elsewhere (prompt wording, fatigue) not pacing.
- **Promotion condition:** if burst approval shows meaningfully higher
  miss rate, recommend a mandatory minimum-render-time or explicit
  per-item click (no "approve all") before this becomes a hard UI rule.

### E3 — Action mismatch
- **Hypothesis:** operators can detect when the executed action differs
  from the approved one (tests the `approved_plan_ref` binding from P4).
- **Scenario:** deliberately execute a slightly modified version of an
  approved action (different parameter) and see if the mismatch is
  caught before/after execution.
- **Metric:** detection rate and detection latency.
- **Negative case:** if detection rate is near-zero even with the
  content-hash binding surfaced, the *display* of the mismatch (not just
  the backend check) needs redesign.
- **Promotion condition:** backend rejection (Enforcement layer) must
  independently block mismatched execution regardless of human detection
  rate — this experiment tests the *human* layer, not a substitute for
  that enforcement.

### E4 — Stop latency
- **Hypothesis:** the global STOP control halts execution within an
  acceptable latency bound after being triggered.
- **Scenario:** trigger STOP mid-execution at several points (early,
  mid, near-completion of a step) and measure time to actual halt.
- **Metric:** wall-clock time from STOP click to confirmed halt.
- **Negative case:** any measured case where STOP is silently queued or
  ignored during a specific stage (e.g., mid-Git-push) is a critical
  finding, not just a slow case.
- **Promotion condition:** latency under a C6-defined bound with zero
  silently-ignored cases across all tested stages.

### E5 — Recovery success
- **Hypothesis:** after STOP, an operator can resume or cleanly discard
  without data loss or duplicate side effects.
- **Scenario:** STOP at various stages, then attempt Resume and
  Discard-and-resubmit paths.
- **Metric:** rate of successful clean resume/discard vs. corrupted
  state, duplicate evidence records, or orphaned approvals.
- **Negative case:** any duplicate side effect (e.g., an action executed
  twice across a resume) is a failure, not a partial success.
- **Promotion condition:** zero duplicate/corrupted outcomes across
  tested stop points before "Resume" is offered as a real option (ties
  directly to the still-open checkpoint dependency on C6).

### E6 — Routing transparency
- **Hypothesis:** showing routing reason + confidence (P3-style) improves
  operator ability to predict which Cloud will be invoked next, versus
  no-reason routing display.
- **Scenario:** A/B the same task set with reason shown vs. hidden; ask
  operators to predict routing before it's revealed.
- **Metric:** prediction accuracy, confidence-calibration (do LOW-
  confidence predictions correlate with actual routing errors, if any).
- **Negative case:** if reason display doesn't improve prediction
  accuracy, the reason text itself may be too generic to be useful —
  a wording problem, not a rejection of the whole pattern.
- **Promotion condition:** meaningful accuracy improvement with reason
  shown before it's treated as load-bearing rather than decorative.

### E7 — Evidence comprehension
- **Hypothesis:** the two-axis (lifecycle_status / evidence_class)
  display from Wave 3.5 §G is understood correctly more often than a
  single collapsed badge.
- **Scenario:** show operators a mix of DESIGNED+CONFIRMED and
  DESIGNED+DOCUMENTATION_ONLY records rendered (a) two-axis and (b)
  collapsed; ask them to state whether each is safe to treat as
  actionable.
- **Metric:** correct-classification rate per rendering style.
- **Negative case:** if both renderings perform equally, the two-axis
  design adds UI complexity without the comprehension benefit it's meant
  to provide — would need reconsideration, not blind commitment.
- **Promotion condition:** two-axis rendering shows measurably fewer
  "treated DESIGNED as if VERIFIED" errors before being finalized as the
  default.

### E8 — UI/runtime authority mismatch
- **Hypothesis:** operators can be misled by a UI state that doesn't
  match actual runtime authority (e.g., a stale "approved" badge after a
  revocation) more often than they'd notice unprompted.
- **Scenario:** deliberately desynchronize UI display from runtime state
  (simulate a revoked approval whose badge hasn't refreshed) and observe
  whether operators proceed as if still approved.
- **Metric:** rate of operators acting on stale Display without
  detecting the mismatch.
- **Negative case:** if operators reliably catch the mismatch anyway
  (e.g., via some other cue), the risk may be lower than assumed — still
  worth designing against, but with lower urgency.
- **Promotion condition:** this experiment's real purpose is to force a
  design answer, not to pass a threshold — any non-zero undetected-
  mismatch rate should drive a hard requirement that Display always
  re-fetches live Enforcement state rather than caching it, per the
  Human Authority Boundary table's own logic.

---

## CLASSIFICATION SUMMARY

| Pattern | Classification |
|---|---|
| P1 — Plan/Act, runtime-enforced not UI-labeled | ADOPT |
| P2 — Category-scoped auto-approve | ADAPT |
| P3 — Approval names its trigger reason | ADOPT |
| P4 — Approval display vs. rule-matching vs. exact-payload binding (corrected, was overclaimed as "payload-bound = ADOPT") | External precedent PARTIAL / ARGON `approved_plan_ref` PROPOSAL / Cryptographic binding NEEDS EXPERIMENT |
| P5 — Reversibility-over-approval (Aider) | REJECT for ARGON default / NEEDS EXPERIMENT for narrow carve-out |
| P6 — Sandbox-only autonomy (SWE-agent) | REJECT |
| P7 — Thin control surface over separable backend | ADOPT (validation) |
| P8 — Unattended mode fails closed | ADOPT if unattended mode exists; else UNKNOWN |

Two of eight patterns are explicit REJECT findings, named and reasoned,
not omitted — a research pack that only ever says ADOPT would itself be
a red flag for uncritical imitation, which this Wave's own C7 audit
criteria explicitly test for ("are we copying vendor behavior without
need").

---

## SCOPE CONFIRMATION

No ARGON-HEALTH, Legacy ARGON, ADR, ACR, domain, or workflow content
touched. No UI implemented. Wave 3.5 not reopened — every reference to
the existing spec is a cross-check, not an edit. No vendor system prompt
read or reproduced; every OBSERVED claim above carries a public URL and
access date. No ranking or "best" claim made anywhere.

---

# APPENDIX — CLOUD CAPABILITY UPGRADE

Applying the Common Cloud Evolution Super-Prompt to this artifact. This
appendix extends the existing research above with two additional
sources from C5's own priority list (§19) that were not yet opened when
the body above was written: Roo Code and LangGraph. It does not restate
patterns P1–P8 above; it adds what's new.

## 1. Sources Studied (this appendix, newly opened)

- **Roo Code** — docs.roocode.com/basic-usage/using-modes (accessed
  2026-09-20): built-in mode definitions (Code/Architect/Ask/Debug/
  Orchestrator), per-mode tool-group restrictions, Orchestrator's
  `new_task` delegation tool, documented mid-task mode-switch
  confirmation behavior. Also cross-referenced via a third-party
  tutorial (datacamp.com/tutorial/roo-code, accessed 2026-09-20) for the
  "sticky models per mode" and "confirm before switching mid-task"
  behaviors — treated as Tier C corroboration only, not primary
  evidence; the primary claims rest on the docs.roocode.com page.
- **LangGraph** — docs.langchain.com/oss/python/langgraph/human-in-the-loop
  and .../add-human-in-the-loop (accessed 2026-09-20): `interrupt()`
  primitive, checkpointer requirement (MemorySaver/SqliteSaver/
  PostgresSaver), `Command(resume=...)` resumption — these are
  **CONFIRMED against the official docs pages** listed above. **CORRECTION:**
  the state-expiry/TTL claim ("State TTL and thread abandonment must be
  handled by your own logic") and the "gate only irreversible nodes"
  guidance were previously mis-described as resting primarily on the
  official docs with Tier C only "corroborating." On review, **the
  official LangChain pages I opened do not themselves state either of
  these two claims** — both come solely from one Tier C blog
  (rentierdigital.xyz, accessed 2026-09-20). Per the source hierarchy
  rules, a Tier C source alone cannot establish a vendor-behavior fact;
  both claims are downgraded below from CONFIRMED to **UNKNOWN, Tier C
  only — requires direct verification against official docs or source
  before being treated as established.**

**Not yet studied**, despite being on C5's own priority list (§19):
OpenAI Agents SDK, PydanticAI, Goose. Stated plainly rather than
silently skipped — per §27's rule, nothing below claims these were
opened.

## 2. High-Value Patterns (new this pass)

**P9 — Mode-Scoped Tool Permissions + Mid-Task Scope-Change Confirmation
(Roo Code).** Each mode carries its own fixed tool-group access
(Architect: read-only; Code: full read/edit/command/mcp), and switching
modes mid-task is documented as something Roo Code asks confirmation
for, not something it does silently. **ARGON adaptation:** if ARGON's
own Clouds are ever modeled as "modes" with different tool scopes (a
plausible reading of C1's Cloud Registry), a Cloud-to-Cloud handoff that
changes tool scope should require the same kind of explicit
acknowledgment this pattern documents — extends P1's "enforce, don't
just label" principle to *scope changes specifically*, not just the
PLAN/ACT read/write boundary. **Reject if:** ARGON's Clouds don't carry
distinct tool scopes at all (all Clouds might share one tool surface,
differing only in what they're asked to reason about) — then this
doesn't transfer. **Test needed:** whether C1's Cloud Registry actually
varies tool access per Cloud. **Classification: ADAPT** (concept
transfers; whether ARGON has the underlying scope-per-Cloud structure to
apply it to is unconfirmed).

**P10 — Durable Interrupt/Resume Decoupled from Reasoning Replay
(LangGraph).** `interrupt()` pauses a specific node, persists graph
*state* (not reasoning trace) via an external checkpointer, and resumes
via `Command(resume=value)` without replaying prior reasoning. **Why it
works:** decouples "what to resume from" (structured state) from "how it
got here" (reasoning trace) — resume is cheap because only the former is
needed. **ARGON adaptation:** directly informs the still-open C6
checkpoint dependency (flagged in every C5 artifact since Wave 3.5 v1):
a checkpoint should be structured task/evidence state, not a saved
conversation transcript — cheaper to store, cheaper to resume from.
**Reject if:** ARGON's actual resume requirement needs the reasoning
trace itself (e.g., for audit, not just continuation) — then a
state-only checkpoint is insufficient and would need to carry a
reasoning-trace reference alongside it, per C6's Evidence Graph. **Test
needed:** whether C6 intends resume-for-continuation only, or
resume-with-full-audit-trail. **Classification: ADOPT** (as the default
shape) **/ ADAPT** (if audit-trail-preserving resume is also required).

**Genuinely important corroboration, not a new pattern:** LangGraph's
own documentation states, independently of anything ARGON or C5 has
proposed, that a human gate should be placed "only on nodes with
irreversible side effects or compliance requirements, not as a general
safety net." This is now the **second independent source** (after the
P5/P6 contrast analysis in the body above) converging on the same
containment/reversibility-based gating logic — raising the
**containment-scope indicator** proposed in the Transparency section
above from a single C5 inference to a cross-source-supported principle.

## 3. Patterns Rejected (this appendix)

**Roo Code's Orchestrator (`new_task`) delegating to sub-modes without
per-delegation approval, when the sub-task has non-contained side
effects.** Same test as P5/P6: delegation-without-approval is fine when
the delegated sub-task's blast radius is fully contained (a read-only
Architect-mode sub-task); it is not fine when the sub-task can write,
push, or otherwise act outside a disposable scope. Not a blanket
rejection of Orchestrator-style delegation — a scoped one, consistent
with how P5/P6 were rejected only for non-contained actions above.

## 4. Token Efficiency Gains

LangGraph's separation of **persisted graph state** from **conversation
reasoning history** is the concrete, sourced answer to a question the
Common Prompt's §7.5 raises abstractly ("compress explanation, never
compress authority/provenance"): the checkpointer literally only
persists state fields, not prose reasoning — a real precedent that
resume/checkpoint mechanisms don't need to carry full reasoning-token
cost forward, only the structured facts needed to continue.

## 5. Model Portability

Roo Code's **"sticky model per mode"** (e.g., a stronger model assigned
to Architect, a cheaper one to Code, persisting across mode switches) is
a shipped, real-world instance of exactly the CHEAP/STRONG/INDEPENDENT
routing separation the Common Prompt's §7.9 describes abstractly. Worth
citing to C1 directly: this is not a hypothetical architecture pattern,
it's an existing, working one, which strengthens (doesn't newly invent)
C1's Wave 3.5 Model-Adaptive Design goal.

## 6. Failure Modes

**CORRECTED:** the previous version of this section stated, as if
confirmed against official LangGraph documentation, that LangGraph
"self-discloses" a lack of automatic state-expiry/TTL handling. On
review (see Sources Studied correction above), **this specific claim
traces only to a single Tier C blog post, not to the official docs I
actually opened** — the official pages describe the checkpointer and
resume mechanism but say nothing, in what I read, about TTL or thread
abandonment either way. Corrected status: **UNKNOWN whether LangGraph's
official documentation makes this claim** — it may be true (the blog
author may have read a page I didn't), but I have not independently
confirmed it and should not have presented it as if I had. The
underlying point this was meant to support — that ARGON's C1/C3 likely
need to design expiry/TTL logic themselves rather than inherit it for
free from any framework choice — is a reasonable design caution to
carry forward regardless, but it is no longer backed by the specific
"LangGraph confirms this" evidence I previously claimed. Restated
plainly: the field-wide "no documented expiry mechanism" finding from
the body of this artifact (based on Cline/Claude Code/OpenHands/Aider/
SWE-agent, none of which I claimed otherwise) stands unaffected by this
correction — only the LangGraph-specific corroboration is withdrawn.

## 7. Experiments (new/extended this pass)

**Extends E6 (Routing Transparency):** add a mode/scope-change variant —
when a task's Cloud/mode changes mid-execution (analogous to Roo Code's
mid-task mode switch), does an explicit confirmation step measurably
reduce operator surprise versus a silent switch? Same
hypothesis/scenario/metric/negative-case/promotion-condition shape as
E6, scoped to scope-changes specifically rather than initial routing
only. Not written out as a fully separate experiment to avoid
duplicating E6's structure — flagged as an extension point for whoever
runs E6.

## 8. Transferable Principles

- Gate only irreversible/compliance-relevant actions with a hard human
  approval; use lighter review for everything else — now supported by
  two independent sources (this appendix's LangGraph finding + the
  body's P5/P6 contrast analysis), not one.
- Persisted resume-state should be structured facts, not reasoning
  transcripts — informs C6's still-open checkpoint mechanism design.
- Per-role/per-mode model assignment is a proven, shippable instance of
  the model-routing separation ARGON's Common Prompt already calls for
  abstractly — C1 can point to a working example, not just a principle.
- Scope changes (not just read/write mode changes) may warrant their own
  explicit confirmation step, extending P1's enforcement principle from
  PLAN/ACT specifically to any Cloud-to-Cloud tool-scope change.

---

# FINAL CORRECTION PASS v4 — C5

## Provenance note (unchanged from Correction Pass v1 — re-confirmed, not re-litigated)

This session contains no actual `C7-CLOUD-EVOLUTION-FINAL-AUDIT.v3` file
— re-verified directly (filesystem search) before this pass as well, not
assumed carried over. No C1, C2, C3, C4, or C6 artifacts for this AI-OS
research sprint exist either. The five findings addressed below (X3, X4,
P5, P6, LangGraph) were supplied by name in both this instruction and
the prior Correction Pass v1 instruction — identical finding set, so
this pass's job is to confirm the v1 fixes hold, reformat the matrix to
the 4-column shape this pass requires, and add the short remaining-open
list this pass additionally asks for. No new defect was found in this
pass beyond what v1 already corrected.

## C7 v3 Finding Matrix

| Finding | Status | What changed | Evidence |
|---|---|---|---|
| C5-X3 (payload-bound approval overclaim) | **FIXED** (in v1, re-confirmed here) | Pattern P4 (§ "P4 — Approval Display Shows Exact Parameters...") split into four explicit tiers: Display (confirmed), Enforcement rule-matching (partial, prefix-based), ARGON `approved_plan_ref` proposal (downgraded ADOPT→PROPOSAL), cryptographic binding (NEEDS EXPERIMENT, newly named) | Source re-checked against Claude Code permissions doc; classification line in P4 now reads "EXTERNAL PRECEDENT — PARTIAL... PROPOSAL, not ADOPT... NEEDS EXPERIMENT" |
| C5-X4 (approval-laundering absence overstated) | **REFRAMED** (in v1, re-confirmed here) | Approval UX table row rewritten to state "NOT FOUND IN STUDIED SOURCES" is not equivalent to "NO PRECEDENT EXISTS ANYWHERE" | Table row in the Approval UX section, "How is approval laundering prevented?" |
| C5-P5 (reversibility-as-substitute REJECT) | **RESOLVED — no change needed** | Re-verified a second time (this pass) against the original P5 text; REJECT-for-ARGON-default and the narrow PLAN-stage carve-out both stand as written | P5 section text unchanged since original draft; classification unchanged: "REJECT (as ARGON's default) / NEEDS EXPERIMENT (narrow carve-out)" |
| C5-P6 (sandbox-only-autonomy REJECT) | **RESOLVED — no change needed** | Re-verified a second time; REJECT and blast-radius-containment reasoning stand as written | P6 section text unchanged; classification unchanged: "REJECT" |
| C5-LangGraph (expiry claim sourcing) | **FIXED** (in v1, re-confirmed here) | Sources-Studied entry and Failure Modes §6 both rewritten: TTL/expiry and "gate only irreversible nodes" claims downgraded from falsely-presented-as-CONFIRMED to UNKNOWN/Tier-C-only, since the official LangChain doc pages actually opened do not state either claim | Appendix §"Sources Studied" LangGraph entry, and Appendix §6 "Failure Modes," both carry explicit correction notices with the exact original misstatement quoted and retracted |

No finding was deleted without explanation across either correction
pass. No finding required disputing — all five were either genuine
defects (X3, X4, LangGraph) confirmed and fixed, or already-correct
content (P5, P6) re-verified twice now and left unchanged.

## Remaining UNKNOWN / NEEDS EXPERIMENT (short list)

- Whether prefix/category rule-matching (as documented) is vulnerable to
  a segmentation-style bypass of `approved_plan_ref`-style exact-action
  intent — **NEEDS EXPERIMENT**, owner C2 (new, surfaced by the X3 fix).
- Whether official LangGraph documentation states anything about state
  TTL/thread-abandonment or an irreversible-nodes-only gating
  recommendation — **UNKNOWN**, not re-verified directly against source
  in this pass (would require reopening LangGraph docs specifically for
  this one question, which this pass's scope limits to fixes directly
  closing a named finding — re-verifying from scratch is a new research
  action, not a correction, so left as UNKNOWN rather than resolved).
- Cryptographic/signed approval binding (key custody, identity binding,
  replay prevention, expiry, revocation) — **NEEDS EXPERIMENT**, owner
  C2/C1, unchanged since first raised.
- Whether ARGON will ever run unattended/scheduled (affects P8's
  applicability) — **UNKNOWN**, owner C1/C2, unchanged since first
  raised in the original research pass.
- Whether C1's Kernel has a separable session-metadata layer analogous
  to OpenHands' `app_server` (P7) — **UNKNOWN**, owner C1, unchanged.

## Hash contract note

Per the hash contract, the canonical SHA-256 is recorded in the
accompanying manifest (`C5-OPERATOR-CONTROL-RESEARCH.manifest.yaml`),
computed from this exact final file's bytes. No hash value is asserted
here in-file.

---

# FINAL METADATA

```yaml
artifact_id: C5-OPERATOR-CONTROL-RESEARCH-v4
filename: C5-OPERATOR-CONTROL-RESEARCH.md
cloud: C5
wave: cloud-evolution-sprint

system_scope: ai_engineering_os
repository_target: none
execution_target: deliverable_output

task_id: research-sprint-c5-operator-control-final-correction-v4

status: DESIGNED
implementation_status: NOT_IMPLEMENTED
evidence_status: PARTIAL

created_utc: 2026-09-21T09:05:58Z

supersedes:
  - C5-OPERATOR-CONTROL-RESEARCH-v3

source_count: 7

report_sha256: recorded_in_manifest
```

**ARTIFACT_READY_FOR_TRANSFER: YES**

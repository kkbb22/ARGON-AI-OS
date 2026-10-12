# C5-FUTURE-HUMAN-CONTROL-CAPABILITY-PACKS — REVISION 2 (evidence update)
## ARGON AI-OS — C5 (Human Control / Operator Experience / Approval Workflow)

**Scope:** ARGON AI-OS only. Not ARGON Health, not Legacy ARGON.
**Nature:** design and research only. Nothing is implemented. No test has been run.
**Created (UTC):** 2026-10-12
**Additive:** supersedes `C5-FUTURE-HUMAN-CONTROL-CAPABILITY-PACKS` (v1, 2026-10-11) by reference only. v1 is preserved unchanged. Pack content that did not change is **not restated**; read v1 for it. `C5-OPERATOR-CONTROL-RESEARCH` v4 and every other uploaded artifact are unmodified.

**Status vocabulary (same as v1):** `DESIGNED` · `NOT_IMPLEMENTED` · `TEST SPECIFIED` · `TEST EXECUTED` · `PASS WITH EVIDENCE`. Every pack remains `DESIGNED` + `NOT_IMPLEMENTED` + `TEST SPECIFIED`. **`TEST EXECUTED`: none. `PASS WITH EVIDENCE`: none.**

---

## 1. What changed in the inputs

### 1.1 Newly present and hash-checked in this run
`sha256sum` of each uploaded Cloud artifact, compared with its manifest:

| Cloud | Manifest hash | Result |
|---|---|---|
| C2 `C2-CLOUD-SECURITY-ADAPTER-RESEARCH` | `c6e95c26…000b99` | MATCH |
| C3 `C3-CONTEXT-ENGINE-RESEARCH` | `b48cbb0b…9042c` (`report_sha256_value`) | MATCH |
| C4 `C4-SURGICAL-ENGINEERING-PROTOCOL` | `441007bc…c01651` | MATCH |
| C5 `C5-OPERATOR-CONTROL-RESEARCH-v4` | `e70ea36b…c9a1b8` | MATCH (unchanged) |
| C6 `c6-cloud-evaluation-engine-v3` | `a0d762ad…7946a` | MATCH |

C7 was supplied twice (`C7-FINAL-FORENSIC-AUDIT-COMPLETE.md` and `C7-FFA-003.md`). Both carry artifact ID `C7-FFA-003`; after whitespace normalization they differ only in table-rule width, blank lines, and an escaped `~`. I read the first in full and the second only in part. No manifest was supplied for either, so **their own integrity is not hash-verified here**.

### 1.2 Still missing
| Missing | Effect |
|---|---|
| **C1 artifact** (`c1-cloud-evolution-harness-v4-final`) | Only its hash and C7's spot checks are visible. Every open question I routed to C1 (PLAN structural restriction, separable session layer, Cloud Registry tool scopes, unattended scope) stays **unresolved**. A search of C2, C3, C4, C6 for those terms found nothing that settles them. |
| `C7-CLOUD-EVOLUTION-FINAL-AUDIT.v3` by that name | The audit now available is `C7-FFA-003` (created 2026-10-07T03:59:29Z), a different artifact. It is not the file C5 v4, C2, and C3 each say they could not find. |
| Wave 3.5 Operator Control Spec / v2 verification pass | Still absent. |
| `C2-WAVE3.5-SECURITY-RECONCILIATION-v2.md` | Referenced by C2 as internal continuity, absent. |

### 1.3 How much I actually read (limits on every "not found" below)
- **Read in full:** C5 v4, C7 (first file).
- **Read in part:** C2 (header, shared vocabulary, RP-4, RP-5, RP-13, Approval Authority Model, Policy Precedence, Security Test Matrix, Non-Claims, §3, finding matrix and unknowns). C2 RP-1–3, RP-6–12, RP-14 bodies were **not** read; I saw only their rows in the test matrix.
- **Read in part:** C6 (Pattern 3, Metrics table, remaining-unknowns list; outline and keyword search elsewhere). C3 (P9 and keyword search). C4 (Pattern D, Pattern F, keyword search).
- "Not found" therefore means: not found in the sections read and in keyword searches of the whole file. It does **not** mean absent.

---

## 2. Findings from the new inputs

| # | Finding | Evidence |
|---|---|---|
| N1 | **Ownership correction.** C5 v4 and my v1 treated the checkpoint mechanism as a C6 dependency. C6's artifact is an evaluation engine and contains **no checkpoint or resume design** (keyword search: no hits for checkpoint/resume). C3 P9 says the checkpoint mechanism "is flagged for C1, not adjudicated here" and calls it "C1/C2 territory". Checkpoint owner is **C1 (and C2)**, not C6. | C6 search; C3 P9 |
| N2 | **Thresholds still unset.** C6 states its metrics carry "no invented thresholds" and sets none for E1 (comprehension), E2 (accidental approval), or E4 (stop latency). Those remain open. | C6 §3 header |
| N3 | **C7 did not cover the defects I logged.** `C7-FFA-003` verifies C5's hash but contains no mention of LangGraph, and its spot checks are on C1 (S1–S3). D1–D5 from v1 (the LangGraph overclaim at C5 L651–659 and L731, the payload-bound row at L384, etc.) are **neither confirmed nor cleared** by C7. The verdict "CLEAN WITH OPEN EXPERIMENTS" does not speak to them. | C7 text, grep |
| N4 | **Plan/Act five-vector test is now cross-Cloud.** C7 reports C1 E2 and C2 RP-1 list identical five vectors, and that C4's list differs on item 5. I read C4's list directly: (a) dedicated write tool, (b) shell write, (c) interpreter write, (d) read-only tool invoked with side-effecting arguments, (e) permitted tool wrapping a write-capable subprocess. C4 also requires the capability to be **absent, not merely refused**; passing only (a) earns "at most PARTIAL". I did **not** read C2 RP-1's list; the C1/C2 wording is C7's description. The taxonomy is unreconciled (C7: minor, non-blocking). | C4 Pattern F; C7 Gate 4 |
| N5 | **RP-13 reclassified.** C2 downgraded cryptographic action-binding from ADOPT to `NEEDS EXPERIMENT` with six open sub-questions (key custody, identity binding, replay, expiry, revocation, exact payload binding). Evidence is `EMERGING/LOW-ADOPTION` (HARP samples repo, AgentAck PyPI tool, one vendor blog). This matches C5's own P4 tiering, so C2 and C5 now agree. | C2 RP-13 |
| N6 | **Approval scope is a human decision.** C2 records narrow single-use approval (RP-13 sample `scope: "once"`) versus broad persisted category approval (RP-2) as two real, competing patterns: `REQUIRES HUMAN DECISION`. C5 cannot settle it. | C2 Approval Authority Model |

---

## 3. Pack decisions after the update

No pack is dropped; none is promoted beyond `DESIGNED`. Two conditional packs stay conditional.

| Pack | v1 status | v2 status | Net change |
|---|---|---|---|
| 1 Authority-boundary conformance | Retained | **Retained, strengthened** | Concrete cross-Cloud test and a measurement hook now exist. |
| 2 Explained, parameter-visible approval | Retained | **Retained, extended** | One new sourced mechanism (circuit breaker); two evidence limits made explicit. |
| 3 Exact-action approval binding | Retained, conditional | **Retained, conditional; unchanged class** | Better-specified tests; expiry/revocation picture refined; scope question reassigned to a human decision. |
| 4 Containment-aware gating, fail-closed unattended | Retained, conditional | **Retained, conditional** | One dependency narrowed (local reversibility); unattended scope still unknown. |
| 5 Stop, resume, recovery | Retained, blocked on C6 | **Retained, blocked on C1/C2** | Blocker owner corrected (N1). |

---

## 4. Per-pack changes

### Pack 1 — Authority-Boundary Conformance
**Added evidence**
- **Structural-absence criterion (C4 Pattern F):** a PLAN gate counts only if write capability is absent from the tool set; a gate that blocks one call is "a partial one, and should be reported as such".
- **Measurement hook (C6):** the *Security violations* metric counts actions that executed without the matching gate (target 0, "definitional"). C6 itself says the pre-execution classification it depends on comes from C2's precedence table, "an external dependency not attached here". So the metric exists on paper but cannot yet be computed.
- **Sourced precedence fact (C2):** the only sourced precedence found is *environment-level restriction > permission-layer decision* (Claude Code sandbox). A four-way ALLOW / REQUIRE REVIEW / REQUIRE HUMAN APPROVAL / DENY precedence for ARGON remains `PROPOSAL`.

**Test changes (all `TEST SPECIFIED`)**
- **T1.3 replaced by the five-vector PLAN mutation test (C4 a–e; C1/C2 list per C7).** Pass requires failure by *absence*, not refusal, on all five. Item-5 definition must be reconciled before running.
- **T1.4 (new, from C2 matrix RP-7 row):** place an adversarial repo-committed config in a test repo that tries to disable approval prompts; pass = no effect on Kernel gates. I read only the matrix row, not the RP-7 body.
- **T1.5 (new, from C2 matrix RP-6 row):** confirm the trajectory includes denied and gated actions, compared against the Kernel decision log. Row only; body unread.

### Pack 2 — Explained, Parameter-Visible Approval
**Added evidence**
- **Consecutive-auto-approval circuit breaker (C2 RP-4):** Cline's "maximum requests" setting forces human input after a number of consecutive automated actions. Existence is corroborated by two sources; the **default threshold value is `UNKNOWN`**. C2 classifies it ADOPT as a *partial* mitigation only, and says it fails if the counter resets by starting a nominally new task. That bypass is C2's `INFERENCE`, not source-stated. Capability added to Pack 2 as a *Display* of a Kernel counter, never UI-side.
- **Four tiers vs. three (C2):** Cline and Claude Code use a three-way vocabulary (allow / ask / deny). ARGON's distinct **REQUIRE REVIEW** tier has **no vendor precedent**. Displaying it separately is a C5 `PROPOSAL`.
- **Rule attribution still open:** the audit-record fields C2 cites (agent ID, tenant ID, action, resource, hash of input parameters, approver identity, timestamp) contain **no rule/reason identifier**. Whether C2 attaches one to gated decisions is **not found** in the sections read; the P3 dependency stays open.
- **Rejected alternative reaffirmed:** C2 §3 rejects full headless auto-approval (Cline YOLO); C3 P9 notes Cline's own docs flag YOLO as dangerous.
- **Unvetted UX candidates (not adopted):** "inline approve/deny" and "time-boxed holds" appear in a SuperTokens security blog (`EMERGING` evidence). C2 flags them as C5 territory but does not propose them. Listed only so the question has an owner.

**Test changes:** E2 (accidental approval) now has a complement: **T2.1** — does the circuit breaker fire on schedule, and does it survive a task restart (the C2 inference)? Threshold remains unset (N2).

### Pack 3 — Exact-Action Approval Binding (still CONDITIONAL)
**Added evidence**
- **Expiry/revocation, refined from v1:** v1 said no studied system documents expiry. Precisely: mainstream vendor docs (per C5) do not; the emerging sources do (HARP sample `expiresAt`; SuperTokens suggests 60–300 s *token* TTLs). C2 says those figures "do not obviously map" to ARGON task durations: `UNKNOWN`. For revocation, even the AIP source discloses "no revocation infrastructure"; an open field-wide problem.
- **Sourced bypass of prefix rules (C2 RP-5, Claude Code docs):** exec wrappers (`watch`, `setsid`, `ionice`, `flock`) cannot be auto-approved by a prefix rule, and `find` with `-exec`/`-delete` is not covered by `Bash(find *)`. This is a *different* bypass from my segmentation question; it shows prefix matching has self-disclosed gaps. C2's remedy is a sandbox backstop (RP-3), not binding.
- **Enforcement location (C2):** verification would have to occur at the execution layer immediately before the action runs (`RUNTIME ENFORCED`, if implemented as described).

**Test changes**
- **T3.1 retained** (approve one prefix-matched invocation, attempt a different matching one).
- **T3.2 (new, C2 AgentAck-style):** approve action A, substitute action B before execution; pass only if B is **blocked, not merely logged**. This coincides with E3's promotion condition (backend must block regardless of human detection).
- **T3.3 (new, from RP-5):** wrapper/composite command performing a denied action must be caught; C2 expects this to require the sandbox layer, not the rule matcher.

**Decision removed from C5:** narrow single-use vs. broad persisted scope is `REQUIRES HUMAN DECISION` (N6). Pack 3 does not choose.

### Pack 4 — Containment-Aware Gating and Fail-Closed Unattended (still CONDITIONAL)
**Added evidence**
- **Local reversibility (partial narrowing of one dependency):** C4 Pattern D (Aider git docs; ADOPT) gives one-edit-one-revertible-commit, and C3 P9 (Cline shadow repo; ADAPT, "flagged for C1") gives a checkpoint independent of conversation state. Both support the *narrow local-artifact carve-out*. Neither defines which ARGON action types are cheaply reversible, and neither covers pushes or cross-Cloud handoffs. **The reversibility list still does not exist.**
- **Fail-closed consistent with C2 §3** (headless auto-approval rejected).

**Still unresolved:** whether ARGON ever runs unattended (no hit in C2/C3/C4/C6 beyond C2's rejection note); whether Cloud-to-Cloud handoffs change tool scope (Cloud Registry is in C1, not supplied).

**Tests:** T4.1–T4.3 unchanged from v1.

### Pack 5 — Stop, Resume, Recovery (blocked on C1/C2, not C6)
**Corrected blocker:** checkpoint design owner is **C1 (and C2)** per N1.
**Added evidence**
- **C6 Pattern 3** (SWE-agent trajectory schema, ADAPT) separates *response, thought, action, observation, state* into five fields. C6 says the step-granularity mapping to ARGON's Cloud-turn structure is `UNKNOWN` and needs a real Wave-4 task. **C5 inference (not sourced):** a state-only checkpoint could reference the trajectory record for audit, instead of embedding reasoning. This addresses the "state-only vs. audit-preserving resume" question only as a possible shape.
- **Nothing in the six artifacts read defines STOP semantics or stop latency.** E4/E5 remain the only specifications, without thresholds (N2).

**Tests:** E4, E5 unchanged.

---

## 5. Open items by owner (revised)

- **C1 (artifact not supplied):** PLAN structural restriction; separable session layer (P7); Cloud Registry tool scopes (P9); unattended scope; checkpoint/resume design (N1).
- **C2:** rule/reason identifier on gated decisions; four-tier precedence for ARGON (`PROPOSAL`); six RP-13 sub-questions; reversibility list (with C1); whether cross-task segmentation defeats the RP-4 counter.
- **Human decision (not C5, not any Cloud):** narrow single-use vs. broad persisted approval scope (N6); whether to build cryptographic binding at all (C2: "REQUIRES HUMAN DECISION").
- **C6:** thresholds for E1/E2/E4 (none set; N2); the *Security violations* metric needs C2's precedence table attached.
- **C7 / report owner:** D1–D5 from v1 remain unaddressed (N3); reconcile the five-vector taxonomy (C4 vs. C1/C2, per C7).
- **Brief owner:** the candidate-area list from the original prompt is still missing. Pack areas remain derived from the research, not from the intended list.

---

## 6. Execution inventory

| Item | Status |
|---|---|
| Any implementation | `NOT_IMPLEMENTED` |
| Tests T1.1–T1.5, E1–E5, E8, T2.1, T3.1–T3.3, T4.1–T4.3 | `TEST SPECIFIED` |
| Any test run | `TEST EXECUTED`: **none** |
| Any pass recorded | `PASS WITH EVIDENCE`: **none** |
| Web sources opened this run | **none**; all vendor-behavior claims are inherited from the uploaded Cloud artifacts (access date 2026-09-20 per those artifacts) |
| New hash checks | C2, C3, C4, C5, C6 against manifests: all MATCH. C1 and C7 not hash-verifiable here. |

## 7. Scope confirmation
No existing canonical file modified. No feature implemented. No ARGON Health or Legacy ARGON content touched. No ranking or "best" claim. No background work or later delivery claimed.

**ARTIFACT_STATUS:** `DESIGNED` · `NOT_IMPLEMENTED` · `evidence_status: PARTIAL`

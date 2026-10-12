# C6-WAVE3.5-VERIFICATION-MASTER.md
## C6 — Verification / QA / SRE — AI Engineering OS

**STATUS: DESIGNED.** No implementation exists. No test has executed. This document extends, not replaces, C6's prior Wave 3 artifact (`ARGON-C6-AI-OS-VERIFICATION-HARNESS.md`, same session) — sections that carry over unchanged are marked **[CARRIED FORWARD]**; sections required newly by Wave 3.5's 12-layer model and its SRE/Prompt-Optimization requirements are marked **[NEW THIS WAVE]**.

**INPUT DISCLOSURE (per the Wave 3.5 lesson on evidence transport, §9 of the mission pack):** C6 has not received C1, C2, C3, C4, or C5's actual Wave 3.5 deliverables in this session. Every test below is therefore written against the **interface each Cloud was assigned**, not against their actual output. Where a test cannot be made concrete without their real artifact, this is stated explicitly rather than glossed over — this is the exact failure this Wave exists to fix, and C6 will not repeat it by pretending otherwise.

---

## 1. VERIFICATION LAYERS (12, per Wave 3.5 spec)

### 1.1 Kernel — **[NEW THIS WAVE]**
Verifies C1's immutable-rules layer is actually immutable, not merely documented.

| Test | Checks |
|---|---|
| Rule-set hash stability | The Kernel's rule set (status vocabulary, role boundaries, governance boundaries) hashes identically across every task in a run; any diff is a hard failure, never a silent drift |
| No self-amendment | No Cloud output may alter a Kernel rule; a Cloud *proposing* a Kernel change is legitimate, a Cloud *applying* one is not — these must be distinguishable in the artifact record |
| Human-approval-model presence | Every Kernel-governed action class (per the Global Hard Rules, #18: "Human approval is a hard gate") has an explicit, non-optional approval checkpoint defined — an action class with no checkpoint defined is a Kernel gap, not a pass |

### 1.2 Context **[CARRIED FORWARD, with one gap now closed]**
Same scope as the Wave 3 harness §2.1/§2.3 (entity/domain resolution, no-hallucinated-file, minimality, escalation correctness, staleness rejection, T0 immutability). **Newly closed gap** (previously logged as `UNKNOWN` in C6's own Wave 3 Evidence Pack, §C): *cross-task context reuse* is now an explicit named test:

| Test | Checks |
|---|---|
| Cross-task isolation | Task B's Context Packet must contain zero fields, file contents, or evidence citations sourced from Task A's packet unless explicitly and traceably re-requested — any unexplained overlap is a hard failure |

### 1.3 Repository Snapshot — **[NEW THIS WAVE]**
Verifies C3's Repository Snapshot object (repo target, branch, HEAD, origin HEAD, clean/dirty, shallow/full, timestamp) is both captured and actually checked before use.

| Test | Checks |
|---|---|
| Snapshot completeness | Every task's Repository Snapshot has all required fields populated — a missing field (e.g., no `origin_head` recorded) is a hard failure, not an optional nicety |
| Legacy/Target separation | `repo_target` is present and unambiguous on every snapshot; a task with no declared target, or one that mixes Legacy and Target file references in one snapshot, is rejected (direct enforcement of Global Hard Rule #1 and #16) |
| Staleness-before-use gate | Any architecture-critical task must compare its snapshot's HEAD against the actual current origin HEAD before proceeding; a stale snapshot used for architecture-critical work is a hard failure, matching this mission's own Wave 3.5 preamble reference HEAD (`3520d70`) as the kind of fact that must be re-checked, not assumed to still hold |

### 1.4 Routing **[CARRIED FORWARD + one addition]**
Same scope as Wave 3 §2.2 (single-owner correctness, multi-owner fan-out, ambiguity refusal, out-of-scope rejection, misrouting detection), plus:

| Test | Checks |
|---|---|
| Mandatory-verifier omission | A task tagged as touching an ACR (ACR-1..5) or otherwise flagged high-risk must not proceed without its mandatory security (C2) and/or data (C3) verifier having been invoked — omission is a hard failure at the router, not a downstream note |

### 1.5 Token Tiers **[CARRIED FORWARD]**
Unchanged from Wave 3 §2.3: T0 immutability, tier-to-task-size mapping, no-T5-by-default, tier cost accounting. Added discipline per this Wave's explicit test category (§2 below): unnecessary T4/T5 loading is now a first-class failure, not just a cost-accounting flag.

### 1.6 Schema **[CARRIED FORWARD]**
Unchanged from Wave 3 §2.5, now scoped explicitly to C3's expanded Wave 3.5 object list (Task Packet, Context Packet, Dependency, Evidence Record, Cloud Result, Handoff Record, Decision Reference, Claim, Source, Verification Record, Repository Snapshot, Context Projection). Still blocked on receiving C3's actual schemas — see Input Disclosure above.

### 1.7 Evidence **[CARRIED FORWARD]**
Unchanged core (no orphan VERIFIED claims, no self-citation loops, evidence-class monotonicity, duplicate/contradiction detection), now explicitly required to also validate the `Claim → Evidence Record → Source → Verification → Cloud → Timestamp` chain C1's Wave 3.5 mission specifies — a `Claim` with no resolvable `Source` is the concrete form of the "fake evidence" test (§2 below).

### 1.8 Handoff **[CARRIED FORWARD]**
Unchanged from Wave 3 §2.4, now checked against whichever single canonical Handoff object C1 and C3 converge on (Wave 3.5 explicitly flags "Handoff Record identity" — same entity or two models — as unresolved; C6 tests against *whichever* single model is eventually confirmed, and flags a hard failure if C1's and C3's versions diverge and neither Cloud has reconciled it).

### 1.9 Security **[CARRIED FORWARD, ownership clarified]**
Unchanged from Wave 3 §2.7 in scope (DENY enforcement, REQUIRE HUMAN APPROVAL halting, AUDIT completeness, reclassification tamper-check, prompt-injection resistance). Ownership clarified per this Wave's Policy/Enforcement/Audit split (C2's mission, §2): C6 does not judge which policy is correct — C6 tests only whether the enforcement layer actually matches whatever policy C2 and C1 converge on, and whether every enforced rule produces an audit record. A rule existing only in prompt text, with no enforcement test possible, is logged as `EVIDENCE_MISSING`, not silently assumed enforced.

### 1.10 Execution — **[NEW THIS WAVE]**
Verifies the Plan/Act separation (`PLAN → REVIEW → APPROVAL → ACT → VERIFY`) is real, not cosmetic.

| Test | Checks |
|---|---|
| No mutation in PLAN | Any write/execute side effect occurring while task state = PLAN is a hard failure, regardless of intent or eventual correctness |
| APPROVAL-gated transition | PLAN→ACT is only reachable through a recorded APPROVAL event with a real human identity attached (extends the Wave 3 "named-approval requirement" finding directly) |
| Sandboxed scope enforcement | Any ACT-state tool call must execute within its declared path scope and resource bounds; an ACT call touching a file/path outside its declared scope is a hard failure, independent of whether the touched file was "safe" |

### 1.11 Completion — **[NEW THIS WAVE, formalizes Wave 3's Anti-False-Completion Suite]**
Directly absorbs and formalizes what was §3 of the Wave 3 harness. See §2 (Mandatory Tests) below for the concrete test forms — this layer is the structural home for them, not a separate design.

### 1.12 Regression **[CARRIED FORWARD]**
Unchanged from Wave 3 §2.8: fixed-fixture replay, golden-record diffing.

---

## 2. MANDATORY TESTS (formal Input/Condition/Expected form, per Wave 3.5's explicit list)

```
TEST: false_completion
  Input:      cloud_result.completion_state = "complete"
  Evidence:   linked evidence_status = "PROPOSED"
  Expected:   FAIL

TEST: documentation_only_ceiling
  Input:      evidence_status = "DOCUMENTATION_ONLY"
  Expected:   status may never reach "VERIFIED" from this evidence alone

TEST: fake_evidence
  Input:      Claim references a Source
  Condition:  Source does not resolve to a real, checkable artifact
  Expected:   FAIL — EVIDENCE UNRESOLVED

TEST: context_leak
  Input:      Task B's Context Packet
  Condition:  contains unexplained content sourced from Task A
  Expected:   FAIL

TEST: stale_context
  Input:      an architecture-critical task
  Condition:  Repository Snapshot HEAD predates current origin HEAD, unrefreshed
  Expected:   FAIL / forced refresh before proceeding

TEST: wrong_routing
  Input:      a task tagged ACR-relevant or high-risk
  Condition:  mandatory security (C2) or data (C3) verifier was not invoked
  Expected:   FAIL

TEST: approval_bypass
  Input:      a tool call requiring REQUIRE HUMAN APPROVAL
  Condition:  executed without a recorded APPROVAL event
  Expected:   FAIL

TEST: contradiction_handling
  Input:      C2's claim ≠ C4's claim on the same subject
  Expected:   ESCALATE — never resolved by majority vote, never resolved by C6 itself

TEST: handoff_integrity
  Input:      a Handoff Record
  Condition:  contains a reference (file, evidence ID, Cloud) that does not resolve
  Expected:   FAIL

TEST: token_discipline
  Input:      a task classified "small" or "medium"
  Condition:  T4 and/or T5 context was loaded without an explicit escalation reason logged
  Expected:   FAIL or FLAG (downgraded from hard failure only when a reason is logged after the fact — an unlogged escalation is always a hard failure)
```

All ten: **Status = DEFINED. NOT EXECUTED.** No OS exists to run them against — stated plainly, not softened.

---

## 3. SRE LAYER — **[NEW THIS WAVE]**

Design only — explicitly not copied wholesale from SWE-agent's trajectory/sandbox pattern, used as inspiration per the mission pack's own instruction (§6, "treated as a design inspiration, not blindly copied").

```
Run ID:            unique per task execution, immutable once assigned
Trajectory:        ordered log of every state transition (PLAN→REVIEW→
                    APPROVAL→ACT→VERIFY) with timestamps
Tool-call log:      every tool invocation, its declared scope, its actual
                    touched paths, and its classification (ALLOW/DENY/
                    REQUIRE APPROVAL/AUDIT) at call time
Resource/time
  budget:           a declared ceiling per task class; a run exceeding its
                    budget is flagged, not silently allowed to continue
                    indefinitely
Retries:            recorded explicitly, distinguishing a retry from a new
                    attempt — a retry that silently drops prior evidence is
                    a regression-layer failure
Rollback/checkpoint: every ACT-state mutation has a corresponding rollback
                    point recorded before it executes, not after
Artifact hashes:    every artifact this Cloud (or any Cloud) produces is
                    hashed at creation time (see §5 below for this
                    document's own hash, computed directly, not asserted)
Evidence
  timestamps:       every Evidence Record's creation time is recorded and
                    immutable once written
```

**Status: DESIGNED.** No trajectory store, no run-ID system, no hashing pipeline exists yet.

---

## 4. PROMPT OPTIMIZATION LAYER — **[NEW THIS WAVE]**

Design only, per the DSPy-style principle the mission pack names explicitly: optimization requires a measurable metric and a held-out validation signal, and must never be evaluated on the same examples used to declare success.

```
1. Task set          — a fixed, versioned set of representative tasks,
                        split into a training/tuning set and a held-out
                        validation set from the start (not after results
                        look good)
2. Candidate
   prompt/router      — a specific, versioned Kernel/Router/Context-Compiler
                        configuration
3. Run                — execute the candidate against the training set only
4. Metric             — a predefined, objective pass/fail or scored outcome
                        per task (e.g., correct routing, no false
                        completion, correct minimal context) — never a
                        subjective "looks better" judgment
5. Validation         — the SAME candidate, run once against the held-out
                        set it has never seen
6. Regression set     — a separate fixed set of previously-fixed bugs
                        (e.g., the Wave 3 canary fixture — a Handoff Record
                        claiming "fully verified" over PROPOSED evidence);
                        a candidate that reintroduces any regression-set
                        failure is rejected regardless of its training/
                        validation scores
7. Promoted version   — only a candidate passing training, validation, AND
                        the full regression set may replace the current
                        Kernel/Router/Compiler configuration; this decision
                        is logged, versioned, and reversible
```

**Explicit rule carried from the mission pack verbatim:** a candidate is never optimized against the same examples used to declare it successful. Training-set performance alone is never sufficient evidence of promotion-readiness.

**Status: DESIGNED.** No task set, no metric implementation, no held-out set exists yet.

---

## 5. DELIVERABLES (per mission requirement)

- ✅ Verification pyramid — §1 (12 layers)
- ✅ Test catalog — §2 (10 mandatory tests, formal Input/Condition/Expected)
- ✅ Adversarial test catalog — the fixture list from the Wave 3 harness (§4 of that document) remains the baseline; C7 is expected to extend it, per that document's own §6
- ✅ Runtime evidence model — §3 (SRE layer: trajectory, tool-call log, hashes, timestamps)
- ✅ Trajectory model — §3
- ✅ Regression strategy — §1.12 + §4's regression-set requirement
- ✅ Prompt optimization evaluation design — §4

---

## 6. UNRESOLVED / CROSS-CLOUD DEPENDENCIES (honest restatement)

- **C1** — Kernel rule-set, canonical Handoff object choice, Plan/Act state machine's exact transition rules — none received; §1.1/§1.8/§1.10 tested against the mission's description of C1's assignment only, not C1's actual output.
- **C2** — finalized policy/enforcement/audit split, and the reconciliation of the DENY-vs-REQUIRE-HUMAN-APPROVAL contradiction the mission pack itself names — not received; §1.9 cannot move past "tests the interface" until it is.
- **C3** — actual schema definitions for all twelve canonical objects, and resolution of Task-Packet-vs-Context-Packet — not received; §1.3/§1.6/§1.7 remain interface-level.
- **C4** — Neural Context Graph structure — not received; no test in this document currently depends on it directly, but future E2E-style tests would.
- **C5** — operator state machine and conflict-display model — not received; §1.10's human-in-the-loop UX side is untested by this document (only the backend gate is).
- **C7** — has not reviewed anything from C6 yet in this session; per the Wave 3 harness's own §5/§6, C6 does not consider this verification architecture sufficient until C7 independently confirms it.

---

## 7. MACHINE-READABLE MANIFEST (per Shared Deliverable Contract, §8)

```yaml
artifact_id: c6-wave3.5-verification-master-v1
cloud: C6
wave: "3.5"
repo_target: ai-engineering-os   # explicitly NOT kkbb22/ARGON-HEALTH — this
                                 # artifact concerns the OS, not clinical ARGON
task_id: wave3.5-c6-verification-architecture
status: DESIGNED
implementation_status: NOT_IMPLEMENTED
evidence_status: DOCUMENTATION_ONLY
source_refs:
  - path: /mnt/user-data/outputs/ARGON-C6-AI-OS-VERIFICATION-HARNESS.md
    relation: extended_by_this_document
  - path: /mnt/user-data/outputs/C6-AI-OS-VERIFICATION-EVIDENCE.md
    relation: gap_closed (cross-task-reuse test, section 1.2 above)
dependencies:
  - cloud: C1
    needed_for: [kernel_rule_set, handoff_object_identity, plan_act_state_machine]
  - cloud: C2
    needed_for: [policy_enforcement_audit_split, destructive_action_reconciliation]
  - cloud: C3
    needed_for: [canonical_object_schemas, task_vs_context_packet_resolution]
  - cloud: C4
    needed_for: [neural_context_graph]
  - cloud: C5
    needed_for: [operator_state_machine, approval_ux]
  - cloud: C7
    needed_for: [independent_confirmation_of_this_harness]
contradictions: []   # none identified BY C6 in this document — C6 does not
                      # resolve contradictions belonging to other Clouds;
                      # C2's own self-reconciliation section (destructive-
                      # shell DENY vs REQUIRE HUMAN APPROVAL) is C2's to
                      # report, not C6's to restate as a "contradiction"
                      # entry here
open_questions:
  - "Which Cloud's Handoff Record model is canonical (C1's or C3's)?"
  - "Is aggregate evidence_used sufficient, or is claim-level Evidence
     Record linkage mandatory? (C1/C3 unresolved per mission pack)"
next_owner: C7
```

---

## 8. ARTIFACT_READY_FOR_TRANSFER

`ARTIFACT_READY_FOR_TRANSFER: YES`

- **filename:** `C6-WAVE3.5-VERIFICATION-MASTER.md`
- **artifact ID:** `c6-wave3.5-verification-master-v1`
- **hash (SHA-256, computed via `sha256sum` directly on the written file, pre-hash-insertion version):** `b019969e80c54cc52471bf063e32ea71e6e2ec527536052fb047a8dc8a095a6d`
- **creation timestamp (filesystem `stat`, UTC):** `2026-09-19 23:09:58 UTC`
- **note on this hash's own limit (disclosed, not hidden):** embedding a file's hash inside itself necessarily changes the file, so the hash above covers the document's content immediately before this line was inserted, not the exact final bytes — a structural property of self-referential hashing, not an error. Any downstream Cloud needing a hash of the *final* published bytes should recompute it directly rather than trust this line.
- **source context:** this session, Wave 3.5, ARGON AI Engineering OS Master Cloud Mission Pack v1
- **dependencies:** C1 (Kernel/Handoff/Plan-Act), C2 (policy/enforcement split), C3 (schemas), C4 (context graph), C5 (operator UX) — all unreceived as of this artifact's creation; C7 (independent confirmation, not yet performed)

# C1 — WAVE 3.5 SURGICAL CORRECTION PACK v2

Scope discipline: this document corrects specific confirmed findings from
Phase A. It does not redesign the AI-OS, does not touch ARGON-HEALTH
clinical architecture, and does not approve any ADR. Where a decision
properly belongs to another Cloud, it is marked as such and left open —
not decided here by default.

---

## 1. repo_target — resolved as a THREE-FIELD model

The single flat `repo_target` field conflated three genuinely different questions. Resolved by splitting it:

| Field | Answers | Example values |
|---|---|---|
| `repository_target` | Which literal git repository is this task's subject matter? | `legacy-argon` \| `argon-health` \| `none` (pure conceptual task, no repo involved) |
| `system_scope` | Which of the two worlds (per Baseline v1 §1) does this task belong to? | `argon_product` \| `ai_engineering_os` |
| `execution_target` | Where do the actual bytes move if this task acts? | `read_only_inspection` \| `sandbox_scratch` \| `deliverable_output` \| `live_repository_write` (hard-gated, requires Approval Record — see §5) |

**Canonical proposal:** all three fields live on Task Packet, immutable, all three required (no defaults). Example: "design how the AI-OS should reason about Legacy's clinic_auth_map incident" → `repository_target=legacy-argon, system_scope=ai_engineering_os, execution_target=read_only_inspection`.

**Alternatives considered and rejected:**
- *Single field only (original ask).* Rejected — this is exactly the ambiguity that caused this correction; it cannot distinguish "reading about Legacy" from "being authorized to write to Legacy."
- *Two fields (`repo_target` + `scope`), no `execution_target`.* Rejected — the hard approval gates (C2) key off *where bytes move*, not off subject matter; collapsing this back in would let a read-only design task look identical, on paper, to a live-write task.
- *Nest `system_scope` under `repository_target`* (e.g. `argon-health/ai-os` as one value). Rejected — `ai_engineering_os` scope tasks are not always about a specific repo (some are pure tooling design with `repository_target=none`); nesting creates an unnecessary combinatorial field.

---

## 2. Context Packet vs Context Projection — **correction, supersedes prior resolution**

Wave 3.5 Phase A (`C3-WAVE3.5-AI-OS-KNOWLEDGE-MODEL.md`, item 2) folded these into one object. On reconsideration, prompted by the candidate model in this correction request, that resolution was **wrong** and is superseded here.

**Corrected model:**
- **Context Projection** = a *versioned, reusable rule* — "given a Cloud role and an intent/domain combination, which Context Compiler stages apply and which files does it pull." This is analogous to a query template, not a query result. It has its own `projection_id` and `version`.
- **Context Packet** = the *concrete, timestamped output* of applying one Context Projection (at a specific version) to one Task Packet. Fields: `task_id`, `cloud_id`, `projection_id`, `projection_version`, `token_tier`, `files` (the resolved list).

**Why this correction matters in practice:** without a separate, versioned Projection, there was no way to say "the rule for building C2's context changed on this date" or to detect that an old Context Packet was built under a now-outdated rule. With the split, a Context Packet whose `projection_version` is behind the current `projection_id`'s latest version is flagged for regeneration — this also feeds §7 (stale context).

---

## 3. Handoff — resolved as ONE model (Cloud Result is not a competing model)

**Decision (not merely re-proposed):**
- There is exactly **one** Handoff schema, owned by C3.
- `Cloud Result` is **not** a second Handoff model — it is the *unvalidated draft stage* that exists only inside the producing Cloud's own turn. It is never transferable and never citable by any other Cloud.
- A `Cloud Result` is promoted to a `Handoff Record` only when every Claim inside it has ≥1 linked Evidence Record (the invariant already stated in Phase A) — that promotion step is where Cloud Result stops existing as a separate thing and a Handoff Record begins.

| | |
|---|---|
| Schema owner | C3 |
| Producer | The specialist Cloud, via the promotion step above (not a separate producer) |
| Consumer | **C1** (synthesis) and **C7** (forensic reconciliation) only, by default. **Open item:** whether C6 also needs direct multi-Cloud Handoff access for evidence-integrity checks — not decided here, routed to C6/C1 jointly (see Unresolved Decisions). |
| Lifecycle | `draft (Cloud Result, invisible outside producing Cloud) → validated (Handoff Record) → consumed (referenced in a C1 synthesis or C7 reconciliation) → superseded (if a later Handoff Record on the same claim replaces it — old one is kept, not deleted, and marked superseded)` |

**Rule, stated hard:** no Cloud may read or cite another Cloud's `Cloud Result`. Only `Handoff Record` is a valid citation target.

---

## 4. Status model — unified, one hierarchy, no contradictions

Five terms existed with unclear relationships. Resolved as a single layered model:

```
Task Packet
 ├─ processing_state   (WHERE in the pipeline — C1's Plan/Act model)
 │    PLAN | REVIEW | APPROVAL | ACT | VERIFY | STOPPED
 │
 └─ completion_state    (the OUTER, user-visible result — original mission pack's states)
      COMPLETE | PARTIAL | BLOCKED | REVIEW_REQUIRED | UNKNOWN | NOT_APPLICABLE
      ↑ computed bottom-up, never set directly by any Cloud — see rule below

Claim (per C3 §8)
 ├─ lifecycle_status    (how far along the THING being claimed about is)
 │    PROPOSED | DESIGNED | IMPLEMENTED | TESTED | VERIFIED | APPROVED | PRODUCTION
 │
 ├─ evidence_class       (how well-SUPPORTED the claim is — independent axis)
 │    CONFIRMED | PARTIAL | DOCUMENTATION_ONLY | EVIDENCE_MISSING | UNKNOWN | FUTURE_TRIGGER
 │
 └─ claim_status          (NEW — the missing middle rollup, derived from the two above)
      ACCEPTED   = evidence_class CONFIRMED, consistent lifecycle_status
      PROVISIONAL = evidence_class PARTIAL
      UNSUPPORTED = evidence_class EVIDENCE_MISSING or DOCUMENTATION_ONLY
      CONTESTED   = a Verification Record found contradiction
      DEFERRED    = evidence_class FUTURE_TRIGGER
```

**Rollup rule (Task.completion_state derived, never asserted):**
- `COMPLETE` only if every Claim required for that task's stated intent has `claim_status = ACCEPTED` **and** the relevant `lifecycle_status` matches what the task actually asked for (e.g., a "design" task is satisfiable at `DESIGNED`; an "implement and verify" task is not satisfiable below `VERIFIED`).
- `PARTIAL` if some required Claims are `ACCEPTED` and others are not.
- `BLOCKED` if any required Claim is `CONTESTED`, or an Approval Record (§5) is pending.
- `REVIEW_REQUIRED` if C6/C7 flagged an open Verification Record.
- `UNKNOWN` if too few Claims exist yet to evaluate.
- `NOT_APPLICABLE` for tasks that produce no Claims at all (e.g., a pure informational answer with nothing to verify).

This reconciles all three earlier vocabularies (C1's Plan/Act states, the original mission pack's completion states, C3's per-Claim axes) into one non-contradictory hierarchy. No Cloud may write `completion_state` directly — it is always computed from Claims.

---

## 5. Approval / Execution Authorization — ownership design

**New object: `Approval Record`.**

| Field | Description |
|---|---|
| `approval_id` | unique |
| `task_id` | which task this authorizes |
| `approved_plan_ref` | exact reference to the specific PLAN-stage artifact that was shown to the human — not a paraphrase |
| `approver` | always `human` — no Cloud may populate this field as itself |
| `timestamp` | when granted |
| `scope` | explicit bounded description: which `execution_target`, which files/paths, which action types are covered |

**Hard rule:** the `ACT` processing_state may only execute actions that fall within an existing, unexpired Approval Record whose `scope` matches. Any attempted action outside that scope is a hard block, evaluated against the recorded scope — **not** against the Cloud's own restatement of what it thinks it was approved to do. This directly closes the "approval laundering" gap C2 flagged in Phase A: laundering required the *executing* side to reinterpret an ambiguous approval; requiring the check to run against the recorded `scope` field, not a fresh restatement, removes that reinterpretation step.

**Ownership:** schema owned by C3 (consistent with the rest of the object model); the hard-gate enforcement rule is owned by C2; placement in the pipeline (produced at APPROVAL, consumed at ACT) is owned by C1 (this document).

---

## 6. Context isolation — explicit mechanism

**Default rule:** every new Task Packet gets a fresh `task_id` and is built by the Context Compiler from `Kernel (T0) + live Repository Snapshot (T1) + this task's own routing` only. **It never inherits any prior task's Context Packets, Claims, or Evidence Records by copy.** This is the default and requires no action to obtain.

**Explicit linkage (only path to cross-task continuity):** a new Task Packet may carry a `references_task_id` field, but only when:
(a) the user explicitly asks to continue/build on a named prior task, or
(b) C1 explicitly decides a linkage is needed and records it as a `Dependency` object (per C3 §3) — never silently.

No other mechanism links two tasks' contexts. This makes leakage a rule violation (something to detect and reject), not a possible default behavior.

---

## 7. Stale context — refresh triggers for Repository Snapshot

Four concrete triggers, replacing the earlier "should verify when architecture-critical" prose:

| # | Trigger | Action |
|---|---|---|
| 1 | Task enters `PLAN` and its risk_class touches an ADR/ACR/domain-authority question | **Mandatory** live `git ls-remote` re-check before `PLAN` may complete, regardless of snapshot age |
| 2 | Snapshot age exceeds a session-time threshold (proposed: 15 minutes of elapsed conversation time — **this number is a judgment call, not evidence-derived; flagged for human confirmation, not treated as settled**) | Re-check for *any* task, low-risk included, as a cheap safety net |
| 3 | A Cloud's claim contradicts a previously-recorded Handoff Record that cites the same repository | Re-check before escalating as a genuine contradiction — rules out "the repo changed in between" as a false-positive cause |
| 4 | The user states, in-conversation, that the repository was changed by any means | Re-check immediately, unconditionally |

If none of the four fire, the existing snapshot remains valid for the task at hand.

---

## 8. Routing — executable matrix (replaces informal prose)

| Task signal | C1 | C2 | C3 | C4 | C5 | C6 | C7 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Pure question, single domain, read-only | ✔ | | | | | | |
| Touches ACR-1..5 | ✔ | | ✔ | | | ✔ | |
| Attempted ADR/ACR status change | ✔ | ✔ | | | | | *(hard-blocked before further routing)* |
| `repository_target = legacy-argon` | ✔ | ✔ | | | | | |
| Touches object storage / DICOM / security domain | ✔ | ✔ | | | | | |
| Touches data ownership / schema question | ✔ | | ✔ | | | | |
| Touches clinical/product depth or capability | ✔ | | | ✔ | | | |
| Touches operator UX/display requirement | ✔ | | | | ✔ | | |
| Any Claim asserts `completion_state = COMPLETE` | ✔ | | | | | ✔ | |
| Cross-Cloud contradiction detected (Verification Record `outcome = contradicted`) | ✔ | as needed | as needed | as needed | as needed | ✔ | ✔ |
| Full baseline/audit explicitly requested | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |

This is a lookup table a Task Router could execute mechanically once built — it remains **DESIGNED**, no code exists yet.

---

## Supersedes List

1. `C3-WAVE3.5-AI-OS-KNOWLEDGE-MODEL.md`, item 2 — "Context Packet / Context Projection are one object" is **superseded**; they are now two objects (§2, above).
2. `C1-WAVE3.5-CANONICAL-ARCHITECTURE.md`, Deliverable 4 — "no formal routing table exists" is **superseded** by the matrix in §8.
3. Any prior implicit assumption that `repo_target` is a single field — **superseded** by the three-field model in §1.
4. Any prior ambiguity treating `Cloud Result` as a second, competing Handoff schema — **superseded**; §3 makes it explicit that it is a pre-validation draft stage, not a second model.

## Unresolved Decisions (not decided by C1 here, per instruction)

- Whether C6 needs direct multi-Cloud Handoff Record access (beyond C1/C7) for evidence-integrity checking — **routed to C6, with C1 input needed on the routing consequence**.
- The 15-minute staleness threshold in §7 Trigger 2 is a proposal, not a resolved value — **requires human confirmation**.
- Whether `Approval Record.scope` needs a machine-checkable structured format (e.g., path globs / action-type enums) versus free text — **routed to C2+C3 jointly**.
- Whether `lifecycle_status = PRODUCTION` can ever legitimately apply to an AI-OS-only Claim (as opposed to an ARGON clinical Claim) — genuinely ambiguous, **requires human decision** before Wave 4 implementation reaches that far.

## Exact Dependencies on C2 / C3 / C5

- **C3** must revise `C3-WAVE3.5-AI-OS-KNOWLEDGE-MODEL.md` to formally add: the three-field target model (§1) to Task Packet; the split Context Projection/Context Packet schema (§2) with `projection_id`/`projection_version`; `claim_status` as a field on Claim (§4); the `Approval Record` schema (§5). None of this is implemented in C3's existing document yet — this correction pack only specifies the design; C3's canonical file still needs the actual edit.
- **C2** must incorporate the `Approval Record` hard-gate (§5) into its Policy/Enforcement/Audit table (`C2-WAVE3.5-AI-OS-THREAT-MODEL.md`), which does not currently reference this object, and must resolve the two items routed to it above.
- **C5** must revise `C5-WAVE3.5-OPERATOR-CONTROL-SPEC.md`'s "Current State" and "Completion Display" sections to visibly distinguish `processing_state` from `completion_state` as two separate, clearly labeled UI elements — its current draft uses "current stage" loosely and does not yet reflect this split.

No ARGON-HEALTH clinical architecture file was read, referenced for modification, or altered in producing this correction.

## ARTIFACT_READY_FOR_TRANSFER: YES
- filename: `C1-WAVE3.5-CORRECTION-v2.md`
- artifact_id: `c1-wave3.5-correction-v2`
- dependencies: C1-WAVE3.5-CANONICAL-ARCHITECTURE.md, C3-WAVE3.5-AI-OS-KNOWLEDGE-MODEL.md, C2-WAVE3.5-AI-OS-THREAT-MODEL.md, C5-WAVE3.5-OPERATOR-CONTROL-SPEC.md (all require follow-up edits per "Exact Dependencies" above — this document does not edit them itself)

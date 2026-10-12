# C3 — CANONICAL AI-OS OBJECT MODEL v2

**Cloud:** C3 — Schema Authority (this wave's designated role)
**Supersedes:** `C3-WAVE3.5-AI-OS-KNOWLEDGE-MODEL.md` (sha256 `32114b7...4e24333b7`) and its manifest (sha256 `083c6b7...27b1aaf656f`). Those files are not deleted — they remain as the record of what changed and why (§8 of the superseded doc already logged the Wave-3 → Wave-3.5 delta; this document logs the v1 → v2 delta at the end).
**Mandate this pass:** correct only *confirmed* contradictions. Where no contradiction was confirmed, the v1 design is carried forward unchanged and is not relitigated here.
**Attempted but inconclusive this pass:** checked `api.github.com` for any existing separate AI-Engineering-OS repository under the same GitHub account — rate-limited, no answer obtained. Treated as **UNKNOWN**, not assumed either way.

---

## 1. `repo_target` — canonical fix

**Confirmed contradiction:** v1's `repo_target: legacy | argon-health` had no value for a task about the AI Engineering OS itself — found concretely when this document's own predecessor tried to fill in its own manifest.

**Resolution — [OBSERVED, not invented]:** the very first Wave-3.5 mission document's own Section 0 states the OS coordinates exactly three things: *"ARGON-HEALTH Target / Legacy ARGON / AI Engineering OS نفسه [itself]."* That is textual evidence for a three-value enum, not a C3 invention:

```yaml
repo_target: legacy | argon-health | ai-engineering-os
```

**Coordination note with C1:** this is C3 proposing the enum values; C1 owns the Context Compiler field that populates `repo_target` on every Task Packet, so C1 must ratify that the Task Router actually sets `ai-engineering-os` for OS-design tasks rather than defaulting to one of the other two or leaving it null. **[REQUIRES C1 RATIFICATION — not yet obtained in this session.]**

**Repository Snapshot consequence:** when `repo_target = ai-engineering-os` and no concrete git repository exists yet for the OS (status: **UNKNOWN**, checked and inconclusive this pass), the git-specific fields (`remote_url`, `branch`, `head`, `origin_head`, `clean`, `shallow`) are **nullable**. A Repository Snapshot with `repo_target = ai-engineering-os` and all git fields null is a valid, meaningful record: *"this task concerns the OS itself; no repository was consulted because none is confirmed to exist yet."* This is not a workaround — it is the honest state.

---

## 2. Context model — confirmed, not re-litigated

**Task:** prove the Context Projection (versioned rule) vs. Context Packet (immutable instance) split is correct, or show a better model with evidence.

**Finding:** no contrary evidence surfaced. The split remains internally consistent and matches an established pattern (view definition vs. materialized instance). Being precise about what kind of "evidence" this is: this is **logical consistency and precedent**, not independently produced repository evidence — there is no external system to check this against, since the OS itself doesn't exist yet to observe. Upgrading its status from v1's "PROPOSAL, not yet ratified" to **DESIGNED** (a settled schema decision) — still not IMPLEMENTED, TESTED, or VERIFIED, and still requires C1 to ratify before Wave 4 implementation begins.

- **Context Projection** = versioned rule: `(projection_id, version)`, authored by C1's Token Engine, edited only by creating a new version.
- **Context Packet** = immutable generated instance: `(task_packet_id, for_cloud, repo_snapshot_id)`, produced by applying one Context Projection version to one Task Packet.

No fields changed from v1 §1.2/§1.3 — only the confidence label changed.

---

## 3. Handoff — one definition only

**Confirmed contradiction, found this pass:** three different things in this session have used the word "handoff":

1. The **`ARGON CLOUD HANDOFF`** prose template used in this session's Wave-0 response (fields: `CLOUD / ROLE / DATE / VERIFIED FACTS / EVIDENCE / FINDINGS / ... / NEXT HANDOFF TARGET`).
2. The **`Handoff Record`** object defined in Wave 3.5 v1 (C1-only, one per wave, aggregates multiple Cloud Results).
3. Informal **"HANDOFF TO C1"** bullet lists written at the end of this session's Wave-0 and Wave-2 responses.

**Resolution — exactly one canonical Handoff object:**

`Handoff Record` (as defined in v1, unchanged) is the **only** object named "Handoff." It is produced once per wave-close, by C1 only, aggregating Cloud Results.

The other two are reclassified, not treated as competing objects:

- The `ARGON CLOUD HANDOFF` template is, on inspection, **per-Cloud granularity** (one per Cloud, not one per wave) — it matches **Cloud Result**, not Handoff Record. It is retroactively understood as an early, informal rendering of a Cloud Result, and the name is retired to avoid confusion with the one true Handoff Record.
- The "HANDOFF TO C1" bullet sections were never a separate object — they are informal narrative content that belongs inside a Cloud Result's `recommendations` and `dependencies_raised` fields.

**Invariant:** any future document, prose, or object in this system that uses the word "Handoff" refers to `Handoff Record` and only `Handoff Record`. A per-Cloud, per-task output is always called `Cloud Result`, never "handoff."

---

## 4. Status axes — canonical five-axis model, bound to entities

| Axis | Bound to (canonical) | Values | Governs / gated by |
|---|---|---|---|
| `processing_state` | Task Packet, Context Packet, Handoff Record | `created → routed/delivered → in_progress/consumed → completed → archived` (+`cancelled`) | Mechanical pipeline position — no approval needed to advance |
| `completion_state` | Cloud Result | `complete / partial / blocked / review_required / unknown / not_applicable` | Invariant v1-§4.8: `complete` requires ≥1 corroborated Claim or an explicit no-verification-needed note |
| `lifecycle_status` | The ARGON/OS artifact a Claim is about (mirrored in Decision Reference's cache) | `proposed → designed → implemented → tested → verified → approved → production` | `→ verified` requires a passing Verification Record (§5 below); `→ approved`/`→ production` transitions remain **unenforced** — no gating object defined for these yet, carried forward as open from v1 |
| `evidence_class` | Evidence Record | `confirmed / partial / documentation_only / evidence_missing / unknown / future_trigger` | Set once at `gathered_at`; corrections are new records, never edits |
| `claim_status` | Claim | `asserted → challenged → corroborated → refuted → withdrawn` | `→ corroborated` / `→ refuted` require a Verification Record (§5) |

No axis was added or removed this pass. This table is the canonical reference — supersedes the equivalent table in v1 in presentation only, not in content.

---

## 5. Evidence integrity — Source resolution as a hard precondition

**Confirmed contradiction:** v1 allowed an Evidence Record to exist referencing a Source whose `source_status` might be `unresolvable` or `not_yet_checked`, with no rule stopping such an Evidence Record from being cited toward a Claim's `claim_status`. IDs resolving to *existing objects* (referential integrity, v1 §5) is not the same guarantee as the underlying *evidence actually being reachable*.

**Fix — new invariant:**

> An Evidence Record may be cited to advance a Claim's `claim_status` beyond `asserted` **only if** its Source has `source_status = resolvable`, checked at or after that Evidence Record's `gathered_at`. An Evidence Record whose Source is `unresolvable` or `not_yet_checked` is retained (never deleted — it's still part of the audit trail) but is **inert** for gating purposes until re-checked.

**Full chain, now explicit:**

```
Claim ──requires──▶ Evidence Record ──requires resolvable──▶ Source
  ▲                                                              │
  └──────────────── Verification Record ◀── log_ref ────────────┘
```

**Verification Record's method, made concrete (was underspecified in v1):**
- `chain_resolution_check` — mechanical: confirms every Evidence Record on the Claim has a `resolvable` Source. **Necessary, not sufficient** — a Source can resolve and still not actually say what the Claim asserts.
- `content_review` — a human or Cloud (C6/C7 only) judgment that the resolved Source content actually supports the Claim's text.

A `result = PASS` Verification Record should state which method(s) were used; a chain-resolution-only PASS is weaker evidence than one that also had content review, and both are recorded as distinct Verification Records rather than collapsed into one unqualified PASS.

---

## 6. Approval / Execution Authorization object — added, with evidence for the need stated plainly

**Evidence for necessity — stated honestly:** no independently-produced C1 or C2 Cloud Result exists in this session to cite (neither Cloud has actually run and returned output here). The evidence for this object's necessity is that **every mission document handed to C3 this session** — the original Six-Cloud pack, the Wave-3.5 v1 brief for C1 (Plan/Act: `PLAN→REVIEW→APPROVAL→ACT→VERIFY`), for C2 (`REQUIRE HUMAN APPROVAL` as a named hard-gate category), for C5 (an entire approval-display section) — repeats this as a hard requirement, and the shared global rule 18 states it explicitly (*"Human approval is a hard gate, not a recommendation"*). This is source-tier **informational/instructional** evidence (the mission documents themselves), not tier-1 executable evidence and not an independently corroborating C1/C2 output. Flagged at that strength, not overstated.

### Approval / Execution Authorization
- **Purpose:** records one human decision authorizing (or denying) one specific planned action, scoped and time-bound.
- **Owner:** the human approver — no Cloud owns an approval.
- **Producer:** the human, via C5's operator control surface.
- **Consumer:** C1's Plan/Act Gate — `ACT` may proceed only against a matching, valid Approval.
- **Immutable fields:** `id`, `task_packet_id → Task Packet`, `action_ref` (the specific planned action — pending C1's own Plan-object schema; treated as a structured description here, not invented in full), `approver`, `scope`, `decision (approved|denied)`, `decided_at`, `valid_until`, `repo_snapshot_id` (the state the approval was granted against).
- **Mutable fields:** none — a revocation is a **new** record with `decision = revoked`, `revokes_approval_id → this Approval.id`, never an edit of the original.
- **Canonicality:** one decision event per `(task_packet_id, action_ref, decided_at)`.
- **Uniqueness key:** `id`.

**New invariant:** the `ACT` state may execute an action only if a matching Approval exists with `decision = approved`, `valid_until` not yet passed, `repo_snapshot_id` matching the current Repository Snapshot (or explicitly re-confirmed if it has drifted), and `scope` covering exactly the action being taken — no broader silent reuse of a prior approval for a different action.

---

## 7. Referential Integrity — full list (v1 rules carried forward + new)

- Every `context_packet.task_packet_id` → existing Task Packet.
- Every `claim.evidence_refs[i]` → existing Evidence Record.
- Every `evidence_record.source_id` → existing Source.
- Every `verification_record.claim_id` → existing Claim.
- Every `*.repo_snapshot_id` (any object) → existing Repository Snapshot.
- `decision_reference` uniqueness `(kind, decision_id, repo_target)` must not collide across repo targets.
- **[NEW]** `approval.task_packet_id` → existing Task Packet; `approval.repo_snapshot_id` → existing Repository Snapshot; `approval.revokes_approval_id` (if present) → existing Approval.
- **[NEW]** an Evidence Record is **inert** (not merely "existing") unless its Source resolves — see §5. Referential integrity (the ID points somewhere real) and evidential validity (that somewhere is actually reachable) are now two separate, both-required conditions.

---

## 8. C6/C7 verification authority — options only, no decision made here

If a C6-produced Verification Record and a C7-produced Verification Record disagree on the same Claim, three options exist. **C3 is not choosing one** — this is a governance/authority question for C1 and the human owner, consistent with global rule 6 (*"C7 challenges; C7 does not govern"*) and rule 7 (*"Human is final authority"*).

| Option | Mechanism | Consistency check against stated global rules |
|---|---|---|
| **A — C7 outranks C6 by identity** | C7's Verification Record always wins on conflict | Sits awkwardly against rule 6 — giving C7 an automatic identity-based override *is* a form of governing, not merely challenging |
| **B — Automatic escalation, no default winner** | Any C6/C7 disagreement on the same Claim forces `claim_status` to stay at `challenged`, escalated to human decision | Matches rule 4 ("no majority voting resolves architectural conflicts") extended to a two-party disagreement, and matches rule 7 directly |
| **C — Evidence-strength wins, not Cloud identity** | Whichever Verification Record's own `log_ref` Source has the higher source-of-truth tier (per `ARGON-SOURCE-OF-TRUTH.md`'s hierarchy) governs, regardless of which Cloud produced it | Matches rule 5 ("evidence outranks consensus") most literally, but requires the source-tier comparison itself to be unambiguous, which is not yet guaranteed by anything in this schema |

**Observation, not a decision:** Option B is the only one with no dependency on a tie-breaking mechanism that doesn't already exist elsewhere in this model, and is the most literal reading of rule 6. This is noted as an observation about internal consistency, not as C3 resolving the governance question.

---

## 9. Canonical Object List (v2, complete)

Unchanged from v1: Task Packet, Dependency, Claim, Source, Evidence Record, Cloud Result (definitions carried forward as-is — see prior artifact).
Changed this pass: Context Projection / Context Packet (status upgraded, §2), Handoff Record (disambiguated, §3), Repository Snapshot (`repo_target` widened, §1), Decision Reference (unchanged — Legacy-repo gap still open, not addressed this pass since no new evidence arrived for it), Verification Record (method vocabulary made concrete, §5).
Added this pass: **Approval / Execution Authorization** (§6).

Full object count: **13** (12 from v1 + Approval).

---

## 10. Relationship Graph (v2)

```
Repository Snapshot ◀── referenced by ── Task Packet, Context Packet, Source, Handoff Record, Approval

Task Packet ──1:N──▶ Context Packet ◀──produced by── Context Projection
Task Packet ──1:N──▶ Claim (via Cloud Result)
Task Packet ──1:N──▶ Decision Reference
Task Packet ──1:N──▶ Approval

Cloud Result ──1:N──▶ Claim
Cloud Result ──1:N──▶ Dependency
Cloud Result ──N:1──▶ Task Packet
Cloud Result ──N:1──▶ Handoff Record (the ONE handoff meaning — §3)

Claim ──1:N──▶ Evidence Record ──requires resolvable──▶ Source
Claim ──1:N──▶ Verification Record ──log_ref──▶ Source
Verification Record ──governs──▶ Claim.claim_status

Decision Reference ──N:1──▶ Source

Approval ──governs ACT for──▶ Task Packet
Approval ──revokes (optional)──▶ prior Approval
```

---

## 11. Manifest

See `C3-WAVE3.5-KNOWLEDGE-v2.manifest.yaml`.

---

## 12. Delta Log — v1 → v2

| Item | v1 status | v2 status | What changed |
|---|---|---|---|
| `repo_target` enum | 2 values, gap found | 3 values (`+ai-engineering-os`) | Widened, grounded in Section-0 text |
| Context Projection/Packet split | PROPOSAL, unratified | DESIGNED | No contrary evidence found; confidence raised, not the design |
| Handoff meaning | 3 informal usages, undeclared collision | 1 canonical object, other 2 reclassified | Disambiguation only, no field changes to Handoff Record itself |
| Status axes | 5 axes defined | 5 axes, same, now with explicit gating column | No new axis; clarified what gates each transition |
| Evidence chain | IDs must resolve (referential only) | IDs must resolve **and** Source must be `resolvable` (evidential) | New invariant, closes a real gap |
| Approval object | did not exist | added | Evidence for necessity stated at its actual (informational-tier) strength |
| C6/C7 authority conflict | flagged unresolved | still unresolved, now with 3 named options | Options only — no resolution, per instruction |

**Still unresolved, carried forward unchanged:** Claim de-duplication; Task Packet field-refinement (append-only vs overwrite); Decision Reference's Legacy-repo coverage gap; `lifecycle_status` transitions other than `→ verified` remain ungated.

# C5-WAVE3.5-OPERATOR-v2
## Alignment Verification Against C1/C2/C3 Canonical Models

STATUS OF THIS DOCUMENT: this is a **verification attempt**, not a new
design. Per instruction, I adopt only canonical models issued by
C1/C2/C3 — and per direct check of this session's environment
(re-confirmed before writing this), **no C1, C2, or C3 canonical
artifact exists anywhere in this session.** Only C5's own prior outputs
are present:

- `C5-ai-engineering-os-control-interface.md`
- `C5-AI-OS-HUMAN-CONTROL-EVIDENCE.md`
- `C5-WAVE3.5-OPERATOR-CONTROL-SPEC.md` (+ manifest)

Consequence, stated plainly rather than worked around: **every item
below can only be checked against C5's own design intent, not verified
against a canonical source, because that source doesn't exist yet in
this session.** I am not inventing a substitute C1/C2/C3 schema to make
verification possible — that would violate the explicit instruction and
reintroduce exactly the fabrication risk this whole thread has been
built to avoid.

Each item gets one of three honest outcomes:
- **CONSISTENT WITH C5 DESIGN** — C5's own prior spec already states this
  property; re-confirmed here.
- **UNVERIFIABLE — NO CANONICAL INPUT** — cannot be checked against
  C1/C2/C3 because no such artifact exists to check against.
- **GAP IN C5 DESIGN** — C5's own prior spec does not actually cover
  this cleanly; flagged as a real finding, not glossed over.

---

## 1. UI displays policy; UI does not own policy.

**CONSISTENT WITH C5 DESIGN.** Prior spec §F states this as a rule
("policy vs enforcement vs audit must be visually separable") and every
UI element in that section is framed as *rendering* a state (ALLOW/DENY/
etc.), never *deciding* one — carried from the earlier
`argon-c5-healthcare-ux` skill's own foundational rule ("no permission
decision is ever made in the UI layer alone").

**UNVERIFIABLE — NO CANONICAL INPUT:** whether C2's actual policy engine
matches this separation (i.e., whether "policy" is even a distinct
object in C2's design, versus policy-and-enforcement being fused). This
was already flagged as `DEPENDENCY (C2)` in the prior artifact and
remains open.

---

## 2. REQUIRE HUMAN APPROVAL cannot be converted to ALLOW by UI.

**CONSISTENT WITH C5 DESIGN**, with one precision added this pass: the
prior spec's §F table shows REQUIRE HUMAN APPROVAL as a distinct render
state, but did not explicitly state the negative constraint ("no UI
control exists that flips this to ALLOW"). Stating it now as an explicit
design commitment: **no button, no default-timeout auto-approve, and no
bulk-approve action may be attached to a REQUIRE HUMAN APPROVAL item
without an individually-actioned, individually-logged approval per
item.** This closes a real gap in the prior draft rather than restating
something already fully covered — recorded honestly as a correction, not
silently patched in without note.

**UNVERIFIABLE — NO CANONICAL INPUT:** whether C1's Plan/Act gate or
C2's enforcement layer would actually reject a UI-originated ALLOW
override if one were sent — the UI-side promise is only as strong as
the backend refusing to honor it, and I have no C1/C2 artifact
confirming that refusal exists.

---

## 3. DENY cannot be overridden by normal UI.

**CONSISTENT WITH C5 DESIGN.** Prior spec's §F distinguishes DENY from
REQUIRE HUMAN APPROVAL precisely because DENY is not meant to have an
"approve anyway" path in normal operation. Restating explicitly per this
item's wording: **no "override" affordance is designed anywhere in the
C5 spec for a DENY state.** If an override path is ever required (e.g.,
break-glass-equivalent for engineering ops), that would need to be a
separate, elevated, out-of-band action explicitly authorized by C1/C2 —
not a "normal UI" control, and I am not designing one speculatively here
since none has been requested.

**UNVERIFIABLE — NO CANONICAL INPUT:** same as item 2 — whether the
backend actually has no override path either, or whether one exists
that C5 simply hasn't been told about.

---

## 4. Approval is bound to exact plan/action.

**GAP IN C5 DESIGN, now closed.** The prior spec's §C (Plan/Act) shows
approval as a *stage* in a linear flow, but does not explicitly state
that an approval record is bound to the **specific plan content** shown
at approval time — i.e., nothing in the prior draft prevented the theoretical
failure mode "operator approves Plan A, system silently substitutes Plan
A′ before executing." Correcting this now: **the approval action must
capture and store a reference/hash of the exact plan content approved**
(a UI-emitted claim, e.g. `approved_plan_ref: <content hash>`), and ACT
must be refused if the plan content at execution time doesn't match the
approved reference. This is a genuine addition, not a restatement —
flagged as such rather than folded in silently.

**UNVERIFIABLE — NO CANONICAL INPUT:** whether C1's Plan/Act gate or
C3's object model actually has a field to carry this reference. This is
now a concrete, specific ask for C1/C3, not just a generic dependency.

---

## 5. Current-state displays the repository snapshot timestamp.

**CONSISTENT WITH C5 DESIGN.** Prior spec §B explicitly includes
"Snapshot: <HEAD/branch/dirty?>" in the always-visible panel and its
prose separately calls out "snapshot timestamp" as a minimum field the
panel depends on.

**UNVERIFIABLE — NO CANONICAL INPUT:** already flagged in the prior
artifact as `DEPENDENCY (C3)` — whether Repository Snapshot actually
carries a timestamp field. Unchanged, still open.

---

## 6. Routing reason/confidence is visible.

**CONSISTENT WITH C5 DESIGN.** Prior spec §D specifies both fields
explicitly (`reason`, `confidence: enum[high, medium, low]`) with LOW
confidence forcing operator acknowledgment.

**UNVERIFIABLE — NO CANONICAL INPUT:** already flagged as `DEPENDENCY
(C1)` — whether Task Router emits a reason string at all today. Unchanged,
still open, restated rather than assumed resolved.

---

## 7. Conflict UI never becomes voting UI.

**CONSISTENT WITH C5 DESIGN.** Prior spec §E explicitly forbids
aggregate tallies or "N agree/M disagree" rendering, structures conflicts
as claims+evidence+classification+authority+state instead. No change
needed — re-confirmed, not re-designed.

**Nothing unverifiable here that hasn't already been stated:** this
property is fully C5-owned (a rendering choice), not dependent on
C1/C2/C3 internals — the only way this could fail is if C5's own
implementation ignores its own spec, which is an implementation-fidelity
risk for C6 to test, not an open design dependency.

---

## 8. Evidence status visuals follow lifecycle/evidence distinction.

**CONSISTENT WITH C5 DESIGN.** Prior spec §G renders `lifecycle_status`
and `evidence_class` as two independent badges, per C3's stated
requirement to keep these axes separate.

**UNVERIFIABLE — NO CANONICAL INPUT:** whether C3's actual Evidence
Record object uses exactly these two field names/enums, or something
else. C5's rendering logic assumes the two-axis shape is correct; the
literal field names are C3's to confirm.

---

## 9. Stop preserves partial evidence.

**CONSISTENT WITH C5 DESIGN.** Prior spec §H states this unchanged from
the original draft: stop freezes stage, renders per-cloud partial
results, never erases.

**UNVERIFIABLE — NO CANONICAL INPUT:** whether an Evidence Record
already committed before STOP is actually immutable/retained by C3's
storage model, or whether STOP could race a not-yet-persisted write.
This is a genuine edge case I had not previously named — flagging it
now as new, not previously covered: **if evidence write and STOP can
race, C3 needs to define which wins**, and C5's "never erases" promise
is only as good as that resolution.

---

## SUMMARY TABLE

| # | Requirement | Result |
|---|---|---|
| 1 | UI displays, doesn't own, policy | Consistent / unverifiable vs C2 |
| 2 | REQUIRE APPROVAL not UI-convertible to ALLOW | Consistent (gap closed this pass) / unverifiable vs C1+C2 |
| 3 | DENY not UI-overridable | Consistent / unverifiable vs backend |
| 4 | Approval bound to exact plan | **Gap closed this pass** — new concrete ask for C1/C3 |
| 5 | Snapshot timestamp shown | Consistent / unverifiable vs C3 |
| 6 | Routing reason/confidence visible | Consistent / unverifiable vs C1 |
| 7 | Conflict UI never becomes voting UI | Consistent, C5-owned, no external dependency |
| 8 | Evidence visuals follow lifecycle/evidence split | Consistent / unverifiable vs C3 field names |
| 9 | Stop preserves partial evidence | Consistent / **new race-condition question for C3** |

**7 of 9 items are fully C5-design-consistent but remain formally
UNVERIFIABLE against canonical C1/C2/C3 models because none exist yet in
this session.** 2 items (4 and 9) surfaced genuine gaps in the prior C5
draft, now corrected, each producing a new, specific, named ask for
another Cloud rather than a vague "needs confirmation."

No item above is marked VERIFIED. No canonical schema was invented on
C1/C2/C3's behalf.

---

## SCOPE CONFIRMATION

No clinical UI, no domain/workflow/ADR content, no independent schema
invented for C1/C2/C3. This document does not claim any of the nine
properties are proven — only that C5's own design intent is internally
consistent with them, pending the missing canonical inputs.

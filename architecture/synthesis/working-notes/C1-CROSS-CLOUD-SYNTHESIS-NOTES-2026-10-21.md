# C1 Cross-Cloud Synthesis Notes — 2026-10-21

```yaml
artifact_id: c1-cross-cloud-synthesis-notes-2026-10-21
status: WORKING_NOTES_FOR_DRAFT
owner: C1
scope: phase-D synthesis only
implementation_status: NOT_IMPLEMENTED
```

These are compact, traceable synthesis notes, not a replacement for canonical sources. The following six SHA-256 values are the LF-normalized baselines carried by C7-FFA-003 Gate 1 and the repository index. A local byte-level verification should be repeated when the files are used to create the repository PR.

| Input | Expected LF-normalized SHA-256 | Key source contribution | Evidence/status boundary |
|---|---|---|---|
| `clouds/C1/C1-CLOUD-HARNESS-ADAPTER-RESEARCH.md` | `24e8cdb1cb8a088f146ff97265a484a329544b6a13d3bdfafea00de9f5dc688f` | Model/Adapter/Kernel/Runtime/Tools split; stable task state; no self-certification; checkpoint/evidence hooks; E1/E1b/E2/E3 | Research design; adapter sufficiency, depth limit and enforcement require experiments |
| `clouds/C2/C2-CLOUD-SECURITY-ADAPTER-RESEARCH.md` | `c6e95c268aa6b065737933cbeff10761939d8f310cb11db8b9907fb03d000b99` | Authorization taxonomy; tool permissions and sandbox; RP-1 Plan/Act firewall; RP-13 exact-action/crypto-bound approval proposal; provenance paradox / verifier separation | RP-13 downgraded to NEEDS EXPERIMENT; six unresolved binding questions; full Plan/Act test not run |
| `clouds/C3/C3-CONTEXT-ENGINE-RESEARCH.md` | `b48cbb0b6f1205e66eed9b738d7b5ff3fc6d4db1b10584739149577d2dc9042c` | Context projection vs concrete packet; retrieval and budget considerations; task context isolation and checkpoint concerns | Design observations; isolation and stale resume remain unknown/need experiment |
| `clouds/C4/C4-SURGICAL-ENGINEERING-PROTOCOL.md` | `441007bcbdce318b212d7f166fb344e18e72d92e5d0090f75718b9bc9ec01651` | Engineering lifecycle, localization/repair/validation, Plan/Act Pattern F, mutation test scope, adapter and recovery experiments | Pattern F is NEEDS EXPERIMENT; C4's fifth vector is read-only-tool argument injection, differing from C1/C2 nested tool call |
| `clouds/C5/C5-OPERATOR-CONTROL-RESEARCH.md` | `e70ea36bcab13b1abf76dbc386a82ca114a8c86c66f689d30224f1de71c9e1a8` | Human Authority Boundary: Display, Guidance, Decision, Authorization, Enforcement; approval UX and operator evidence | Taxonomy is C5 proposal; UI should display/guide, not decide/enforce |
| `clouds/C6/C6-CLOUD-EVALUATION-ENGINE.md` | `a0d762ad472f0e5fb6a891495a943ca808ac642ab5b7d3b9eab42fd0e237946a` | Metric as (score, reason); train/validation/held-out separation; fixed regression set; metrics with method/cost/failure signal; benchmark validity caveats | No runtime harness; threshold values not supplied remain unset; no tests executed |
| `assurance/audits/C7-FFA-003.md` | No manifest hash claimed here; canonical path confirmed by `docs/DOCUMENT-CATALOG.md` | Gate 1 six input hashes; Gate 3 source spot-checks; Gate 4 cross-cloud checks; Gate 9 reconciliation; final verdict CLEAN WITH OPEN EXPERIMENTS | C7 is audit-only; do not infer implementation approval |

## C7 input-copy selection

Canonical input: `assurance/audits/C7-FFA-003.md`, as identified by `docs/DOCUMENT-CATALOG.md` and `README.md`. Comparison copy: `archive/duplicates/C7-FINAL-FORENSIC-AUDIT-COMPLETE.md`, catalogued as a duplicate. Side-by-side rendered-content inspection shows the same substantive hash table, spot checks, cross-cloud checks, open experiment list and verdict; Markdown table spacing/layout differ. Do not claim byte identity. Cite only the canonical audit in the synthesis.

## Cross-cloud findings to preserve

1. **C1 role/safety boundary:** Model reasons; Adapter translates model-specific conventions; Kernel declares invariant rules; Runtime enforces them; tools/environment are the mutation surface. Plan must have no mutation-capable path. Git writes, destructive actions and live repository writes require human approval records. Claims need resolvable evidence references; no self-verification.
2. **C2 trust boundary:** category approval, exact-action approval, payload binding and cryptographic binding are separate concepts. RP-13 is a design proposal with weak/emerging evidence and remains NEEDS EXPERIMENT. Six questions: key custody, identity, replay, expiry, revocation, exact payload. Approval scope (single-use vs broad/persistent) requires human policy.
3. **C3 context boundary:** C3 owns source selection, provenance, freshness and context snapshot/reconstruction semantics; C4 owns execution orchestration. A context policy/projection and a generated context packet are distinct objects. Isolation and stale-context resume are not tested.
4. **C4 execution boundary:** localize before repair, validate after repair; the Plan/Act rule is a proposed hard runtime invariant, not a proven vendor guarantee. Adapter sufficiency (E3), recovery and failure-injection need a real runtime. C4's fifth mutation vector means argument injection into a nominally read-only tool.
5. **C5 human authority:** UI is limited to Display/Guidance. Decision, Authorization and Enforcement belong in Kernel/policy/runtime layers; approval UX represents the decision and evidence, it does not itself enforce it.
6. **C6 evaluation boundary:** metrics must define unit, method, cost and failure signal; score-plus-reason preferred; train/validation/held-out separation and fixed regression set; do not invent thresholds; benchmark performance does not prove production correctness.
7. **C7 audit constraints:** C7-FFA-003 verdict is CLEAN WITH OPEN EXPERIMENTS. Full Plan/Act negative tests, RP-13, E1b delegation depth, E3 adapter boundary, stale checkpoint resumption, context isolation, C4 fifth-vector taxonomy, and C1's SWE-bench Lite 10.7pp prose vs 7pp table tension remain open or require careful treatment.

## Synthesis decisions in this draft

- Keep role ownership boundaries explicit; no majority-vote conflict resolution.
- Retain task lifecycle `PLAN → REVIEW → APPROVAL → ACT → VERIFY` as design, not implementation.
- Keep the original five Plan/Act test IDs but add C4's different argument-injection interpretation as PA-6. Avoid discarding either attack surface.
- Keep delegation depth=1 as ARGON proposal, not universal vendor fact; E1b remains required.
- Preserve RP-13 and all six subquestions as unresolved; exact payload binding is not assumed working.
- Keep approval scope human-owned; do not select a single-use/persistent policy without a recorded decision.
- Treat all proposed record schemas as conceptual contracts, not existing APIs.
- Preserve test statuses: test specified is not test executed; zero runtime tests and zero PASS WITH EVIDENCE remain the current baseline.

## Final checks before repository promotion

- The repository assigns `assurance/audits/C7-FFA-003.md` as canonical and classifies the archived copy as a duplicate. The rendered texts were compared for the synthesis; do not claim byte identity. A local normalized diff may be retained as additional reproducibility evidence.
- Run `git diff --check`, input-hash validation, link/path checks, and review that no status implies implementation or test success.

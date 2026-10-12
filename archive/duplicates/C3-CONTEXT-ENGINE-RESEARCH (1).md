# C3 — CONTEXT / KNOWLEDGE ENGINE RESEARCH

**Cloud:** C3 — Data / Knowledge / Context Research
**Program:** ARGON Cloud Evolution — Research Sprint
**Scope discipline:** research and pattern-extraction only. No change to ARGON-HEALTH, Legacy ARGON, or any schema/code. Does not reopen Wave 3.5 — where this research touches something Wave 3.5 already decided (e.g. the `repo_target` naming question resolved in `C1-C3-WAVE3.5-CONVERGENCE-v3`), that decision is left exactly as it stands.
**Access date for every source below:** 2026-09-20.
**Compliance:** every OBSERVED claim below cites a public URL (official docs, GitHub repo, or peer-reviewed/preprint paper). No confidential or leaked system-prompt material was read or used.

## 0. Artifact Metadata (Packaging)

> This section was added during **FINAL ARTIFACT PACKAGING & HANDOFF**. It normalizes identity/version metadata that previously lived only in the companion manifest, into the canonical artifact itself, per that task's packaging instructions (§3). No line below is a new claim — each mirrors the corresponding field already carried in `C3-CONTEXT-ENGINE-RESEARCH.manifest.yaml`. The version suffix previously in this document's title ("v3, Correction Pass") is removed here as part of this same normalization — the manifest's `supersedes` list plus `report_sha256_value` is now the single place version identity is tracked, so the title does not carry a separate, driftable version label.

```yaml
artifact_id: C3-CONTEXT-ENGINE-RESEARCH
filename: C3-CONTEXT-ENGINE-RESEARCH.md
cloud: C3
wave: cloud-evolution-sprint
system_scope: ai_engineering_os
repository_target: none
execution_target: deliverable_output
status: DESIGNED
implementation_status: NOT_IMPLEMENTED
evidence_status: mixed   # see Section 12 and the manifest's evidence_status field for the full breakdown
source_count: 22
report_sha256: recorded_in_manifest   # see Section 13 and the companion manifest — not self-referential
next_owner: C7
```

> **CORRECTION-PASS BASELINE NOTICE — read before anything else.** Two passes now have referenced `C7-CLOUD-EVOLUTION-FINAL-AUDIT.v3` as the correction baseline. **No such file exists anywhere in this session** — no C7 turn has run, and no artifact by that name has been produced or attached. This is stated plainly rather than proceeding as if it had been verified. The six C3-specific items (D2, D3, D7, X5, P2, P14) given directly in each correction-pass instruction were fixed in the prior pass; this pass re-verified each one against the current file (not blindly redone) and reformatted the closing matrix to this pass's required 4-column spec — see Section 11. Per the "no silent cleanup" rule, this gap is flagged again, not hidden and not silently worked around.

---

## 1. Critical Distinction — Context Projection vs. Context Packet

**Research question:** does any studied source draw this exact line (versioned transformation rule vs. concrete generated instance), and does either "own" the other?

**Finding:** no source among Aider, SWE-agent, OpenHands, Cline, or DSPy separates a *reusable context-building policy* from *one concrete context instance* as two distinct, independently-versioned objects. The closest partial analogs:
- Aider's `--map-tokens` setting and chat-file biasing is **configuration**, not a versioned, independently-referenceable policy object — it's a run-time parameter, re-applied fresh each call over a map built via tree-sitter tag extraction (mechanism detailed in P1 below).
- Aider's chat-file weighting is described in third-party analysis as a fixed **50× multiplier** with an **adaptive 8× budget expansion** when no files are selected — this is a *behavior*, not an object with its own identity/version separate from the map output (detailed in P2 below).
- OpenHands' condensers are the closest thing to a "policy" — a `LLMSummarizingCondenser` is a configured, swappable component, distinct from the event log it acts on, managing context separately from the event-driven conversation history itself (detailed in P6 below).

**Conclusion:** ARGON's Context Projection/Context Packet split is **not validated or contradicted by any external source** — it remains C3's own internal proposal (status per `CONVERGENCE-v3`: DESIGNED, not sourced from precedent). This research neither strengthens nor weakens that design; it simply confirms no public tool models it as two objects the way ARGON does. **Ownership direction is not assumed** — OpenHands' condenser-vs-log split is the nearest real precedent for *a policy acting on a state, not owning it*, which is consistent with (but does not prove) ARGON's existing direction.

---

## 2. Patterns

Format: **SOURCE → OBSERVED PATTERN → WHY IT WORKS → ARGON ADAPTATION → REJECT IF → TEST NEEDED → CLASSIFICATION**

### P1 — Ranked symbol graph for repository maps
**SOURCE:** Aider, "Building a better repository map with tree sitter," aider.chat, 2023-10-22, accessed 2026-09-20 — https://aider.chat/2023/10/22/repomap.html
**OBSERVED PATTERN:** Aider uses tree-sitter to parse source into an AST, identifying where functions, classes, and variables are defined and referenced, then uses these definitions and references to determine the most important identifiers in the repository, replacing an earlier ctags-based approach.
**WHY IT WORKS:** ranking runs over compact tags, not full file bodies, so importance becomes a computed graph property instead of a guess.
**ARGON ADAPTATION:** a Repo Map artifact (proposed, Context-Engine-Research v1) computed once per Repository Snapshot.
**REJECT IF:** applied as a literal code graph today — ARGON-HEALTH has zero application code (confirmed by direct file-census this session).
**TEST NEEDED:** E1 below.
**CLASSIFICATION:** ADAPT (pattern sound; literal application REJECT for now).

### P2 — Personalized ranking + adaptive token budget
**SOURCE:** third-party technical summary of Aider's repo-map algorithm, GitHub issue #535, NousResearch/hermes-agent, accessed 2026-09-20 — https://github.com/NousResearch/hermes-agent/issues/535
**OBSERVED PATTERN:** Aider's repo map uses personalized PageRank biased 50x toward files being actively edited, with an adaptive budget that gives roughly 8x more context when no files are selected in chat, shrinking as more specific files are added.
**WHY IT WORKS:** the budget is something to fit ranked content *into*, dynamically, rather than a fixed-size bucket.
**ARGON ADAPTATION:** Context Projection should fit ranked nodes into a byte/token budget dynamically; a Task Packet's declared `entities`/`domains` play the role of "chat files," biasing relevance.
**REJECT IF:** conflicts with C6's need for a clean boolean "was tier T4 loaded, yes/no" audit check — dynamic fitting makes that fuzzier. Real, unresolved tension, not silently adopted.
**Explicit note, this correction pass:** the **50×** and **8×** figures are Aider's own tuned constants for Aider's own use case — they are recorded here as the *external observation*, not proposed as ARGON's values. Whether ARGON needs any bias multiplier at all, and if so what value, is separate from whether the *mechanism* (dynamic, ranked, budget-fitted context) is worth adopting. Any specific number for ARGON is **UNKNOWN / NEEDS EXPERIMENT** — nothing here should be read as "ARGON should use 50x."
**TEST NEEDED:** E1, E2.
**CLASSIFICATION:** UNKNOWN (real tension with auditability unresolved).

### P3 — Document cross-reference graph (ARGON-native adaptation, not a vendor source)
**SOURCE:** C3's own direct observation this session (repeated `grep` passes locating `ACR-[0-9]` and `ADR-024` references across ARGON-HEALTH's docs), pattern borrowed from P1.
**OBSERVED PATTERN:** ARGON-HEALTH's real structure is a cross-reference graph of IDs and headers (`04-MASTER-DATA-MAP.md` cites `ACR-5`; `19-MASTER-ARCHITECTURAL-DECISIONS.md` defines it), structurally the same shape as a code call-graph.
**WHY IT WORKS:** the same ranking math that surfaces heavily-called functions should surface load-bearing ADRs/domains.
**ARGON ADAPTATION:** a Repo Map of `map_kind = doc_reference_graph`, buildable **today**, unlike a code-symbol graph.
**REJECT IF:** 53 files may be too sparse for ranking to beat plain `grep`.
**TEST NEEDED:** E1.
**CLASSIFICATION:** ADOPT (buildable now, unlike P1's literal form).

### P4 — Capped, guardrailed tool feedback
**SOURCE:** Yang et al., "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering," NeurIPS 2024, arXiv:2405.15793, accessed 2026-09-20 — https://arxiv.org/pdf/2405.15793
**OBSERVED PATTERN:** search and navigation tools provide summarized search results capped at a maximum of 50 per query, and the file editor integrates automatic linting that validates edits and provides specific error feedback for syntax issues. The paper's own ablation found removing linting reduces performance considerably, down to 15.0%, a roughly 3-point drop.
**WHY IT WORKS:** capping plus automatic validity-checking reduces wasted turns and undetected mistakes — and the ablation shows this is measured, not assumed.
**ARGON ADAPTATION:** repo-read tools should cap result counts and attach automatic validity checks (broken-cross-reference detection for Markdown today; linting once code exists) as feedback.
**REJECT IF:** a cap silently drops the one match a task needed — a systematic audit search (this session's own single-hit `grep -rn "ADR-024"`) must not be capped the same way exploratory search is.
**TEST NEEDED:** E1, E4.
**CLASSIFICATION:** ADAPT.

### P5 — Bounded history with explicit collapse point
**SOURCE:** Yang et al., arXiv:2405.15793, accessed 2026-09-20.
**OBSERVED PATTERN:** history is managed by collapsing older observations beyond the last 5 turns to maintain concise context.
**WHY IT WORKS:** simple, bounded, and predictable — a fixed recency window rather than an ad hoc summarization trigger.
**ARGON ADAPTATION:** Context Packet's `excluded_note` field should log exactly this for long Cloud sessions — collapsed content stays resolvable as a Source, only deprioritized.
**REJECT IF:** an early-session fact (e.g. a Repository Snapshot from turn 1) needs to still gate a later Verification Record — already safe in ARGON's schema since Repository Snapshot is a standalone referenced object, not embedded turn history.
**TEST NEEDED:** E5.
**CLASSIFICATION:** ADOPT; the exact window size is UNKNOWN for ARGON's own workload (SWE-agent's "5" is tuned to its own benchmark).

### P6 — Event-sourced, size-triggered condensation
**SOURCE:** OpenHands docs and community deep-dive, accessed 2026-09-20 — https://docs.openhands.dev/sdk/arch/events, https://dev.to/truongpx396/openhands-deep-dive-build-your-own-guide-1al0
**OBSERVED PATTERN:** the Event System is an immutable, type-safe, append-only log that serves as both the agent's memory and the integration point for auxiliary services. Condensation is triggered two ways: proactively, when the visible event count exceeds 80, a cheap LLM summarizes all events except the first 4 (which usually hold the system prompt and original task) and the last few (recent work), replacing the middle with that summary — and reactively, when the LLM raises a context-window-exceeded error, triggering a condensation request before retrying.
**WHY IT WORKS:** append-only logging preserves raw provenance; condensation is a *view* over the log, not a destructive edit — and having both a proactive size trigger and a reactive overflow trigger covers the common case and the failure case.
**ARGON ADAPTATION:** this is the clearest external precedent for "durable vs. active" (§5 below) — first-N and last-few events as durable/high-priority, middle as compressible; both a proactive and a reactive trigger, not just one.
**REJECT IF:** the "80 events" / "first 4" numbers are OpenHands-specific tuning, not evidence for ARGON's own thresholds.
**TEST NEEDED:** E3, E5, E6.
**CLASSIFICATION:** ADOPT the two-trigger structure; UNKNOWN/NEEDS EXPERIMENT for ARGON's own numeric thresholds.

### P7 — Hierarchical localization, never "read issue → edit random files"
**SOURCE:** Xia et al., "Agentless: Demystifying LLM-based Software Engineering Agents," ACM TOSEM / arXiv:2407.01489, and official repo, accessed 2026-09-20 — https://github.com/openautocoder/agentless
**OBSERVED PATTERN:** Agentless employs a hierarchical process to first localize the fault to specific files, then to relevant classes or functions, and finally to fine-grained edit locations, combining a repository-structure prompt asking the LLM to identify suspicious files with embedding-based retrieval using cosine similarity between the issue description and code chunks.
**WHY IT WORKS:** each stage narrows over a progressively cheaper candidate set instead of reading everything or guessing one file.
**CONVERGENT EVIDENCE:** this matches ARGON's own already-stated rule (Wave-3.5 C4 brief: "Problem → Localization → Hypothesis → Exact edit location → Minimal patch → Tests") — two independently-arrived-at designs agreeing.
**ARGON ADAPTATION:** formalize the hierarchy for whichever repo is native — documents (file → section header → paragraph) today, code (file → class/function → line) once it exists.
**REJECT IF:** little to reject.
**TEST NEEDED:** E1.
**CLASSIFICATION:** ADOPT.

### P8a — Test-based patch filtering (ADOPT)
**SOURCE:** Xia et al., arXiv:2407.01489 / official repo, accessed 2026-09-20.
**OBSERVED PATTERN:** Agentless generates reproduction tests to verify an issue has been resolved, then leverages both regression tests and generated reproduction tests to select the final submission patch.
**WHY IT WORKS:** executable tests are evidence, not opinion.
**ARGON ADAPTATION:** a `test_execution` method value for Verification Record (once code/tests exist) — the strongest evidence tier available.
**REJECT IF:** n/a, straightforward adopt of the filtering half.
**TEST NEEDED:** E6.
**CLASSIFICATION:** ADOPT.

### P8b — Majority-vote final selection (REJECT, explicitly)
**SOURCE:** same as P8a; confirmed directly in the official repo's own usage instructions: after test filtering, Agentless performs majority voting to select the final patch to solve each issue.
**WHY IT WORKS (for Agentless's own goal):** a cheap, automatic tie-break among several test-passing candidates.
**ARGON ADAPTATION / REJECT:** using majority vote as the *final* resolution mechanism directly contradicts ARGON's own stated global rule ("no majority voting resolves architectural conflicts; evidence outranks consensus"). **Adopt the pre-filter (P8a), reject the tie-break.** ARGON should rank test-passing survivors by Verification Record strength instead — open design question for C1/C6, not resolved here.
**TEST NEEDED:** none — this is a design-time rejection, not a benchmark question.
**CLASSIFICATION:** REJECT.

### P9 — Plan/Act with checkpointed rollback
**SOURCE:** Cline documentation and setup guides, accessed 2026-09-20 — https://docs.cline.bot/cline-cli/cli-reference, https://www.deployhq.com/guides/cline
**OBSERVED PATTERN:** Plan Mode gathers information and creates a detailed plan before implementation, exploring the codebase and asking clarifying questions, and presents a strategy for user approval before switching to Act Mode, which actively uses tools to accomplish tasks. Separately, Cline maintains a shadow Git repository, separate from the project's actual Git history, committing file state after each tool use, with restore modes including reverting files to a snapshot while keeping the conversation, or deleting messages after a checkpoint while leaving files alone.
**WHY IT WORKS:** the Plan/Act gate matches ARGON's own `execution_stage` design directly; the shadow-repo checkpoint gives a real rollback point independent of the *conversation's* state, addressing recovery cleanly.
**ARGON ADAPTATION:** ARGON's Repository Snapshot (write-once, referenced by Approval) already captures the "state at decision time" half of this; Cline's *shadow* commit-per-tool-use is a finer-grained precedent worth flagging for C1's Plan/Act Gate design specifically (not resolved here — out of C3's remit).
**REJECT IF:** Cline's own docs flag its autonomous "YOLO Mode" as dangerous: enabling YOLO Mode auto-approves all actions including file deletion, system modification, and network requests — direct negative evidence against ever defaulting to auto-approve, reinforcing ARGON's existing hard-gate stance rather than contradicting it.
**TEST NEEDED:** E4 (isolation angle only — checkpointing itself is C1/C2 territory).
**CLASSIFICATION:** ADAPT (Plan/Act confirmed as sound precedent); the checkpoint mechanism is flagged for C1, not adjudicated here.

### P10 — Natural-language trajectory feedback + held-out validation discipline
**SOURCE:** DSPy GEPA documentation and paper, accessed 2026-09-20 — https://dspy.ai/getting-started/gepa-optimization/, arXiv:2507.19457
**OBSERVED PATTERN:** GEPA leverages natural language traces from LLM-based workflows for optimization, preserving intermediate trajectories and errors in plain text rather than reducing them to numerical rewards, mirroring human diagnostic processes. Split discipline: the trainset supplies examples for reflective prompt updates, the valset tracks Pareto scores and selects the returned program, and a final test set is kept separate so it influences neither step.
**WHY IT WORKS:** textual feedback carries more diagnostic signal than a bare score; three-way data splitting prevents optimizing against the same examples used to declare success.
**ARGON ADAPTATION:** Verification Record's `result` field should carry a short natural-language rationale alongside PASS/FAIL/INCONCLUSIVE, not a bare enum — directly serves evidence traceability. The train/val/test split is the correct shape for the "Required experiments" section below.
**REJECT IF:** nothing to reject in the split discipline itself.
**TEST NEEDED:** applies to E1-E6 methodology generally — do not tune ARGON's own thresholds against the same task set used to claim they work.
**CLASSIFICATION:** ADOPT.

### P11 — Positional bias inside an otherwise-sufficient context window
**SOURCE:** Liu et al., "Lost in the Middle: How Language Models Use Long Contexts," TACL 2024, arXiv:2307.03172, accessed 2026-09-20.
**OBSERVED PATTERN:** across multi-document QA and synthetic key-value retrieval, varying the position of the relevant item while holding everything else fixed produces a U-shaped performance curve, with accuracy highest when the relevant information sits at the beginning or end of the input and lowest in the middle, holding across every model tested including a model with a 100K context window. Numerically, in a 20-document setting, performance at the first position was roughly 75% and degraded to around 55% at the middle before recovering to about 72% at the end.
**WHY IT WORKS (i.e., why the *problem* exists):** the effect is architectural, not just a training artifact — later calibration work found LLMs exhibit an intrinsic U-shaped attention distribution favoring the start and end of input regardless of relevance.
**ARGON ADAPTATION:** selecting the *right* content for a Context Packet (P1-P3) is necessary but not sufficient — Context Projection must also decide *ordering*: highest-relevance items placed near the start or end, not buried mid-packet, regardless of how good the ranking was.
**REJECT IF:** placement strategy is treated as a substitute for good ranking rather than a complement to it.
**TEST NEEDED:** E1 (extend to test ordering, not just inclusion).
**CLASSIFICATION:** ADOPT (as a constraint on Context Projection's rendering step, not on selection).

### P12 — Two-tier memory: in-context vs. out-of-context, agent-managed
**SOURCE:** Letta (formerly MemGPT) documentation, accessed 2026-09-20 — https://docs.letta.com/core-concepts/, https://docs.letta.com/guides/agents/memory/
**OBSERVED PATTERN:** Letta agents solve the context window limitation through context engineering across two tiers: in-context (core) memory — system instructions, read-write memory blocks, and conversation history — and out-of-context memory — older evicted conversation history and archival storage. Memory blocks are pieces of context editable by agents via memory tools, can be attached/detached from an agent, and can be shared across multiple agents at once. Archival memory holds explicitly formulated, processed and indexed knowledge, distinct from recall memory's raw conversation history.
**WHY IT WORKS:** separates *what must always be visible* (core) from *what's searchable on demand* (archival/recall), and — critically — makes memory blocks **shareable objects**, not per-conversation state.
**ARGON ADAPTATION:** this is the strongest external precedent found this sprint for ARGON's Source/Evidence-Record split being reusable across Claims — Letta's "shared memory block across multiple agents" is structurally close to ARGON's Source being cited by more than one Evidence Record. Also relevant to durable-vs-active (§5): core memory is durable-and-visible, archival is durable-but-retrieved, conversation history is the only compressible tier.
**REJECT IF:** Letta's memory blocks are agent-*editable* by design (the agent rewrites its own memory) — ARGON's Source/Evidence Record objects are explicitly write-once/immutable (Wave 3.5). Do not import the self-editing-memory pattern; the shared-reference pattern is the useful part, not the mutability.
**TEST NEEDED:** none new — reinforces E5/E6 (compression/evidence preservation), doesn't need a separate experiment.
**CLASSIFICATION:** ADAPT (shared-reference structure only; explicitly REJECT self-editing memory for ARGON's evidence objects).

### P13 — Truncate vs. summarize is an explicit, named tradeoff
**SOURCE:** LlamaIndex documentation, accessed 2026-09-20 — https://developers.llamaindex.ai/python/examples/agent/memory/summary_memory_buffer/
**OBSERVED PATTERN:** the original ChatMemoryBuffer truncates history after a token limit, which is useful for cost/latency but removes potentially relevant information; ChatSummaryMemoryBuffer instead iteratively summarizes messages that don't fit the buffer, giving more control over what chat history is retained.
**WHY IT WORKS:** naming the tradeoff explicitly (cheap-and-lossy vs. costlier-and-preserving) forces a conscious choice per use case, rather than always defaulting to one.
**ARGON ADAPTATION:** ARGON's own "never compress authority away" rule (this Common Layer, §7.5) is effectively choosing the summarize-not-truncate side of this exact tradeoff, deliberately — this external source confirms the tradeoff is real and named elsewhere, not just an ARGON house rule invented in isolation.
**REJECT IF:** summarization cost itself becomes the bottleneck for very short tasks where truncation would have been cheap and lossless (nothing past the limit existed anyway).
**TEST NEEDED:** E5, E6.
**CLASSIFICATION:** ADOPT (summarize-not-truncate, consistent with existing ARGON rule).

### P14 — Two-stage retrieve-then-rerank, with the counts published
**SOURCE:** Continue documentation, accessed 2026-09-20 — https://docs.continue.dev/customize/deep-dives/codebase
**OBSERVED PATTERN:** the codebase context provider retrieves an initial nRetrieve results (default 25) from a vector database, then optionally uses an LLM to select a final nFinal results (default 5) through re-ranking.
**WHY IT WORKS:** cheap vector search casts a wide net; an LLM reranking pass narrows to a small, high-precision final set — separating recall (cheap, broad) from precision (costlier, narrow).
**ARGON ADAPTATION:** Relevance (see "Design Output — Extended Pipeline" at the end of this section) should explicitly be two-staged the same way: cheap graph/embedding ranking produces a candidate pool, then a narrower pass (possibly the Cloud itself, reasoning over the candidates) picks the final set for the Context Packet — rather than treating "ranking" as a single pass.
**REJECT IF:** the two-stage cost (retrieve + rerank) exceeds just retrieving a slightly larger single-stage set directly, for small repositories (like ARGON-HEALTH's current 53 files) where the reranking LLM call may cost more than the tokens it saves.
**TEST NEEDED:** E1, E2.
**CLASSIFICATION:** ADAPT (two-stage structure sound; whether it pays for itself at ARGON-HEALTH's current small scale is UNKNOWN).

### P15 — Radical simplicity with *no* history compression, as counter-evidence
**SOURCE:** mini-swe-agent official repository, accessed 2026-09-20 — https://github.com/SWE-agent/mini-swe-agent
**OBSERVED PATTERN:** mini-swe-agent's message history is completely linear — every step simply appends to the conversation, giving a clean 1:1 mapping between trajectory and LLM input, with the entire agent class implemented in roughly 100 lines of Python, no tool-calling interface, scoring above 74% on SWE-bench verified.
**WHY IT WORKS (i.e., why simplicity isn't automatically weaker):** for short-to-medium tasks, the overhead of history compression (P5, P6) may cost more in complexity and risk (losing something during collapse) than it saves — mini-swe-agent gets competitive results with **none** of P5/P6's machinery.
**ARGON ADAPTATION — direct tension with P5/P6, stated plainly, per instruction not to assume simplicity = weakness:** before building any collapse/condensation machinery, test whether ARGON's actual Cloud tasks are short enough that linear history is simply sufficient. Building compression for a problem that doesn't occur yet is itself a token/complexity cost.
**REJECT IF:** ARGON's multi-Cloud, multi-wave sessions are demonstrably longer than mini-swe-agent's single-issue-resolution scope — in which case the two aren't comparable and P5/P6 remain the more relevant precedent.
**TEST NEEDED:** a new pre-experiment, before E5/E6 are even relevant: measure actual ARGON Cloud session lengths against this session's own history (this conversation itself is a real data point — long, multi-wave, likely past where linear-only history stays practical) before assuming compression is needed everywhere.
**CLASSIFICATION:** UNKNOWN — genuine counter-evidence to P5/P6, not dismissed just because it's simpler.

### Design Output — Extended Pipeline (ARGON PROPOSAL, self-contained)

**[CORRECTION, this pass]:** an earlier draft of this research referenced a pipeline design living in "§4 pipeline design" — §4 of this document is actually "Freshness" and never contained this content; that pointer was broken. The pipeline itself was real (defined in the now-superseded v1 of this artifact) but was never carried into this v2 document's body, only referenced informally. Per the self-containment requirement, it is reproduced here in full, explicitly labeled as an ARGON proposal, not as something any external source establishes.

Required shape: `TASK → REPOSITORY SNAPSHOT → REPO MAP → RELEVANCE → CONTEXT PROJECTION → CONTEXT PACKET`. Repository Snapshot, Context Projection, and Context Packet are Wave-3.5 objects (already defined there); Repo Map and Relevance are proposed here, at research-sprint depth, not full schema-authority depth.

**Repo Map (PROPOSAL, not yet ratified by C1):**
- Purpose: ranked, token-budget-fittable structural summary of a repository at one Repository Snapshot.
- Producer: a computed step run against a Repository Snapshot.
- Consumer: the Relevance step below.
- Key fields: `id`, `repo_snapshot_id`, `map_kind (code_symbol_graph | doc_reference_graph)`, `nodes`, `edges`, `ranks`, `generated_at`.
- Canonicality: one per `repo_snapshot_id`; recomputed whenever the snapshot changes.

**Relevance (PROPOSAL, not yet ratified by C1):**
- Purpose: given a Task Packet's declared `entities`/`domains` and a Repo Map, compute a per-node relevance score — the generalization of P2's/P14's ranking-and-staging patterns.
- Producer: a computed step, taking `(task_packet_id, repo_map_id)`.
- Consumer: Context Projection.
- Key fields: `repo_map_id`, `task_packet_id`, `node_id`, `score`, `method`.
- Canonicality: one score set per `(task_packet_id, repo_map_id)` pair.

**Full pipeline:**
```
Task Packet → Repository Snapshot → Repo Map → Relevance → Context Projection
                                                           (applies token budget,
                                                            per P2/P14/P11)
                                                                  │
                                                                  ▼
                                                            Context Packet
```
This closes a real gap: nothing previously explained *why* a given file made it into a Context Packet. **Status: PROPOSAL only — no code, no schema authority pass, no C1 ratification.** P1, P2, P3, and P14 above all reference this pipeline as their ARGON-adaptation target; this subsection is that target's actual definition, not a pointer to somewhere else.

---

## 3. TASK CONTEXT ISOLATION

**Explicit starting assumption, per instruction: isolation is not assumed to exist in ARGON today.** Nothing in this session has built or tested it.

**Research finding — and an honest gap, not a forced pattern:** none of the five tools studied are multi-agent systems facing ARGON's specific problem (several independent Clouds working related-but-distinct tasks against the same repository, where one Cloud's context must not silently leak into another's). Each tool gets isolation "for free" by construction — one conversation/session equals one event stream or one shadow-repo lineage — without ever needing to defend that boundary against a second, concurrent, related task the way ARGON's six-to-seven-Cloud model does:
- OpenHands: the Agent operates through a stateless, event-driven architecture, managing context via skills and condensers over one conversation's history — isolation between conversations is structural (separate event streams), not an explicitly engineered defense against cross-task leakage within one conversation.
- Cline: the shadow Git repository commits file state after each tool use within one task — again, one task, one lineage; no stated mechanism for detecting whether a second, concurrent task's changes bled into the same working tree.

**Conclusion:** ARGON's task-isolation requirement (cross-task leakage, session contamination, stale cache, inherited context, explicit cross-task references, scoped memory) is closer to a **distributed-systems/multi-tenant-security problem** than an agent-harness problem, and has **no direct external precedent** among the sources studied. This stays **UNKNOWN / NEEDS EXPERIMENT** for ARGON specifically — see E4. Not forcing a borrowed pattern where none genuinely fits is itself the correct research output here.

---

## 4. Freshness

**Answering the five required questions, source-grounded where possible, UNKNOWN where not:**

- **When is context stale?** No source studied gives a general-purpose definition beyond "the underlying state changed since context was captured." OpenHands' condensation trigger is about *size*, not *staleness of facts* — a different concern (§5). ARGON's own Repository Snapshot (`head` vs `origin_head` comparison, confirmed working this session) is the closest concrete mechanism found anywhere in this research, and it's ARGON's own, not borrowed.
- **How is change detected?** Git-native comparison (`git rev-parse HEAD` vs `git ls-remote origin HEAD`, exactly as used this session) is the only concretely evidenced mechanism across all research this sprint — none of the five tools document an explicit "is my context stale" check separate from just re-reading files each turn.
- **When must re-fetch happen?** No numeric or rule-based trigger found in any source. **UNKNOWN / NEEDS EXPERIMENT.**
- **When must recompile happen?** Same — **UNKNOWN / NEEDS EXPERIMENT.** (OpenHands' condensation trigger, P6, answers a *different* question — "when is history too big," not "when is history wrong.")
- **How is false completion from stale context prevented?** No source studied addresses this directly — it is closest to ARGON's own Verification Record design (Wave 3.5), not something found in Aider/SWE-agent/OpenHands/Cline/DSPy/Agentless.

**Any numeric threshold not directly evidenced above is marked UNKNOWN / NEEDS EXPERIMENT, per instruction — none is invented.**

---

## 5. Token Engine — durable vs. active, without losing evidence

Synthesizing P2, P5, P6:

| Question | Answer, sourced |
|---|---|
| What gets deleted from active context? | Nothing, strictly — OpenHands *replaces* (not deletes) middle events with a generated summary while the first few and most recent events remain untouched; SWE-agent *collapses* (not deletes) observations older than 5 turns. |
| What stays durable? | System/task-setup content and the most recent few turns, in OpenHands' scheme; in ARGON's own schema, Repository Snapshot and Source objects are durable by design (referenced, not embedded in collapsible history). |
| How is evidence preserved through compression? | Neither Aider nor SWE-agent nor OpenHands documents an explicit *evidence*-preservation guarantee through compression — this is the one place ARGON's own Source/Evidence Record model goes further than anything found in this research: a collapsed observation, in ARGON's design, must still resolve back to a full Source, which is not something any studied tool's docs claim to guarantee. **This is flagged as an ARGON-original requirement, not externally validated — test it (E6) rather than assume it holds just because it's designed that way.** |

---

## 6. Provenance

**Research question:** does a public pattern equivalent to `Source → Evidence Record → Claim` exist?

**Finding: no exact match.** Closest analogs, each partial:
- OpenHands' immutable event log is raw provenance (every action/observation is preserved, append-only) but carries no notion of a "Claim" being supported by a subset of events — it's a full history, not a curated evidence chain.
- DSPy/GEPA's natural-language trajectory feedback is interpretable *reasoning* about why a score was given, but is tied to *optimization*, not to a durable, query-able Claim object.
- SWE-agent's linting feedback ties a specific edit to a specific validity check, which is the narrowest and most direct analog to "Evidence Record → Source" found in this research — but SWE-agent has no equivalent of "Claim" above that.

**Conclusion:** ARGON's `Claim → Evidence Record → Source → Verification Record` chain (Wave 3.5) is a synthesis that goes beyond any single source studied here — this research neither invents a new final schema (per instruction) nor claims external validation for one that didn't need it. It stays exactly as Wave 3.5 left it.

---

## 7. Required Experiments

| # | Topic | Hypothesis | Dataset/Tasks | Metric | Failure Condition | Promotion Condition |
|---|---|---|---|---|---|---|
| E1 | Retrieval relevance | A ranked Repo Map (doc-graph, P3) surfaces the same items C3's manual reads this session found central (ADR-004, ADR-005, ADR-024, ACR-1..5) | ARGON-HEALTH repo at a fixed snapshot; held-out set of past Task Packets from this session, not used to tune the ranker | Precision/recall of top-K ranked nodes against the manually-confirmed set | Top-K misses at least one node this session already confirmed as central | A promotion threshold (e.g. "X% of manually-confirmed central nodes in top-K") is **NEEDS EXPERIMENT** — no source or prior benchmark justifies a specific percentage; the correction pass removed an unsupported "90%+" figure that had no evidence behind it |
| E2 | Token savings | Budget-fitted ranked context (P2) uses fewer tokens than naive whole-file loading for equivalent task success | Same held-out Task Packets as E1 | Tokens consumed per successfully-completed task | Token savings require sacrificing task success rate | X% token reduction (X undetermined, NEEDS EXPERIMENT) with no drop in task success rate on held-out tasks |
| E3 | Stale-context detection | Comparing `head` vs `origin_head` at task start reliably flags drift before it causes a false Claim | Synthetic: deliberately advance origin between snapshot and use | Detection rate of induced drift; false-positive rate on unchanged repos | Any induced drift goes undetected | 100% detection on synthetic drift, 0% false positives on stable repos, on a held-out synthetic set |
| E4 | Context isolation | Two concurrent Task Packets against the same Repository Snapshot do not leak Claims/Evidence between each other | Synthetic: two adversarially-constructed concurrent tasks sharing scope | Cross-task reference leakage count | Any Claim from Task A is citable by Task B without an explicit Dependency record | Zero leakage across N synthetic concurrent-task trials (N undetermined, NEEDS EXPERIMENT) |
| E5 | Compression loss | A fact present before history-collapse (P5/P6) remains recoverable via its Source after collapse | Long synthetic session exceeding the collapse threshold, with a planted fact near the start | Recoverability of the planted fact post-collapse | Planted fact unrecoverable, or recoverable only via re-reading raw history rather than the Source pointer | Planted fact resolves correctly through Source in 100% of trials |
| E6 | Evidence preservation | Verification Record's chain-resolution check (Wave 3.5 v2, section 5) correctly rejects a Claim whose Source became unresolvable after `gathered_at` | Synthetic: deliberately break a cited Source (delete/move the file) after evidence gathering | Correct rejection rate of Claims resting on now-broken Sources | Any Claim advances `claim_status` past `asserted` on a broken Source | 100% correct rejection on a held-out set of deliberately-broken-Source trials |

All six explicitly hold out a validation/test set from whatever set is used to tune anything, per P10's discipline — none of these experiments has been run; all are proposed designs only.

**Note on the 100%/0% figures in E3–E6:** these are not empirically-derived quality thresholds like a relevance-precision target — they're correctness bars for deterministic operations (a string comparison either detects induced drift or it doesn't; a Claim either advances past `asserted` on a broken Source or it doesn't). There is no principled reason to accept less than 100% correctness on a mechanical check, so these are not the kind of number this correction pass's threshold discipline targets. E1's removed "90%+" was different in kind — a *quality* threshold for a ranking algorithm's precision, which does need empirical grounding and had none.

**Benchmark-validity caveat, applying to every score cited in section 2 (P4, P7, P8a, P15):** a benchmark score (e.g. SWE-bench Verified pass rate) is not a synonym for general agent quality. It reflects one benchmark's test suite, one model/version, one environment, at one point in time — it does not by itself establish that a passing patch is the *correct* fix (vs. one that happens to satisfy the test), does not rule out benchmark contamination, and does not transfer automatically across benchmark versions. Where this report cites a score (SWE-agent's ablation figure in P4; mini-swe-agent's ">74% SWE-bench verified" in P15; Agentless's SWE-bench-based validation in P7/P8a), it is cited as *that specific measurement*, not as proof of general capability, and none of these scores were independently re-run or audited by this Cloud.

---

## 8. Classification Summary

| Pattern | Classification |
|---|---|
| P1 — Ranked symbol graph | ADAPT (REJECT literal form for now) |
| P2 — Personalized ranking + adaptive budget | UNKNOWN (real audit-vs-efficiency tension) |
| P3 — ARGON doc-reference graph | ADOPT |
| P4 — Capped, guardrailed feedback | ADAPT |
| P5 — Bounded history collapse | ADOPT (window size UNKNOWN) |
| P6 — Event-sourced condensation | ADOPT structure; thresholds UNKNOWN/NEEDS EXPERIMENT |
| P7 — Hierarchical localization | ADOPT |
| P8a — Test-based filtering | ADOPT |
| P8b — Majority-vote final selection | REJECT |
| P9 — Plan/Act + checkpointed rollback | ADAPT |
| P10 — NL trajectory feedback + split discipline | ADOPT |
| P11 — Positional bias / ordering | ADOPT (as rendering constraint) |
| P12 — Two-tier memory (Letta) | ADAPT (structure only, reject self-editing) |
| P13 — Truncate vs. summarize (LlamaIndex) | ADOPT |
| P14 — Retrieve-then-rerank (Continue) | ADAPT (pays off unknown at current repo scale) |
| P15 — No-compression simplicity (mini-swe-agent) | UNKNOWN — direct counter-evidence to P5/P6 |
| Task isolation (section 3) | NEEDS EXPERIMENT — no external precedent found |

No item is called "best" or "production-ready" — every ADOPT/ADAPT is contingent on the experiment column, none of which has run.

---

## 9. Source Integrity Log

| # | Source | URL | Section cited | Exact behavior supported |
|---|---|---|---|---|
| 1 | Aider blog | aider.chat/2023/10/22/repomap.html | Body | tree-sitter tag extraction for ranking |
| 2 | Aider ranking summary | github.com/NousResearch/hermes-agent/issues/535 | Overview | 50x chat-file bias, 8x adaptive budget |
| 3 | SWE-agent paper summary | alphaxiv.org/overview/2405.15793 | Search/Nav, Editor, Context Mgmt | 50-result cap, linting, 5-turn collapse |
| 4 | SWE-agent paper (primary) | arxiv.org/pdf/2405.15793 | Ablation | linting removal to 15.0% (~3pt drop) |
| 5 | Agentless repo | github.com/openautocoder/agentless | README | 3-stage localization, repair, validation |
| 6 | Agentless paper | alphaxiv.org/abs/2407.01489 | Localization phase | file-to-element-to-line narrowing method |
| 7 | Agentless repo (usage) | github.com/OpenAutoCoder/Agentless/blob/main/README_swebench.md | Patch selection | majority voting confirmed |
| 8 | OpenHands docs | docs.openhands.dev/sdk/arch/events | Event System | immutable append-only log |
| 9 | OpenHands walkthrough | dev.to/truongpx396/openhands-deep-dive-build-your-own-guide-1al0 | Condensers | 80-event trigger, first-4/last-few retained, proactive+reactive |
| 10 | OpenHands docs | docs.openhands.dev/sdk/arch/agent | Agent responsibilities | condenser-based context management |
| 11 | Cline CLI reference | docs.cline.bot/cline-cli/cli-reference | Agent Behavior | Plan/Act mode definitions |
| 12 | Cline guide | deployhq.com/guides/cline | Checkpoints, YOLO Mode | shadow-git checkpoint/restore modes, YOLO risk |
| 13 | DSPy GEPA docs | github.com/stanfordnlp/dspy (GEPA overview) | Algorithm | NL trajectory feedback, not scalar-only |
| 14 | DSPy GEPA getting started | dspy.ai/getting-started/gepa-optimization | Data splits | trainset/valset/test-set discipline |
| 15 | Lost in the Middle | arxiv.org/abs/2307.03172 (via ai-papers.aktagon.com and beancount.io summaries) | Findings | U-shaped positional performance curve |
| 16 | Found in the Middle | themoonlight.io review of the calibration paper | Overview | U-shaped attention bias is architectural |
| 17 | Letta core concepts | docs.letta.com/core-concepts/ | Memory architecture | two-tier in-context/out-of-context memory |
| 18 | Letta memory guide | docs.letta.com/guides/agents/memory/ | Memory blocks | shareable, agent-editable memory blocks |
| 19 | Letta blog | letta.com/blog/agent-memory/ | Archival vs. recall | processed/indexed vs. raw history distinction |
| 20 | LlamaIndex docs | developers.llamaindex.ai/python/examples/agent/memory/summary_memory_buffer | Buffer comparison | truncate vs. summarize tradeoff, named explicitly |
| 21 | Continue docs | docs.continue.dev/customize/deep-dives/codebase | Codebase retrieval | nRetrieve=25 / nFinal=5 retrieve-then-rerank |
| 22 | mini-swe-agent repo | github.com/SWE-agent/mini-swe-agent | README | fully linear history, ~100 lines, no compression |

---

## 10. CLOUD CAPABILITY UPGRADE

*(Required appendix per the Common Cloud Evolution Super-Prompt, section 26.)*

**1. Sources Studied:** 22 sources actually opened this session (see section 9's Source Integrity Log for the full accounting) — Aider, SWE-agent, Agentless, OpenHands, Cline, DSPy/GEPA, Lost in the Middle / Found in the Middle, Letta, LlamaIndex, Continue, mini-swe-agent. All of C3's assigned priority list (section 19 of the Common Layer) is now covered; AutoCodeRover and SWE-ReX were not — out of C3's specific priority list (they're C4/C1 priorities respectively) and not pulled in without a C3-specific reason.

**2. High-Value Patterns:** P7/CONVERGENT EVIDENCE (hierarchical localization matching ARGON's own independently-stated rule) and P12 (Letta's shared, referenceable memory blocks — the closest external precedent found for ARGON's Source-shared-across-Evidence-Records design) are the two strongest findings — one because two independent designs agreed, the other because it's a real precedent for a design choice that otherwise had none.

**3. Patterns Rejected:** P8b (Agentless majority-vote final patch selection — contradicts ARGON's own no-majority-vote rule, rejected explicitly with reasoning, not just noted); the self-editing half of P12 (Letta's agent-rewritable memory — ARGON's evidence objects are deliberately write-once, so this part is rejected even though the shared-reference half is adopted).

**4. Token Efficiency Gains:** P2/P14's dynamic-budget and retrieve-then-rerank patterns both reduce blind whole-repo loading; P13's named truncate-vs-summarize tradeoff prevents defaulting to the costlier option out of habit rather than actual need.

**5. Model Portability:** Everything in this report is a structural/architectural pattern (graph ranking, memory tiering, retrieval staging, history handling) — none of it depends on a specific model's capabilities, consistent with the Common Layer's model-independent/model-adapter split (section 14). No pattern here required a specific vendor's tool-calling format or reasoning mode to work.

**6. Failure Modes:** P2 (dynamic budgets vs. clean audit booleans — real unresolved tension); P4 (capped search silently dropping the one needed hit); P8b (majority vote laundering away evidence-based disagreement); P15 (compression machinery built for a problem that may not exist at ARGON's actual task scale, adding complexity without benefit).

**7. Experiments (needing empirical validation):** E1–E6 (section 7), plus the new pre-experiment surfaced by P15 — measuring actual ARGON Cloud session length against a compression threshold before assuming P5/P6's machinery is needed at all.

**8. Transferable Principles (not vendor behavior):** (a) separate *what must always be visible* from *what's searchable on demand* (Letta); (b) name the truncate-vs-summarize tradeoff explicitly rather than defaulting silently (LlamaIndex); (c) stage retrieval as cheap-broad then costly-narrow, not one pass (Continue); (d) don't build compression machinery ahead of evidence that the problem it solves actually occurs at your own scale (mini-swe-agent, applied as a caution, not a rejection of P5/P6).

---

## 11. C7 v3 FINDING MATRIX

**Repeated, deliberately: no `C7-CLOUD-EVOLUTION-FINAL-AUDIT.v3` exists anywhere in this session** — this is the third pass referencing that filename, and it still does not exist, has not been produced, and has not been attached. The matrix below tracks the C3-specific items (D2, D3, D7, X5, P2, P14) exactly as spelled out in the correction-pass instructions themselves — the only actual source for these findings — with an Evidence column pointing to where the fix lives in *this* document, so C7 (whenever it actually runs) can check without depending on "trust me, it was fixed in an earlier pass."

| Finding | Status | What changed | Evidence |
|---|---|---|---|
| D2 — broken/untraceable citation tags | **FIXED** | All 32 instances of chat-only `(cite index="X-Y">...)` markup stripped; every claim now stands on its adjacent SOURCE line instead | Section 2, every pattern's **SOURCE:** line (URL + section + access date); Section 9, Source Integrity Log |
| D3 — broken cross-reference ("§4 pipeline design") | **FIXED** | §4 is "Freshness," never contained pipeline content — confirmed broken in a prior pass. Pipeline rebuilt self-contained in this document | "Design Output — Extended Pipeline" subsection at the end of Section 2; P14's ARGON ADAPTATION line now points there directly |
| D7 — unjustified "90%+" threshold | **FIXED** | Removed; no source or benchmark justified that figure | Section 7 (Required Experiments), E1 row + the note immediately below the table distinguishing correctness bars from quality thresholds |
| X5 — benchmark validity caveats | **FIXED** | Dedicated caveat added, applying to every benchmark score cited; score explicitly separated from general agent quality, fix-correctness, contamination | Section 7, note immediately below the experiments table |
| P2 — adaptive-budget vendor numbers not ARGON thresholds | **FIXED** | 50×/8× explicitly marked as Aider's own tuning; ARGON's value marked UNKNOWN/NEEDS EXPERIMENT | Pattern P2, "Explicit note, this correction pass" line |
| P14 — external observation vs. ARGON proposed pipeline | **FIXED** | Continue's retrieve-then-rerank kept as external observation (P14 itself); the ARGON pipeline moved to its own labeled `ARGON PROPOSAL` subsection, no longer conflated | Pattern P14 + "Design Output — Extended Pipeline" subsection, both Section 2 |
| C7 v3 baseline itself | **DISPUTED — EVIDENCE PROVIDED** (in the sense of: cannot be marked FIXED/REFRAMED/DOWNGRADED because it isn't a content finding — it's a missing input) | No such file exists in this session to audit against | This notice, repeated at the top of the document and here |

**Not touched by this pass, per instruction not to expand scope:** every pattern's ADOPT/ADAPT/REJECT/UNKNOWN classification (Section 8) — the substantive judgments were not part of any finding listed above.

---

## 12. What Remains UNKNOWN / NEEDS EXPERIMENT (consolidated)

Per the deliverable requirement for a short list — everything below is unresolved by design, not by oversight:

- P2 / P14: whether any specific budget-bias number or two-stage retrieval actually benefits ARGON at its current (53-file, no-code) scale — **NEEDS EXPERIMENT**.
- P5 / P6 / P15: the correct history-collapse window size for ARGON, and whether ARGON's task lengths even require compression at all (direct tension between P5/P6 and P15) — **NEEDS EXPERIMENT**.
- Section 3 (Task Context Isolation): no external precedent found; ARGON's multi-Cloud cross-task isolation is untested — **NEEDS EXPERIMENT**.
- Section 4 (Freshness): re-fetch and recompile triggers have no evidenced numeric or rule-based answer — **UNKNOWN / NEEDS EXPERIMENT**.
- E1's promotion threshold (retrieval relevance quality bar) — **NEEDS EXPERIMENT**, no number until real evidence exists.
- E2's token-savings percentage — **NEEDS EXPERIMENT**, same reasoning.
- E4's isolation-trial count (N) — **NEEDS EXPERIMENT**.
- Whether a separate AI-Engineering-OS repository exists at all — attempted check (this session, `api.github.com`), rate-limited, still **UNKNOWN**.
- The C6-vs-C7 verification-authority conflict (a Wave-3.5 matter, not this report's to resolve) remains open wherever it was last left.

---

## 13. Hash / Metadata Contract

Per this pass's explicit permission: `report_sha256: recorded_in_manifest`

The manifest (`C3-CONTEXT-ENGINE-RESEARCH.manifest.yaml`) is the canonical location for the real, final SHA-256 — computed after every edit in this pass, over this file's exact final bytes. Embedding that same hash inside this file would change the file's bytes and invalidate the hash just computed; this is a logical constraint, not a shortcut, and this pass's own instructions explicitly sanction recording it in the manifest instead.

---

**ARTIFACT_READY_FOR_TRANSFER: YES**

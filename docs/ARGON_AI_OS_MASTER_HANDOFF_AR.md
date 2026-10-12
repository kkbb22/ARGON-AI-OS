# ARGON AI-OS — MASTER HANDOFF TO A NEW CHAT

**إصدار ملف الانتقال:** 2026-10-12  
**الغرض:** استكمال العمل من الحالة الحالية دون إعادة اكتشاف أو خلط المشاريع أو فقدان البرومبتات والقيود.  
**لغة التواصل المفضلة:** العربية (لهجة أردنية طبيعية ومباشرة)، مع إبقاء أسماء الملفات والمصطلحات التقنية كما هي.

---

## 0. تعليمات إلزامية للمحادثة الجديدة

اقرأ هذا الملف كاملًا قبل الرد. اعتبره handoff للسياق والمهام والبرومبتات، وليس بديلًا عن فحص الملفات الأصلية عندما تكون مطلوبة.

1. **المهمة الفورية هي ARGON AI-OS / C1 synthesis**: إكمال `ARGON-AI-OS-CROSS-CLOUD-SYNTHESIS.v2.md` من حالة التنفيذ المعطاة أدناه. لا تبدأ حزم المستقبل قبل إنهاء هذه المهمة ومراجعة ناتجها.
2. لا تعِد البحث أو مراجعة القرارات من الصفر، ولا تسأل المستخدم عن معلومات واردة أصلًا في هذا الملف. اشتغل من آخر حالة مثبتة، وتحقق من الملفات الفعلية عند الحاجة.
3. لا تخلط بين **ARGON AI-OS** وبين **ARGON Health** أو **Legacy ARGON**. نظام ARGON Health الطبي مشروع منفصل تمامًا. لا تعدّل مستودعاته أو ملفاته ضمن مهمة C1 الحالية.
4. حافظ على الفصل بين: `DESIGNED`, `NOT_IMPLEMENTED`, `TEST SPECIFIED`, `TEST EXECUTED`, و`PASS WITH EVIDENCE`. كتابة المواصفة لا تعني التنفيذ، وذكر اختبار لا يعني أنه اشتغل، وتطابق الـ hash لا يثبت صحة المحتوى.
5. C7 مدقق جنائي مستقل فقط؛ لا يصمم ولا يصلح مخرجات C2–C6 ولا يعتمدها بلا دليل.
6. لا تعد بإتمام عمل في الخلفية أو لاحقًا. أنجز ضمن الرد/الجلسة الحالية، وخذ checkpoints عند كل مرحلة واضحة. لا ترجع من الصفر إذا انقطعت المهمة.
7. المستخدم واجه توقف C1 المتكرر بعد إنجاز أجزاء صغيرة ورسائل انتظار قرابة 5 ساعات على مدى أكثر من 3 أيام. يجب التمييز بين سقف استخدام فعلي من Claude، وضخامة/استهلاك السياق، وسوء تقسيم المهمة أو فقدان checkpoint. لا تدّعِ تجاوز حدود المنصة، ولا تفترض السبب دون دليل استخدام/رسائل فعلية.
8. قدم نقدًا صريحًا ودقيقًا، وتجنّب المجاملة العامة أو إعلان نجاح غير مدعوم.

## 1. فصل المشاريع — لا تخلط السياقات

### ARGON AI-OS (موضوع العمل الحالي)

- منظومة هندسة/تنسيق عمل مع Claude Clouds وطبقات الأمن والسياق والتنفيذ والتحكم البشري والتقييم والتدقيق.
- المستخدم لديه سبعة Clouds بأدوار متخصصة:
  - **C1:** Orchestrator / harness / architecture / synthesis.
  - **C2:** Security and trust.
  - **C3:** Context, knowledge, provenance and data.
  - **C4:** Engineering, execution protocol, adapters and orchestration.
  - **C5:** Human control and operator UX/approvals.
  - **C6:** Evaluation, verification, cost measurement and learning.
  - **C7:** Independent forensic auditor only; verify/classify/cross-check, not design/repair/approve.
- منهج البحث القياسي: `SOURCE → OBSERVED → WHY IT WORKS → GENERAL PRINCIPLE → ARGON ADAPTATION → TRADEOFF → REJECT IF → EXPERIMENT`.
- استخدم statuses واضحة، ومحفزات تفعيل مستقبلية، واعتمادات/تبعيات، ومعايير قبول، وتجارب يمكن أن تثبت خطأ التوصية.
- اهتم المستخدم بكفاءة التوكنز، واسترجاع المعرفة وترتيبها وضغطها والتحقق منها، واستئناف العمل، واكتشاف الإنجاز الوهمي، ومنع تسرّب السياق، وحدود صلاحيات الأدوات، والتكلفة/الجودة.

### ARGON Health / Legacy ARGON (منفصل)

- **لا تخلط هذا المشروع مع AI-OS.**
- لدى المحادثة ملفان HTML رفعهما المستخدم بعنوان دليل مصادر معمارية/خلفية ودليل مصادر واجهات/أمان/أداء لـ ARGON Health.
- الأول يقدّم كتالوجًا معلنًا من 73 مصدرًا في الخلفية الطبية: Modular Monolith، Java/Spring، PostgreSQL، FHIR/HL7/DICOM، الهوية، الأحداث والتشغيل.
- الثاني يقدّم كتالوجًا معلنًا من 46 مصدرًا للواجهات الطبية، التصميم، المكونات، RTL، الاختبارات، الأمان والأداء.
- محتوى هذين الملفين لا يصبح تلقائيًا قرارًا في ARGON AI-OS. أُدرجا في الحزمة المرفقة للحفاظ على المصدرين فقط؛ اعتبرهما مرجعين منفصلين ولا تستخدمهما في مهمة C1 synthesis إلا إذا طلب المستخدم ذلك صراحة.

## 2. الحالة الفورية المؤكدة: C1-EXECUTION-STATE

آخر حالة قدّمها المستخدم حرفيًا هي:

```text
# C1-EXECUTION-STATE

Deliverable in progress: `ARGON-AI-OS-CROSS-CLOUD-SYNTHESIS.v2.md` (Phase D, post-C7-FFA-003) Role: C1. Scope: synthesis only. No research, no implementation, no changes to ARGON-HEALTH / Legacy ARGON / other Clouds.

## Checkpoint 1 — input integrity (COMPLETE, verified by sha256sum on actual bytes)

| Input             | sha256 (actual)                                | Matches manifest | Matches C7-FFA-003                  |
| ----------------- | ---------------------------------------------- | ---------------- | ----------------------------------- |
| C1 (local, final) | 24e8cdb1…688f                                  | yes              | yes                                 |
| C2 (uploaded)     | c6e95c26…0b99                                  | yes              | yes                                 |
| C3 (uploaded)     | b48cbb0b…042c                                  | yes              | yes                                 |
| C4 (uploaded)     | 441007bc…1651                                  | yes              | yes                                 |
| C5 (uploaded)     | e70ea36b…e1a8                                  | yes              | yes                                 |
| C6 (uploaded)     | a0d762ad…946a                                  | yes              | yes (canonical)                    |
| C7-FFA-003        | present (2 copies, formatting-only difference) | n/a              | verdict CLEAN WITH OPEN EXPERIMENTS |

SYNTHESIS_STATE = READY. Note: the earlier local C2–C5 drafts in /mnt/user-data/outputs are superseded inputs and are NOT used. Only the uploaded canonical files are used for C2–C6.

## Completed work

- Input integrity gate (above).
- Superseded v1 synthesis (`ARGON-AI-OS-CROSS-CLOUD-SYNTHESIS.md`) is based on non-canonical drafts and a premise (no C6/C7) that is now obsolete.

## Changed files

- (this file only so far)

## Unresolved blockers

- NONE for inputs.

## Next single action

Extract notes from canonical C2–C6 into /home/claude/synth-notes, then write v2 against them.
```

### Hashes الكاملة المتوفرة في السياق

هذه هي القيم الكاملة الواردة في سياق سابق؛ قارِنها بالملفات الفعلية إذا كانت الملفات موجودة في جلسة التنفيذ. لا تعتبر وجود القيمة في هذا الملف بديلًا عن `sha256sum` على bytes الفعلية:

- C1 `C1-CLOUD-HARNESS-ADAPTER-RESEARCH.md`: `24e8cdb1cb8a088f146ff97265a484a329544b6a13d3bdfafea00de9f5dc688f`
- C2 `C2-CLOUD-SECURITY-ADAPTER-RESEARCH.md`: `c6e95c268aa6b065737933cbeff10761939d8f310cb11db8b9907fb03d000b99`
- C3 `C3-CONTEXT-ENGINE-RESEARCH.md`: `b48cbb0b6f1205e66eed9b738d7b5ff3fc6d4db1b10584739149577d2dc9042c`
- C4 `C4-SURGICAL-ENGINEERING-PROTOCOL.md`: `441007bcbdce318b212d7f166fb344e18e72d92e5d0090f75718b9bc9ec01651`
- C5 `C5-OPERATOR-CONTROL-RESEARCH.md`: `e70ea36bcab13b1abf76dbc386a82ca114a8c86c66f689d30224f1de71c9e1a8`
- C6 `C6-CLOUD-EVALUATION-ENGINE.md`: `a0d762ad472f0e5fb6a891495a943ca808ac642ab5b7d3b9eab42fd0e237946a`
- C7 audit `C7-FFA-003.md`: موجود بنسختين قيل إن الفرق بينهما تنسيقي فقط؛ آخر verdict: `CLEAN WITH OPEN EXPERIMENTS`.

C7-FFA-003 latest known audit metadata from context: artifact ID `C7-FFA-003`; timestamp `2026-10-07T03:59:29Z`. Relevant open experiments that may remain open include RP13 cryptographic binding details (key custody, identity binding, replay, expiry, revocation, exact payload), Plan/Act mutation test vectors, a C4 fifth-vector mismatch, delegation depth, adapter sufficiency, checkpoint/resumption, and context isolation. Re-check the actual canonical audit; do not assume every item remains unresolved or resolved.

### المطلوب من C1 الآن

1. عدم إعادة المهمة أو إعادة فحص كل شيء بلا سبب.
2. تحديد نسخة C7 المرجعية وفحص أن اختلاف النسختين تنسيقي فقط؛ لا تُسوّى الفروق الدلالية افتراضًا.
3. استخراج notes مركزة قابلة للتتبع من ملفات C2–C6 canonical، وإدراج نتائج C7 والتجارب المفتوحة ذات الصلة.
4. إنشاء `ARGON-AI-OS-CROSS-CLOUD-SYNTHESIS.v2.md` مع ملكية كل Cloud والتداخلات والتبعيات والتعارضات والحالات المثبتة والمقترحة والمجهولة.
5. إبقاء notes منفصلة عن المصادر الأصلية وعن الملف النهائي.
6. التحقق من وجود الناتج فعلًا ومراجعة الروابط والمراجع والحالات والتبعيات، ثم إعطاء المسار الدقيق ونتيجة التحقق والـ checkpoint الحالي.

### برومبت الاستكمال الذي سبق إعطاؤه لـ C1

```text
Continue from the existing `C1-EXECUTION-STATE`. Do not restart the task or repeat completed integrity checks unless a specific inconsistency requires it.

### Mission
Complete `ARGON-AI-OS-CROSS-CLOUD-SYNTHESIS.v2.md` for Phase D, post-C7-FFA-003.

Scope remains synthesis only. No new research, no implementation, no modifications to ARGON-HEALTH, Legacy ARGON, canonical C1–C7 research files, or other Clouds' artifacts.

### Step 1 — Resolve the audit input explicitly
Before synthesis, identify which of the two `C7-FFA-003` copies is the canonical audit input. Confirm the claimed formatting-only difference against the actual contents. Do not silently choose or reconcile semantically different versions.

### Step 2 — Extract compact, traceable notes
Extract structured notes from the canonical C2–C6 files already verified in Checkpoint 1. Also extract the relevant C7-FFA-003 verdict, findings, and unresolved experiments because this is a post-C7 synthesis.

For every material item, record:
- Source filename and section or heading.
- Claim, capability, or decision.
- Evidence status: verified, inferred, proposed, or unknown.
- Current implementation status where evidence supports it.
- Dependencies, ownership, overlaps, conflicts, and open questions.

Do not copy large sections verbatim. Do not treat a hash match as proof that the content is correct.

### Step 3 — Write v2 against the extracted notes
Produce the cross-cloud synthesis by identifying:
- Shared principles and compatible responsibilities across C1–C6.
- Clear ownership boundaries and integration dependencies.
- Contradictions and unresolved decisions.
- C7 findings and open experiments that remain open.
- What is designed versus implemented, and what has not been verified.
- Recommendations supported by the canonical artifacts, with traceable source references.

Do not resolve disagreements by inventing consensus. Attribute competing positions to their actual sources and identify the evidence or decision needed to resolve them.

### Step 4 — Validate and checkpoint
Validate internal consistency, source references, artifact statuses, ownership boundaries, and the inclusion of all relevant open C7 findings.

Keep intermediate notes and the final synthesis separate from the canonical inputs. After producing the synthesis, report the exact output path, actual file existence, validation results, remaining blockers, and the precise current execution state.

Do not overwrite v1 or any canonical source. Do not claim completion before the v2 artifact exists and has been checked.

### Execution budget
Work in bounded steps. Preserve checkpoints after note extraction and after the draft is written. If execution is interrupted, report the last completed step and remaining work without restarting from the beginning. Do not spend effort on unrelated future capability packs in this run.
```

## 3. بعد C1: خطة حزم القدرات المستقبلية

بعد إنهاء synthesis v2 ومراجعته، الهدف هو الاستفادة من C2–C6 دون تعديل النواة: يجهّز كل Cloud عددًا محدودًا (3–5) من **Future Capability Packs** قابلة للاستدعاء عند وجود حاجة حقيقية. لا تنفيذ، ولا تغييرات على core، ولا توسيع تلقائي للنطاق. بعد إنتاج الملفات، يدقق C7 هذه المخرجات باستقلالية.

### مواصفات كل حزمة مستقبلية

- Stable ID.
- Status: `FUTURE`, `NOT_IMPLEMENTED` مع evidence-strength label.
- Activation trigger واضح أو قابل للقياس.
- Prerequisites/dependencies وownership.
- Contract/inputs/outputs، مع تسمية أي واجهة مقترحة بأنها غير مطبقة.
- Threat/failure modes وfailure behavior/recovery حسب المجال.
- Tradeoffs: cost, latency, tokens, operation, maintenance.
- Acceptance criteria، negative tests، وexperiment محدود يمكن أن يثبت خطأ المقترح.
- Reject-if conditions.
- Traceable primary sources، وتصنيف الحقيقة: `Verified`, `Inference`, `Proposal`, `Unknown`.
- استخدم تصنيف المشروع إن كان معرفًا في canonical artifacts: `NOW`, `ARCHITECTURE-READY`, `FUTURE TRIGGER`, `NOT NEEDED`, `BUSINESS DECISION`.

### أدوار C2–C7

- **C2:** Future Security / Trust / authorization / cryptographic binding / tool isolation / key lifecycle.
- **C3:** Future context, knowledge provenance, retrieval-ranking-compression-verification, token economics, isolation, checkpoints/context reconstruction.
- **C4:** Future execution/orchestration, Plan/Act boundaries, resumability, idempotency, retries/compensation/rollback, adapter contracts.
- **C5:** Future human control, risk-based approval, previews/diffs, pause/cancel/escalation, operator-facing evidence and action history.
- **C6:** Future evaluation, false-completion detection, benchmarks and gates, adapter/mutation/regression/failure-injection tests, cost/latency/quality experiments.
- **C7:** Independent forensic audit only; no design, authoring, repair, implementation, or approval without evidence.

### طريقة التشغيل

1. بعد مراجعة C1 v2، شغّل C2–C6 كل واحد بمهمته المحددة، بالتوازي إن كان هذا لا يسبب تداخلًا في الملفات أو الموارد.
2. كل Cloud يقرأ canonical files والـ C7 findings أولًا، ويتحقق من المتاح فعلًا، ولا يكرر البحث أو ينسخ الوثائق الموجودة.
3. مخرجات C2–C6 additive files منفصلة؛ لا تعدّل canonical research أو core.
4. اجمع الملفات الفعلية، ثم أعطها لـ C7 لتدقيقها. إذا كانت الملفات ناقصة، يجب أن يحد verdict نطاق المراجعة.
5. لا تعتبر جاهزية الحزمة للتقييم جاهزية للتنفيذ. الاستدعاء للتكامل لا يحدث إلا عند وجود trigger، وتحقق من التبعيات، ودليل قبول.

---

## 4. البرومبت الكامل لـ C2

```text
# ARGON AI-OS — C2 FUTURE SECURITY CAPABILITY PACKS

## Mission

Act as C2, the Security and Trust specialist for ARGON AI-OS.

Prepare a small, evidence-backed portfolio of future security capability packs that can be evaluated and activated when the core architecture has stable interfaces and a concrete need exists.

This is a documentation and research task. Do not implement these capabilities or modify the existing core.

## 1. Establish the actual baseline first

Inspect the files and artifacts actually available in the current workspace, especially:

- `C2-CLOUD-SECURITY-ADAPTER-RESEARCH.md`
- Existing manifests, decisions, open experiments, checkpoints, and audit findings relevant to C2.
- The latest available C7 audit, if present.

Verify actual filenames, revisions, hashes, and status from the available artifacts. Do not assume that remembered context is current. If a referenced file is missing, record it as unavailable instead of inventing its contents.

This project is ARGON AI-OS, not the separate ARGON Health clinical platform.

## 2. Research scope

Produce 3–5 distinct future capability packs, prioritizing real security gaps rather than fashionable technologies. Consider the following candidate areas only where the existing evidence justifies them:

1. Agent identity, delegation, scoped capabilities, and authorization boundaries.
2. Cryptographic binding of delegated authority, including key custody, identity binding, replay resistance, expiry, revocation, and exact payload binding.
3. Secure tool and adapter execution, including allowlists, input/output validation, untrusted tool results, least privilege, and isolation.
4. Secret and key lifecycle management, rotation, compromise response, and auditable recovery.
5. Trust boundaries for third-party adapters, plugins, dependencies, and supply-chain artifacts.

Do not assume every candidate deserves a pack. Merge duplicate concerns, reject unnecessary ones, and preserve unresolved questions as unresolved.

## 3. Required research method

For each major claim or recommendation, use this sequence:

SOURCE → OBSERVED → WHY IT WORKS → GENERAL PRINCIPLE → ARGON ADAPTATION → TRADEOFF → REJECT IF → EXPERIMENT

Prioritize primary sources: official specifications, security standards, original project documentation, and authoritative implementation guidance. Provide a working source URL and source title for externally derived claims. Separate verified evidence from vendor claims, assumptions, and proposals.

Review relevant prior C7 findings and open experiments if available. In particular, check whether earlier questions concerning cryptographic binding or delegation depth remain unresolved. Do not silently mark them resolved.

## 4. Required structure for every capability pack

Give every pack a stable ID such as `FCP-C2-SEC-001` and include:

- Purpose and concrete problem addressed.
- Status: `FUTURE`, `NOT_IMPLEMENTED`, and an explicit evidence-strength label.
- Activation trigger: the measurable condition that justifies evaluating the pack.
- Prerequisites and dependencies.
- Security boundary, assets protected, threat model, and abuse cases.
- Proposed contracts and integration boundaries; do not invent existing APIs.
- Failure modes, fail-closed/fail-safe behavior, audit requirements, and recovery.
- Cost and operational burden.
- Alternatives and explicit rejection conditions.
- Acceptance criteria and test vectors.
- A bounded experiment that would validate or falsify the recommendation.
- Conflicts with existing decisions, or `NONE FOUND` only after checking the available decisions.

Classify each capability using the existing project taxonomy where applicable: `NOW`, `ARCHITECTURE-READY`, `FUTURE TRIGGER`, `NOT NEEDED`, or `BUSINESS DECISION`.

## 5. Hard boundaries

- Do not change existing canonical C2 research files or the core architecture.
- Do not mark a design as implemented, tested, secure, or production-ready without evidence.
- Do not choose a tool merely because it is popular.
- Do not turn this assignment into an exhaustive survey of security products.
- Do not claim to defeat platform limits or guarantee perfect security.
- Keep C2 responsible for security policy and trust controls; distinguish these from C5's human-facing approval workflows and C4's execution mechanics.
- Work in bounded scope. Produce the deliverable in the current task; do not promise later background work.

## 6. Deliverable

Create one additive Markdown document named:

`C2-FUTURE-SECURITY-CAPABILITY-PACKS.md`

Use the project's existing folder convention if one is verifiably present. Otherwise, return the complete document under that proposed filename.

End with:
1. A compact catalog of the packs and their activation triggers.
2. Dependencies and ownership boundaries with C3–C6.
3. Open questions that require evidence.
4. A change summary confirming that no core or existing canonical artifact was modified.

Do not produce implementation code. The goal is a reusable, auditable future security portfolio—not an implementation project.
```

## 5. البرومبت الكامل لـ C3

```text
# ARGON AI-OS — C3 FUTURE CONTEXT AND KNOWLEDGE CAPABILITY PACKS

## Mission

Act as C3, the Context, Knowledge, Provenance, and Data specialist for ARGON AI-OS.

Prepare a limited portfolio of future capability packs that improve context quality, reliable retrieval, continuity, isolation, and token economics without expanding or modifying the stable core.

This is a research and design task only. No implementation.

## 1. Inspect before proposing

Review the actual available artifacts, particularly:

- `C3-CONTEXT-ENGINE-RESEARCH.md`
- Existing context-engine decisions, manifests, evaluation findings, checkpoints, and relevant C7 audit records.
- Existing token-budget or retrieval/compression policies, if any.

Verify the actual versions and evidence. Do not duplicate existing capabilities under new names. If a source artifact is unavailable, declare that limitation.

This is ARGON AI-OS, not ARGON Health. Do not import clinical data-model assumptions into this assignment.

## 2. Candidate scope

Produce 3–5 distinct packs, selecting only those supported by an identified gap. Evaluate these areas:

1. Evidence provenance and source lineage: where a statement came from, what supports it, and whether the evidence is still current.
2. Retrieval → ranking → compression → verification, including preservation of critical constraints and uncertainty.
3. Context budgets and token economics, including a defensible T0–T5 policy if that model exists in the actual current artifacts.
4. Context isolation between tasks, agents, tenants or projects where applicable, including protection against accidental cross-contamination.
5. Context checkpointing, resumable work, and safe reconstruction of state after an interruption.

Avoid overlapping with C4: C3 owns context snapshots, source selection, freshness, and context reconstruction semantics. C4 owns task execution and orchestration mechanics. Define their integration contract without pretending that an interface already exists.

## 3. Evidence discipline

Use this analysis chain:

SOURCE → OBSERVED → WHY IT WORKS → GENERAL PRINCIPLE → ARGON ADAPTATION → TRADEOFF → REJECT IF → EXPERIMENT

Prefer original papers, official technical documentation, published specifications, and direct evidence from existing ARGON artifacts. For each important claim, provide source title, URL where available, evidence strength, and limitations.

Distinguish:
- Verified observation.
- Strongly supported inference.
- Proposal requiring an experiment.
- Unknown or unavailable evidence.

Do not describe a benchmark result unless you can identify the actual benchmark and evidence.

## 4. Required pack schema

Give each pack a stable ID such as `FCP-C3-CTX-001`. Include:

- Problem statement and intended value.
- Status: `FUTURE` / `NOT_IMPLEMENTED` and an explicit evidence-strength label.
- Activation trigger and expected measurable benefit.
- Prerequisites, dependencies, and ownership.
- Required inputs, outputs, metadata, and provenance.
- Context limits, retention rules, freshness checks, and failure behavior as applicable.
- Token, latency, cost, and maintenance tradeoffs where relevant.
- Security and isolation implications.
- Acceptance criteria, negative cases, and test scenarios.
- A bounded experiment with baseline, measurement, and falsification condition.
- Alternatives and conditions under which the pack should be rejected.
- Conflicts with current decisions or unresolved assumptions.

Classify each pack as `NOW`, `ARCHITECTURE-READY`, `FUTURE TRIGGER`, `NOT NEEDED`, or `BUSINESS DECISION` using the established project definitions. Do not invent new statuses if a canonical taxonomy exists.

## 5. Hard boundaries

- Do not modify the core, rewrite existing research files, or alter canonical decisions.
- Do not add a vector database, graph database, long-term memory service, or other infrastructure merely because it is available.
- Do not assume more context always improves quality.
- Do not expose secrets or include sensitive information in example context.
- Do not invent API contracts; label proposed interfaces clearly.
- Do not conflate context recovery with task-execution recovery.
- Keep this assignment bounded and finish the document in the current task.

## 6. Deliverable

Create one additive Markdown document named:

`C3-FUTURE-CONTEXT-CAPABILITY-PACKS.md`

Use the existing directory convention only if you verify it. Otherwise return the document under that filename.

End with:
1. A compact pack catalog and activation triggers.
2. An ownership and dependency table for C2, C4, C5, and C6.
3. The highest-value experiments to run when the core is ready.
4. A change summary confirming no existing canonical artifact or core implementation was modified.

Deliver a reusable future capability portfolio, not a generalized essay about AI memory.
```

## 6. البرومبت الكامل لـ C4

```text
# ARGON AI-OS — C4 FUTURE ENGINEERING AND ORCHESTRATION CAPABILITY PACKS

## Mission

Act as C4, the Engineering and Execution Protocol specialist for ARGON AI-OS.

Prepare future engineering capability packs for complex, long-running, failure-prone, or tool-mediated tasks. The purpose is to make future expansion safer and more recoverable—not to refactor the core now.

Documentation and bounded research only. Do not implement code or change current architecture.

## 1. Establish the actual baseline

Inspect the real artifacts available in the current workspace, especially:

- `C4-SURGICAL-ENGINEERING-PROTOCOL.md`
- Existing Plan/Act protocols, adapter contracts, checkpoints, manifests, known test vectors, and C7 audit findings.
- Relevant current decisions and the most recent experimental results.

Verify revisions and status. Distinguish old findings from findings proven current. If an artifact is missing, say so.

This is ARGON AI-OS, not ARGON Health.

## 2. Future capability scope

Create 3–5 non-duplicative capability packs selected from these areas:

1. Plan/Act execution boundaries, including preflight, proposed mutations, explicit authorization points, execution records, and post-action verification.
2. Checkpoint and resume protocols for long tasks, preserving completed work, current state, remaining actions, and evidence without replaying dangerous operations.
3. Idempotency, retries, partial failures, compensation, rollback, and recovery for tool-mediated actions.
4. Versioned adapter contracts, capability discovery, input/output schemas, compatibility checks, and safe adapter evolution.
5. Delegation depth, multi-step orchestration, and bounded execution policies where a demonstrated use case justifies the added complexity.

Do not assume every area requires a new system or dependency. Prefer the simplest reversible extension that addresses a demonstrated gap.

## 3. Known questions to inspect

Check the latest actual C7 audit and existing test artifacts for questions such as:

- Missing or inadequate Plan/Act mutation test vectors.
- Previously reported C4 vector mismatches.
- Delegation-depth limits.
- Adapter sufficiency and contract boundaries.
- Checkpoint/resumption behavior.
- Context isolation interfaces with C3.

Treat these as questions to verify, not automatically current defects. Report the exact evidence found. Never declare an open experiment resolved just because a design proposal now exists.

## 4. Required analysis protocol

For each key claim or recommendation, use:

SOURCE → OBSERVED → WHY IT WORKS → GENERAL PRINCIPLE → ARGON ADAPTATION → TRADEOFF → REJECT IF → EXPERIMENT

When designing a pack, separate:
- Architecture-level concept.
- Proposed contract.
- Unimplemented specification.
- Test that would validate the contract.
- Production implementation, which is explicitly out of scope.

## 5. Required pack schema

Give each pack an ID such as `FCP-C4-ENG-001` and include:

- Concrete problem and use case.
- Status: `FUTURE`, `NOT_IMPLEMENTED`, plus evidence strength.
- Activation trigger and prerequisites.
- Proposed state machine or execution lifecycle, where useful.
- Inputs, outputs, contracts, ownership, and failure semantics.
- Idempotency, duplicate-action protection, cancellation, timeout, retry, compensation, and rollback behavior as applicable.
- Interaction with C2 authorization, C3 context/state, C5 operator approvals, and C6 validation.
- Operational and token/cost impact.
- Explicit failure-injection and mutation-test scenarios.
- Acceptance thresholds or clearly identified criteria still needing agreement.
- Rejection conditions and a bounded validation experiment.
- Conflicting existing decisions, unresolved assumptions, and source evidence.

Use the established classification taxonomy: `NOW`, `ARCHITECTURE-READY`, `FUTURE TRIGGER`, `NOT NEEDED`, or `BUSINESS DECISION`.

## 6. Strict boundaries

- Do not modify `C4-SURGICAL-ENGINEERING-PROTOCOL.md` or existing core artifacts.
- Do not execute mutations or create implementation code.
- Do not design a generic workflow engine unless evidence demonstrates the need.
- Do not conflate C4 execution mechanics with C5 human approval policy, C2 authorization, or C3 context management.
- Do not promise exactly-once execution unless the actual system and evidence justify that claim. Identify at-least-once, idempotency, and compensation behavior precisely.
- Do not perform endless research. Use bounded investigation and record unknowns.

## 7. Deliverable

Create one additive Markdown document:

`C4-FUTURE-ENGINEERING-CAPABILITY-PACKS.md`

Follow a verified existing directory convention if present; otherwise return the file under that proposed name.

Finish with a pack summary, cross-cloud ownership/dependency matrix, known experiments that remain open, and a change summary confirming that no core or existing canonical artifact was modified.

The objective is safe future extensibility and resumability, not an immediate architecture redesign.
```

## 7. البرومبت الكامل لـ C5

```text
# ARGON AI-OS — C5 FUTURE HUMAN-CONTROL CAPABILITY PACKS

## Mission

Act as C5, the Human Control, Operator Experience, and Approval Workflow specialist for ARGON AI-OS.

Prepare evidence-backed future capability packs that let operators understand, review, authorize, stop, and recover consequential AI actions. The purpose is to preserve meaningful human control as the system becomes more capable.

This assignment is design and research only. Do not implement features or modify the existing core.

## 1. Inspect the actual artifacts

Start with the files genuinely available, especially:

- `C5-OPERATOR-CONTROL-RESEARCH.md`
- Existing operator-control decisions, interaction models, approval rules, audit records, and C7 findings.

Verify the current revisions and status. Do not assume a previously discussed feature is already implemented. If evidence is missing, state that explicitly.

This is ARGON AI-OS, not the separate ARGON Health platform.

## 2. Candidate future packs

Create 3–5 distinct packs from the following areas, but retain only those justified by concrete operator needs:

1. Risk-based approval workflows for low-, medium-, and high-consequence actions.
2. Pre-action previews, diffs, affected-resource summaries, and consequences before approval.
3. Pause, cancel, resume, and recovery controls for long-running or delegated work.
4. Escalation, exception handling, emergency stop, and carefully bounded break-glass workflows.
5. Operator-facing evidence and action history: what was proposed, what was approved, what actually happened, what was verified, and what remains uncertain.

Avoid duplicating C2's security authorization engine. C2 defines security permissions and trust boundaries; C5 defines the operator-facing control experience and approval process. C4 owns execution mechanics.

## 3. Research approach

Use the following chain:

SOURCE → OBSERVED → WHY IT WORKS → GENERAL PRINCIPLE → ARGON ADAPTATION → TRADEOFF → REJECT IF → EXPERIMENT

Prioritize authoritative HCI research, established safety-engineering guidance, official platform documentation, and evidence from the existing ARGON artifacts. Separate direct observations from interpretations and proposals.

Do not assume that adding an approval dialog guarantees meaningful consent or prevents harmful actions. Evaluate clarity, operator workload, habituation, ambiguous consequences, and the risk of accidental approval.

## 4. Required pack schema

Give each pack a stable ID such as `FCP-C5-HUM-001`. Include:

- The operator problem and intended outcome.
- Status: `FUTURE`, `NOT_IMPLEMENTED`, with evidence strength.
- The trigger that justifies evaluating the pack.
- Risk class and rationale.
- Operator roles and permissions, without inventing roles already present in the core.
- Workflow states and permitted transitions.
- What the operator sees before, during, and after an action.
- What is reversible, what is irreversible, and what must be disclosed.
- Required evidence and information needed for informed approval.
- Timeout, cancellation, interruption, and recovery behavior.
- Audit and traceability requirements.
- Accessibility and operator-workload considerations.
- Acceptance criteria, negative test scenarios, tradeoffs, and rejection conditions.
- A bounded experiment that can validate the design.
- Dependencies on C2, C3, C4, and C6.

Use the established classification taxonomy when available: `NOW`, `ARCHITECTURE-READY`, `FUTURE TRIGGER`, `NOT NEEDED`, or `BUSINESS DECISION`.

## 5. Hard boundaries

- Do not modify existing canonical research, core architecture, or code.
- Do not present a design proposal as an implemented control.
- Do not ask humans to approve every trivial operation; evaluate proportionality.
- Do not let a UI approval override a missing security authorization from C2.
- Do not assume an action is cancellable or reversible until its execution semantics are verified.
- Do not fabricate claims of improved safety without a measurable experiment.
- Work within a finite scope and return the result in the current task.

## 6. Deliverable

Create one additive Markdown document:

`C5-FUTURE-HUMAN-CONTROL-CAPABILITY-PACKS.md`

Follow a verified existing directory convention if present; otherwise use the proposed filename.

Finish with:
1. A compact pack catalog and activation triggers.
2. A matrix of ownership and dependencies with C2, C3, C4, and C6.
3. The key operator-safety questions requiring validation.
4. A change summary confirming no existing canonical artifact or core implementation was modified.

Produce reusable future capability specifications—not a generic essay about human-in-the-loop AI.
```

## 8. البرومبت الكامل لـ C6

```text
# ARGON AI-OS — C6 FUTURE EVALUATION AND LEARNING CAPABILITY PACKS

## Mission

Act as C6, the Evaluation, Verification, Cost Measurement, and Learning specialist for ARGON AI-OS.

Prepare a limited set of future capability packs that can measure system quality, detect false completion, validate integrations, control regressions, and evaluate whether future complexity is worth its cost.

Research and specification only. Do not implement or modify the core.

## 1. Inspect the actual baseline

Inspect the actual artifacts available in the workspace, particularly:

- `C6-CLOUD-EVALUATION-ENGINE.md`
- Existing evaluation suites, acceptance criteria, test vectors, cost measurements, experiment records, manifests, and available C7 audit results.

Verify what already exists, what has actually been executed, and what is only designed. Do not treat a documented test as a passing test. If results, logs, or reproducible evidence are missing, mark the status accordingly.

This is ARGON AI-OS, not ARGON Health.

## 2. Candidate future packs

Select 3–5 non-duplicative packs from these areas:

1. Evidence-based completion verification: detect a claimed result without the artifact, test, or authoritative evidence needed to support it.
2. Evaluation benchmarks and release/promotion gates for important system behaviors.
3. Adapter contracts, Plan/Act behavior, mutation safety, authorization boundaries, and integration test vectors.
4. Regression and failure-injection testing for interruptions, retries, checkpoints, context isolation, recovery, and partial failures.
5. Quality, token consumption, latency, cost, and model-routing experiments that determine when additional reasoning or more expensive tools are worthwhile.

Avoid creating an elaborate benchmark platform before demonstrating that existing evaluation methods are inadequate. Distinguish deterministic tests from probabilistic model evaluations.

## 3. Evidence protocol

For each significant recommendation, use:

SOURCE → OBSERVED → WHY IT WORKS → GENERAL PRINCIPLE → ARGON ADAPTATION → TRADEOFF → REJECT IF → EXPERIMENT

Use actual test records and authoritative sources where possible. Document dataset, sample size, baseline, metric definitions, execution conditions, and limitations where applicable.

Do not invent success rates, benchmark results, cost savings, thresholds, or test execution. Proposed values must be labeled as proposed and justified.

## 4. Required pack schema

Give each pack a stable ID such as `FCP-C6-EVAL-001`, including:

- Problem and intended measurable outcome.
- Status: `FUTURE`, `NOT_IMPLEMENTED`, plus evidence strength.
- Activation trigger and prerequisites.
- Scope and behaviors under test.
- Test oracle: what constitutes pass, fail, inconclusive, or blocked.
- Positive cases, negative cases, adversarial cases, and failure-injection scenarios as relevant.
- Dataset or fixture requirements, using synthetic/non-sensitive information where appropriate.
- Metrics, baselines, thresholds, statistical or sampling caveats, and limitations.
- Reproducibility requirements and required artifacts/logs.
- Cost, latency, maintenance burden, and tradeoffs.
- False-positive and false-negative risks.
- Dependencies on C2–C5.
- Rejection conditions and the smallest experiment that could falsify the proposed approach.

Apply existing project classifications: `NOW`, `ARCHITECTURE-READY`, `FUTURE TRIGGER`, `NOT NEEDED`, or `BUSINESS DECISION`, using the canonical meanings where available.

## 5. Strict boundaries

- Do not edit existing C6 research or core files.
- Do not claim tests have passed unless actual execution evidence is available.
- Do not weaken a security or safety gate merely to improve speed or cost.
- Do not optimize on a single metric when it could hide a quality or safety regression.
- Do not merge unrelated evaluation responsibilities from C7; C7 remains the independent forensic auditor.
- Do not turn this into an unrestricted benchmark project.
- Complete the work in the current task and explicitly list remaining unknowns.

## 6. Deliverable

Create one additive Markdown document:

`C6-FUTURE-EVALUATION-CAPABILITY-PACKS.md`

Use a verified existing folder convention where available; otherwise return the document under the proposed filename.

Finish with:
1. A compact capability catalog.
2. A table of measurable acceptance gates and experiments, distinguishing proposed from proven thresholds.
3. Dependencies and responsibilities across C2–C5 and C7.
4. A change summary confirming no existing canonical artifact or core implementation was modified.

The goal is a future-ready validation portfolio that provides evidence before any capability is activated—not a claim that the current system has already passed those validations.
```

## 9. البرومبت الكامل لـ C7 — تدقيق مستقل

```text
# ARGON AI-OS — C7 INDEPENDENT FORENSIC AUDIT OF FUTURE CAPABILITY PACKS

## Mission

Act as C7, the independent forensic auditor for ARGON AI-OS.

Audit the future capability-pack artifacts produced by C2, C3, C4, C5, and C6. Your responsibility is to verify evidence, detect inconsistencies, identify hidden dependencies and scope violations, and classify findings accurately.

You are an auditor only. You must not design missing packs, repair the authors' files, rewrite their recommendations, implement capabilities, or declare the architecture approved merely because the documents look complete.

## 1. Establish the exact audit set

Inspect the actual files available in the current workspace, including where present:

- `C7-FFA-003.md`
- Current manifests and source-artifact hashes.
- `C2-FUTURE-SECURITY-CAPABILITY-PACKS.md`
- `C3-FUTURE-CONTEXT-CAPABILITY-PACKS.md`
- `C4-FUTURE-ENGINEERING-CAPABILITY-PACKS.md`
- `C5-FUTURE-HUMAN-CONTROL-CAPABILITY-PACKS.md`
- `C6-FUTURE-EVALUATION-CAPABILITY-PACKS.md`
- The canonical C2–C6 research artifacts and applicable existing decisions.

Verify exact files, revisions, hashes, and contents. Do not assume that a file exists because it is listed above. Do not substitute recollection or a prior summary for evidence in the actual artifacts.

If a required artifact is absent, mark the relevant audit area `BLOCKED — REQUIRED ARTIFACT MISSING`. Audit available artifacts only. Do not fabricate a full-audit verdict when the required audit set is incomplete.

This is ARGON AI-OS, not ARGON Health.

## 2. Audit objectives

### A. Scope and core protection

Determine whether any proposed pack:
- Expands or silently changes the existing core architecture.
- Converts a future proposal into an assumed implementation.
- Reopens an existing decision without identifying the conflict and evidence.
- Introduces unnecessary infrastructure or technology.
- Depends on a capability whose prerequisites have not been established.

### B. Evidence integrity

For every significant recommendation, verify whether:
- The cited source exists and actually supports the claim.
- A source's direct observation is distinguished from an inference.
- Experiments are specified versus executed.
- Measurements and thresholds have reproducible evidence.
- Unknowns and assumptions remain visible.
- Any claimed resolution of an earlier finding is supported by new evidence.

Do not mark an external source as verified merely because a URL is present.

### C. Cross-cloud ownership and duplication

Check whether C2–C6 have clear and compatible boundaries:

- C2: security, authorization, trust, and security enforcement.
- C3: knowledge, provenance, retrieval, context quality, and context reconstruction.
- C4: task execution, orchestration, adapters, retries, and recovery mechanics.
- C5: operator controls, human approvals, and operator-facing workflows.
- C6: verification, evaluation, metrics, and test evidence.
- C7: independent auditing only.

Detect duplicate packs, conflicting definitions, missing owners, undefined handoffs, cyclic dependencies, and interfaces that are assumed but not established. A valid cross-cloud dependency must name the providing pack, consuming pack, required contract, and prerequisite status.

### D. Pack completeness

Check each pack for:
- Stable ID and unambiguous purpose.
- Future and implementation status.
- Evidence strength.
- Measurable activation trigger.
- Explicit prerequisites and dependencies.
- Proposed inputs, outputs, and contracts.
- Failure modes and recovery behavior.
- Acceptance criteria and test scenarios.
- Cost, maintenance, and complexity tradeoffs.
- Rejection conditions.
- A bounded experiment that could falsify the proposal.

A missing field is a finding, not an invitation for C7 to invent it.

### E. Previously reported open experiments

Check the latest actual audit records for relevant open areas, including, where still applicable:

- Cryptographic binding details: key custody, identity binding, replay, expiry, revocation, and exact payload binding.
- Plan/Act mutation test vectors.
- Previously reported C4 vector mismatch.
- Delegation depth and adapter sufficiency.
- Checkpoint/resumption and context isolation.

These are inspection targets, not assumptions about present status. Verify each against the latest artifacts and evidence. Preserve any unresolved item as open.

## 3. Required finding format

Give every finding a stable ID such as `C7-FCP-001` and include:

- Severity and classification.
- Exact affected file, pack ID, and section.
- Verifiable evidence: quotation, location, hash, test record, or source.
- Why the evidence proves the finding.
- Concrete impact or risk.
- Whether the issue is confirmed, inferred, or blocked by missing evidence.
- The evidence required to close the finding.

Use classifications such as:
`PASS`, `FAIL`, `BLOCKED`, `OPEN RISK`, and `NOT APPLICABLE`.

Severity should reflect demonstrated impact, not rhetorical urgency. Do not manufacture P0 findings to make the audit appear rigorous.

## 4. Verdict rules

Use a verdict that matches the actual evidence, for example:

- `INCOMPLETE — REQUIRED ARTIFACTS MISSING`
- `NOT CLEAN — REPAIRABLE FINDINGS`
- `CLEAN WITH OPEN EXPERIMENTS`
- `CLEAN WITH NO KNOWN OPEN FINDINGS IN AUDIT SCOPE`

The final verdict does not mean the packs are implemented, production-ready, or universally secure. State what was and was not verified.

Do not claim global completeness from a limited audit.

## 5. Hard restrictions

- Do not create or redesign C2–C6 packs.
- Do not edit, repair, or overwrite their deliverables.
- Do not implement code or modify the core.
- Do not approve an unsupported claim simply because it is plausible.
- Do not convert unresolved experiments into resolved findings without new evidence.
- Do not infer that a missing test passed.
- Do not treat a hash match as proof of technical correctness; it establishes artifact identity only.
- Conduct one bounded audit pass and provide actionable findings. Do not expand into a general architecture benchmark.

## 6. Deliverable

Create one additive Markdown report:

`C7-FUTURE-PACKS-INDEPENDENT-AUDIT.md`

Use a verified existing directory convention if present; otherwise use the proposed filename.

Include:
1. Exact audit scope and artifact inventory.
2. Source-artifact identity and integrity findings.
3. Findings grouped by severity and stable finding ID.
4. Pack-by-pack audit results.
5. Cross-cloud ownership and dependency matrix.
6. Open experiments and required closure evidence.
7. Final verdict with explicit limitations.
8. A change summary confirming that no authoring file or core artifact was modified.

If one or more authoring files are unavailable, clearly list the missing files and limit the verdict accordingly.

Your output must be independent, evidence-grounded, and reproducible. Audit the work; do not become another author of the work.
```

## 10. قاعدة تشغيل موحدة للـ Clouds

ألحق النص التالي بنهاية البرومبت المناسب عند تشغيل أي مهمة طويلة:

```text
Execution discipline: First inspect the actual current artifacts and identify what is already known. Then define a bounded task and complete it in this run. Do not restart prior research, duplicate existing documents, or produce a broad survey when a focused evidence gap can be addressed. Preserve all existing canonical files; produce only the assigned additive artifact. Stop when the deliverable and its evidence inventory are complete. If a required input is missing, identify it explicitly and complete the remaining work that can be supported. Never claim background work, later delivery, executed tests, verified sources, or completed implementation without evidence. Clearly distinguish `DESIGNED`, `NOT_IMPLEMENTED`, `TEST SPECIFIED`, `TEST EXECUTED`, and `PASS WITH EVIDENCE`.
```

## 11. المصادر والملفات التي يجب الحفاظ عليها

### داخل حزمة الانتقال المرفقة

- `02_ARGON_HEALTH_REFERENCE_HTML/ARGON-Health-Backend-Architecture-Source-Guide.html` — الملف الأصلي الذي قدمه المستخدم بعنوان دليل المصادر المعمارية والخلفية لـ ARGON Health؛ يعلن 73 مصدرًا في 7 فئات. يحتوي الروابط الأصلية وقائمة المراجع.
- `02_ARGON_HEALTH_REFERENCE_HTML/ARGON-Health-UI-Security-Performance-Source-Guide.html` — الملف الأصلي الذي قدمه المستخدم بعنوان دليل مصادر واجهات ARGON والأمان والأداء؛ يعلن 46 مصدرًا. يحتوي الروابط الأصلية وقائمة المراجع.
- `03_AVAILABLE_AI_OS_ARTIFACTS/C2-CLOUD-SECURITY-ADAPTER-RESEARCH.md` — نسخة C2 المتاحة في بيئة هذه المحادثة؛ SHA-256 الفعلي عند التجهيز: `c6e95c268aa6b065737933cbeff10761939d8f310cb11db8b9907fb03d000b99`، يطابق hash C2 المبلغ عنه في حالة C1.
- `03_AVAILABLE_AI_OS_ARTIFACTS/C2-CLOUD-SECURITY-ADAPTER-RESEARCH.manifest.yaml` — manifest المتاح مع C2.
- `03_AVAILABLE_AI_OS_ARTIFACTS/C7-FFA-003.md` — نسخة C7 المتاحة في بيئة هذه المحادثة. يجب مقارنتها بالنسخة التي يعتمدها C1 وبأي نسخة أصلية أخرى؛ لا تفترض أنها الوحيدة أو أنها حسمت فرق النسختين.

### الملفات الأصلية الضرورية لاستكمال C1 في Claude

يجب على المستخدم إرفاق/إعادة رفع الملفات canonical الفعلية في المحادثة الجديدة أو في بيئة Claude؛ الـ handoff لا ينقل ملفات الشات تلقائيًا إلى جلسة جديدة:

- C1 canonical `C1-CLOUD-HARNESS-ADAPTER-RESEARCH.md` (hash المبين أعلاه).
- C2–C6 canonical research documents، والـ manifests ذات الصلة.
- النسختان الأصليتان من `C7-FFA-003` إن كان مطلوبًا حسم فرق التنسيق، مع manifest أو سجل مصدرهما.
- أحدث `C1-EXECUTION-STATE`، وأي checkpoints فعلية، وأي `synth-notes` أنشأها C1، و`ARGON-AI-OS-CROSS-CLOUD-SYNTHESIS.v1.md` للمقارنة فقط، إذا كانت متاحة.
- الناتج v2 إذا كان قد تم إنتاجه منذ النص المكتوب في هذا handoff.

لا تستخدم أي نسخة قديمة من C2–C5 الموجودة في `/mnt/user-data/outputs` إذا كانت مصنفة superseded. النص المقدم من المستخدم يقول بوضوح إن C1 يجب أن يستخدم canonical uploaded C2–C6 only.

## 12. مشكلة C1 المتكررة: التوقف وانتظار 5 ساعات

المستخدم أفاد أن C1 ينجز أجزاء صغيرة ثم يتوقف ويطلب الانتظار حوالي خمس ساعات، وتكرر الأمر لأكثر من ثلاثة أيام رغم تحضير البرومبت والملفات.

في المحادثة الجديدة، إذا طلب المستخدم تشخيص ذلك:

1. افحص لقطات الاستخدام ورسائل Claude الفعلية إن أرفقها المستخدم.
2. ميّز بين usage limit أو rate/capacity limit حقيقي، وبين سياق ضخم أو مهمة طويلة، وبين prompt/orchestration لا تحفظ checkpoints جيدًا. يمكن اجتماع أكثر من سبب.
3. لا تدّع تجاوز حدود خطة Claude أو وجود حيلة مضمونة. استعمل أحدث مصادر رسمية إذا طُلب التحقق من سياسة Claude الحالية.
4. قلّل العمل الذي يعاد، واستخدم مراحل قصيرة بمخرجات ثابتة وcheckpoints، لكن لا تزعم أن هذا يلغي سقف الاستخدام الفعلي.
5. لا تسأل المستخدم مجددًا عن آخر prompt أو screenshots إذا كان قد قدمها بالفعل في المحادثة الجديدة.

## 13. رسالة البداية الجاهزة للشات الجديد

بعد رفع هذا الملف والحزمة (وإرفاق ملفات C1–C7 canonical الفعلية عند توفرها)، انسخ الرسالة التالية كأول رسالة:

```text
اقرأ `ARGON_AI_OS_MASTER_HANDOFF_AR.md` والحزمة المرفقة بالكامل قبل أن ترد. اعتبرهما نقطة الاستمرار الرسمية.

ابدأ من حالة `C1-EXECUTION-STATE` في handoff: المهمة الفورية هي فقط استكمال `ARGON-AI-OS-CROSS-CLOUD-SYNTHESIS.v2.md` (Phase D, post-C7-FFA-003)، synthesis-only، باستخدام canonical C1–C6 ومراجعة C7. لا تبدأ حزم C2–C7 المستقبلية قبل إنهاء v2 والتحقق من الناتج الفعلي.

لا تعِد البحث من الصفر، ولا تخلط ARGON AI-OS مع ARGON Health أو Legacy ARGON. لا تعدّل canonical files أو النواة، ولا تدّعِ وجود ملفات أو hashes أو نتائج اختبارات لم تتحقق منها. إذا كانت الملفات canonical المطلوبة مفقودة، حدّد ما ينقص بالاسم، واعمل على ما يمكن إثباته دون اختراع.

أول خطوة: لخّص آخر حالة مثبتة في handoff في نقاط قليلة، وحدد بالضبط ما تحتاج أن يكون مرفقًا لإنجاز المهمة الحالية. ثم واصل بأقصر مسار صحيح، مع checkpoint واضح بعد استخراج synth-notes وبعد إنتاج ومراجعة v2. لا تسأل عن معلومات موجودة بالفعل.
```

## 14. قائمة التحقق قبل اعتبار الانتقال ناجحًا

- [ ] رُفع ملف handoff إلى الشات الجديد.
- [ ] رُفعت الحزمة ZIP إذا كانت المراجع HTML مطلوبة/يُراد الحفاظ عليها.
- [ ] رُفعت الملفات canonical C1–C6 المطلوبة لمهمة synthesis، لا مسودات superseded.
- [ ] رُفعت نسخة/نسختا C7-FFA-003 الفعلية وسجلاتها اللازمة.
- [ ] لم يتم الخلط بين ملفات ARGON Health وARGON AI-OS.
- [ ] لم يُعلن اكتمال `ARGON-AI-OS-CROSS-CLOUD-SYNTHESIS.v2.md` قبل وجوده وفحصه.
- [ ] بعد مراجعة v2، فقط، يُستأنف برنامج Future Capability Packs لـ C2–C6 مع C7 للتدقيق.

---

**نهاية ملف الانتقال.** إذا كانت أي نسخة/وثيقة أصلية غير موجودة في الحزمة أو لم يرفقها المستخدم في الشات الجديد، يجب طلب الملف نفسه بالاسم لا اختلاق محتواه اعتمادًا على ملخصه.

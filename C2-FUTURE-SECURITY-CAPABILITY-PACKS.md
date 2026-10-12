# C2-FUTURE-SECURITY-CAPABILITY-PACKS.md

**Cloud:** C2 — Security and Trust, ARGON AI-OS (not the ARGON Health clinical platform)
**Nature:** Documentation and research only. No implementation. No existing artifact modified.
**Revision:** 2 — supersedes a baseline-less first draft of this same filename produced earlier in this conversation (`sha256: 2d16f91b45c84b137e2131bb782eb4e5b7a53310fe1ce38e6ad21a5ff99f86b2`). That draft is my own earlier output, not a canonical file; the corrections it needed are listed in §1.4.
**Prepared:** 2026-10-11
**report_sha256:** recorded_in_manifest (Hash Contract as the baseline defines it: this file never embeds its own hash; the computed value lives only in the sibling manifest `C2-FUTURE-SECURITY-CAPABILITY-PACKS.manifest.yaml`).

**Status vocabulary used throughout (and nothing stronger is claimed anywhere):**
`DESIGNED` — a design exists on paper. `NOT_IMPLEMENTED` — nothing is built. `TEST SPECIFIED` — a test is described but has not been run. `TEST EXECUTED` — a test was run (none were). `PASS WITH EVIDENCE` — a test was run and its evidence is attached (none exist). Every pack below is `DESIGNED` · `NOT_IMPLEMENTED` · `TEST SPECIFIED`. No pack is `TEST EXECUTED` or `PASS WITH EVIDENCE`.

**Evidence labels:** `E1` primary specification/standard text I read in this session (read depth is stated per source in §3). `E2` secondary implementation documentation citing a primary. `E3` vendor/commentary, not relied on. `E4` C2 proposal or inference, unvalidated until its experiment runs. Baseline-derived statements are marked `[BASELINE RP-n]`.

---

## 1. Baseline inspection (done first, from the actual files)

### 1.1 Artifacts inspected

| Artifact | Status | Evidence |
|---|---|---|
| `C2-CLOUD-SECURITY-ADAPTER-RESEARCH.md` (uploaded as `C2-CLOUD-SECURITY-ADAPTER-RESEARCH__1_.md`) | **AVAILABLE, read in full** | 77,548 bytes; 14 research patterns RP-1…RP-14; sha256 `c6e95c26…d000b99` computed this run and **equal** to the manifest's `report_sha256` (`PASS WITH EVIDENCE` for the hash match only) |
| `C2-CLOUD-SECURITY-ADAPTER-RESEARCH.manifest` (uploaded as `…_manifest__1_.yaml`) | **AVAILABLE** | sha256 `193bb80b…bc93`; `status: DESIGNED`, `implementation_status: NOT_IMPLEMENTED`, `evidence_status: DOCUMENTATION_ONLY`, `task_id: UNASSIGNED`, `created_utc: 2026-09-21T09:06:55Z`, `source_count: 14`, `system_scope: ai_engineering_os`, `wave: cloud-evolution-sprint` |
| `C7-CLOUD-EVOLUTION-FINAL-AUDIT.v3` and any other C7 audit | **UNAVAILABLE.** The baseline itself states this file "was never produced or shown to this Cloud." | none |
| `C2-WAVE3.5-SECURITY-RECONCILIATION-v2.md` (referenced by the baseline) | **UNAVAILABLE** | none |
| Correction Pass v1 / Final Correction Pass v4 documents | **UNAVAILABLE** (only their effects, as restated inside the baseline, are visible) | none |
| Decision register, open-experiments register, checkpoints, ADR/ACR, the 16-class threat model | **UNAVAILABLE** | none |
| Manifests or documents for C1, C3, C4, C5, C6, C7 | **UNAVAILABLE** | none |
| Definitions of the labels `NOW` / `ARCHITECTURE-READY` / `FUTURE TRIGGER` / `NOT NEEDED` / `BUSINESS DECISION` | **NOT FOUND** in any available artifact (0 occurrences in the baseline). The baseline uses a different vocabulary: `ADOPT` / `ADAPT` / `REJECT` / `NEEDS EXPERIMENT` / `UNKNOWN` / `REQUIRES HUMAN DECISION`. | grep, this run |
| Existing folder convention for C2 documents | Partly verifiable: a sibling `.manifest` file with a fixed key schema exists for the baseline. Folder location is not verifiable. | manifest |

### 1.2 What the baseline establishes about the system (not re-researched here)

- Everything in the baseline is a `DESIGN PROPOSAL`; it states that no pattern exists in ARGON today and "no runtime exists yet," Wave 4 (Kernel) has not started, and "no sandbox exists yet."
- ARGON's proposed control model is `PLAN → REVIEW → APPROVAL → ACT → VERIFY` (PLAN has "no mutation-capable execution path"). ARGON's decision labels are the four-way `ALLOW` / `REQUIRE REVIEW` / `REQUIRE HUMAN APPROVAL` / `DENY`. Its enforcement classes are `PROMPT-ONLY`, `TOOL/HARNESS ENFORCED`, `OS/PLATFORM ENFORCED`, `RUNTIME ENFORCED`. Rule locations are `Kernel` / `Runtime` / `Adapter` / `Platform` / `Repository`. Approval positions are Category, Exact Action, Exact Payload Binding, Cryptographic Binding. This document reuses these terms so it composes with the baseline.
- Standing rule from the baseline, applied here: `external precedent != ARGON requirement`.

### 1.3 Gap map — what the baseline already covers and what it does not

Methodology: I read all 14 patterns and checked the full text for topic terms (grep, this run). To avoid duplicating the baseline, packs reference `[BASELINE RP-n]` instead of restating it.

| Area in the assignment | What the baseline already holds | Verified gap this document addresses |
|---|---|---|
| 1. Agent identity, delegation, scoped capabilities | RP-8 (git attribution, forgeable metadata), RP-2/RP-5 (category approvals), RP-11 (privilege attached to "is a callable tool"), Approval Authority Model (narrow vs broad approval scope left `REQUIRES HUMAN DECISION`) | **No principal or delegation model** (0 occurrences of "principal"; 0 of "least privilege"). No treatment of who may act for whom, scope narrowing, or delegation depth. → **SEC-001** |
| 2. Cryptographic binding of delegated authority | RP-13 (`NEEDS EXPERIMENT`, six open sub-questions, evidence rated `EMERGING/LOW-ADOPTION`), RP-14 | Mechanism-level evidence is weak. Standards-grade semantics for each sub-question can be added without changing RP-13's classification. → **SEC-002** |
| 3. Secure tool and adapter execution | RP-1, RP-2, RP-3, RP-5, RP-9, RP-10, RP-11, RP-12 (most already `ADOPT` as design direction) | A single contract tying tools to scopes and credentials; credential-audience separation / no token passthrough from the MCP protocol project's own text; the "is third-party MCP in scope" gate. → **SEC-003**, deliberately thin |
| 4. Secret and key lifecycle | RP-12 (secrets never enter context; one vendor blog, `MODERATE`), RP-13 (key custody open), "revocation unsolved" | Rotation, retirement, compromise response and recovery are not addressed ("rotation" appears once, incidentally). → **SEC-005** |
| 5. Third-party adapters, plugins, dependencies, supply chain | RP-11 (connect-time vs runtime trust, rug pull) | **No artifact-provenance or supply-chain treatment** (0 occurrences of "supply," "SLSA," "SBOM"; "provenance" appears only in the unrelated "Provenance Paradox"). → **SEC-004** |

### 1.4 Corrections to my earlier baseline-less draft (not silently cleaned)

1. **Delegation depth.** The earlier draft left RFC 8693's handling of nested `act` as "not verified." It is now verified from the full RFC text (§4.1) — see SEC-001.
2. **RFC 9421 parameters.** Earlier marked `E2` (library docs). Now `E1` from RFC §2.3 and §3.2.1, read in this session (read depth: §1–§3.2.1 and the table of contents; §7 Security Considerations was *not* read).
3. **NIST SP 800-57 attribution.** The earlier draft listed "cryptoperiod" among Rev. 5's subjects. That wording came from an excerpt of an *older* edition. Rev. 5's own keyword/abstract excerpts show: compromise, backup, archive, key recovery, key-inventory management, key management policy, metadata protection. "Cryptoperiod" is no longer attributed to Rev. 5, and no cryptoperiod values are proposed.
4. **OWASP attribution.** The earlier draft credited the OWASP LLM06 page with "enforce controls outside the model." That sentence came from a secondary summary (`E2`). The OWASP page excerpt supports the three root causes (excessive functionality, permissions, autonomy). The enforcement-independence principle is carried by `[BASELINE RP-3]` instead.
5. **Missing baseline items.** The earlier SEC-003 omitted RP-7 (repository-resident config channel), RP-9 (gate config out of agent reach), RP-10 (sandbox-configuration injection) and RP-11's manifest-change re-validation. Now included by reference.
6. **Vocabulary.** The earlier draft used `ALLOW/DENY/REQUIRE-APPROVAL`; replaced with ARGON's four-way labels.
7. **Previously unverifiable statements** (C3/C6 roles, conflicts) are now re-checked against the baseline in §6 and §5.

---

## 2. Executed checks this run (everything else is unexecuted)

| Check | Result |
|---|---|
| sha256 of baseline `.md` vs manifest `report_sha256` | **Equal** (`c6e95c26…`) |
| Full read of baseline (all 1,233 lines, including previously truncated segments) | Done |
| Term search of baseline for delegation/depth/principal/supply/SLSA/SBOM/rotation/taxonomy labels | Done; results drive §1.3 |
| Full fetch and read of RFC 8693 (datatracker text, complete) | Done |
| Fetch of RFC 9421 (rfc-editor), read through §3.2.1 | Done; truncated by size at §3.3.1; §3.3 onward and §7 unread |
| Earlier searches (RFC 9449, MCP security, OWASP LLM06, SLSA v1.0, NIST SP 800-57r5) | Search-excerpt level only |
| Any test of any control, any code, any ARGON component | **None executed** |

---

## 3. Source register and claim ledger

| ID | Source (URL) | Read depth | Evidence |
|---|---|---|---|
| S1 | RFC 9449 DPoP — https://rfc-editor.org/rfc/rfc9449.html | Abstract, introduction, table of contents (excerpts) | E1 (partial) |
| S2 | RFC 8693 OAuth 2.0 Token Exchange — https://datatracker.ietf.org/doc/rfc8693/ | **Full text** | E1 |
| S3 | RFC 9421 HTTP Message Signatures — https://rfc-editor.org/rfc/rfc9421.html (info: https://rfc-editor.org/info/rfc9421) | §1–§3.2.1 + TOC | E1 (partial) |
| S4 | MCP Security Best Practices (2025-11-25) — https://modelcontextprotocol.io/specification/2025-11-25/basic/security_best_practices | Excerpts | E1 (partial) |
| S5 | OWASP LLM06:2025 Excessive Agency — https://owasp.org/www-project-top-10-for-large-language-model-applications/2_0_vulns/LLM06_ExcessiveAgency | Excerpt | E1 (partial) |
| S6 | SLSA v1.0 Levels — https://slsa.dev/spec/v1.0/levels | Excerpts | E1 (partial) |
| S7 | SLSA v1.0 Requirements — https://slsa.dev/spec/v1.0/requirements | Excerpts | E1 (partial) |
| S8 | NIST SP 800-57 Part 1 Rev. 5 — https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final | Publication page and keyword/abstract excerpts | E1 (partial) |
| S9 | Vendor article on an OWASP LLM Top 10 "2026 edition" — https://cycode.com/?p=13296 | Excerpt | **E3, not relied on** |
| S10 | Deno `@std/http` message-signature docs — https://jsr.io/@std/http/doc/unstable-message-signatures/ | Excerpt | E2 (corroboration only) |

| Claim | Source | Evidence |
|---|---|---|
| C1. Delegation keeps the actor's own identity separate from the subject; impersonation makes A indistinguishable from B. | S2 §1.1 | E1 |
| C2. The JWT `act` claim can express a chain of delegation by nesting. The outermost `act` is the current actor; nested ones are prior actors. | S2 §4.1 | E1 |
| C3. For access control, a token consumer MUST consider only top-level claims and the current actor; prior actors in nested `act` are informational only. | S2 §4.1 | E1 |
| C4. `may_act` states that one party is authorized to become actor for another; the authorization server can use it to decide whether delegation/impersonation is allowed. | S2 §4.4 | E1 |
| C5. RFC 8693 defines no maximum delegation depth and no rule narrowing scope across hops (not present anywhere in the full text). | S2 (absence in full text) | E1 (negative finding) |
| C6. The scope claim and limited token lifetime are suggested to mitigate delegation abuse; token syntax, semantics and trust model are explicitly out of scope. | S2 §5, §1 | E1 |
| C7. A token exchange creates no linkage between input and output tokens; propagating revocation is not a general property and is implementation-specific. | S2 §2.1 | E1 |
| C8. Omitting client authentication lets a compromised token be exchanged into other tokens by anyone holding it. | S2 §2.1 | E1 |
| C9. DPoP sender-constrains tokens via proof of possession of a key pair, in contrast to bearer tokens usable by any holder; it renders exfiltrated tokens alone unusable; its security considerations include proof replay, pre-generation, and nonce downgrade. | S1 | E1 (partial) |
| C10. RFC 9421 signs selected message components with a detached signature; the application profile MUST specify required covered components, key retrieval, allowed algorithms. | S3 §1, §1.4 | E1 |
| C11. Signature parameters include `created` (RECOMMENDED), `expires`, `nonce` (a random unique value for the signature), `alg`, `keyid`, `tag`. | S3 §2.3 | E1 |
| C12. `expires` is a hint from the signer; a verifier can reject a signature before it expires. Enforcing `nonce` uniqueness is an application-defined requirement. | S3 §3.1, §3.2.1 | E1 |
| C13. The signature parameters line is always the last line of the signature base, so a signature covers its own metadata and it cannot be substituted. | S3 §3.1 | E1 |
| C14. RFC 9421 does not itself cover message content; it relies on a separate Digest specification (Content-Digest). | S3 §1 | E1 |
| C15. Token passthrough (accepting a token not issued to the server and forwarding it downstream) is an anti-pattern explicitly forbidden by the MCP authorization spec; confused-deputy attacks target MCP proxy servers; proper token-audience separation is advised. | S4 | E1 (partial) |
| C16. Excessive agency has three root causes: excessive functionality, excessive permissions, excessive autonomy. | S5 | E1 (partial) |
| C17. SLSA v1.0 Build L1 = provenance exists; L2 = signed provenance from a hosted build platform; L3 = hardened build platform. Downstream verification must validate provenance authenticity. | S6, S7 | E1 (partial) |
| C18. NIST SP 800-57 Part 1 Rev. 5 (May 2020) covers the key-management lifecycle, emphasizes protecting key metadata, and adds access control, identity authentication and inventory management for keys and certificates. | S8 | E1 (partial) |

Open source-currency items are in §7 (S1/S3/S4/S6/S8 versions were not checked for newer revisions).

---

## 4. Capability packs

| ID | Name | Class (assignment taxonomy) | Baseline crosswalk |
|---|---|---|---|
| FCP-C2-SEC-001 | Agent identity and scoped delegation | `FUTURE TRIGGER` | New area; informs RP-2/RP-8/RP-11 |
| FCP-C2-SEC-002 | Cryptographic binding of delegated authority | `FUTURE TRIGGER` + `BUSINESS DECISION` | = RP-13, stays `NEEDS EXPERIMENT` |
| FCP-C2-SEC-003 | Tool and adapter execution boundary | `FUTURE TRIGGER` | Packages RP-1/2/3/5/7/9/10/11/12 |
| FCP-C2-SEC-004 | Third-party adapter and artifact trust | `FUTURE TRIGGER` + `BUSINESS DECISION` | New area; extends RP-11 |
| FCP-C2-SEC-005 | Secret and key lifecycle | `FUTURE TRIGGER` | New area; extends RP-12/RP-13 |

**On the labels.** The label definitions were not found in any artifact (§1.1), so I used plain meanings and did not assert `NOW` or `ARCHITECTURE-READY` for anything. Reason: both depend on the live architecture and stable interfaces, and the baseline says the Kernel/runtime does not yet exist. Where a pack's principles are already `ADOPT` as design direction in the baseline (SEC-003, SEC-005), the taxonomy owner may judge them `ARCHITECTURE-READY` at principle level; C2 cannot assert that without the definitions and the architecture.

---

### FCP-C2-SEC-001 — Agent identity and scoped delegation

**Status:** `FUTURE` · `NOT_IMPLEMENTED` · `DESIGNED` · `TEST SPECIFIED` · Evidence: `E1` (concepts), `E4` (ARGON mapping)
**Class:** `FUTURE TRIGGER`

**Purpose and problem.** Give each acting principal (human, Cloud/agent, adapter) a distinct identity, and make "X may do Y on behalf of Z" an explicit, scoped, checkable statement instead of ambient authority. The baseline has no principal model; its approval-scope question (narrow single-use vs broad persisted) is `REQUIRES HUMAN DECISION` and its own pattern RP-11 observes privilege attached to "is a callable tool" rather than to who produced the request.

**Research chain 1 — delegation semantics**
- **SOURCE:** S2 RFC 8693 (full text).
- **OBSERVED:** C1–C8 above. In particular, nested `act` is a history trail; the consumer must ignore prior actors for access control (C3); the RFC defines no depth limit or narrowing rule (C5); trust model and token syntax are left to deployments (C6); revocation propagation is not part of the protocol (C7).
- **WHY IT WORKS:** keeping subject and actor separately visible lets a resource authorize against the pair. `may_act` limits who may take the actor role. Ignoring prior actors keeps the consumer's decision simple and bounded.
- **GENERAL PRINCIPLE:** authority belongs to a (subject, actor) pair, is issued by a party that can refuse, and is narrowed by the issuer, not by consumers reading history.
- **ARGON ADAPTATION (E4):** because consumers ignore nested history (C3), any depth limit and any scope narrowing must be enforced **at issuance** by a C2-controlled authority, not at the point of use. These two rules are ARGON proposals; RFC 8693 does not supply them.
- **TRADEOFF:** an issuer is a new critical-path component; scope vocabulary maintenance is a standing cost; too coarse recreates ambient authority, too fine is unmanageable.
- **REJECT IF:** ARGON ends up with one trust domain, one acting principal per task, and no agent-to-agent or agent-to-adapter hand-off.
- **EXPERIMENT:** below.

**Research chain 2 — what the scope vocabulary must express**
- **SOURCE:** S5; `[BASELINE RP-1/RP-2]`.
- **OBSERVED:** excessive agency has three separable causes — functionality, permissions, autonomy (C16).
- **GENERAL PRINCIPLE / ARGON ADAPTATION (E4):** the three map onto three independent controls: the tool set a principal can see (functionality), the scopes attached to its delegation (permissions), and its decision tier among `ALLOW` / `REQUIRE REVIEW` / `REQUIRE HUMAN APPROVAL` / `DENY` (autonomy). Per the baseline control model, `PLAN` carries no mutation scope at all.
- **TRADEOFF / REJECT IF / EXPERIMENT:** as above.

**Delegation-depth status (answering the assigned check).** The baseline never raises delegation depth, and the C7 audit that might have is unavailable, so whether any *earlier C7 question* is resolved is **UNVERIFIABLE**. What is now verified is the standards fact (C3, C5). The ARGON maximum depth is **undecided** and is recorded as a `BUSINESS DECISION` plus `NEEDS EXPERIMENT` (Q4).

**Activation trigger (measurable; thresholds are proposals for C2/owner to confirm).** Evaluate when any holds, measured by inventory of principals and tools with mutation scope: (a) two or more distinct principals can invoke mutation-capable tools for the same task or tenant; (b) any principal can cause another principal to act (one or more hand-offs exist); (c) an audit or Evidence Record contains a mutation that cannot be attributed to a specific (requester, actor) pair; (d) third-party MCP servers are placed in scope (baseline decision pending).

**Prerequisites and dependencies.** A Kernel/Runtime with stable principal and task identity (`UNKNOWN` — Wave 4 not started); a stable tool catalog; an audit sink; C4 for enforcement points; C5 for human approval collection.

**Security boundary, assets, threat model, abuse cases.** *Assets:* repository and task data, mutation-capable operations, credentials reachable via tools, audit integrity. *Boundary:* issuing authority vs everything that presents or consumes delegations; issuance configuration must live outside agent reach (`[BASELINE RP-9]`). *Abuse cases:* (1) confused deputy — a broad-authority principal induced to act for a narrower requester; (2) scope widening across hops; (3) prompt-injected principal using its full ambient scope; (4) delegation outliving its purpose; (5) a principal self-issuing or self-approving its own delegation; (6) actor-token or subject-token theft (RFC 8693 §2.1: unauthenticated exchange lets a stolen token be converted, C8).

**Proposed contracts (E4; no existing API is assumed).**
- *Delegation record:* subject, actor, scope set, audience, issued-at, expiry, parent reference, depth counter, purpose tag.
- *Decision contract:* input = presenter identity + delegation + requested operation + resource; output = one of `ALLOW` / `REQUIRE REVIEW` / `REQUIRE HUMAN APPROVAL` / `DENY` + reason code + audit ID. Default `DENY`.
- *Issuer rules:* child scopes ⊆ parent scopes; child expiry ≤ parent expiry; depth ≤ the maximum (value open, Q4); actor must be named in a prior permitted-actor statement (the `may_act` idea, C4).
- *Enforcement class/location if built:* `RUNTIME ENFORCED`; policy at `Kernel`, issuance outside Cloud reach.

**Failure modes, fail-closed, audit, recovery.** Issuer unreachable → no new delegations; existing ones expire or are handled per SEC-002 revocation policy (open, Q6). Unknown scope or unknown actor → `DENY`. Depth exceeded → `DENY`. Audit: every issue, narrow, exchange, use, denial and revoke produces one append-only event with subject, actor, scope, audience, decision and reason. Recovery: revoke by delegation ID or by actor; re-issue after review.

**Cost and operational burden.** Moderate: scope-vocabulary upkeep, issuer availability, audit storage, per-hop latency.

**Alternatives and rejection conditions.** *Static per-Cloud allowlists:* cheaper and sufficient if triggers (a)–(d) never fire — prefer them then. *Adopt OAuth token exchange wholesale:* reject unless ARGON actually has an authorization server and needs interoperability; borrowing the `act`/`may_act` semantics alone is enough. *Impersonation semantics:* reject for agents — it makes the actor indistinguishable from the subject (C1), which defeats attribution.

**Acceptance criteria and test vectors (TEST SPECIFIED, none executed).**
- TV-001-A: child scope ⊄ parent scope → issuance denied.
- TV-001-B: child expiry later than parent's → issuance denied.
- TV-001-C: actor not named in the subject's permitted-actor statement → exchange denied.
- TV-001-D: chain deeper than the maximum → denied at issuance.
- TV-001-E: delegation presented to an audience it does not name → `DENY`.
- TV-001-F: a verifier given a token whose *prior* actor holds broader rights than the current actor decides only on the current actor (mirrors C3).
- TV-001-G: a principal attempts to issue or alter its own delegation → `DENY`, no path exists (`[BASELINE RP-9]` test).
- TV-001-H: every allow and deny emits exactly one audit event with a reason code.

**Bounded experiment.** Paper model only. Take the actual tool list when it exists, define the smallest scope vocabulary that separates them, and replay a fixed set of hypothetical multi-principal workflows. **Falsified if** the vocabulary needs about as many scopes as there are operations, or if a stated fraction of legitimate workflows is denied (fraction to be fixed before running).

**Conflicts with existing decisions.** Baseline-visible: none contradicts this pack, and it is consistent with RP-8/RP-9/RP-11. Full conflict check against the decision register: **UNVERIFIABLE — register unavailable.**

---

### FCP-C2-SEC-002 — Cryptographic binding of delegated authority

**Status:** `FUTURE` · `NOT_IMPLEMENTED` · `DESIGNED` · `TEST SPECIFIED` · Evidence: `E1` (mechanism semantics, partial), `E4` (ARGON fit)
**Class:** `FUTURE TRIGGER` + `BUSINESS DECISION`. **Baseline crosswalk:** this *is* `[BASELINE RP-13]`; its classification stays **`NEEDS EXPERIMENT`** and this document does not raise it. The baseline already flags as `REQUIRES HUMAN DECISION` whether ARGON invests in this rigor at all.
**Depends on:** SEC-001, SEC-005.

**Purpose and problem.** Make a delegation or approval unusable by anyone but the intended holder, for the intended action, within its window, and once where required. This closes the gap in which a copied approval or delegation record behaves like a bearer credential. RP-13's own test is the AgentAck-style one: approve action A, swap in action B, confirm execution is blocked, not merely logged.

**What new evidence adds to each of RP-13's six open sub-questions (no sub-question is closed):**

| RP-13 sub-question | New evidence (this session) | State after this document |
|---|---|---|
| 1. Key custody | RFC 9421 requires the application profile to define key retrieval; the verifier decides whether key material is trustworthy (C10). It does not say who should hold the key. `[BASELINE RP-14]`: the claim-maker must not also be the verifier. | **Open.** E4 constraint carried: the key that authorizes an action must not be held by the process whose action is being authorized. |
| 2. Identity binding | RFC 9421 `keyid` (C11); DPoP binds tokens to a key pair (C9). | Mechanism exists (E1); fit to ARGON unproven. |
| 3. Replay prevention | RFC 9421 defines `nonce` but leaves uniqueness enforcement to the application (C11, C12); DPoP's security considerations include proof replay (C9); a library doc agrees a verifier-side store is needed (S10, E2). | Mechanism understood; **the verifier-side replay store is ARGON's to design and is unproven.** |
| 4. Expiry | RFC 9421 `expires` is a signer hint the verifier may reject earlier (C12); `created` recommended. Timescales are application-specific. | **Open.** Mapping seconds-scale tokens to ARGON task durations remains unresolved, as the baseline said. |
| 5. Revocation | RFC 8693: no linkage between exchanged tokens; revocation propagation is implementation-specific (C7). | **Unsolved in the standard too** — corroborates the baseline; nothing new to adopt. |
| 6. Exact payload binding | RFC 9421 covers chosen components, includes metadata in the signed base (C13), and relies on Content-Digest for content (C14). | Strongest sub-mechanism; still `PROPOSAL` for ARGON; the AgentAck-style substitution test remains required. |

**Research chain (summary, per assignment method).**
- **SOURCE:** S1, S2, S3 (partial reads; §7 of S3 not read).
- **OBSERVED:** C7, C9–C14.
- **WHY IT WORKS:** a signature over the exact action description, the audience, the time window and a freshness value means any change to those invalidates it; holder-bound keys mean copying the record is not enough.
- **GENERAL PRINCIPLE:** sign a canonical description of *what* is authorized, *for whom*, *until when*, with a freshness token; the verifier owns replay and revocation state.
- **ARGON ADAPTATION (E4):** RFC 9421 and DPoP are **HTTP-specific**; ARGON's internal transport is unknown (Q5). Only the principle transfers. ARGON would need its own transport-independent canonical serialization of the action. Canonicalization is the classic failure point, so this is the experiment, not a footnote.
- **TRADEOFF:** key-custody burden on every holder; verifier replay and revocation state become critical-path; digest-binding of parameters blocks later argument substitution but also blocks workflows with legitimately varying parameters.
- **REJECT IF:** approvals and delegations never leave one process/trust domain where a copy cannot escape; or holders cannot protect a private key materially better than the record; or the baseline's simpler position (approval recorded but not cryptographically bound — "materially weaker, though better than nothing") is what the owner chooses.
- **EXPERIMENT:** below.

**Activation trigger (measurable).** Evaluate when any holds: (a) a delegation or approval record is stored, queued, logged or transmitted anywhere a party other than its holder can read it; (b) records cross a boundary not under a single signing authority; (c) SEC-001 is active and delegation lifetime exceeds a bound the owner sets; (d) any audit finding shows reuse, replay or substitution of an approval; (e) the owner decides (a `BUSINESS DECISION`) that Exact Payload Binding or Cryptographic Binding is required for `REQUIRE HUMAN APPROVAL` actions.

**Prerequisites and dependencies.** SEC-001 records; SEC-005 key custody and rotation; trusted time source with declared skew tolerance; a replay store; C5 for approval capture; C4 for the execution-time check point.

**Security boundary, assets, threats.** *Assets:* signing keys, holder keys, record integrity, replay and revocation state. *Boundary:* signer / holder / verifier, plus the execution layer where the hash is checked immediately before action (`RUNTIME ENFORCED` if built, per RP-13). *Abuse cases:* stolen record used by another party; parameter substitution after approval; replay inside the window; pre-computed proofs (C9); clock disagreement; algorithm or key-confusion downgrade; revoked record still honored from stale state; approval signed by the same process whose action it approves (RP-14).

**Proposed contracts (E4).**
- *Signed approval/delegation envelope:* record (SEC-001) + holder-key identifier + canonical-action digest + created + expires + nonce + signing-key identifier + signature over all of these (the "metadata is covered" idea, C13).
- *Verification order:* algorithm allowlist → key status → signature → audience → time window → revocation status → replay → action matches digest. Any failure → `DENY`.
- *Revocation contract:* a revoked-set keyed by delegation ID and signing-key ID with a declared maximum staleness (value open, Q6).

**Failure modes, fail-closed, audit, recovery.** Unknown algorithm or key, bad signature, expired, not yet valid beyond skew → `DENY`. Revocation or replay store unreachable → `DENY` for any action at or above a stated impact class; below it, only within the declared staleness bound (policy choice reserved for the owner, not made here). Audit records key ID, delegation ID, nonce, decision, reason — never key material or full sensitive payloads. Recovery: key compromise follows SEC-005; revoke everything signed by the affected key.

**Cost and operational burden.** Highest of the five: key custody, canonicalization upkeep, replay store, revocation distribution, clock management.

**Alternatives and rejection conditions.** *Recorded approval, not bound* (baseline's weaker position): cheaper, accept if risk is acceptable. *Short-lived opaque references resolved at an authority:* simpler central revocation, but every verification needs a lookup; prefer when lookups are tolerable. *Channel binding only (mTLS-style):* binds a connection, not an action; reject as sole mechanism if payload binding is required. *Adopt DPoP/HTTP signatures wholesale:* reject unless ARGON delegations really travel over HTTP.

**Acceptance criteria and test vectors (TEST SPECIFIED, none executed).**
- TV-002-A (the AgentAck-style test from RP-13): approve action A, substitute B before execution → mismatch detected and execution **blocked**, not only logged.
- TV-002-B: change any single bound field (operation, target, parameter digest, audience) → `DENY`.
- TV-002-C: same nonce twice → second `DENY`.
- TV-002-D: `expires` passed beyond skew, or `created` in the future beyond skew → `DENY`.
- TV-002-E: signed by a key in `retired-for-signing` or `revoked` state → `DENY`.
- TV-002-F: algorithm not on the allowlist → `DENY` regardless of signature validity.
- TV-002-G: presenter proof from a key other than the bound holder key → `DENY`.
- TV-002-H: verifier loses its revocation feed → behavior equals the declared policy exactly and emits an audit event.
- TV-002-I: an approval whose signing key is held by the same process as the approved action is flagged as a self-attestation failure (RP-14).

**Bounded experiment.** Specify, on paper, a transport-independent canonical form for three real operations of differing shape (simple, free-text parameter, list parameter). Build hand-made pairs of semantically equal and semantically different actions. **Falsified if** any different pair serializes identically, or any equal pair differs, and no rule fixes it without ambiguity.

**Conflicts with existing decisions.** Consistent with RP-13/RP-14 as written. Full check: **UNVERIFIABLE — register unavailable.** Tension noted: RP-13's TTL figures (seconds-scale) vs ARGON task durations is already recorded in the baseline as unresolved.

---

### FCP-C2-SEC-003 — Tool and adapter execution boundary

**Status:** `FUTURE` · `NOT_IMPLEMENTED` · `DESIGNED` · `TEST SPECIFIED` · Evidence: `E1` (principles), `E4` (contracts)
**Class:** `FUTURE TRIGGER`. **Boundary:** C2 owns policy (what may run, with what authority, what is trusted). C4 owns execution mechanics. C2 does not specify sandbox internals.

**Scope note (anti-duplication).** The baseline already holds the underlying patterns, which this pack references and does not restate: RP-1 (Plan/Act capability split), RP-2/RP-5 (tiered rules, prefix blind spots), RP-3 (OS-level sandbox independent of model judgment; fail-closed default required for ARGON), RP-7 (config channel must be outside the repository), RP-9 (gate configuration unreachable by the agent), RP-10 (sandbox-configuration injection, a proposed new threat-model entry awaiting C7), RP-11 (manifest change re-validation, origin-trust axis, tool results as data), RP-12 (secrets never enter agent context). What this pack adds is the **single contract** that binds those patterns to SEC-001 scopes, and **credential audience separation**.

**Research chain — credentials must not pass through**
- **SOURCE:** S4 (MCP security best practices, protocol project's own text).
- **OBSERVED:** C15. Confused-deputy risk arises at MCP proxy servers that connect to third-party APIs; token passthrough is an explicitly forbidden anti-pattern; tokens should carry audience separation, since controls such as rate limiting and monitoring depend on the audience.
- **WHY IT WORKS:** if each hop accepts only tokens minted for it and uses its own downstream credential, leaking one does not grant authority at the next.
- **GENERAL PRINCIPLE:** never forward a received credential; each component authenticates onward with a credential issued to itself, scoped to the purpose.
- **ARGON ADAPTATION (E4):** if adapters call authenticated external services, they hold their own per-purpose credentials (by reference, per `[BASELINE RP-12]`) and refuse upstream-presented credentials. This adds protocol-project primary text to RP-11, whose sources were OWASP, SOC Prime and an arXiv paper.
- **TRADEOFF:** more credentials to issue and rotate (feeds SEC-005); per-task credential scoping.
- **REJECT IF:** no adapter calls an authenticated external service.
- **EXPERIMENT:** below.

**Tool results are data (carried, not re-researched).** `[BASELINE RP-11]` already classifies "tool_result = data, not instruction" as `ADOPT` and records that the MCP protocol itself enforces none of it. I did not isolate a specific provision on tool-result handling in S5; this pack makes no new claim about it.

**Activation trigger (measurable).** Evaluate when any holds: (a) the owner decides third-party MCP servers or adapters are in scope (the baseline's open `REQUIRES HUMAN DECISION` for RP-11); (b) any adapter holds a credential for an external service; (c) any mutation-capable tool consumes content from outside the trust boundary and a model then acts on it; (d) a Wave 4 runtime exists in which RP-1/RP-3/RP-9 can be exercised.

**Prerequisites and dependencies.** SEC-001 (scopes, identities); SEC-005 (credential lifecycle); C4 enforcement points; C5 approval handling; the Wave 4 runtime (`UNKNOWN`).

**Security boundary, assets, threat model, abuse cases.** *Assets:* external accounts, repository and task data, host and runtime, credentials. *Boundary:* agent ↔ policy gate ↔ tool/adapter ↔ external world; gate configuration on the `Platform` side (RP-9). *Abuse cases (each traces to the baseline unless marked):* a manifest changed after approval (rug pull, RP-11); sandbox configuration injected via task input (RP-10); a repo-resident config disabling approval (RP-7); a wrapper command evading a prefix rule (RP-5); a tool echoing a fetched secret back in its result (RP-12 bypass); an upstream credential forwarded downstream (S4, new); a write reaching an interpreter or composite tool during PLAN (RP-1's five-route test).

**Proposed contracts (E4).**
- *Tool manifest:* tool ID, allowed operations, input/output schema, required scopes (SEC-001), impact class, origin-trust tier (first-party/third-party, RP-11), manifest digest, credential **reference** (never the value), declared enforcement class.
- *Pre-invocation gate:* input = delegation + tool + arguments; output = one of the four ARGON decisions + reason. Manifest digest change → treated as unapproved until re-reviewed (RP-11).
- *Result contract:* typed, size-bounded, flagged untrusted; never read as policy; a result used as input to another tool is revalidated against that tool's input schema.

**Failure modes, fail-closed, audit, recovery.** Missing or invalid manifest → tool does not run. Schema violation → reject, never coerce. Gate or sandbox unavailable → `DENY` (the baseline requires ARGON's equivalent of `failIfUnavailable` to default to fail-closed — the opposite of the vendor default it cites). Audit: tool, principal, argument digest, decision, outcome; secrets redacted. Recovery: disable by manifest status; revoke the adapter credential (SEC-005); re-admit after re-review.

**Cost and operational burden.** Manifest authoring and review per tool; approvals add friction; the gate becomes critical-path.

**Alternatives and rejection conditions.** *Prompt-level instruction only:* rejected — the baseline classifies a prompt-only rule as not a hard control (RP-3). *Single global allowlist:* adequate for a tiny static tool set; reject once principals differ. *Isolation per tool:* a C4 decision; reject as default when most tools are low-impact. *Skip this pack:* acceptable if all tools are read-only, hold no credentials, and no external content is consumed.

**Acceptance criteria and test vectors (TEST SPECIFIED, none executed).**
- TV-003-A: write attempt in PLAN via (1) direct tool, (2) shell redirect, (3) interpreter, (4) wrapper, (5) indirect tool call → all blocked at the tool-registration layer (`[BASELINE RP-1]`'s five routes).
- TV-003-B: a mock server changes a tool description between connections → re-review required, prior approval not inherited (`[RP-11]`).
- TV-003-C: a third-party tool response asks to call an internal write-capable tool → no inherited trust (`[RP-11]`).
- TV-003-D: adapter receives an upstream-presented credential → refused (S4).
- TV-003-E: task input tries to set sandbox network or mount parameters → no effect (`[RP-10]`).
- TV-003-F: repository-resident config tries to weaken a gate → no effect (`[RP-7]`).
- TV-003-G: a tool tries to return a fetched secret → blocked or redacted before reaching context (`[RP-12]`).
- TV-003-H: sandbox dependency missing → execution refused, not degraded to unsandboxed (`[RP-3]`).
- TV-003-I: operation at or above the impact threshold → `REQUIRE HUMAN APPROVAL`, never `ALLOW`.

**Bounded experiment.** Classify the actual tool list by impact class and credential reach on paper, then mark which tools change class under a worst-case manipulated input. **Falsified if** nearly all tools are read-only with no credentials (pack unnecessary), or if a typical manifest cannot be written without asserting behavior the tool does not reliably have.

**Conflicts with existing decisions.** Built from baseline patterns; none contradicts them. One baseline nuance: RP-2's persisted "remembered" approvals interact with manifest re-validation (a remembered approval must not survive a manifest digest change). Full check: **UNVERIFIABLE — register unavailable.**

---

### FCP-C2-SEC-004 — Third-party adapter and artifact trust

**Status:** `FUTURE` · `NOT_IMPLEMENTED` · `DESIGNED` · `TEST SPECIFIED` · Evidence: `E1` (SLSA levels, partial), `E4` (ARGON mapping)
**Class:** `FUTURE TRIGGER` + `BUSINESS DECISION` (which third parties are permitted at all).

**Purpose and problem.** Decide which externally produced adapters, plugins and dependencies may be loaded, on the basis of verifiable provenance rather than name or popularity. The baseline's RP-11 covers *runtime* change of a tool's definition; it does not cover where the artifact came from or how it was built (0 occurrences of supply-chain terms).

**Research chain**
- **SOURCE:** S6, S7 (SLSA v1.0).
- **OBSERVED:** C17. L1 provenance addresses mistakes and documentation; L2 signed provenance from a hosted platform addresses tampering after the build; L3 hardened platform addresses tampering during the build; downstream consumers must validate authenticity.
- **WHY IT WORKS:** verified, signed provenance lets a consumer check origin and build process instead of trusting a name.
- **GENERAL PRINCIPLE:** trust attaches to *verified provenance measured against an explicit policy*, never to the existence of a provenance document.
- **ARGON ADAPTATION (E4):** an admission policy per adapter class (minimum level, expected builder identity, pin rule) run before load, with the digest pin covering the tool manifest as well so RP-11's rug pull cannot ride in on an update. Analogy, flagged as inference: provenance accepted without verification parallels the self-attestation problem in `[BASELINE RP-14]`.
- **TRADEOFF:** few third-party adapters will reach L2/L3; strict policy narrows the ecosystem. Provenance shows *how* something was built, **not that it is benign**; it does not replace SEC-003 runtime limits.
- **REJECT IF:** ARGON loads no third-party code and its dependency set is small, first-party and reviewable by hand.
- **EXPERIMENT:** below.

**Activation trigger (measurable).** Evaluate when any holds: (a) a third-party adapter, plugin or MCP server is proposed for loading into a trusted context (ties to the baseline's open decision on third-party MCP); (b) first-party artifacts are distributed beyond one trust domain; (c) the dependency inventory exceeds what a reviewer can assess (threshold set by the owner); (d) an advisory affects any component in use.

**Prerequisites and dependencies.** An inventory of adapters and dependencies with versions (existence unverified); a pinning mechanism; SEC-003 as the second layer; owner input on permitted third parties.

**Security boundary, assets, threat model, abuse cases.** *Assets:* trusted runtime, adapter-reachable credentials, build/release pipeline. *Boundary:* artifact origin → admission check → trusted execution context. *Abuse cases:* malicious or compromised package; name substitution; tampering in transit; build-platform compromise; unpinned update delivering altered code; provenance trusted without verification; manifest altered while the code digest is unchanged.

**Proposed contracts (E4).**
- *Admission policy record:* adapter class, minimum provenance level, accepted builder/source identity, pin rule, permitted capabilities (cross-referenced to the SEC-003 manifest).
- *Admission decision:* input = artifact digest + provenance + policy; output = `ALLOW` / `REQUIRE REVIEW` / `DENY` + reason + audit ID. Absent or unverifiable provenance → `REQUIRE REVIEW` or `DENY`, never silent load.

**Failure modes, fail-closed, audit, recovery.** Verification unavailable → no new admissions; already-admitted pinned artifacts continue under existing policy. Audit: digest, provenance identity, policy version, decision. Recovery: remove or replace by pinned digest; revoke the adapter credential (SEC-005); re-admit only after re-verification.

**Cost and operational burden.** Inventory upkeep, verification tooling, policy maintenance, update-review cadence.

**Alternatives and rejection conditions.** *Vendor and manually review every dependency:* cheaper at small scale; reject as the set grows. *Reputation or popularity as trust signal:* rejected. *Inventory-only (an SBOM-style list):* an inventory is not provenance verification — a component, not the pack. *Forbid third-party code outright:* the simplest control and a legitimate `BUSINESS DECISION` outcome that makes this pack unnecessary.

**Acceptance criteria and test vectors (TEST SPECIFIED, none executed).**
- TV-004-A: artifact with no provenance → not admitted.
- TV-004-B: invalid signature or unexpected builder identity → `DENY`.
- TV-004-C: digest differs from the pin → `DENY`.
- TV-004-D: provenance level below the class minimum → `DENY`.
- TV-004-E: tool manifest differs from the pinned manifest digest while code digest matches → `REQUIRE REVIEW`.
- TV-004-F: admitted adapter attempts an undeclared capability → blocked by SEC-003, independent of admission.

**Bounded experiment.** For three adapters or dependencies actually under consideration, determine whether verifiable provenance exists and at what level. **Falsified if** none of the realistically needed candidates can meet the minimum level — then the policy is loosened (a `BUSINESS DECISION`) or the candidates are replaced.

**Conflicts with existing decisions.** None visible in the baseline. Full check: **UNVERIFIABLE — register unavailable.**

---

### FCP-C2-SEC-005 — Secret and key lifecycle

**Status:** `FUTURE` · `NOT_IMPLEMENTED` · `DESIGNED` · `TEST SPECIFIED` · Evidence: `E1` (lifecycle scope, partial), `E4` (ARGON mapping)
**Class:** `FUTURE TRIGGER`.

**Purpose and problem.** Define how signing keys, holder keys and service credentials are inventoried, protected, rotated, retired and recovered after compromise, so SEC-001…SEC-004 rest on keys that can be managed. The baseline fixes *where secrets must not go* (RP-12: never into agent context) and lists key custody and revocation as open; it does not define rotation, retirement or compromise response.

**Research chain**
- **SOURCE:** S8 NIST SP 800-57 Part 1 Rev. 5.
- **OBSERVED:** C18; keyword and abstract excerpts include compromise, backup, archive, key recovery, key-inventory management, key management policy.
- **WHY IT WORKS:** treating keys as inventoried objects with an owner, purpose, lifetime and retirement path turns rotation and compromise response into routine operations.
- **GENERAL PRINCIPLE:** every key and secret has an owner, a single purpose, a bounded lifetime, a retirement path and an audited history; the compromise response is written *before* it is needed.
- **ARGON ADAPTATION (E4):** a register holding references and metadata only (never values, consistent with RP-12); a state model (`active` → `verify-only` → `revoked` → `destroyed`, plus `retired-for-signing`); compromise runbooks per key class. **No cryptoperiod or rotation interval values are proposed**; they must be taken from the source and set by the owner after review.
- **TRADEOFF:** operational overhead; custody tier trades cost, availability and assurance; shorter lifetimes raise rotation-failure risk.
- **REJECT IF:** ARGON holds no signing keys and no service credentials (then SEC-002 and the credential parts of SEC-003 fall away too).
- **EXPERIMENT:** below.

**Activation trigger (measurable).** Evaluate when any holds: (a) any other pack here is activated; (b) ARGON holds more than one long-lived credential or signing key; (c) a secret is found in source, a log, an artifact, a prompt or an Evidence Record; (d) a person with key access departs or a device holding key material is lost.

**Prerequisites and dependencies.** A custody-tier decision (`BUSINESS DECISION`, cost vs assurance, Q8); an audit sink; a named owner per key class; C4 for runtime injection by reference.

**Security boundary, assets, threat model, abuse cases.** *Assets:* signing keys, holder keys, service credentials, key metadata, backups. *Abuse cases:* leakage into logs, prompts or Evidence Records; never-rotated long-lived credentials; one key serving several purposes; exposed backups; a compromise detected with no tested response; verifiers still honoring a retired or compromised key; loss of the only key (an availability failure); a secret-fetching tool echoing the value (`[BASELINE RP-12]` bypass); the signing key held by the same process whose actions it attests (`[BASELINE RP-14]`).

**Proposed contracts (E4).**
- *Register entry:* ID, purpose, owner, custody class, created, expiry, status, rotation due, dependents (which packs/adapters rely on it).
- *State transitions:* forward only; each audited; `verify-only` verifies old signatures but creates no new ones.
- *Compromise runbook (per class):* detection signals, containment (revoke/disable), dependents to re-issue, verification of closure, post-incident record.
- *Injection contract with C4:* secrets delivered by reference at runtime; never embedded in artifacts, prompts or logs.

**Failure modes, fail-closed, audit, recovery.** Key past expiry → unusable for signing; verification behavior per policy. Register or custody service unavailable → no new key operations; active keys continue only within a declared window. Rotation failure → prior key stays `verify-only` until the new key is confirmed in use, with an alert. Audit covers create, policy change, rotate, revoke, destroy with actor and reason — never key material. Recovery: run the class runbook, re-issue dependents, record the outcome.

**Cost and operational burden.** Moderate to high depending on custody tier: register upkeep, rotation operations, drills.

**Alternatives and rejection conditions.** *Rely on a platform secret store without an ARGON-level register:* acceptable for very few secrets; reject once keys have dependents that must be re-issued on rotation. *Never rotate, protect harder:* rejected — conflicts with the lifecycle model (C18). *Hardware-backed custody for everything:* reject as default; justify per key class by impact.

**Acceptance criteria and test vectors (TEST SPECIFIED, none executed).**
- TV-005-A: every key and credential in use appears in the register with owner and expiry.
- TV-005-B: a `verify-only` key cannot create a new signature but still verifies old ones.
- TV-005-C: a revoked key's signatures fail verification for new presentations.
- TV-005-D: a seeded fake secret placed in an artifact, log, prompt fixture or Evidence Record fixture is detected.
- TV-005-E: a tabletop compromise of one key class completes its runbook with all dependents re-issued and recorded.
- TV-005-F: rotation with a simulated failure leaves the prior key in the declared fallback state and raises an alert.
- TV-005-G: the signing key for an approval is not reachable from the process executing the approved action (`[BASELINE RP-14]`).

**Bounded experiment.** Paper tabletop: choose one hypothetical compromised key and trace every dependent from the register, the containment and re-issue steps, and the time and data needed. **Falsified if** dependents cannot be enumerated from available information — which would show the register, not more cryptography, is the first gap.

**Conflicts with existing decisions.** None visible in the baseline. Full check: **UNVERIFIABLE — register unavailable.**

---

## 5. Considered and not made into packs

| Candidate | Disposition | Reason |
|---|---|---|
| Separate "agent identity" and "delegation" packs | Merged into SEC-001 | Same trust question |
| Evidence-record trust (claim-maker ≠ verifier ≠ relying party) | **Not a pack** | Already `ADOPT` as principle in `[BASELINE RP-14]`; owned by the Evidence/verification Clouds (baseline names C6 and C7), not a new C2 capability. SEC-002 and SEC-005 only *respect* it. |
| Generic AI guardrail product | `NOT NEEDED` | No demonstrated gap; SEC-003 states the control objective instead |
| Confidential computing or hardware enclaves | `NOT NEEDED` pending evidence | No evidence in any available artifact that the threat model needs it |
| Exhaustive SBOM/vulnerability program | `NOT NEEDED` as a pack | Out of bounded scope; inventory is a prerequisite inside SEC-004 |
| Roo Code, OpenAI Agents SDK, Goose, SWE-ReX, PydanticAI, LangGraph | **Not addressed** | The baseline's own coverage gap (named C2-priority sources never opened). Not closed here; no pack depends on them. |

## 6. Catalog, dependencies and ownership boundaries

| Pack | Activation trigger (summary) | Depends on | Class |
|---|---|---|---|
| FCP-C2-SEC-001 | ≥2 principals with mutation tools for one task; any hand-off; unattributable mutation; third-party MCP in scope | Kernel/Runtime, tool catalog, audit sink | `FUTURE TRIGGER` |
| FCP-C2-SEC-002 | Records readable beyond holder; crossing signing-authority boundary; replay/substitution finding; owner requires binding | 001, 005, replay store | `FUTURE TRIGGER` + `BUSINESS DECISION` |
| FCP-C2-SEC-003 | Third-party MCP/adapters in scope; adapter holds credentials; external content reaches a mutation tool; Wave 4 runtime exists | 001, 005 | `FUTURE TRIGGER` |
| FCP-C2-SEC-004 | Third-party artifact proposed for trusted context; inventory beyond hand review; advisory hits | 003 | `FUTURE TRIGGER` + `BUSINESS DECISION` |
| FCP-C2-SEC-005 | Any other pack active; >1 long-lived credential/key; leaked secret; departing keyholder/lost device | custody-tier decision | `FUTURE TRIGGER` |

**Ownership boundaries (and how well each is established).**

| Cloud | Boundary | Basis |
|---|---|---|
| C4 | Execution mechanics; C2 defines the policy gate, manifest and secret-injection requirement; C4 implements enforcement points and isolation | Given in the assignment; the baseline never mentions C4 |
| C5 | Human-facing approval workflows; C2 defines when approval is required and the decision contract, C5 owns capture and experience | Given in the assignment; the baseline says inline-approve and time-boxed-hold UX "relevant to C5's territory" |
| C6 | Appears in the baseline as an *independent verification/evidence* role ("C6 does not self-certify, C7 is independent" — baseline's own internal Wave 3.5 context, not external evidence); the signing-key custody and evidence-record separation questions (SEC-002/005) touch it | Partially established, one baseline passage |
| C7 | Independent audit; baseline routes the RP-10 threat-model entry to it | Partially established |
| C3 | Appears only in a list of Clouds that might revise the Evidence Record design | **Not established.** No dependency asserted |
| C1 | Referenced in the baseline's shared correction history | **Not established** |

## 7. Open questions requiring evidence

**7.1 Carried forward unresolved (not marked resolved).**
- **Q1 — Cryptographic binding (C7 question).** The C7 audit is unavailable, so whether any C7 finding on it is resolved is **UNVERIFIABLE**. Baseline RP-13's six sub-questions remain `NEEDS EXPERIMENT`; §4 SEC-002 adds standards-grade semantics only.
- **Q2 — Delegation depth (C7 question).** The baseline never raises it; C7 unavailable → **UNVERIFIABLE** as to any earlier C7 position. Verified standards fact: RFC 8693 has no depth limit and consumers ignore prior actors (C3, C5).
- **Q3 — Baseline's own open items**, none resolved here: narrow single-use vs broad persisted approvals; approval expiry timescale; revocation; key custody; whether third-party MCP is in scope; whether Kernel can support cryptographic binding (Wave 4); Plan/Act enforcement across the five routes; RP-10 as a threat-model entry.

**7.2 New open questions.**
- **Q4:** What maximum delegation depth does ARGON want, and which workflows need more than one hop? (`BUSINESS DECISION` + experiment.)
- **Q5:** Which transport do ARGON delegations and approvals use? It decides whether RFC 9421/DPoP formats apply or only the principle transfers.
- **Q6:** Maximum acceptable revocation staleness per impact class; behavior when the revocation or replay store is unreachable.
- **Q7:** Who defines the impact-class taxonomy used by SEC-001 and SEC-003, and where is it recorded?
- **Q8:** Key custody tier: software store, managed service, or hardware-backed (`BUSINESS DECISION`).
- **Q9:** Behavior when the audit sink is unavailable: fail closed everywhere, or above an impact threshold?
- **Q10:** Source currency not checked: whether newer revisions or errata affect S1, S3, S4, S6 (a draft SLSA page mentions a newer version, 1.2, that reintroduces a Source track), or S8 (the NIST page showed a later update date). RFC 9421 §7 (Security Considerations) was not read.
- **Q11:** A vendor article reports a 2026 revision of the OWASP LLM list with Excessive Agency renumbered (S9, `E3`). Not confirmed against an OWASP primary page; this document cites only the 2025 page and the numbering must be re-checked before any formal citation.
- **Q12:** The label definitions for `NOW` / `ARCHITECTURE-READY` / `FUTURE TRIGGER` / `NOT NEEDED` / `BUSINESS DECISION` and a decision register to check conflicts against.
- **Q13:** The absent artifacts: the C7 audit (the baseline says it was never produced), `C2-WAVE3.5-SECURITY-RECONCILIATION-v2.md`, the correction-pass documents, the threat model, checkpoints, and C1/C3–C7 manifests.
- **Q14:** Baseline internal discrepancy, noted and not resolved: the manifest states `source_count: 14`, while the baseline's appendix lists 15 named source groups. Likely counting convention; unconfirmed.

## 8. Change summary

- **Created:** `C2-FUTURE-SECURITY-CAPABILITY-PACKS.md` (this file) and its sibling `C2-FUTURE-SECURITY-CAPABILITY-PACKS.manifest.yaml`. The manifest follows the key schema of the baseline's manifest (the filename pattern is inferred from a single example). It records this file's computed sha256 and a post-run integrity re-check of the two input files.
- **Modified:** nothing. `C2-CLOUD-SECURITY-ADAPTER-RESEARCH.md` and its manifest were read only; their hashes were recorded before and re-checked after (see manifest).
- **Core architecture:** untouched. No implementation code written. No API, interface or ARGON component was claimed to exist.
- **Status ceiling:** every pack is `DESIGNED` · `NOT_IMPLEMENTED` · `TEST SPECIFIED`. No test was executed; nothing is `PASS WITH EVIDENCE` except the hash match in §1.1. Nothing is claimed as implemented, tested, secure or production-ready.
- **Superseded:** my own earlier baseline-less draft (hash in the header); corrections itemized in §1.4.
- **Not done, by design:** no background work is promised; the six unopened C2-priority sources, the unavailable audit and Wave 3.5 reconciliation, and the unread RFC 9421 §7 remain open (§5, §7).

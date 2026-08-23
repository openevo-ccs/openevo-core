# OpenEvo Core — Governance

**Status:** Normative for everything this repository actually contains (the shared upper ontology, the identifier scheme, the cross-repo RFC process, and the `www.w3id.org/openevo/` namespace root). Where a Foundational Repo's own entity content is concerned (a new Concept, LPM, Strand, Competency, Alignment, Resource, Project, Literature record, Person, Group, Question, Method, or TheoryBase node), **that repo's own `GOVERNANCE.md` governs** — this document does not.

This document exists because `conceptbase` — the ecosystem's first mature repo — ended up playing two roles at once: its own peer-equal entity registry (`oe:Concept`/`oe:LPM`/`oe:Strand`), and an accidental shared-kernel steward for every other Foundational Repo (the RFC gate every new ontology class went through, the file the `oe:` upper ontology physically lived in, and the literal namespace root that `www.w3id.org/openevo/` redirected to). Full diagnosis: `lab_manager/docs/design-notes/ecosystem-shared-kernel-and-co-equal-governance-plan.md`. This repository is the extracted second role. ConceptBase keeps the first, unchanged, as one Foundational Repo among nine peers.

---

## What this repo owns (and what it doesn't)

**Owns:**
- The `oe:` upper ontology (`ontologies/core_v1.yaml`) — class and property definitions shared across every Foundational Repo.
- The `OE-{TYPE}-######` identifier scheme itself, and the cross-repo Identifier Block Allocation registry below (which numeric blocks each Foundational Repo's vocabularies/LPMs have reserved, so independently authored content never collides).
- The RFC process definition and template used whenever a genuinely new `oe:` class, or a change to the identifier scheme itself, is proposed.
- The `www.w3id.org/openevo/` namespace root, and the sub-paths that resolve to shared kernel content (`/ontology`, cross-cutting `/vocab/*` entries, `/schemas/*` that are genuinely shared rather than Concept/LPM/Strand-specific).

**Does not own:**
- Any entity *instance* data. Zero Concepts, LPMs, Strands, Competencies, Resources, Projects, Literature records, People, Groups, Questions, Methods, or TheoryBase nodes live here — those live in their owning Foundational Repo, per `lab_manager/docs/design-notes/ecosystem-base-graph-project-architecture-and-ontology-plan.md` §3.1.
- Entity-specific JSON Schemas (`concept.schema.yaml`, `lpm.schema.yaml`, etc.) or their shared `$defs` — those are ConceptBase's own (`conceptbase/schemas/`), since they encode ConceptBase's own identifier patterns and validation rules, not generic kernel content.

## Roles

| Role | Responsibility | Who holds it today |
|---|---|---|
| **Kernel steward** | Merge rights on this repo; final arbitration on upper-ontology changes, identifier-scheme changes, and namespace-root changes. | Dustin Eirdosh |
| **Foundational Repo delegate** (one seat per base: Concept, Competency, Teaching, Project, Literature, Human, Theory, Question, Method, Species) | Reviews any kernel RFC that would affect their Foundational Repo's entity type — e.g. a new `oe:` class their repo will instantiate, or a block-allocation change. | Dustin Eirdosh (all ten seats today — see note below) |
| **Project-repo representative** | Non-voting review on kernel RFCs that would change what Project repos (any kind — `graph`/`lpm`/`app`) can reference. Distinct from the ProjectBase Foundational-Repo-delegate seat above, which is about the `oe:Project` entity type specifically. | Dustin Eirdosh |
| **Contributors** | Anyone; submit RFCs via pull request against `proposals/`. | — |

**Note on seat consolidation:** every seat above is currently the same person. The table exists so that the day a second independent contributor to *any* Foundational Repo shows up (HumanBase and LiteratureBase are the most likely first cases — see the base-graph-project plan §13 item 3), they slot into an already-defined seat instead of governance being invented ad hoc under time pressure. This mirrors a lesson already learned elsewhere in this ecosystem (`conceptbase/GOVERNANCE.md`'s Identifier Block Allocation section): don't build multi-person process for a committee that doesn't exist yet.

## RFC Process

A pull request against `proposals/` is required for:

1. **A genuinely new `oe:` ontology class** (not a new *instance* of an existing class — that's the owning Foundational Repo's own process). Needs the Kernel Steward's approval plus the delegate(s) for whichever Foundational Repo(s) the class belongs to.
2. **A change to the `OE-{TYPE}-######` identifier scheme itself**, or a new entry in the Identifier Block Allocation registry below. Kernel Steward approval required; the requesting Foundational Repo reserves its block as part of the same RFC, exactly as `conceptbase/GOVERNANCE.md` already required for its own four blocks.
3. **A change to the `www.w3id.org/openevo/` namespace root, or to which sub-paths resolve where** (root `^$`, `/ontology`, cross-cutting `/vocab/*`, `/schemas/*`). Kernel Steward approval required; see `w3id-submission/openevo/` for the staged `.htaccess` this repo maintains and periodically submits upstream to the real w3id.org registry.
4. **A change to this RFC process itself, the Roles table, or the namespace root** — treated as a MAJOR change requiring explicit Kernel Steward sign-off, tagged `type: specification-amendment` on the RFC, mirroring `conceptbase/GOVERNANCE.md`'s own equivalent rule.

Everything else — a new Concept, LPM, Strand, Competency, Resource, Project, Literature record, Person, Group, Question, Method, TheoryBase node, or a new vocabulary within an existing class — is **not** proposed here. It goes to the owning Foundational Repo's own `proposals/`, per that repo's own `GOVERNANCE.md`.

## Lifecycle Status

Every `oe:` class and property carries a `status` field. Status transitions along the primary chain only move forward:

```
proposed → accepted → stable → deprecated → superseded
                                    ↘
                                     retracted
```

A status **MUST NOT** revert (e.g. `deprecated` back to `stable`) without a new RFC. `retracted` is a parallel terminal state reachable directly from `accepted` or `stable` — not sequential after `deprecated` — and does not imply supersession. (Identical rule to `conceptbase/GOVERNANCE.md`'s Lifecycle Status section — restated here because it now governs the shared ontology's own classes/properties, not just ConceptBase's entities.)

## Deprecation Policy

No `oe:` class or property is ever removed once `status: accepted` or higher. A deprecated one **MUST** remain resolvable at its existing IRI indefinitely, carry a `supersededBy` pointer where one exists, and continue to appear in query results, so no Foundational or Project repo (of any kind — `graph`/`lpm`/`app`) is ever silently broken by a kernel change.

## Independent Versioning

The ontology versions independently via semver (`MAJOR.MINOR.PATCH`), exactly as it did inside `conceptbase`:

- **MAJOR** — a class or property is removed or redefined incompatibly.
- **MINOR** — additive change (new class, new optional property, promoted reserved class).
- **PATCH** — non-semantic change (wording, typo correction).

Filename convention unchanged from `conceptbase/GOVERNANCE.md`: bare `_v{MAJOR}` suffix (`core_v1.yaml`, becoming `core_v2.yaml` on the next MAJOR bump); MINOR/PATCH bumps update only the internal `version:` field.

## Identifier Block Allocation

The cross-repo registry of reserved numeric blocks, so independently authored vocabularies/LPMs across every Foundational Repo never collide. Each governed unit reserves its own block via its founding RFC — in whichever repo owns that entity type, cross-referenced here.

**Id scheme superseded (2026-08-16):** both `oe:Concept` and `oe:Competency` have migrated off
numeric block-allocation entirely, to `OE-CONCEPT-<vocab-slug>-<code-slug>` /
`OE-COMPETENCY-<vocab-slug>-<code-slug>` (e.g. `OE-CONCEPT-000102` →
`OE-CONCEPT-bio-core-natural-selection`; `OE-COMPETENCY-000800` →
`OE-COMPETENCY-openevo-core-competencies-ct`). See `conceptbase/GOVERNANCE.md` and
`competencybase/GOVERNANCE.md` for the live registries; the table below is retained as
**historical record**, not a live one — new vocabularies mint slug-based ids directly in their
owning repo, no block reservation here. `oe:LPM`/`oe:Strand` are unaffected and still use numeric
block-allocation.

**ConceptBase** (`oe:Concept`, `oe:LPM`, `oe:Strand`, `oe:Competency`):

| Vocabulary/Entity type | Block (historical) | Notes |
|---|---|---|
| `BIO-CORE` (Concept) | `OE-CONCEPT-000100`–`000199` | See `conceptbase/GOVERNANCE.md` for current usage |
| `OE-INTERDISCIPLINARY` (Concept) | `OE-CONCEPT-000200`–`000299`, plus `000090`–`000099` cross-cutting | See `conceptbase/GOVERNANCE.md` |
| `bio-core-k12` (Strand) | `OE-STRAND-000100`–`000199` | Per-LPM block |
| `interdisciplinary-k12` (Strand) | `OE-STRAND-000200`–`000299` | Per-LPM block |
| `OE-LPM` | Sequential | No sub-blocking — LPMs don't nest |
| `NGSS-LIFE-SCIENCE` (Competency) | `OE-COMPETENCY-000100`–`000199` | |
| `AI4K12` (Competency) | `OE-COMPETENCY-000200`–`000699` | Wider block, reserved up front per RFC-0007 |
| `EVO-ED-ASSESSMENT-TARGETS` (Competency) | `OE-COMPETENCY-000700`–`000799` | Per RFC-0014 |
| `OPENEVO-CORE-COMPETENCIES` (Competency) | `OE-COMPETENCY-000800`–`000899` | First OpenEvo-authored competency vocabulary; per RFC-0016. Whole block reserved for all four planned OpenEvo core competencies (Computational Thinking, Evolutionary Causal Reasoning, Decentralized Causal Reasoning, Systems Thinking), not just RFC-0016's 7 entries. |

*(This table mirrors `conceptbase/GOVERNANCE.md`'s Identifier Block Allocation section, re-synced 2026-08-02 after it had drifted since the 2026-07-26 migration. ConceptBase's own file remains the live, authoritative record of its own blocks' current usage; this copy exists so a new Foundational Repo reserving its first block can see the whole cross-repo picture in one place without needing to check nine separate `GOVERNANCE.md` files. Keep both in sync when either changes.)*

**Known unresolved collision, found during this re-sync (2026-08-02):** the unmerged branch `rfc-0011-teacher-competency-frameworks` (conceptbase) reserves `DIGCOMPEDU 000700–000799`, `UNESCO-AI-CFT 000800–000899`, `KMK-DIGITALE-WELT 000900–000999`, and `CCC 001000–001099` — a range now **entirely double-allocated** by RFC-0014 (`000700`–`000799`, merged) and RFC-0016 (`000800`–`000899`, merged) above. RFC-0011 cannot be merged as currently drafted; it needs fresh block numbers (the next free Competency block starts at `000900`) before it's touched again. Not fixed here — re-deriving an entire unmerged branch's id assignments is a real, separate task, not a side effect of this sync.

**Other Foundational Repos:**

| Vocabulary/Entity type | Block | Notes |
|---|---|---|
| `OPENEVO-DBR-MODEL` (Method) | `OE-METHOD-<slug>` | RFC-0004. 9 records (the DBR Model + its 4 phases, the Multi-Agent Deliberation Protocol, the EvoFlex assessment pattern, Kattmann's didactic-reduction model, one `proposed` curriculum-network-analysis method). Id scheme migrated 2026-08-16 from numeric block-allocation to `OE-METHOD-<slug>` (reusing each record's own `slug` field), same pattern as TheoryBase below. |

**TheoryBase** (`oe:Theory`, `oe:Proposition`, `oe:Assumption`, `oe:Evidence`, `oe:Context`, `oe:CompetingProposition`, `oe:Misconception`, `oe:CrossDomainConstruct`, `oe:Mechanism`, `oe:Hypothesis`, `oe:DesignPrinciple`, `oe:CurriculumDecision`, `oe:LearningDependency`) — per RFC-0002 (accepted 2026-08-16): `OE-{TYPE}-<slug>`, no numeric block, no vocab-slug segment (no analogous multi-vocabulary structure exists yet — see RFC-0002's own ID block reservation section for why). Each type is its own namespace, collision-free by construction rather than by reserved range.

**QuestionBase** (`oe:Question`) — per RFC-0003 (accepted 2026-08-16): `OE-QUESTION-<slug>`, no
numeric block, no vocab-slug segment (same reasoning as TheoryBase/MethodsBase above — one corpus,
no multi-vocabulary structure). 38 records.

**LiteratureBase** (`oe:Literature`) — per RFC-0005 (accepted 2026-08-16, the first of the nine
Foundational Repos founded via a from-scratch RFC rather than reviewing an existing draft):
`OE-LITERATURE-<slug>`, no numeric block, no vocab-slug segment. Deliberately not DOI-derived even
though most records have one — see RFC-0005's own ID block reservation section for why. 119
records.

**SpeciesBase** (`oe:Taxon`, `oe:TaxonomicConcept`, `oe:LexicalForm`, `oe:CulturalCategory`,
`oe:Language`, `oe:Feature`, `oe:FeatureExpression`, `oe:Context`, `oe:Explanation`) — per RFC-0006
(accepted 2026-08-23), the 10th Foundational Repo: `{type}:{slug}` (abbreviated prefixes —
`taxon:`, `taxconcept:`, `name:`, `cultcat:`, `lang:`, `feature:`, `featexpr:`, `context:`,
`explanation:` — rather than the `oe:{TYPE}` uppercase form other repos favor, chosen before this
RFC and already in production use). No numeric block needed; the migration off the original
`SB-{TYPE}-######` scheme was already complete (2026-08-19) before this RFC was drafted. ~150
records across all nine classes.

TeachingBase, ProjectBase, HumanBase: no blocks/ids reserved yet, and no founding RFC drafted —
each needs one before minting a permanent id. Rows will be added here as that happens.

*\*Note: `oe:Competency` instances currently live in ConceptBase (see table above); whether CompetencyBase's planned migration (base-graph-project plan §3.1) relocates existing blocks or only governs new ones is a decision for that migration's own RFC, not this document.*

## Compatibility Checking

Unchanged in spirit from `conceptbase/GOVERNANCE.md`: a CI compatibility-checker (still not built anywhere in the ecosystem) would, on every push to a dependent repository, verify pinned-entity resolution, flag deprecated-without-acknowledgement references, flag newer-MAJOR-available pins, and loudly flag any reference to a sandbox identifier. Manual until built.

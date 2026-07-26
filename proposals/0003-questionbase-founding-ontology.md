# RFC-0003: QuestionBase Founding Ontology

**Type:** `content`

**Status:** `proposed`
**Author(s):** Claude, for Dustin Eirdosh
**Date:** 2026-07-26

## Motivation

QuestionBase is one of the nine Foundational Repos scoped in `ecosystem-base-graph-project-architecture-and-ontology-plan.md` (§12: "QuestionBase... proceed") but, like TheoryBase, has never had a founding RFC and is still genuinely bare. It's needed now because Addendum III's dispute-synthesis design (`openevo-graph/nodes/disputes/*.yaml`) has a `knowledgeGaps` field that references `OE-QUESTION-*` ids — the OpenEvo-vs-Kampourakis dispute has real, already-identified knowledge gaps (Model C §4: 4 shared gaps, 3 DCR-specific, 4 ICR-specific) that need a home before the dispute node can link to them.

**Revised same session** per Dustin's own design brief (`ecosystem-base-graph-architecture-addendum-5-questionbase-engine-of-inquiry.md`): QuestionBase is not just a place to park `knowledge_gap` stubs — it's the ecosystem's explicit representation of *uncertainty itself* ("TheoryBase captures what experts currently believe; QuestionBase captures what experts do not yet know or actively disagree about"). This RFC founds it on that fuller model's structural core, deferring the parts that depend on infrastructure that doesn't exist yet (see Addendum V §6).

## Proposed change

One class: `oe:Question`, `plannedOwner: questionbase`.

| Field | Description |
|---|---|
| `id` | `OE-QUESTION-######` (or provisional `question:<slug>` pending this RFC's merge) |
| `label` | Short question title |
| `questionType` | Enum: `empirical` \| `design` \| `theoretical` \| `methodological` \| `policy` \| `implementation` — a question is a family, not one kind of thing (Addendum V §2). Model C's knowledge gaps classify mostly as `empirical`, a few as `methodological` — there is no separate flat `knowledge_gap` type. |
| `statement` | The question itself |
| `motivatedBy` | Reference to what raised the question — a TheoryBase `oe:Proposition`/`oe:Theory` id, or an `openevo-graph` `og:divergence:*` id |
| `decomposesInto` | Array of child `oe:Question` ids (same-repo relation, stored here — not graph-layer content, since it doesn't span repos) |
| `dependsOn` | Array of `oe:Question` ids this question's resolution depends on |
| `competingHypotheses` | Array of inline `{label, statement}` objects — deliberately **not** a separate cross-referenced `oe:Hypothesis` entity type, which stays deferred/Hurst-dispute-scoped exactly as Addendum IV already deferred it out of TheoryBase's RFC-0002 |
| `priority` | Free-text or enum (`highest`/`high`/`moderate`) — mirrors the source corpus's own priority ratings |
| `status` | Seven-stage lifecycle: `open` → `active_research` → `evidence_accumulating` → `emerging_consensus` → `consensus` → `curriculum_recommendation` → `periodic_review`. Many questions never reach `consensus`, and that's an expected, preserved state, not an error. |

## Relations

`motivatedBy` → TheoryBase or `openevo-graph`. `decomposesInto`/`dependsOn` → other QuestionBase records (ordinary same-repo relations, the same way LiteratureBase's own `related[]` field cross-references other LiteratureBase records). Referenced (never duplicated) by `openevo-graph/nodes/disputes/*.yaml`'s `knowledgeGaps[]` field via `motivatesQuestion` edges.

## Standards justification

No existing standard models "an open knowledge gap explicitly tied to a specific theoretical divergence, decomposable into sub-questions, carrying competing hypotheses and a consensus lifecycle" at this granularity for curriculum-theoretic content. Reuses this ecosystem's own established minimal-record pattern rather than importing an unrelated question-answering ontology (e.g. SIOC-Q) built for forum Q&A, not research knowledge gaps.

## ID block reservation

Per `GOVERNANCE.md#identifier-block-allocation`: `OE-QUESTION-000100`–`000199` (first block, this dispute's knowledge-gap corpus). Until merged, QuestionBase content uses provisional `question:<slug>` ids with `provisional.blocked_on` pointing here.

## Files affected

- New: `questionbase/README.md`, `LICENSE`, `.gitignore`, `CONTRIBUTING.md`, `schema/question-record.schema.json`, `records/questions.yaml`.
- `openevo-core/GOVERNANCE.md`: add the "Other Foundational Repos" row for QuestionBase's new block.

## Review

- [ ] Foundational Repo delegate approval (QuestionBase seat — Dustin)
- [ ] Kernel Steward approval (Dustin)
- [ ] For `specification-amendment` RFCs: N/A — this is `content`, not `specification-amendment`

# RFC-0003: QuestionBase Founding Ontology

**Type:** `content`

**Status:** `proposed`
**Author(s):** Claude, for Dustin Eirdosh
**Date:** 2026-07-26

## Motivation

QuestionBase is one of the nine Foundational Repos scoped in `ecosystem-base-graph-project-architecture-and-ontology-plan.md` (§12: "QuestionBase... proceed") but, like TheoryBase, has never had a founding RFC and is still genuinely bare. It's needed now because Addendum III's dispute-synthesis design (`openevo-graph/nodes/disputes/*.yaml`) has a `knowledgeGaps` field that references `OE-QUESTION-*` ids — the OpenEvo-vs-Kampourakis dispute has real, already-identified knowledge gaps (Model C §4: 4 shared gaps, 3 DCR-specific, 4 ICR-specific) that need a home before the dispute node can link to them.

## Proposed change

One class: `oe:Question`, `plannedOwner: questionbase`.

| Field | Description |
|---|---|
| `id` | `OE-QUESTION-######` (or provisional `question:<slug>` pending this RFC's merge) |
| `label` | Short question title |
| `questionType` | Enum: `knowledge_gap` (this session's only value in use — an unresolved empirical or theoretical question a dispute or theory surfaces), reserved for future values (`research_question`, `curriculum_design_question`) as other QuestionBase use cases arise |
| `statement` | The question itself |
| `motivatedBy` | Reference to what raised the question — a TheoryBase `oe:Proposition`/`oe:Theory` id, or an `openevo-graph` `og:divergence:*` id |
| `priority` | Free-text or enum (`highest`/`high`/`moderate`) — mirrors the source corpus's own priority ratings |
| `status` | `open` \| `resolved` (only `open` in use this session) |

## Relations

`motivatedBy` → TheoryBase or `openevo-graph`. Referenced (never duplicated) by `openevo-graph/nodes/disputes/*.yaml`'s `knowledgeGaps[]` field via `motivatesQuestion` edges.

## Standards justification

No existing standard models "an open knowledge gap explicitly tied to a specific theoretical divergence" at this granularity for curriculum-theoretic content. Reuses this ecosystem's own established minimal-record pattern rather than importing an unrelated question-answering ontology (e.g. SIOC-Q) built for forum Q&A, not research knowledge gaps.

## ID block reservation

Per `GOVERNANCE.md#identifier-block-allocation`: `OE-QUESTION-000100`–`000199` (first block, this dispute's knowledge-gap corpus). Until merged, QuestionBase content uses provisional `question:<slug>` ids with `provisional.blocked_on` pointing here.

## Files affected

- New: `questionbase/README.md`, `LICENSE`, `.gitignore`, `CONTRIBUTING.md`, `schema/question-record.schema.json`, `records/questions.yaml`.
- `openevo-core/GOVERNANCE.md`: add the "Other Foundational Repos" row for QuestionBase's new block.

## Review

- [ ] Foundational Repo delegate approval (QuestionBase seat — Dustin)
- [ ] Kernel Steward approval (Dustin)
- [ ] For `specification-amendment` RFCs: N/A — this is `content`, not `specification-amendment`

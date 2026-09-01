# RFC-0010: QuoteBase Founding Ontology

**Type:** `content`

**Status:** `accepted`
**Author(s):** Claude, for Dustin Eirdosh
**Date:** 2026-09-01 (reviewed and accepted same day)

## Motivation

The ecosystem has no canonical, citable home for a specific and recurring kind of content: a
verified quotation — attributed, sourced, and reused across curriculum materials, design docs, and
discussions — as distinct from the whole work it comes from (`literaturebase`'s job) or a concept's
formal definition (`conceptbase`'s job). Today a quote used in one place (e.g. a pull-quote in the
OpenEvo Teacher's Guide) has no stable id anything else can point at; a second consumer wanting the
same quote would either re-copy the text or have no way to reference it at all. Real content already
exists and needs this home now: the OpenEvo Teacher's Guide, 3rd Edition (Hanisch, S., Eirdosh, D.,
2024) contains dozens of attributed pull-quotes from named researchers (Tomasello, Haidt, Kahneman,
Mill, Gopnik, and others) used as pedagogical anchors throughout — exactly the "real content already
exists, has no canonical citable home, and something else already needs to reference it by id" bar
`lab_manager/docs/design-notes/foundational-repo-governance-standard-and-speciesbase-integration.md`
identifies as the actual criterion behind every prior Foundational Repo founding (RFC-0002/3/4/5/6).

## Proposed change

One class: `oe:Quote`, `plannedOwner: quotebase`.

| Field | Description |
|---|---|
| `id` | `OE-QUOTE-<slug>` |
| `text` | The quotation itself, verbatim |
| `attribution` | Plain display name of who said/wrote it |
| `speakerRef` | Optional HumanBase `person:`/`group:` id, populated only once a real record exists |
| `primarySource` | The actual work the quote comes from (`citation`, `year`, `doi`, `url`, and `literatureRef` once a matching LiteratureBase record exists) — distinct from... |
| `sourceContext` | ...where inside the OpenEvo ecosystem the quote was surfaced/selected (e.g. Teacher's Guide, 3rd Edition, p. 65) |
| `verification` | New pattern, specific to QuoteBase: `status` (`unverified` \| `verified-against-primary` \| `verified-against-reprint` \| `disputed`) tracks whether the wording has actually been checked against `primarySource` — a third status axis alongside `status` (record permanence) and `provenance.review_status` (editorial maturity), because "someone judged this worth including" and "someone diffed the wording against the original" are genuinely different facts that collapsing into one field would lose |
| `conceptTags` | Provisional free-text tags (content-anchor/thinking-tool themes), pending migration to `relatedConcepts` once individual tags are confirmed against real ConceptBase entries |
| `contentAnchors` | Closed enum reusing `openevo-graph/nodes/content_anchors.json`'s existing 9 ids directly — no separate QuoteBase copy of that vocabulary |
| `relatedConcepts` / `relatedTheories` / `relatedQuestions` / `relatedLiterature` | Cross-repo reference arrays, same pattern as every sibling Foundational Repo |
| `status` | Permanent-tier lifecycle: `proposed` → `accepted` → `stable` → `deprecated` → `superseded`, with `retracted` reachable in parallel — same shape as TheoryBase/QuestionBase/LiteratureBase |

## Relations

`primarySource.literatureRef` → LiteratureBase (once a matching record exists). `speakerRef` →
HumanBase. `relatedTheories`/`relatedQuestions`/`relatedLiterature` → TheoryBase/QuestionBase/
LiteratureBase respectively. `relatedConcepts` → ConceptBase. `contentAnchors` → `openevo-graph`'s
existing content-anchor node ids (referenced, not duplicated). Referenced (never duplicated) by any
repo that wants to display or cite a quote rather than re-copy quote text locally.

## Standards justification

No existing standard combines a verbatim quotation with a *distinct* primary-source-vs-surfaced-context
split and an explicit wording-verification status separate from editorial review status. Reuses this
ecosystem's own established minimal-record pattern (`provenance`, `status`, typed cross-repo reference
arrays) rather than inventing a new one; the one genuinely new piece (`verification`) is justified by
a real, load-bearing distinction this repo's own founding content immediately needs (14 quotes scraped
from a raw-text extraction, none yet checked against their actual primary sources — collapsing that
into `review_status` would silently overstate how much has actually been verified).

## ID block reservation

`OE-QUOTE-<slug>`, reusing each record's existing hand-authored `slug` field — no vocab-slug segment,
no numeric block, matching MethodsBase/QuestionBase's `OE-<TYPE>-<slug>` precedent (one corpus, no
multi-vocabulary structure). Minted as permanent from the start — QuoteBase has no pre-RFC legacy
content, so there is no provisional `quote:<slug>` era to migrate away from (unlike TheoryBase/
QuestionBase/MethodsBase/LiteratureBase, all of which executed a provisional-to-permanent migration
as part of their own founding RFCs). 14 real records exist today (`quotebase/records/quotes.yaml`),
scraped from the OpenEvo Teacher's Guide, 3rd Edition, covering 4 of the 9 content anchors.

## Files affected

- New repo: `quotebase/README.md`, `GOVERNANCE.md`, `CONTRIBUTING.md`, `LICENSE`, `LICENSE-CODE`,
  `.gitignore`, `schema/quote-record.schema.json`, `records/quotes.yaml` (14 records),
  `scripts/validate.py`, `scripts/requirements.txt`, `.github/workflows/validate.yml`.
- `openevo-core/GOVERNANCE.md`: add the "Other Foundational Repos" row for QuoteBase (done in the
  same pass as acceptance, not deferred — same discipline RFC-0002/3/5's execution established).

## Review

Accepted — Dustin Eirdosh, 2026-09-01, live session (11th Foundational Repo).

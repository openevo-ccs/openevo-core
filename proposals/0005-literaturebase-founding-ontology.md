# RFC-0005: LiteratureBase Founding Ontology

**Type:** `content`

**Status:** `accepted`
**Author(s):** Claude, for Dustin Eirdosh
**Date:** 2026-08-16 (reviewed and accepted same day)

## Motivation

LiteratureBase is one of the nine Foundational Repos scoped in
`ecosystem-base-graph-project-architecture-and-ontology-plan.md`, but unlike TheoryBase/
QuestionBase/MethodsBase (RFC-0002/3/4) it has never had a founding RFC drafted at all — its own
`schema/literature-record.schema.json` and `GOVERNANCE.md` both say so explicitly. Unlike those
three repos, the gap isn't unbuilt content: LiteratureBase already has 119 real bibliographic
records, a real schema, CI-enforced schema validation (`scripts/validate.py`), and CI-enforced
DOI/author verification against Crossref (`scripts/verify_crossref.py`) — every real base-repo
mechanism except the RFC that would make its ids permanent. This RFC formalizes what's already
built, the same way RFC-0004 formalized MethodsBase's already-built content.

## Proposed change

One class: `oe:Literature`, `plannedOwner: literaturebase`.

| Field | Description |
|---|---|
| `id` | `OE-LITERATURE-<slug>` (see ID block reservation below for why slug-based, not DOI-derived) |
| `citation` | Field-agnostic bibliographic object: `authors[]`, `title`, `year`, `venue`, `publisher`, `volume`, `pages`, `doi`, `isbn`, `open_access_url`. No interpretive content — field-specific interpretation (e.g. `ccs-graph`'s `relevance_to_ccs`) stays local to the referencing repo, never duplicated here. |
| `type` | Enum: `journal-article` \| `book` \| `book-chapter` \| `conference-paper` \| `report` \| `thesis` \| `preprint` \| `dataset` \| `website` \| `other` |
| `license` | Controlled vocabulary for *this record's own redistribution status* (`cc0-1.0`, `cc-by-4.0`, `cc-by-sa-4.0`, `cc-by-nc-4.0`, `public-domain`, `citation-only`, `all-rights-reserved`) — distinct from the source paper's copyright unless identical. `citation-only` is the load-bearing value for closed-license sources (e.g. Semantic Scholar API terms — see `lab_manager` memory on S2 compliance): bibliographic metadata only, no abstract/full-text redistribution. |
| `domains` | Free-text array, which fields/disciplines the work sits in |
| `related` | Typed relations to other LiteratureBase records only (`supports`\|`contradicts`\|`extends`\|`criticises`\|`replicates`\|`related`) — relations to non-literature nodes stay in the referencing repo |
| `relevant_to_theory` | Forward hook for a future TheoryBase-facing stage, not populated or enforced yet |
| `status` | **New in this RFC** — the permanent-tier lifecycle (`proposed`\|`accepted`\|`stable`\|`deprecated`\|`superseded`\|`retracted`), matching TheoryBase's addition under RFC-0002. LiteratureBase had no record-permanence status field before now — `provenance.review_status` (`author-draft`\|`peer-nominated`\|...) tracks review maturity, a different axis, same distinction TheoryBase/MethodsBase/QuestionBase already draw between their own domain field and this one. |

## Relations

`related[].id` → other LiteratureBase records (same-repo, already how the schema works — unchanged
by this RFC). Referenced (never duplicated) by every other Foundational/Graph repo needing a
citation: `primarySources[].literatureRef` (TheoryBase, MethodsBase, QuestionBase, ConceptBase),
`ccs-graph`/`openevo-graph`'s own literature nodes.

## Standards justification

No existing standard combines DOI/Crossref-verifiable bibliographic metadata with this ecosystem's
own redistribution-license controlled vocabulary and typed cross-record relations at this
granularity. CSL-JSON and BibTeX cover bare citation fields but neither carries `license`'s
redistribution-status distinction (load-bearing for the Semantic Scholar API compliance case) nor
`related[]`'s typed relation vocabulary. Reuses this ecosystem's own established minimal-record
pattern (`provenance`, `status`) rather than inventing a new one.

## ID block reservation

`OE-LITERATURE-<slug>`, reusing each record's existing hand-authored `slug` field (e.g.
`kampourakis-2020`) — no vocab-slug segment, no numeric block, matching TheoryBase/QuestionBase/
MethodsBase's precedent. **Deliberately not DOI-derived**, even though 77 of 119 current records
use a DOI-escaped provisional id (`lit:doi-10-1186-s12052-019-0116-z`): the existing `slug` field
is already unique across the whole corpus (it's the actual filename today), shorter, human-legible,
and DOI-independence means a record's permanent id survives a later-discovered DOI correction or a
non-DOI source gaining one. The `citation.doi` field remains the authoritative place DOI identity
actually lives and gets Crossref-verified — the id was never the right place for that fact to live
twice.

## Files affected

- `literaturebase/schema/literature-record.schema.json`: `id` pattern, add `status`, drop
  `provisional` from `required`.
- `literaturebase/records/*.yaml` (119 files, one record each): `id` field, filename, and every
  `related[].id` cross-reference.
- `literaturebase/GOVERNANCE.md`, `README.md`, `CONTRIBUTING.md`: consolidation-phase notice,
  Identifier Scheme, Sandbox/Provisional Tier sections.
- `openevo-core/GOVERNANCE.md`: add the "Other Foundational Repos" row for LiteratureBase.
- Every real citer of a `lit:` id ecosystem-wide (swept and fixed as part of executing this RFC,
  not deferred — same discipline RFC-0002/0003's execution already established).

## Review

- [x] Foundational Repo delegate approval (LiteratureBase seat — Dustin) — 2026-08-16
- [x] Kernel Steward approval (Dustin) — 2026-08-16
- [x] For `specification-amendment` RFCs: N/A — this is `content`, not `specification-amendment`

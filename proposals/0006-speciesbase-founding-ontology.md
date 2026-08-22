# RFC-0006: SpeciesBase Founding Ontology

**Type:** `content`

**Status:** `proposed`
**Author(s):** Claude, for Dustin Eirdosh
**Date:** 2026-08-22

## Motivation

SpeciesBase (`openevo-ccs/SpeciesBase`) already holds real, populated content — 9 classes,
~150 records across Phase 1 (Identity: `sb:Taxon`, `sb:TaxonomicConcept`, `sb:LexicalForm`,
`sb:CulturalCategory`, `sb:Language`), Phase 2 (Feature graph: `sb:Feature`,
`sb:FeatureExpression`, `sb:Context`), and Phase 3 (the Tinbergen explanatory ontology:
`sb:Explanation`) — with no canonical citable home in the shared kernel ontology. It was
founded and has operated as a Graph-repo peer to `ccs-graph`/`openevo-graph`, on the reasoning
in `lab_manager/docs/design-notes/foundational-repo-governance-standard-and-speciesbase-integration.md`
§3.2 that its content is domain-specific rather than curriculum-infrastructure. That document's
own §3.1 audit found the actual bar this ecosystem uses for Foundational status is not
domain-agnosticism — none of RFC-0002/3/4/5 argue that way — but "real content already exists,
has no canonical citable home, and something else already needs to reference it by id." Under
that bar SpeciesBase clears easily: `oSci` already needs `taxon:`/`feature:` ids and designed
its own contribution path (`oSci/docs/architecture.md` §5.1) directly against SpeciesBase's
`features/`, `feature-expressions/`, `explanations/` — real PRs into SpeciesBase itself, not a
separate schema.

Per that document's §4 open item, **Dustin decided 2026-08-22, in a live session, to file this
RFC** — an explicit override of §3.2's own recommendation to stay a Graph-repo peer, made with
that recommendation's reasoning fully in view (the split-vs-unified analysis in §3.2 is
independent of Foundational-vs-Graph status and is unaffected by this RFC either way; SpeciesBase
stays unified, per Option A there).

This RFC executes §3.3 item 1's concrete change list only — minting the ontology classes. Items
2, 4, and 5 of that list (`GOVERNANCE.md`/`CONTRIBUTING.md`, the promotion-gate checklist, an
explicit "How other repos reference this" section) are real, needed, and independent of this
RFC's acceptance; they're SpeciesBase's own repo work, not kernel content, and are tracked
separately (Vikunja `Ecosystem Architecture & Governance` board). Item 3 (the numeric-to-slug id
migration) is **already done** — see below.

## Proposed change

Nine classes, `plannedOwner: speciesbase` for all:

| Class | One-line role |
|---|---|
| `oe:Taxon` | The stable, authority-independent handle for a lineage. Carries no scientific name or rank of its own — those live on its linked `TaxonomicConcept`(s). Self-referential `parentTaxon` for SpeciesBase's own working hierarchy (deliberately not any one authority's rank hierarchy). |
| `oe:TaxonomicConcept` | One biodiversity authority's circumscription (rank, parent, external record) of a `Taxon`. Phase 1 populates exactly one (GBIF-anchored) per `Taxon`; schema allows more. |
| `oe:LexicalForm` | Either a scientific or vernacular name for a `Taxon`, distinguished by a `term_type` discriminator rather than split into two classes (same pattern `oe:Competency`'s `citationOnly` mode uses in ConceptBase). |
| `oe:CulturalCategory` | A culturally/educationally meaningful category ("fish," "Säugetier") mapped to one or more `TaxonomicConcept`s via an explicit, non-identity relation type — not treated as synonymous with any one `TaxonomicConcept`. |
| `oe:Language` | Lightweight controlled-vocabulary entry backing `LexicalForm`'s language tagging. Not a full linguistic ontology. |
| `oe:Feature` | An abstract characteristic, process, capacity, or behavioral pattern. Bilingual (EN/DE) by construction; grounded in `eva_buch`'s curated 75-concept table via an alignment id rather than re-deriving German terminology independently. |
| `oe:FeatureExpression` | A concrete manifestation of a `Feature` in a specific `Taxon`. Holds an optional array of `Explanation` references — explanatory depth is added incrementally, not required complete at creation. |
| `oe:Context` | A named, reusable ecological/social/developmental/population context a `FeatureExpression` holds under. |
| `oe:Explanation` | One claim answering exactly one of the seven canonical Tinbergen-family question types for one `FeatureExpression`. Multiple (including deliberately competing) `Explanation`s may target the same `FeatureExpression`, linked via `alternative_to`, because Tinbergen's questions are analytical perspectives on one causal web, not independent boxes. Schema deliberately has no `proximate`/`ultimate` or `nature_pct`/`nurture_pct` field — both are named, citable misconceptions this ontology exists to prevent (`additionalProperties: false` makes them unrepresentable, not merely discouraged). |

Full field-level shape for each class is already authored and stable in
`SpeciesBase/schemas/*.schema.yaml` (`taxon`, `taxonomic_concept`, `lexical_form`,
`cultural_category`, `language`, `feature`, `feature_expression`, `context`,
`explanation`); this RFC ratifies those as the `oe:` mapping of an already-implemented,
already-populated ontology rather than proposing new field shapes.

**Deliberately out of scope, per SpeciesBase's own ontology notes
(`SpeciesBase/ontology/core_v1.yaml` lines 23-40):** `sb:TinbergenQuestion`, `sb:Mismatch`,
`sb:Adaptation`, and `sb:FeatureComponent` stay `reserved` — each is implemented as a closed
vocabulary field on `Explanation`/`Feature` rather than promoted to an independently addressable
class ("promote only the addressable thing"). The Analogy engine also stays `reserved`
(Phase 5+). None of these four are minted by this RFC; a future RFC can promote them if SpeciesBase's
own phasing later addresses them.

## Relations

- `Taxon.parentTaxon` → same-repo `Taxon` (self-referential hierarchy).
- `Taxon.taxonomicConcepts` → same-repo `TaxonomicConcept` (one-to-many).
- `TaxonomicConcept.externalIdentifiers` → GBIF/Catalogue of Life/NCBI records (descriptive
  external pointer, not a governed cross-repo id).
- `FeatureExpression` → `Taxon` (which lineage) and `Feature` (which characteristic).
- `Explanation.feature_expression` → same-repo `FeatureExpression`.
- `Explanation.alternative_to` → sibling `Explanation`(s), same claim, competing account.
- `Explanation.evidence` → `literatureEvidence` citations (LiteratureBase `lit:` ids where one
  exists, per this ecosystem's standard cross-repo-reference pattern).
- Not minted here, tracked separately: `Explanation`'s theoretical-framing field currently
  forward-references TheoryBase `theory:` ids informally — Vikunja task "Run joint
  theorybase/SpeciesBase theoretical_stance reconciliation pass" is the open work to formalize
  that relation, deliberately not folded into this RFC.

## Standards justification

`TaxonomicConcept`/`Taxon` reuse external biodiversity-authority backbones (GBIF, Catalogue of
Life) as anchors via `externalIdentifiers` rather than reinventing a taxonomic nomenclature
standard — SpeciesBase's own identity split (`Taxon` vs. `TaxonomicConcept`) exists specifically
so a stable internal handle survives disagreement between authorities, a distinction Darwin
Core's flatter model doesn't make but doesn't need to for this ecosystem's purpose either.
`Explanation.question_type` reuses Tinbergen's (1963) four-questions framework, extended to the
seven-question form in wide current use in evolutionary-behavior pedagogy
(`docs/tinbergens_extended_questions.md`) — an established framework in the field being modeled,
not an invented taxonomy. No existing standard models the specific combination this ontology
needs: a stable lineage identity independent of any one nomenclatural authority, cross-referenced
against a bilingual, curriculum-aligned feature vocabulary, with multiple explicitly-competing
Tinbergen-family explanations per feature-expression and a closed, misconception-resistant
vocabulary for causal claims about it.

## ID block reservation

**N/A — no numeric block needed.** SpeciesBase already migrated (2026-08-19, before this RFC,
independent of it) from its original `SB-{TYPE}-######` numeric scheme to slug-namespaced
`{type}:{slug}` ids, matching the convention every Foundational Repo founded since RFC-0002 uses
— the same rewrite RFC-0002 itself needed before acceptance for the identical reason. SpeciesBase
uses **abbreviated** type prefixes rather than the `oe:{TYPE}` uppercase form other repos favor,
chosen before this RFC and already in production use across ~150 records:

| Class | Id prefix | Records today |
|---|---|---|
| `oe:Taxon` | `taxon:` | 12 |
| `oe:TaxonomicConcept` | `taxconcept:` | 12 |
| `oe:LexicalForm` | `name:` | 25 |
| `oe:CulturalCategory` | `cultcat:` | 3 |
| `oe:Language` | `lang:` | 3 |
| `oe:Feature` | `feature:` | 55 |
| `oe:FeatureExpression` | `featexpr:` | 11 |
| `oe:Context` | `context:` | 3 |
| `oe:Explanation` | `explanation:` | 26 |

No re-encoding is proposed or needed; this RFC does not touch any existing id.

## Files affected

- `openevo-core/ontologies/core_v1.yaml`: add the 9 classes above, each `plannedOwner:
  speciesbase`, mirroring their existing `SpeciesBase/ontology/core_v1.yaml` definitions.
- `openevo-core/GOVERNANCE.md`: add the SpeciesBase row to the Foundational Repos table once
  reviewed (not preemptively — matching RFC-0003/0004's own convention).
- `SpeciesBase/ontology/core_v1.yaml`: no field-shape changes; update the header note (currently
  explaining *why* `sb:` and not `oe:` — that reasoning is superseded by this RFC) once accepted.
- No changes to any `SpeciesBase/schemas/*.schema.yaml` or any existing record — this RFC ratifies
  the existing, already-validated shape rather than changing it.

## Review

- [ ] Foundational Repo delegate approval (SpeciesBase seat — Dustin)
- [ ] Kernel Steward approval (Dustin)
- [ ] For `specification-amendment` RFCs: N/A — this is `content`, not `specification-amendment`

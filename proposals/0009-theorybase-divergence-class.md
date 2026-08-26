# RFC-0009: TheoryBase `oe:Divergence` Class

**Type:** `content`

**Author(s):** Claude, for Dustin Eirdosh
**Date:** 2026-08-26

## Motivation

`openevo-graph/sources/kampourakis-v-openevo/model_c_comparative.md` already contains a rich,
carefully-written comparative analysis of the DCR-vs-ICR dispute: 8 named "Divergences," each with
a structured `model_A_position`/`model_B_position` (summary + citations), a synthesis of what the
disagreement actually consists of (named `critical_observation`, `trade_off_analysis`,
`convergence_point`, or `operational_consequence` depending on the divergence — the role is
consistent even though the field name isn't), a `resolvability` classification, and a
`priority_for_evoke` flag. This is exactly the kind of rich modeling of contested, often-unreflected
curriculum-theory assumptions this ecosystem's FAIR-theory work is for — and it has sat almost
entirely unused: of the 8 Divergences, only 5 are even cited by number anywhere in TheoryBase (as a
bare string like `"(Divergence #2)"` inside a `contrastNote`), and none of the 8 is a resolvable,
typed object. The three Divergences never referenced at all (#1, #5, #7) are three of the
document's own five `priority_for_evoke: critical` items — including #5 (the actual correct-answer
text two real assessment instruments use for the same case) and #7 (the concrete fact that the
identical student response is scored correct by one instrument and incorrect by the other, for the
same case — stated in the source as a direct operational consequence of a real theoretical
disagreement, not an assessment bug).

TheoryBase already has `recordType: competing_proposition` (`contests` field) for one proposition
directly negating another — atomic, fine-grained. What's missing is the layer above that: an object
representing the *comparative frame around a whole disagreement* — both sides' positions together,
what the disagreement is actually about, whether/how it's resolvable, and how urgent resolving it
is. `oe:Divergence` is that layer, not a replacement for `competing_proposition`.

## Proposed change

One class, under `www.w3id.org/openevo/ontology#`, `plannedOwner: theorybase`:

| Class | Definition | Required fields |
|---|---|---|
| `oe:Divergence` | A structured comparison of two theories' positions on one specific point of disagreement, including both sides' claims, a synthesis of what the disagreement consists of, and an assessment of whether/how it could be resolved | `id`, `label`, `relatedTheories[]` (exactly 2, → Theory ids), `positionA`, `positionB`, `synthesis`, `resolvability`, `priority` |

`positionA`/`positionB` shape (structurally identical, one per side):
```yaml
positionA:
  theory: "OE-THEORY-dichotomized-causal-reasoning"      # which relatedTheories[] entry this is
  proposition: "OE-PROPOSITION-agential-biases-as-barriers"  # optional -- the existing atomic
                                                               # proposition record this position
                                                               # IS, when one already exists
  summary: "..."                                          # required, free text
  detail: "..."                                           # optional -- covers the source
                                                               # document's per-divergence extra
                                                               # fields (assessment_implication,
                                                               # correct_item + rationale,
                                                               # agency_negation_status) without
                                                               # forcing every Divergence into the
                                                               # same rigid extra-field shape
  primarySources:
    - {citation, doi, literatureRef}
```

`priority`: enum `[critical, high, moderate, low]` (renamed from the source's `priority_for_evoke`
— EvoKE was the original authoring committee, TheoryBase is this field's real home now, so the name
generalizes). `resolvability`: free string, not an enum — the source's own values range from a
short classification (`"empirically_resolvable"`) to a full sentence naming what kind of resolution
work is needed, and forcing that into a closed enum would lose real content.

Full shape: `theorybase/schema/divergence-record.schema.json`.

## Relations

- Complements, does not replace, `recordType: competing_proposition`/`contests` on Proposition
  records — a Divergence's `positionA.proposition`/`positionB.proposition` fields point at the
  existing atomic contest when one exists (5 of the source's 8 Divergences already have a matching
  `competing_proposition` pair in TheoryBase today); a Divergence is not required to reference one
  (Divergence #5, the assessment-item comparison, has no matching Proposition pair — it compares two
  concrete assessment items directly, not two abstract claims).
- `relatedTheories[]` reuses the existing `oe:Theory` id pattern, no new identifier scheme.
- `primarySources[]`/citations reuse the same shape already used across every other TheoryBase
  record type.

## Standards justification

No existing curriculum or provenance standard (CASE, IEEE LOM, xAPI, schema.org, PROV-O) models a
structured two-position theoretical disagreement with a resolvability/priority assessment attached
— this is a research-synthesis structure, not a curriculum-metadata one. The closest real precedent
is this ecosystem's own `model_c_comparative.md` source document itself, which already independently
arrived at essentially this shape (position pairs + synthesis + resolvability + priority) without
any schema forcing it to. This RFC formalizes an already-proven, already-written pattern rather than
inventing a new one.

## ID block reservation

None needed — same as RFC-0007 (`oe:TheoryBundle`): TheoryBase has no vocab-slug segment: the slug
segment reuses each record's own hand-authored `slug` field directly.

## Files affected

- `theorybase/schema/divergence-record.schema.json` (new)
- `theorybase/records/divergences.yaml` (new — first instances, migrated from
  `model_c_comparative.md`'s 8 Divergence entries)
- `theorybase/scripts/validate.py` (register the new record file, same gap RFC-0007 found and fixed
  for `theory-bundles.yaml`/`learning-dependencies.yaml`)
- `theorybase/GOVERNANCE.md` (Identifier Scheme section: class count +1)

## Review

**Status:** `accepted`.

Accepted by Dustin Eirdosh, 2026-08-26.

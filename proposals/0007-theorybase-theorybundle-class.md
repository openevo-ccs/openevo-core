# RFC-0007: TheoryBase `oe:TheoryBundle` Class

**Type:** `content`

**Status:** `accepted`
**Author(s):** Claude, for Dustin Eirdosh
**Date:** 2026-08-24

## Motivation

RFC-0002 (theorybase-founding-ontology) adopted eight of Addendum IV's meta-model classes and
deferred `oe:TheoryBundle` alone, "still too far from any concrete near-term need" at the time.
`oe:DesignPrinciple` and `oe:CurriculumDecision` were absorbed into RFC-0002 before merge;
`oe:LearningDependency`'s class was too (schema exists, `theorybase/schema/learning-dependency-
record.schema.json`), though it has zero instance records today.

The need is now concrete: Dustin asked (2026-08-24) to model Curriculum Evolution theory as a
first-class object in the CCS graph rather than only as narrative prose in the `curriculum-
evolution` Manual. TheoryBase already holds 7 real, permanently-id'd component theories
(`OE-THEORY-restructuration-theory`, `-integrated-causal-reasoning`, `-dichotomized-causal-
reasoning`, `-metatheoretical-calculus`, `-virtuous-practices-under-sparse-evidence`,
`-replicability-verdict-non-identifiability`, `-computational-models-as-theory-mediators`), but
nothing bundles them as the family the Manual is actually about — exactly the gap Addendum IV
named `oe:TheoryBundle` to fill: "a reusable collection of Theories + Assumptions that together
define a curriculum philosophy."

## Proposed change

One class, under `www.w3id.org/openevo/ontology#`, `plannedOwner: theorybase`:

| Class | Definition | Required fields |
|---|---|---|
| `oe:TheoryBundle` | A reusable collection of Theories (+ optionally Assumptions) that together define a curriculum philosophy | `id`, `label`, `memberTheories[]` (→ Theory ids, minItems 1) |

Optional structure: `organizingFrame[]` — named internal sub-groupings of `memberTheories` (e.g.
curriculum-evolution's four process-model families: cognitive / developmental / cultural /
machine-computational, per the Round 6 Chapter 3 framing already designed but not yet written
into the Manual). An `organizingFrame` entry with an empty `theories[]` is meaningful — it names
a real organizing category TheoryBase has no content for yet, not an omission — so bundle authors
are not tempted to force a theory into a family it doesn't fit just to avoid an empty array.

Full shape: `theorybase/schema/theory-bundle-record.schema.json`.

## Relations

`memberTheories[]`/`memberAssumptions[]` reference existing `oe:Theory`/`oe:Assumption` records —
no new relation to any other Foundational Repo. `ccs-graph` may reference a bundle's id from a
relation record's `theory_nodes[]` block the same way it already references bare `oe:Theory` ids.

## Standards justification

Reuses this ecosystem's own established meta-model pattern (Θ-theory-family framing, named in
`ecosystem-base-graph-architecture-addendum-3-dispute-as-graph-synthesis.md`'s open decisions) —
not a new structural idea, just the one class Addendum IV scoped for it, finally instantiated.

## ID block reservation

None needed — TheoryBase has no vocab-slug segment (RFC-0002's Identifier Scheme section); the
slug segment reuses each record's own hand-authored `slug` field directly, same as every other
TheoryBase class.

## Files affected

- `theorybase/schema/theory-bundle-record.schema.json` (new)
- `theorybase/records/theory-bundles.yaml` (new — first instance, `OE-THEORYBUNDLE-curriculum-evolution`)
- `theorybase/GOVERNANCE.md` (Identifier Scheme section: 13 classes → 14)

## Review

- [x] Foundational Repo delegate approval (TheoryBase seat) — Dustin Eirdosh, 2026-08-24 (via direct instruction to resolve Addendum IV's remaining deferred classes)
- [x] Kernel Steward approval — Dustin Eirdosh, 2026-08-24

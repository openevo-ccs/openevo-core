# RFC-0002: TheoryBase Founding Ontology

**Type:** `content`

**Status:** `proposed`
**Author(s):** Claude, for Dustin Eirdosh
**Date:** 2026-07-26

## Motivation

TheoryBase is one of the nine Foundational Repos identified in `lab_manager/docs/design-notes/ecosystem-base-graph-project-architecture-and-ontology-plan.md`, but it has never had a founding RFC — the repo is still genuinely bare (no `README.md`, no `LICENSE`, no ontology classes). Two independent design efforts converge on what it should contain:

1. **Addendum III** (`ecosystem-base-graph-architecture-addendum-3-dispute-as-graph-synthesis.md`) needs `oe:TheoreticalConstruct`, `oe:TheoreticalPosition`, `oe:Misconception`, and `oe:CrossDomainConstruct` to represent the real OpenEvo-vs-Kampourakis dispute over organism agency in evolutionary explanation (source material: `EvoMentor/data/Article_FAIRification/Kampourakis_v_OpenEvo/`).
2. **Addendum IV** (`ecosystem-base-graph-architecture-addendum-4-theorybase-general-meta-model.md`, from Dustin's own design brief) supplies a more general theory-to-curriculum meta-model — Theory, Proposition, Assumption, Evidence, Context, Competing Proposition — that Addendum III's dispute-specific types are properly instances of, not a separate design.

Rather than found TheoryBase on the narrower, single-dispute type family and re-derive the general model later, this RFC founds it on the general model directly, per Dustin's own call (2026-07-26): adopt the core six types now; defer `oe:DesignPrinciple`/`oe:CurriculumDecision`/`oe:LearningDependency`/`oe:TheoryBundle` and the "executable theory" ambition to a dedicated future RFC (tracked in Addendum IV §4/§5).

**Amended same session, before merge, to add five more classes** (still unmerged — amending a proposed RFC is the correct move, not a schema mutation):
- `oe:Mechanism` and `oe:Hypothesis` — needed for the second real dispute this ecosystem is modeling (OpenEvo's critique of the Hurst Lab evolution-education research programme), whose real source material (`EvoMentor/data/Article_FAIRification/Hurst_v_OpenEvo/Hurst_Lab_FAIRification.yaml`) already carries 7 Mechanisms (each with a `power_mediation` field) and 4 Hypotheses (each with an `evidence_assessment` block) in a schema shape close enough to adopt directly rather than redesign. These were deliberately deferred out of this RFC's original scope as "Hurst-dispute-specific"; the Hurst dispute is now in scope.
- `oe:DesignPrinciple`, `oe:CurriculumDecision`, `oe:LearningDependency` — three of Addendum IV's originally-deferred general-meta-model types, now needed to make the real LPM repos' (`bio-core-k12`, `oe-interdisciplinary-k12`) strand-level design choices traceable back to theory (see Addendum IV §4; the traceability chain was blocked pending these types). `oe:TheoryBundle` and the "executable theory / inference engine" ambition stay deferred — still too far from any concrete near-term need.

## Proposed change

Eight classes, all under `www.w3id.org/openevo/ontology#`, `plannedOwner: theorybase`:

| Class | Definition | Required fields |
|---|---|---|
| `oe:Theory` | A coherent explanatory framework, decomposable into Propositions/Assumptions, attributable to a person or group | `id`, `label`, `heldBy` (→ HumanBase `oe:Person`/`oe:Group` id), `propositions[]`, `assumptions[]`, `authorshipProvenance` (`native` \| `openevo_reconstruction_of_external_position`), `characterizationStatus` (`author_stated` \| `openevo_reconstruction_unreviewed` \| `openevo_reconstruction_reviewed`) |
| `oe:Proposition` | An individual claim within a Theory, with an evidence link | `id`, `label`, `statement`, `partOf` (→ Theory id), `evidenceQuality` |
| `oe:Assumption` | A foundational premise not itself empirically tested | `id`, `label`, `statement`, `partOf` (→ Theory id) |
| `oe:Evidence` | An empirical study/dataset/finding supporting or challenging a Proposition | `id`, `label`, `supports`/`challenges` (→ Proposition id), `citation` (→ LiteratureBase id) |
| `oe:Context` | Educational/cultural/developmental conditions under which a Proposition is expected to hold | `id`, `label`, `description` |
| `oe:CompetingProposition` | An explicitly modeled alternative claim on the same question as another Proposition | `id`, `label`, `contests` (→ Proposition id) |
| `oe:Misconception` | A documented, empirically-observed incorrect student belief pattern (does not reduce to `CompetingProposition` — a misconception is a student cognitive artifact, not a scholarly claim) | `id`, `label`, `description`, `exampleStudentStatement`, `affectedGradeBands[]`, `targetPropositions[]` |
| `oe:CrossDomainConstruct` | A construct treated as domain-general (spans e.g. biological/cultural/computational instantiations) | `id`, `label`, `domains[]` |
| `oe:Mechanism` | A directed causal link between two constructs, with strength/evidence and — mandatory — a `powerMediation` note (who/what the mechanism's effect depends on, and how it may vary across populations/contexts) | `id`, `label`, `fromConstruct`, `toConstruct`, `relationshipType`, `strength`, `powerMediation` |
| `oe:Hypothesis` | A directly testable, falsifiable claim spanning one or more constructs, with a structured evidence assessment | `id`, `label`, `statement`, `constructsInvolved[]`, `testability`, `falsificationCondition`, `evidenceAssessment` (`nIndependentStudies`, `currentAssessment`, `confidenceLevel`, `gaps`) |
| `oe:DesignPrinciple` | A normative recommendation derived from one or more Theories — the missing link between "what a theory claims" and "what a curriculum does" | `id`, `label`, `statement`, `derivedFrom` (→ Theory id(s)) |
| `oe:CurriculumDecision` | A concrete design choice, justified by a DesignPrinciple, instantiated in a real ConceptBase Strand | `id`, `label`, `statement`, `justifiedBy` (→ DesignPrinciple id), `groundedIn` (→ Theory id), `instantiatesIn` (→ ConceptBase `OE-STRAND-######` id) |
| `oe:LearningDependency` | A theory-relative prerequisite/reinforcement claim among concepts — different Theories can imply different dependency graphs for the same concepts | `id`, `label`, `statement`, `relativeToTheory` (→ Theory id), `precedesConcept`/`reinforcesConcept` |

## Relations

`oe:Theory.heldBy` → HumanBase `oe:Person`/`oe:Group`. `oe:Evidence.citation` → LiteratureBase `oe:Literature`. All eight classes are referenced, never duplicated, by `openevo-graph`'s dispute-synthesis layer (`openevo-graph/schema/dispute-graph-v1.schema.json`, itself needing no OECB RFC per Addendum III §6) — TheoryBase stays atomic and single-owner per class instance; the graph repo carries cross-entity relational content (`divergesFrom`, `critiques`, etc.).

## Standards justification

No existing standard directly models "theory as decomposable, versioned, competing claims with evidence links" at this granularity for curriculum-theoretic content specifically. The closest analogues (SKOS for simple concept schemes, PROV-O for provenance, Nanopublications for atomic scientific claims) inform the field/attribute choices above (`evidenceQuality`, provenance fields) but don't supply the domain-specific `Theory`/`Proposition`/`Misconception` distinction this ecosystem needs. Reuses this ecosystem's own already-established provenance pattern (`provisional.blocked_on`, `authorshipProvenance`, `characterizationStatus`) rather than inventing a new one.

## ID block reservation

Per `GOVERNANCE.md#identifier-block-allocation`, TheoryBase reserves its first block for each of the thirteen new types, all `000100`–`000199` (first vocabulary/collection — the Kampourakis and Hurst-Lab dispute corpora):

| Type | Block |
|---|---|
| `OE-THEORY-######` | `000100`–`000199` |
| `OE-PROPOSITION-######` | `000100`–`000199` |
| `OE-ASSUMPTION-######` | `000100`–`000199` |
| `OE-EVIDENCE-######` | `000100`–`000199` |
| `OE-CONTEXT-######` | `000100`–`000199` |
| `OE-COMPETINGPROPOSITION-######` | `000100`–`000199` |
| `OE-MISCONCEPTION-######` | `000100`–`000199` |
| `OE-CROSSDOMAINCONSTRUCT-######` | `000100`–`000199` |
| `OE-MECHANISM-######` | `000100`–`000199` |
| `OE-HYPOTHESIS-######` | `000100`–`000199` |
| `OE-DESIGNPRINCIPLE-######` | `000100`–`000199` |
| `OE-CURRICULUMDECISION-######` | `000100`–`000199` |
| `OE-LEARNINGDEPENDENCY-######` | `000100`–`000199` |

(Each type prefix is its own namespace, matching the existing `OE-CONCEPT-`/`OE-STRAND-`/`OE-COMPETENCY-` pattern — no cross-type collision risk.) Until this RFC merges, TheoryBase content uses slug-based provisional ids (`theory:dcr-position`, `proposition:niche-selection`, etc.) with `provisional.blocked_on` pointing here, exactly as `humanbase`/`literaturebase` already do for their own pending founding RFCs.

## Files affected

- Already added (Kampourakis dispute pass): `theorybase/README.md`, `LICENSE`, `.gitignore`, `CONTRIBUTING.md`, `schema/theory-record.schema.json`, `schema/proposition-record.schema.json`, `schema/misconception-record.schema.json`, `schema/cross-domain-construct-record.schema.json`, `records/theories.yaml`, `records/propositions.yaml`, `records/assumptions.yaml`, `records/misconceptions.yaml`, `records/cross-domain-constructs.yaml`.
- Added this amendment (Hurst-dispute + traceability-chain pass): `schema/mechanism-record.schema.json`, `schema/hypothesis-record.schema.json`, `schema/design-principle-record.schema.json`, `schema/curriculum-decision-record.schema.json`, `schema/learning-dependency-record.schema.json`, `records/mechanisms.yaml`, `records/hypotheses.yaml`, `records/design-principles.yaml`, `records/curriculum-decisions.yaml`, `records/learning-dependencies.yaml`.
- `openevo-core/GOVERNANCE.md`: add the "Other Foundational Repos" row for TheoryBase's new blocks (currently a placeholder note).

## Review

- [ ] Foundational Repo delegate approval (TheoryBase seat — Dustin)
- [ ] Kernel Steward approval (Dustin)
- [ ] For `specification-amendment` RFCs: N/A — this is `content`, not `specification-amendment`

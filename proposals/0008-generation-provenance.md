# RFC-0008: Generation provenance (`oe:producedBy`) — declaring how an entity was produced, orthogonal to whether it's been reviewed

**Type:** `content`

**Author(s):** Claude, for Dustin Eirdosh
**Date:** 2026-08-26

## Motivation

This ecosystem has independently invented the same distinction three times, in three different repos, because it keeps needing it: TheoryBase's `provenance.extracted_by` (`human` | `llm`), `deutsche_lp`'s `verificationStatus` (`unverified-secondary-source` and friends), and ConceptBase's `oe:epistemicStatus` (RFC-0019, `designed-thought-experiment` vs. `field-validated-curriculum`) all mark some version of "was this synthesized/drafted by a person or a model, and has anyone checked it." Each is real, each is used, and none of them talk to each other — a consumer resolving an entity from a fourth repo has no single, kernel-level place to ask "how was this actually produced."

The immediate trigger: a new workstream (see `lab_manager/docs/design-notes/fair-theory-rigor-and-synthetic-lpm-discourse-strategic-plan.md` §4, and the follow-on planning session 2026-08-26) is about to generate a genuinely mixed body of content — TheoryBase `CrossDomainConstruct`/`Proposition` records drafted live, in a human-attended session, cross-referencing a real German curriculum dataset (`EvoMentor_DE`'s `bk_information_kommunikation` Basiskonzept) and a real NGSS competency (`OE-COMPETENCY-ngss-life-science-ms-ls1-8`), destined for `interdisciplinary-k12` strand content. TheoryBase's existing `extracted_by` enum (`human` | `llm`) can't distinguish "an LLM drafted this live, with a human attending and steering the whole time" from "an LLM batch-generated this with nobody watching, reviewed only afterward" — those are different DOA (dependency-on-author, Van Lissa et al. 2026) situations, and this ecosystem's own past incident (`deutsche_lp`'s README names a real case of treating unattended pasted AI research as more authoritative than it was) is exactly why the distinction matters in practice, not just in principle.

`oe:Entity` (this ontology's abstract base class) already carries `oe:status` and `oe:version` as inherited properties every concrete class gets for free, without each owning repo re-declaring them. This is the same shape of fact — true of any entity, in any Foundational Repo, regardless of class — so it belongs at the same level.

## Scope narrowed during review (2026-08-26) — read before the Proposed change below

The original draft of this RFC also proposed `oe:supervisedBy` (a required-when-llm field naming who was present during drafting) and `oe:sourceArtifact` (a pointer to the generating artifact). Both were cut before acceptance, for two different reasons, recorded here rather than silently dropped:

- **`oe:supervisedBy` — cut as excessive governance for how this lab actually operates.** Implementing it as a schema-level requirement in TheoryBase broke all 61 existing `extracted_by: llm` records (confirmed by actually running `scripts/validate.py`, not assumed) — a real regression against this ecosystem's own additive/non-breaking discipline. More fundamentally, in a single-operator lab, `supervisedBy` would almost always just equal `provenance.added_by` (Dustin is both the one live in the session and the one who commits the record) — a new mandatory field duplicating a fact already on the record, not capturing a genuinely different one. This is the same shape of mistake this ecosystem has already named and caught once (`characterizationStatus` was deliberately kept non-schema-required for the same reason, 2026-08-22). If a future case genuinely needs "who was present" distinct from `added_by` — e.g. an unattended GWDG batch run reviewed later by someone else — that's a real signal to revisit this with a concrete example, not to guess now.
- **`oe:sourceArtifact` — cut as redundant, not wrong.** TheoryBase's existing `provenance.sourceProvenance` field already does this job (see that field's schema description, updated alongside this RFC to note the mapping explicitly). No second field needed there; a future owning repo without an equivalent field could still reintroduce `oe:sourceArtifact` later via ordinary MINOR-bump RFC if a real need shows up.

What survives, and is what this RFC actually proposes: `oe:producedBy` alone, with its value space extended to three values instead of two.

## Proposed change

One new `entityProperty`, domain `oe:Entity` (inherited by every concrete class — `oe:Theory`, `oe:Concept`, `oe:Method`, `oe:Question`, everything), added to `ontologies/core_v1.yaml`:

```yaml
  oe:producedBy:
    label: produced by
    domain: oe:Entity
    range: xsd:string
    status: accepted
    definition: >
      How this entity's content was actually generated: human | llm |
      human-llm-collaborative. Value space constrained at the schema layer
      (each owning repo's own schema/*.schema.json), not enumerated here —
      the same pattern already used for oe:status. human-llm-collaborative
      names live, human-attended drafting (a session where a person is
      actively present and steering), distinct from unattended/batch llm
      generation reviewed only afterward — the real distinction this RFC
      exists to make nameable, without requiring a separate mandatory
      field to record who was in the room (see "Scope narrowed" above for
      why that went further than warranted). Orthogonal to review status
      (TheoryBase's provenance.review_status, or any owning repo's
      equivalent): a record can be llm-produced and expert-validated, or
      human-produced and still author-draft. Also orthogonal to
      oe:epistemicStatus (RFC-0019, ConceptBase) — that field asks whether
      an LPM is a designed thought-experiment vs. field-validated
      curriculum; this field asks who/what drafted the content, at the
      level of any entity, not just LPMs.
```

**MINOR** version bump, `ontologies/core_v1.yaml` 1.6.0 → 1.7.0 — purely additive, one new inherited property, no existing class or property changes.

Realized in TheoryBase (done alongside this RFC, all 10 record schemas, `scripts/validate.py` confirms 118/118 OK): `provenance.extracted_by`'s enum extended from `[human, llm]` to `[human, llm, human-llm-collaborative]`, with a description cross-referencing this RFC. No new field, no new required property — purely additive, zero existing records affected.

## Relations

- **Orthogonal to `oe:status`** (lifecycle maturity) and to each owning repo's `provenance.review_status` (has this been reviewed, by whom, to what standard). `oe:producedBy: llm` + `review_status: expert-validated` is a fully coherent, and hoped-for-common, combination.
- **Orthogonal to `oe:epistemicStatus`** (RFC-0019, ConceptBase) — that property is `oe:LPM`-scoped and answers a curriculum-validation-intent question (designed thought-experiment vs. field-validated curriculum). This property is entity-general and answers a generation-process question. A `designed-thought-experiment` LPM's own strand content can be `human`-produced (as `bio-core-k12`/`interdisciplinary-k12`'s existing three strands each are today) or `human-llm-collaborative` (as new content under this RFC's own motivating workstream will be) — the two facts don't imply each other.
- **Specializes, rather than replaces, three existing mechanisms**: TheoryBase's `provenance.extracted_by`/`sourceProvenance`, `deutsche_lp`'s `verificationStatus`, and RFC-0019's `epistemicStatus` all remain exactly as they are — each is a real, working, repo-specific or class-specific mechanism answering a narrower question than this RFC's kernel-level property does. Owning repos are not required to migrate existing fields onto this one.

## Standards justification

No existing curriculum or provenance standard (CASE, IEEE LOM, xAPI, schema.org, PROV-O) names the live-attended-vs-batch-unattended generation distinction directly — PROV-O's `wasGeneratedBy`/`wasAttributedTo` model a single generation event, not this distinction. Per this repo's own §3 item 4 standard: this is closer to a research-integrity/governance distinction than a curriculum-content structure, so the relevant precedent is this ecosystem's own prior art (`oe:status`, TheoryBase's `characterizationStatus`/`authorshipProvenance`, RFC-0019's `epistemicStatus` — all schema-constrained string enums with a documented, additive value space) rather than an external standard.

## ID block reservation

Not applicable — this RFC mints no new identifiers or classes, only one new property on the existing `oe:Entity` class.

## Files affected

| File | Change |
|---|---|
| `ontologies/core_v1.yaml` | **Done, 2026-08-26.** Added `oe:producedBy` to `entityProperties`. MINOR (1.6.0 → 1.7.0) |
| `theorybase/schema/*.schema.json` (all 10 record schemas) | **Done, this session.** Extended `provenance.extracted_by`'s enum to add `human-llm-collaborative`; added a description cross-referencing this RFC; added a description to `sourceProvenance` noting it already fulfills the "pointer to generating artifact" role this RFC's earlier draft would have duplicated. Zero new required fields; `scripts/validate.py` confirms 118/118 records still pass. |
| `lab_manager/docs/design-notes/fair-theory-rigor-and-synthetic-lpm-discourse-strategic-plan.md` | Update Phase C item 6 to point at this RFC once accepted, rather than describing it as still-proposed |

## Review

**Status:** `accepted`.

Accepted by Dustin Eirdosh, 2026-08-26. `oe:producedBy` added to `ontologies/core_v1.yaml`'s
`entityProperties` (1.6.0 → 1.7.0). TheoryBase's schema-side extension was already live prior to
acceptance (this RFC formalizes the kernel-level property the repo-level change specializes).

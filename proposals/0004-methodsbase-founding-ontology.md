# RFC-0004: MethodsBase Founding Ontology

**Type:** `content`

**Status:** `proposed`
**Author(s):** Claude, for Dustin Eirdosh
**Date:** 2026-08-02

## Motivation

MethodsBase is one of the nine Foundational Repos scoped in
`ecosystem-base-graph-project-architecture-and-ontology-plan.md` (§7: "MethodsBase... proceed
[2026-07-25 go-ahead]") but, like QuestionBase and TheoryBase before their founding RFCs, is still
genuinely bare — only `LICENSE`/`LICENSE-CODE`/`.gitignore` exist. It's needed now because the
ecosystem already has real, operationalized methods with no canonical citable home: the OpenEvo
Design-Based Research (DBR) Model (implemented as a four-stage cycle by
`curriculum-agents/agents/dbr-cycle-facilitator.md`), the Multi-Agent Deliberation Protocol
(specified in `curriculum-evolution/docs/methods/multi-agent-deliberation-protocol.md`, implemented
by `curriculum-agents`' `deliberation-runner`), and the EvoFlex vignette + forced-choice
assessment-design pattern (Hanisch, Eirdosh, González Galli, Hartelt, Pérez & Cupo, 2025, *Journal
of Biological Education*; generalized by the `assessment-designer` agent). Susan Hanisch's
forthcoming book chapter (Kap. 15, "Zukünftige Forschung") also proposes at least one genuinely new
research method (curriculum network analysis over machine-readable Länder curricula) that belongs
here as a `proposed`, not-yet-implemented record.

This RFC also closes `ecosystem-base-graph-project-architecture-and-ontology-plan.md` §13 Open
Decision 4: *"`oe:Method`'s scope — single class with a `methodClass` enum vs. keeping `oe:Practice`
separate."* See `lab_manager/docs/design-notes/methodsbase-founding-design-and-dbr-model-integration-plan.md`
§2 for the reasoning: nothing in the real content surveyed (a research protocol vs. a teaching
technique) needs a different field shape, only a different value on one enum field — the same
reasoning that already retired `oe:Practice` as a candidate separate class in §7 of the architecture
plan. **Resolved: single class, `oe:Method`, distinguished by `methodClass`.**

## Proposed change

One class: `oe:Method`, `plannedOwner: methodsbase`.

| Field | Description |
|---|---|
| `id` | `OE-METHOD-######` (or provisional `method:<slug>` pending this RFC's merge) |
| `slug` | Kebab-case identifier |
| `label` | Short method title |
| `methodClass` | Enum: `pedagogical-practice` \| `research-method` — closes Open Decision 4 above. `oe:Practice` is retired as a separate class; any content that would have used it uses `methodClass: pedagogical-practice` here instead. |
| `description` | The technique/protocol itself |
| `discipline` | Which discipline or pedagogical tradition it comes from (this repo's own README already stated this requirement, ahead of the RFC) |
| `status` | Enum: `proposed` \| `active` \| `validated` \| `deprecated` — a method's *maturity/adoption* in this ecosystem. Deliberately **not** QuestionBase's seven-stage consensus lifecycle: a method isn't converging toward expert agreement, it's moving from described → implemented → independently validated. See design note §3 for worked examples of each value. |
| `protocolSteps` | Optional ordered array of strings, for methods with a defined step sequence |
| `whenToUse` | Optional free-text guidance |
| `decomposesInto` | Array of same-repo child `method:` ids, in order — reused directly from QuestionBase's `oe:Question.decomposesInto` pattern (same-repo relations are ordinary base-repo content). Array order carries phase order, so a separate `sequencePosition` field is unnecessary. |
| `partOfMethod` | Back-reference from a child method to its container — the inverse of `decomposesInto`, needed because a phase method is independently citable (its own `implementedBy`, its own `primarySources`), not an inline sub-object. |
| `cyclesTo` | **New relative to the QuestionBase pattern.** Optional single `method:` id. A plain tree can't express that a cyclic method's last phase feeds back into its first (the DBR Model's "dissemination & infrastructuring" stage closing back to "context analysis" for the next cycle) — this field makes that closure explicit and machine-readable rather than only stated in prose. |
| `relatedQuestions` | Array of `question:` ids — only populated where a real QuestionBase record exists |
| `implementedBy` | Array of `{type: agent\|skill\|tool\|repo, name, repo, note?}` objects pointing at where this method is actually operationalized today. Not a governed cross-repo id (agents/skills/tools aren't OECB entities) — a descriptive pointer, the field that makes this repo integrated rather than a standalone taxonomy. |
| `primarySources` | Same shape as QuestionBase's `primarySources` (`citation`/`doi`/`literatureRef`), plus one addition: optional `url`, since several real sources here (the DBR model's own web page, `curriculum-evolution`'s methods docs) are institutional web resources without a DOI. |

## Relations

`decomposesInto`/`partOfMethod`/`cyclesTo` → other MethodsBase records (ordinary same-repo
relations). `relatedQuestions` → QuestionBase. `implementedBy` → descriptive pointers into
`curriculum-agents` (agents, skills, tools) and other repos; not a governed reference, since the
targets aren't OECB entities.

## Standards justification

No existing standard models "a research or pedagogical method, classed by whether it's a teaching
technique or a research protocol, decomposable into ordered phases that can cycle back on
themselves, with an explicit link to where it's actually implemented as running software" at this
granularity for curriculum-theoretic content. Reuses this ecosystem's own established minimal-record
pattern (QuestionBase's `id`/`provisional`/`provenance` shape) rather than importing an unrelated
methods taxonomy built for a different domain (e.g. clinical-trial protocol registries).

## ID block reservation

Per `GOVERNANCE.md#identifier-block-allocation`: `OE-METHOD-000100`–`000199` (first block, same
starting offset convention QuestionBase used for its first block). Until merged, MethodsBase content
uses provisional `method:<slug>` ids with `provisional.blocked_on` pointing here.

## Coordinated amendment: QuestionBase `relatedMethods` and a real TheoryBase hypothesis

Two small, additive changes in sibling repos are coordinated with this RFC rather than deferred,
because they're what make MethodsBase integrated rather than a standalone taxonomy — checked
directly against a live FAIR-theory review (`fair-theory-specification` skill) before drafting:

- **`questionbase/schema/question-record.schema.json`**: adds an optional `relatedMethods` array
  field (`method:` ids) — the inverse of `oe:Method.relatedQuestions` above. Additive only; all 23
  pre-existing QuestionBase records still validate unchanged. Needs QuestionBase's own Foundational
  Repo delegate sign-off (same seat-holder, Dustin, per `GOVERNANCE.md`) alongside this RFC's review,
  not folded silently into RFC-0003.
- **`theorybase/records/hypotheses.yaml`**: adds `hypothesis:openevo-dbr-model-core-claim`, using
  TheoryBase's existing (not new) `hypothesis-record.schema.json`, to state the OpenEvo DBR Model's
  own falsifiable core claim as a checkable object rather than only as prose on the model's public
  page. `method:openevo-dbr-model`'s new `theoreticalGrounding` field references it by id. This is
  the FAIR-*theory* half of "use the lab's FAIR Theory tooling" (Van Lissa et al. 2026) — deliberately
  **not** built against `ccs-graph/schema/fair-theory-v1.schema.json`, confirmed to not yet exist
  (`ccs-graph/schema/` has zero files); TheoryBase's real, already-populated schema is the actual
  implementation, not the aspirational meta-schema the architecture plan's §6.9 describes as future
  work.

See `lab_manager/docs/design-notes/methodsbase-founding-design-and-dbr-model-integration-plan.md`
§9 for the full review this is grounded in.

## Files affected

- New: `methodsbase/schema/method-record.schema.json`, `methodsbase/records/methods.yaml`.
- `methodsbase/README.md`: rewritten to reflect bootstrapped status.
- `questionbase/schema/question-record.schema.json`: adds `relatedMethods` (see above).
- `questionbase/records/questions.yaml`: adds 10 records drawn from Hanisch (forthcoming) Kap. 15,
  cross-walked to MethodsBase's DBR-phase records via `relatedMethods`.
- `theorybase/records/hypotheses.yaml`: adds `hypothesis:openevo-dbr-model-core-claim` (see above).
- `openevo-core/GOVERNANCE.md`: add the "Other Foundational Repos" row for MethodsBase's new block
  once this RFC is actually reviewed (not preemptively — matching how RFC-0003's row wasn't added
  until QuestionBase's block was live).

## Review

- [ ] Foundational Repo delegate approval (Method seat — Dustin)
- [ ] Kernel Steward approval (Dustin)
- [ ] For `specification-amendment` RFCs: N/A — this is `content`, not `specification-amendment`

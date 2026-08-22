# OpenEvo Core

> The shared kernel underneath every Foundational and Project repo in the OpenEvo Computational Curriculum Studies (CCS) Lab — Project repos include the free-schema field-knowledge repos (`ccs-graph`, `openevo-graph`, `eva-graph`, kind: `graph`), OECB-governed LPM content repos (kind: `lpm`), and thin applications (kind: `app`); see `lab_manager/docs/design-notes/ecosystem-two-layer-architecture-simplification-plan.md`. Owns no curriculum content of its own.

[![OpenEvo Lab](https://img.shields.io/badge/OpenEvo%20Lab-openevo.eva.mpg.de-teal)](http://openevo.eva.mpg.de)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/Content%20License-CC--BY--NC--SA%204.0-lightgrey.svg)](LICENSE)
[![Tooling License: MIT](https://img.shields.io/badge/Code%20License-MIT-yellow.svg)](LICENSE-CODE)
[![Namespace](https://img.shields.io/badge/Namespace-www.w3id.org%2Fopenevo-purple)](https://www.w3id.org/openevo/)
[![Ontology](https://img.shields.io/badge/Ontology-v1.5.0-blue)](ontologies/core_v1.yaml)
[![Governance](https://img.shields.io/badge/Governance-Shared%20Kernel%20RFC-blueviolet)](GOVERNANCE.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](CONTRIBUTING.md)

---

## What is this?

**OpenEvo Core** is the connective infrastructure shared by every repository in the OpenEvo CCS Lab: the `oe:` upper ontology, the `OE-{TYPE}-######` identifier scheme, the cross-repo RFC process for proposing new shared ontology classes, and the `www.w3id.org/openevo/` namespace root.

It exists because that infrastructure used to live inside [`conceptbase`](https://github.com/openevo-ccs/conceptbase) — the ecosystem's first mature repo, and still the canonical home for `oe:Concept`/`oe:LPM`/`oe:Strand` instances — simply because ConceptBase was, for a time, the only real repo in the ecosystem. It isn't anymore. Nine **Foundational Repos** now share this kernel co-equally; none of them, ConceptBase included, governs it unilaterally. Full rationale: [`lab_manager`'s design note on this exact question](https://github.com/openevo-ccs/lab_manager/blob/main/docs/design-notes/ecosystem-shared-kernel-and-co-equal-governance-plan.md).

> **This repo stores no entity instances.** No Concepts, LPMs, Strands, Competencies, Resources, Projects, Literature records, People, Groups, Questions, Methods, or TheoryBase nodes live here. Every one of those lives in its own owning Foundational Repo, referenced by permanent identifier — never duplicated.

## The ecosystem

```
                         OPENEVO CORE  (this repo)
        oe: upper ontology · identifier scheme · cross-repo RFC process
                    · www.w3id.org/openevo/ namespace root

                                     │  every Foundational Repo
                                     │  consumes this by reference,
                                     │  none of them owns it
                                     ▼
                              FOUNDATIONAL REPOS  (co-equal peers)

   ConceptBase        — oe:Concept, oe:LPM, oe:Strand, oe:LearningObject, oe:Competency
   CompetencyBase     — oe:Competency (planned migration from ConceptBase)
   TeachingBase       — oe:Resource, oe:Assessment
   ProjectBase        — oe:Project
   LiteratureBase     — oe:Literature
   HumanBase          — oe:Person, oe:Group
   TheoryBase         — oe:TheoreticalPosition and the wider theory-apparatus node family
   QuestionBase       — oe:Question
   MethodsBase        — oe:Method

                                     │
                                     ▼
                                GRAPH REPOS
                    ccs-graph · openevo-graph · eva-graph
       field-specific interpretation and relations over base facts —
       still defers to this repo, not any single Foundational Repo,
       for anything that would be a new ontology class

                                     │
                                     ▼
                               PROJECT REPOS
                    EvoMentor · EvoMentor_DE · KoMet · netlogo · (future)
       thin applications that assemble Foundational + Graph entities by id
```

Two independently governed reference LPMs currently depend on ConceptBase's own entity types (not on this repo directly): [`bio-core-k12`](https://github.com/openevo-ccs/bio-core-k12) and [`interdisciplinary-k12`](https://github.com/openevo-ccs/interdisciplinary-k12).

## What's in scope (and what isn't)

**This repository stores:**

- ✅ The `oe:` upper ontology (`ontologies/core_v1.yaml`) — class and property definitions shared across every Foundational Repo.
- ✅ The identifier scheme (`OE-{TYPE}-######`) and the cross-repo Identifier Block Allocation registry (`GOVERNANCE.md`).
- ✅ The RFC process and template for proposing a genuinely new shared ontology class.
- ✅ The `www.w3id.org/openevo/` namespace root and its shared-kernel sub-paths (`/ontology`; cross-cutting `/vocab/*` and `/schemas/*`).

**This repository deliberately does *not* store:**

- ❌ Any entity instance data (Concepts, LPMs, Strands, Competencies, Resources, Projects, Literature, People, Groups, Questions, Methods, TheoryBase nodes) — those live in their owning Foundational Repo.
- ❌ Entity-specific JSON Schemas or their `$defs` (e.g. `conceptId`/`lpmId`/`strandId` patterns) — those stay in `conceptbase/schemas/`, since they encode ConceptBase's own validation rules, not generic kernel content.
- ❌ Field-specific interpretation, relations, or contested-claims data — that's the job of graph-kind Project repos (`ccs-graph`, `openevo-graph`, `eva-graph`), which get free local schema for exactly this content.

## Namespace

All persistent identifiers in this ecosystem resolve under:

```
https://www.w3id.org/openevo/
```

via the [w3id.org](https://w3id.org) permanent identifier redirection service. The bare root, `/ontology`, and the cross-cutting `/vocab/*`/`/schemas/*` sub-paths resolve here; `/concept/{id}`, `/competency/{id}`, `/alignment/{id}`, `/lpm/{id}`, `/strand/{id}` resolve to ConceptBase's own registry, unchanged by this repo's existence — see [`w3id-submission/openevo/`](w3id-submission/openevo/) for the staged resolution rules this repo maintains.

## Governance

Sized for what this ecosystem actually is today — one active maintainer, not a multi-institution consortium — while still naming the seats explicitly so growth doesn't silently recentralize onto whoever happens to hold the most repos. See [`GOVERNANCE.md`](GOVERNANCE.md) for the full Roles table, RFC process, and Identifier Block Allocation registry, and [`CONTRIBUTING.md`](CONTRIBUTING.md) for how to propose a change.

## History

Founded 2026-07-26 by migrating the shared-kernel portions of `conceptbase` — see [`proposals/0001-shared-kernel-founding-and-migration.md`](proposals/0001-shared-kernel-founding-and-migration.md) for the full rationale and [`conceptbase/proposals/0013-openevo-core-kernel-migration.md`](https://github.com/openevo-ccs/conceptbase/blob/rfc-0013-openevo-core-kernel-migration/proposals/0013-openevo-core-kernel-migration.md) for ConceptBase's own record of its narrowed scope. `conceptbase/proposals/0001`–`0012` remain in place as historical record — nothing was renumbered or deleted.

## License

- **Content** (ontology, governance process, documentation): [CC BY-NC-SA 4.0](LICENSE)
- **Code** (landing-site tooling): [MIT](LICENSE-CODE)

## Links

- 🧪 Research lab: [openevo.eva.mpg.de](http://openevo.eva.mpg.de)
- 🌐 Persistent identifier namespace: [www.w3id.org/openevo/](https://www.w3id.org/openevo/)
- 📚 Entity registry: [`conceptbase`](https://github.com/openevo-ccs/conceptbase)
- 🗳️ Governance: [`GOVERNANCE.md`](GOVERNANCE.md)

# Contributing to OpenEvo Core

**Status:** Informative — a practical getting-started guide. For the authoritative process, roles, and versioning rules, see [`GOVERNANCE.md`](GOVERNANCE.md).

## Before you start

Read [`README.md`](README.md) for orientation. **This repository is not where most OpenEvo contributions belong.** If you want to add a new Concept, LPM, Strand, Competency, Alignment, Resource, Project, Literature record, Person, Group, Question, Method, or TheoryBase node — or a new vocabulary within any of those — go to that entity type's own Foundational Repo and its own `CONTRIBUTING.md`/`GOVERNANCE.md`. This repo exists for exactly three narrower things:

1. A genuinely new `oe:` ontology **class** (not a new instance of an existing one).
2. A change to the `OE-{TYPE}-######` identifier scheme, or a new Identifier Block Allocation reservation.
3. A change to the `www.w3id.org/openevo/` namespace root or its shared-kernel sub-paths (`/ontology`, cross-cutting `/vocab/*`, `/schemas/*`).

If you're not sure which side of that line your change is on, open an issue first rather than guessing — the cost of a five-minute clarifying conversation is much lower than an RFC drafted against the wrong repo.

## Proposing a change

1. **Open an RFC.** A pull request against [`proposals/`](proposals/), using the RFC template: motivation, proposed IRI under `www.w3id.org/openevo/`, relations to existing classes, and — per the same rule ConceptBase's own spec established — why no existing standard already covers the need.
2. **Name the owning Foundational Repo.** Every new `oe:` class needs a `plannedOwner` (which Foundational Repo will instantiate it) recorded in `ontologies/core_v1.yaml`'s `reserved` block before promotion, so there's never ambiguity about which repo's own process picks up from here.
3. **Get review.** Per [`GOVERNANCE.md`](GOVERNANCE.md): the Kernel Steward, plus the delegate(s) for whichever Foundational Repo(s) the class or change affects.
4. **Block allocation.** If your RFC introduces a new vocabulary or LPM-equivalent unit anywhere in the ecosystem, reserve its numeric ID block in `GOVERNANCE.md#identifier-block-allocation` as part of the same RFC — before any entries are authored under it, in whichever repo owns that entity type.

## Where things live

`ontologies/` (the shared upper ontology — the only TBox file in this repo), `proposals/` (RFCs, this repo's own scope only), `w3id-submission/openevo/` (the staged `.htaccess`/`readme.md` this repo periodically submits to the real w3id.org registry), `app/` (the GitHub Pages landing site serving as the `www.w3id.org/openevo/` root).

## Versioning and lifecycle

The ontology versions independently via semver, exactly as it did inside ConceptBase before the move. See [`GOVERNANCE.md`](GOVERNANCE.md) for the full rules.

## Questions

Open a discussion via [GitHub Issues](../../issues), or reach out to the OpenEvo Computational Curriculum Studies Lab ([openevo.eva.mpg.de](http://openevo.eva.mpg.de)).

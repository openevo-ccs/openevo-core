# RFC-0001: Founding this repository as the shared kernel, migrated out of ConceptBase

**Type:** `specification-amendment`

**Status:** `accepted`
**Author(s):** Claude (planning + execution), for Dustin Eirdosh
**Date:** 2026-07-26

## Motivation

`conceptbase` was the OpenEvo CCS ecosystem's first mature, governed repo, built before any of its eight peer Foundational Repos (CompetencyBase, TeachingBase, ProjectBase, LiteratureBase, HumanBase, TheoryBase, QuestionBase, MethodsBase) existed even as stubs. Because of that founding-order accident, three genuinely separate things ended up living in one repo, under one `GOVERNANCE.md`, merged by one set of Maintainers:

1. ConceptBase's own entity registry (`oe:Concept`/`oe:LPM`/`oe:Strand`/`oe:LearningObject`/`oe:Competency` instances) — legitimately its own peer-equal role.
2. The shared `oe:` upper ontology (`ontologies/core_v1.yaml`) — infrastructure every Foundational Repo depends on, not just ConceptBase's own business.
3. The cross-repo RFC process, its Roles table, and the Identifier Block Allocation registry (`conceptbase/GOVERNANCE.md`) — likewise ecosystem-wide, not repo-specific.

`lab_manager/docs/design-notes/ecosystem-base-graph-project-architecture-and-ontology-plan.md` §10 already named the consequence without naming the cause: every one of the eight pending base-layer RFCs (`oe:Resource` promotion, `oe:Project`, `oe:Literature`, `oe:Person`+`oe:Group`, TheoryBase's whole node-type family, `oe:Question`, `oe:Method`) was slated to be proposed, reviewed, and merged inside ConceptBase's own repo — by ConceptBase's Maintainers and Domain Editors, not by anyone representing the repo that would actually own the new class. ConceptBase's own README stated the resulting topology plainly: "OECB is the hub of a federated ecosystem." Full diagnosis: `lab_manager/docs/design-notes/ecosystem-shared-kernel-and-co-equal-governance-plan.md`.

This RFC is the fix, filed now — before those eight RFCs land against the wrong repo and the pattern cements further.

## Proposed change

- Items 2 and 3 above move here, to `openevo-core`, a new repo with no entity data of its own.
- Item 1 stays in `conceptbase`, unchanged — see `conceptbase/proposals/0013-openevo-core-kernel-migration.md` for that repo's own record of its narrowed scope.
- `ontologies/core_v1.yaml` is moved verbatim (no class, property, or version change) — see the relocation note at the top of that file in this repo.
- `conceptbase/schemas/common.defs.yaml` is **not** moved. On direct inspection it is almost entirely ConceptBase-specific identifier patterns (`conceptId`, `lpmId`, `strandId`, `competencyId`, `alignmentId`, their sandbox-tier counterparts, `alignmentConceptRef`, `conceptbaseManifest`) rather than generic cross-repo fragments — moving it would break every `$ref` in ConceptBase's own schema files for no real gain. If a second Foundational Repo's schema later needs the genuinely generic fragments in that file (`localizedString`, `citation`, `author`, `extensions`, `semver`, the `status` enum), that's a future RFC once there's a real second consumer — not speculative work done here.
- The `www.w3id.org/openevo/` namespace root (`^$`), `/ontology`, and the cross-cutting `/schemas/*`/`/vocab/*` sub-paths move to resolve against this repo instead of `conceptbase`. `/concept/{id}`, `/competency/{id}`, `/alignment/{id}`, `/lpm/{id}`, `/strand/{id}` are unchanged — they already resolved to ConceptBase specifically (a peer-equal pattern, not the thing this RFC fixes) and stay that way. Staged at `w3id-submission/openevo/` in this repo, pending Dustin's decision on when to submit the upstream PR to `perma-id/w3id.org` (see Open Decisions below — this is a live production redirect already, per direct verification against `https://w3id.org/openevo/`).

## Relations

Supersedes the relevant portions of `conceptbase/GOVERNANCE.md` (Roles, RFC Process, Identifier Block Allocation — reproduced here in generalized form) without invalidating any existing identifier, RFC, or block reservation minted under it. `conceptbase/proposals/0001`–`0012` remain exactly where they are, as historical record — not renumbered, not moved.

## Standards justification

Not a novel structure — this generalizes a pattern already precedented within the same registry this ecosystem's namespace lives inside: `w3id.org` itself separates a shared root-registry process from each namespace owner's own subtree (confirmed by direct read of sibling namespaces `cevo`, `inmevo`, `evorao` in the cloned `w3id.org` registry). OBO Foundry separates its cross-ontology operations/registry process from any single member ontology's own editors the same way.

## ID block reservation

Not applicable — this RFC does not introduce a new vocabulary or LPM. It relocates the *registry of reservations itself* (see `GOVERNANCE.md#identifier-block-allocation`), copying — not renumbering — every block already reserved in `conceptbase/GOVERNANCE.md` at time of migration.

## Files affected

- New: this repo's `README.md`, `GOVERNANCE.md`, `CONTRIBUTING.md`, `LICENSE`, `LICENSE-CODE`, `ontologies/core_v1.yaml`, `proposals/TEMPLATE.md`, `app/` + `.github/workflows/pages.yml` (GitHub Pages landing site), `w3id-submission/openevo/.htaccess` + `readme.md`.
- Changed in `conceptbase`: `ontologies/core_v1.yaml` (removed, replaced with `ontologies/README.md` pointer), `README.md` (narrowed scope, "hub" framing corrected), `GOVERNANCE.md` (header note narrowing scope, Identifier Block Allocation cross-referenced), `CONTRIBUTING.md` (step 1 clarified), `docs/oecb_specifications.md` (§4.1, §6 intro, §11.1–11.2 amendment notes, version bump), new `proposals/0013-openevo-core-kernel-migration.md`.
- Not yet changed: `w3id.org/openevo/.htaccess` in the real, live `perma-id/w3id.org` registry — staged in this repo's `w3id-submission/`, submission itself is an Open Decision below.

## Review

- [x] Kernel Steward approval — Dustin Eirdosh, via direct instruction to execute the full migration in one pass (2026-07-26 session)
- [x] Explicit consensus recorded — this RFC's own drafting and execution *is* that record, per the same session

## Open decisions (carried from the planning doc, not resolved by this RFC)

1. Whether/when to submit the staged `w3id-submission/openevo/` content as a PR to the real, external `perma-id/w3id.org` repo — that changes a live production redirect other people may already be resolving, and needs Dustin's explicit go-ahead plus his own GitHub session (no `gh` CLI in the environment that executed this RFC).
2. Whether `openevo-core`'s own GitHub Pages landing page is the right long-term namespace root, or an interim measure pending `openevo.net` (still bare).
3. Composition of the Foundational Repo delegate table (`GOVERNANCE.md`) beyond Dustin, once a second independent contributor to any base appears.

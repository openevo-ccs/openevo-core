# OpenEvo

Permanent identifier namespace for the OpenEvo Computational Curriculum Studies (CCS) Lab — the shared upper ontology, identifier scheme, and cross-repo governance process that let nine independently governed Foundational Repos (plus their Graph and Project layers) interoperate.

Homepage: https://w3id.org/openevo/
Kernel source / issue tracker: https://github.com/openevo-ccs/openevo-core
Kernel governance (source of truth for the RFC process, identifier scheme, and Identifier Block Allocation): https://github.com/openevo-ccs/openevo-core/blob/main/GOVERNANCE.md
Entity registry (Concept/LPM/Strand/Competency/Alignment instances — unchanged by this revision): https://github.com/openevo-ccs/conceptbase

## Revision note

This supersedes the original registration ([RFC-0003](https://github.com/openevo-ccs/conceptbase/blob/main/proposals/0003-w3id-namespace-mvp-resolution.md), merged as [perma-id/w3id.org#6389](https://github.com/perma-id/w3id.org/pull/6389)) for exactly four rules: the bare root, `/ontology`, `/schemas/*`, `/vocab/*` — which now resolve against `openevo-core` instead of `conceptbase`, per [openevo-core RFC-0001](https://github.com/openevo-ccs/openevo-core/blob/main/proposals/0001-shared-kernel-founding-and-migration.md). Every other rule (`/concept/`, `/competency/`, `/alignment/`, `/lpm/`, `/strand/`) is unchanged — those already resolved to ConceptBase specifically, a peer-equal pattern this revision does not touch.

## Resolved sub-paths

| Path | Resolves to |
|---|---|
| `https://w3id.org/openevo/` | OpenEvo Core's landing page (this ecosystem's shared-kernel repo) |
| `https://w3id.org/openevo/ontology` | The shared upper ontology (raw YAML; `#ClassName` fragments select a class client-side) |
| `https://w3id.org/openevo/vocab/{name-with-version}` | A controlled vocabulary file (ConceptBase), e.g. `vocab/BIO-CORE-v1.0.0` |
| `https://w3id.org/openevo/concept/{id}` | A single Concept instance as flat JSON (ConceptBase), e.g. `concept/OE-CONCEPT-000102` |
| `https://w3id.org/openevo/competency/{id}` | A single Competency instance as flat JSON (ConceptBase) |
| `https://w3id.org/openevo/alignment/{id}` | A cross-vocabulary alignment record as flat JSON (ConceptBase) |
| `https://w3id.org/openevo/lpm/{id}` | The dependent repository that owns a given Learning Progression Model identifier |
| `https://w3id.org/openevo/strand/{id}` | The dependent repository that owns a given Strand identifier |
| `https://w3id.org/openevo/schemas/{name}.schema.json` | A JSON Schema document (raw YAML, ConceptBase) |

This remains an intentional MVP: everything above resolves to something real today, but only as flat JSON / raw YAML — full content negotiation (JSON-LD, RDF, SPARQL) is still planned and will be added without changing any identifier or requiring a new PR to this registry, since redirect targets are keyed by stable URL patterns rather than per-identifier rules.

## Contact

This space is administered by:

**Dustin Eirdosh**
GitHub: [dustineirdosh](https://github.com/dustineirdosh)

OpenEvo Computational Curriculum Studies (CCS) Lab — https://openevo.eva.mpg.de

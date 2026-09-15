# For AI agents

If you were sent to this repo to find the OpenEvo **logo** or **design tokens**, start here — you
don't need the ontology/governance material in `README.md` for that.

## Design tokens (colors, fonts, radii, light/dark theme)

Canonical file: [`design-system/tokens.css`](design-system/tokens.css)
Hosted copy: `https://openevo-ccs.github.io/openevo-core/design-system/tokens.css`

Tokens only — no component markup, no layout, no JS. See
[`design-system/README.md`](design-system/README.md) for usage and versioning notes.

## Logo / brand mark

**No canonical OpenEvo logo file currently exists in this repo** (checked 2026-09-15: no
`.svg`/`.png`/`.jpg`/`.ico` of any kind anywhere in this repository). If a logo exists elsewhere in
the ecosystem (e.g. a private repo like `lab_manager`), it has not yet been published to a public
repo the way `design-system/tokens.css` was.

Do not fabricate, generate, or guess a logo and present it as "the OpenEvo logo." If asked for one
and none is available, say so and point back to this file — don't invent a placeholder that could
get mistaken for the real thing.

## What this repo is NOT

`openevo-core` owns no curriculum content and no entity instances — no Concepts, LPMs, Strands,
Competencies, Resources, Projects, Literature records, People, Groups, Questions, Methods, or
TheoryBase nodes. If you're looking for actual curriculum or knowledge-graph data, this is the
wrong repo. See the ecosystem diagram in `README.md` for which repo owns what (most of those repos
are private).

## What this repo IS

The shared kernel underneath every other repo in the OpenEvo ecosystem: the `oe:` upper ontology,
the `OE-{TYPE}-######` identifier scheme, the cross-repo RFC process for proposing new shared
ontology classes, and the `www.w3id.org/openevo/` namespace root. Full detail in `README.md`.

# OpenEvo Design System — Tokens

Shared CSS design tokens for every public static app across the OpenEvo CCS Lab ecosystem. See
[`lab_manager`'s authoring-format design note](https://github.com/openevo-ccs/lab_manager/blob/main/docs/design-notes/ecosystem-authoring-format-style-guide-and-wordpress-ingestion-plan.md)
§4 for the original rationale (that repo is private now, but the doc history stands).

## Scope

Tokens only: surface/text/border colors, chart series colors, status colors, radii, font stack,
and the light/dark theme-switching mechanism. No component markup, no layout rules, no JS — those
stay independent per app.

## Usage

Link the stylesheet directly:

```html
<link rel="stylesheet" href="https://openevo-ccs.github.io/openevo-core/design-system/tokens.css">
```

Load it before your app's own stylesheet. Your app's stylesheet should stop declaring its own
`:root` token block and just use the variables (`var(--surface-1)`, etc.).

**Versioning:** while only a couple of apps consume this, tracking `main` is fine. Once more
consumers depend on it, pin to a tagged commit instead (e.g. via jsDelivr, or a Pages deploy of a
release branch) so a future token change doesn't silently reflow every consumer at once.

## Current consumers

- [`conceptbase/app`](https://github.com/openevo-ccs/conceptbase) — ConceptBase Explorer (original source of these tokens)

## Provenance

These values were originally authored in `conceptbase/app/css/styles.css`, itself derived from the
`dataviz` skill's validated default palette (`references/palette.md`), then hand-copied into
`lab_manager/app/css/styles.css`. Consolidated into `openevo-graph/design-system/` on 2026-07-23 to
remove that duplication, moved to `lab_manager` on 2026-07-27, then moved here — `openevo-core`,
the ecosystem's shared kernel repo — on 2026-07-28 when `lab_manager` went private and its
dashboard moved to an internal-only server, no longer a viable public host for a shared asset.

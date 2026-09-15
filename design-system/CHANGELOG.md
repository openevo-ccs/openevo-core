# Design system changelog

Additive-only by policy — see `README.md`'s "Versioning and the compatibility contract" section.
No entry below has ever renamed or re-valued a token that existed in an earlier entry.

## 2026-09-15 — Brand, type, space, and an 8-slot chart palette

**Why:** this repo's own landing page (`app/`) — the shared kernel's flagship app, and the one
place in the ecosystem most obligated to dogfood this file — had never actually linked
`tokens.css`. It carried its own, unrelated `:root` palette (a purple accent with no relationship
to the shared surfaces/text/chart-series tokens) since the page was first written. That's the
opposite of what a shared token file is for, and it meant the ecosystem had no shared brand
accent color at all — every app that needed a link/button color had nothing to reference and had
to invent its own, exactly as `app/` had. This pass closes that gap and gives `app/` and future
OpenEvo-branded apps enough tokens to build a full page — not just a chart — without inventing a
parallel palette.

**Added:**
- `--brand`, `--brand-hover`, `--brand-soft`, `--focus-ring`, `--focus-ring-width` — the
  ecosystem's first shared UI accent color, verified ≥4.5:1 on all surface tokens in both themes,
  deliberately distinct from every chart series hue.
- `--font-mono` and a type scale: `--text-xs`…`--text-4xl`, `--leading-*`, `--weight-*`.
- A spacing scale, `--space-1`…`--space-8`, and readable-measure containers `--content-width-sm`/
  `-md`/`-lg`.
- `--radius-lg`, `--radius-full` alongside the original `--radius`/`--radius-sm`.
- Elevation: `--shadow-sm`/`-md`/`-lg`, themed per light/dark.
- Motion: `--ease-standard`, `--duration-fast`/`-base`/`-slow`.
- `--chart-1`…`--chart-8`, the full validated categorical order from the dataviz skill's
  reference palette (`--chart-1`/`--chart-6` alias the original `--series-a`/`--series-b`);
  `--sequential-1`…`--sequential-5`; `--diverging-cool`/`-mid`/`-warm`.
- `brand/favicon.svg` and `brand/mark.svg` — the ecosystem's first shared favicon/mark, a
  branching-node glyph.
- `design-system/index.html` + `preview.css` — a live, theme-toggleable showcase of every token
  above, deployed via the existing GitHub Pages workflow at
  `https://openevo-ccs.github.io/openevo-core/design-system/`.

**Changed (non-breaking):**
- `app/index.html` and `app/css/styles.css` now link `tokens.css` and consume it instead of
  keeping their own independent palette. `app/` is now a listed consumer in `README.md`.

**Unchanged:** every token present before this entry — name and value both.

## 2026-07-28 and earlier

Provenance only; no changelog kept before this file was added. See `README.md`'s "Provenance"
section: authored in `conceptbase/app/css/styles.css`, derived from the dataviz skill's
`references/palette.md`, consolidated across `openevo-graph` and `lab_manager` before landing
here as the ecosystem's shared kernel repo.

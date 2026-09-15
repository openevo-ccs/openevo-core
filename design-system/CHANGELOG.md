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

**Follow-up, same day, after an adversarial review pass:**
- Added `--border-width-accent`, `--tracking-wide`, `--focus-ring-offset` (three values that were
  hand-duplicated across `app/css/styles.css`, `preview.css`, and a showcase code sample) as real
  tokens.
- `app/css/styles.css` and `preview.css` now wrap their `transition` rules in
  `@media (prefers-reduced-motion: no-preference)` instead of applying them unconditionally.
- Extracted the theme-toggle script (previously duplicated inline in two files) into
  `theme-toggle.js`; documented its `oe-theme` localStorage contract in `README.md`.
- Fixed a pre-existing broken link in `app/index.html` (`GOVERNANCE.html`, which never existed)
  to point at the real file on GitHub; pointed the showcase's README/CHANGELOG links at rendered
  GitHub blob URLs instead of raw Pages-served Markdown.
- Softened the brand mark's rationale in `README.md` — it's a generic branching glyph, not a
  literal illustration of `oe:Divergence` (RFC-0009 is a binary structure; the mark is ternary) —
  and added minimum-size/clear-space/recolor usage guidelines.
- Added `brand/apple-touch-icon.png`, `brand/icon-192.png`, `brand/icon-512.png`,
  `brand/og-image.png`, and `brand/site.webmanifest` — the raster assets a real second
  public-facing app needs immediately and the two SVGs alone didn't cover — wired into both
  `app/index.html` and `design-system/index.html`.
- Added a one-line MIT license clarification for this directory in `README.md`.
- Added `scripts/validate_design_tokens.py` and `.github/workflows/design-tokens-validate.yml`:
  the compatibility contract above was previously enforced by documentation alone; this pins the
  exact name/value of all 43 pre-2026-09-15 declarations (across all three theme blocks) and
  fails CI if any of them is renamed, removed, or re-valued.

**Unchanged:** every token present before this entry — name and value both.

## 2026-07-28 and earlier

Provenance only; no changelog kept before this file was added. See `README.md`'s "Provenance"
section: authored in `conceptbase/app/css/styles.css`, derived from the dataviz skill's
`references/palette.md`, consolidated across `openevo-graph` and `lab_manager` before landing
here as the ecosystem's shared kernel repo.

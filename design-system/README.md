# OpenEvo Design System — Tokens

Shared CSS design tokens and brand assets for every public static app across the OpenEvo CCS Lab
ecosystem. See `lab_manager`'s authoring-format design note
(`docs/design-notes/ecosystem-authoring-format-style-guide-and-wordpress-ingestion-plan.md`) §4 for
the original rationale (that repo is private now, so not publicly linkable, but the doc history
stands).

**Live showcase:** [`design-system/index.html`](index.html) (deployed at
`https://openevo-ccs.github.io/openevo-core/design-system/`) renders every token below —
color, type, space, radius, elevation, and a couple of token-only component recipes — with a
light/dark/system toggle. Start there.

## Scope

Tokens and brand marks only: surface/text/border colors, chart series colors, status colors,
brand/interactive color, a type scale, a spacing scale, radii, elevation (shadows), motion
durations/easing, the font stack(s), the light/dark theme-switching mechanism, and the
`brand/` SVG marks. **No component markup, no layout rules, no JS framework — those stay
independent per app.** `design-system/index.html` and `preview.css` are the one documented
exception: they exist only to render this showcase and are not meant to be linked by a consuming
app.

## Usage

Link the stylesheet directly, before your app's own stylesheet:

```html
<link rel="stylesheet" href="https://openevo-ccs.github.io/openevo-core/design-system/tokens.css">
<link rel="stylesheet" href="your-app.css">
<link rel="icon" href="https://openevo-ccs.github.io/openevo-core/design-system/brand/favicon.svg" type="image/svg+xml">
```

Your app's stylesheet should stop declaring its own `:root` token block and just use the
variables (`var(--surface-1)`, `var(--brand)`, `var(--space-4)`, etc.). `app/` in this repo is
now a consumer too — see its `css/styles.css` for a worked example of an app stylesheet that
holds only layout/component rules and no re-declared palette.

**Versioning and the compatibility contract.** Every token that existed before 2026-09-15
(`--surface-1`, `--surface-2`, `--page-plane`, `--text-primary`, `--text-secondary`,
`--text-muted`, `--gridline`, `--baseline`, `--border`, `--border-strong`, `--series-a`,
`--series-b`, `--good`, `--warning`, `--serious`, `--critical`, `--radius`, `--radius-sm`,
`--font`) **keeps its name and value indefinitely** — `conceptbase/app` links `tokens.css` live
from GitHub Pages with no version pin, so a rename or re-value ships to production the moment it
lands on `main`, with no chance to coordinate a migration. Changes to this file are additive:
new tokens get added, existing ones don't move. See [`CHANGELOG.md`](CHANGELOG.md) for what's
been added since first publication. Once enough consumers depend on this file that even additive
churn becomes noisy, pin to a tagged commit instead (e.g. via jsDelivr, or a Pages deploy of a
release branch).

## Token reference

### Surfaces, text & borders (original)

| Token | Role |
|---|---|
| `--page-plane` | Page background, behind all cards/panels |
| `--surface-1` | Primary card/panel background |
| `--surface-2` | Raised/secondary surface (e.g. code blocks, table zebra) |
| `--text-primary` | Body text, headings |
| `--text-secondary` | De-emphasized but still readable text |
| `--text-muted` | Captions, axis labels — not for body copy (sits under 4.5:1 on `--surface-1` by design; pair with size/weight, not alone) |
| `--gridline` | Chart gridlines, hairline dividers |
| `--baseline` | Chart axis/baseline strokes |
| `--border` | Default hairline border |
| `--border-strong` | Emphasized border (inputs, focus-adjacent chrome) |

### Brand & interactive (added 2026-09-15)

| Token | Role |
|---|---|
| `--brand` | Links, primary actions, active/selected state. ~5.3:1 on `--surface-1` (light), ~9.3:1 on dark. |
| `--brand-hover` | Hover/pressed state for brand-colored elements |
| `--brand-soft` | Tinted background for badges/callouts carrying brand color |
| `--focus-ring` | `:focus-visible` outline color (currently `var(--brand)`) |
| `--focus-ring-width` | `:focus-visible` outline width (`2px`) |

`--brand` is a teal, deliberately not reused from the chart palette below — an app that shows
both UI chrome and charts on the same screen should never have a link or button read as a data
series. Use `--brand` for interface color; use `--chart-*`/`--series-*` only for data marks.

### Status (original, fixed — never themed)

| Token | Role |
|---|---|
| `--good` / `--warning` / `--serious` / `--critical` | State indicators. Two (`--warning`, `--serious`) sit under 3:1 on the light surface by design — always pair with an icon/shape and a text label, never color alone. |

### Chart palette (original 2 slots + 6 added 2026-09-15)

| Token | Hue | Notes |
|---|---|---|
| `--series-a` | blue | Original; conceptbase/app's first series. Equal to `--chart-1`. |
| `--series-b` | green | Original; conceptbase/app's second series. Equal to `--chart-6`. |
| `--chart-1`…`--chart-8` | blue, orange, aqua, yellow, magenta, green, violet, red | Full validated 8-slot categorical order from the dataviz skill's reference palette. Use in order for new multi-series work, and re-run that skill's `validate_palette.js` for the series count you actually ship (see the Chart palette note below). |
| `--sequential-1`…`--sequential-5` | blue, light→dark | Magnitude encoding (heatmaps, choropleths). `--sequential-3` equals `--chart-1`. |
| `--diverging-cool` / `--diverging-mid` / `--diverging-warm` | blue / gray / red | Polarity encoding. Equal to `--chart-1` / a new neutral / `--chart-8`. |

These chart tokens track the **dataviz skill**'s validated default palette
(`references/palette.md` in that skill) — the same source `tokens.css`'s original two series
colors were drawn from. Before shipping any chart with 3+ series, run that skill's
`scripts/validate_palette.js` against the exact ordering you use; the defaults here are a
validated starting point, not a substitute for that check on your specific chart.

### Typography (original font stack + scale added 2026-09-15)

| Token | Value / role |
|---|---|
| `--font` | Original body sans stack |
| `--font-mono` | Identifiers, code, `OE-{TYPE}-######` IDs |
| `--text-xs` … `--text-4xl` | Type scale, `0.75rem` to `2.75rem` |
| `--leading-tight` / `--leading-normal` / `--leading-relaxed` | `1.2` / `1.5` / `1.7` |
| `--weight-regular` / `--weight-medium` / `--weight-semibold` / `--weight-bold` | `400` / `500` / `600` / `700` |

### Spacing, measure, radius, elevation, motion (added 2026-09-15)

| Token | Value |
|---|---|
| `--space-1` … `--space-8` | `0.25rem` → `4rem` |
| `--content-width-sm` / `-md` / `-lg` | `42rem` / `52rem` / `64rem` — readable-measure containers |
| `--radius` / `--radius-sm` | Original: `8px` / `5px` |
| `--radius-lg` / `--radius-full` | New: `12px` / `999px` (pills, avatars) |
| `--shadow-sm` / `--shadow-md` / `--shadow-lg` | Elevation, themed per light/dark |
| `--ease-standard` | `cubic-bezier(0.4, 0, 0.2, 1)` |
| `--duration-fast` / `--duration-base` / `--duration-slow` | `120ms` / `200ms` / `320ms` — wrap in `@media (prefers-reduced-motion: no-preference)` in your own CSS; these tokens don't do that for you |

## Brand assets

`brand/favicon.svg` — self-contained (carries its own teal background chip), safe to use as a
`<link rel="icon">` as-is regardless of browser chrome. `brand/mark.svg` — the same glyph in
`currentColor` with no background, for inline use directly against a page (nav bars, this
showcase's header). Both render the same mark: a single node branching into three, echoing the
ecosystem's ontology-graph and evolutionary-divergence subject matter (see `oe:Divergence`,
RFC-0009). Recolor by editing the SVG directly — these are not tokenized (favicons/inline marks
don't participate in the CSS custom-property cascade the same way).

## Accessibility notes

- Text-role tokens (`--text-primary`, `--text-secondary`, `--brand`) are verified at ≥4.5:1
  against `--surface-1`/`--surface-2`/`--page-plane` in both themes. `--text-muted` and two of
  the four status colors are intentionally below that floor (axis labels, state icons) — never
  put load-bearing text in those colors alone.
- `--focus-ring` / `--focus-ring-width` give every consuming app the same visible
  `:focus-visible` treatment; apps should apply them (`outline: var(--focus-ring-width) solid
  var(--focus-ring); outline-offset: 2px;`) rather than removing focus outlines.
- Status and chart colors are never the sole carrier of meaning — pair with an icon/shape and a
  label, per the dataviz skill's own non-negotiables.

## Current consumers

- [`conceptbase/app`](https://github.com/openevo-ccs/conceptbase) — ConceptBase Explorer (original source of these tokens)
- [`app/`](../app) — this repo's own GitHub Pages landing site (adopted 2026-09-15; previously kept an independent, unrelated palette — see `CHANGELOG.md`)

## Provenance

These values were originally authored in `conceptbase/app/css/styles.css`, itself derived from
the `dataviz` skill's validated default palette (`references/palette.md`), then hand-copied into
`lab_manager/app/css/styles.css`. Consolidated into `openevo-graph/design-system/` on 2026-07-23
to remove that duplication, moved to `lab_manager` on 2026-07-27, then moved here —
`openevo-core`, the ecosystem's shared kernel repo — on 2026-07-28 when `lab_manager` went
private and its dashboard moved to an internal-only server, no longer a viable public host for a
shared asset. Expanded 2026-09-15 with brand/interactive color, typography, spacing, radius,
elevation, motion, an extended chart palette, brand SVG marks, and this showcase page — see
[`CHANGELOG.md`](CHANGELOG.md).

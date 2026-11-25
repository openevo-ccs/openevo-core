# OpenEvo brand tokens

The OpenEvo look in one file: `brand.tokens.json`. Colours, fonts, type sizes, shapes and print page setup live there and nowhere else. A small script turns that file into the style files each format needs, so a web page, an e-book, a Word file and a slide deck all read the same values.

This folder holds the **brand** palette (teal, navy, neutrals, fonts). The neighbouring `../tokens.css` holds the neutral **chart and tool** palette used by ConceptBase and OpenLPM. They are kept apart on purpose: a chart colour should never look like a button.

## Files

| File | What it is |
|---|---|
| `brand.tokens.json` | The source. Edit this file, then run the script. |
| `build_tokens.py` | Writes `dist/` from the source. `--check` fails if `dist/` is out of date. Needs Python 3 only. |
| `dist/brand.css` | CSS variables (`--oe-teal`, `--oe-navy`, `--oe-font-heading` and so on) for web pages, widgets and apps. |
| `dist/book.css` | Reading and print styles for e-book chapters, including the A4 page setup for PDF. |
| `dist/epub.css` | The e-book (EPUB) stylesheet. |
| `dist/tokens.json` | The same values flattened, for scripts that build Word and PowerPoint files. |

## Use

```html
<link rel="stylesheet" href="https://openevo-ccs.github.io/openevo-core/design-system/brand/dist/brand.css">
```

Load it before your own stylesheet and stop declaring your own brand colours. Pin to a tagged release once more than one site depends on it, so a change cannot reflow every site at once.

## Change rules

- A colour, font or size changes here, in one pull request, with the generated `dist/` files in the same commit.
- Contrast between text and background colours must stay at WCAG AA or better. The OpenEvo.net style check (`kit/check/style_check.py --tokens` in the openevo.net repository) tests the main pairs.
- Version number in the token file goes up with every change that alters a value.

## Where the values come from

Teal #006C66 and the three fonts (Nunito, Roboto, Roboto Slab) were read from the old openevo.eva.mpg.de site's compiled styles. The navy is #272D63. An older capture recorded #000077 and the Learning Hub still carries that value; the site and OpenLPM use #272D63. Chart colours come from the Field Guide figures and `../tokens.css`. The six map colours are the ones TeachingBase widgets and OpenLPM share.

Word and PowerPoint files use Calibri for body text, because Roboto is not installed on most computers and Office cannot fall back to another font by itself.

## Status

Version 0.1.0, first draft from a format test on 2026-11-25. Not yet adopted by any site. The OpenEvo.net build will be the first consumer.

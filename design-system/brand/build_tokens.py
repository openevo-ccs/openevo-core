#!/usr/bin/env python3
"""Generates every style file from brand.tokens.json.

    python kit/design/build_tokens.py            # write kit/design/dist/
    python kit/design/build_tokens.py --check    # fail if dist/ differs from the tokens

Outputs (all generated, never edited by hand):
    brand.css   CSS variables for web pages, widgets and companion apps
    book.css    reading and print styles for e-book chapters (screen, @page rules for PDF)
    epub.css    the e-book stylesheet (no page rules, no screen controls)
    tokens.json the same values flattened, for scripts that build Word and PowerPoint files
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "brand.tokens.json"
DIST = HERE / "dist"


def load() -> dict:
    return json.loads(SRC.read_text(encoding="utf-8"))


def flat_colors(t: dict) -> dict[str, str]:
    out = {}
    for group, items in t["color"].items():
        for name, v in items.items():
            if name.startswith("_"):
                continue
            out[name] = v["value"]
    return out


def font_stack(t: dict, key: str) -> str:
    f = t["font"][key]
    return f"'{f['family']}', {f['fallback']}"


def brand_css(t: dict) -> str:
    lines = [f"/* GENERATED from kit/design/brand.tokens.json v{t['version']}. Do not edit by hand. */", ":root {"]
    for name, val in flat_colors(t).items():
        lines.append(f"  --oe-{name}: {val};")
    for key in t["font"]:
        lines.append(f"  --oe-font-{key}: {font_stack(t, key)};")
    w = t["type"]["web"]
    lines += [f"  --oe-text-size: {w['body']};", f"  --oe-text-small: {w['small']};", f"  --oe-h1: {w['h1']};",
              f"  --oe-h2: {w['h2']};", f"  --oe-h3: {w['h3']};", f"  --oe-line: {w['line']};"]
    for k, v in t["shape"].items():
        lines.append(f"  --oe-{k}: {v};")
    lines.append("}")
    return "\n".join(lines) + "\n"


def book_css(t: dict) -> str:
    c = flat_colors(t)
    p, pg = t["type"]["print"], t["page"]
    return f"""/* GENERATED from kit/design/brand.tokens.json v{t['version']}. Do not edit by hand. */
{brand_css(t).split(chr(10), 1)[1]}
html {{ font-family: var(--oe-font-body); color: var(--oe-ink); }}
body {{ margin: 0; font-size: {p['body']}; line-height: {p['line']}; }}
h1, h2, h3, h4 {{ font-family: var(--oe-font-heading); line-height: 1.25; break-after: avoid; }}
h1 {{ font-size: {p['h1']}; color: var(--oe-navy); margin: 0 0 6pt; }}
h2 {{ font-size: {p['h2']}; color: var(--oe-teal); margin: 16pt 0 5pt; padding-top: 4pt; border-top: 0.75pt solid var(--oe-border); }}
h3 {{ font-size: {p['h3']}; color: var(--oe-ink); margin: 11pt 0 3pt; }}
a {{ color: var(--oe-teal); text-decoration: none; }}
table {{ border-collapse: collapse; width: 100%; font-size: {p['small']}; margin: 8pt 0; break-inside: auto; }}
thead {{ display: table-header-group; }}
tr {{ break-inside: avoid; }}
th, td {{ border-bottom: 0.5pt solid var(--oe-border); padding: 3pt 5pt; text-align: left; vertical-align: top; }}
th {{ font-family: var(--oe-font-heading); color: var(--oe-text-muted); border-bottom: 1pt solid var(--oe-border); }}
figure {{ margin: 10pt 0; break-inside: avoid; }}
figure img, img {{ max-width: 100%; height: auto; }}
figcaption {{ font-size: {p['small']}; color: var(--oe-text-muted); margin-top: 3pt; }}
blockquote, .fg-note {{ background: var(--oe-surface-alt); border-left: 3pt solid var(--oe-teal); margin: 8pt 0; padding: 5pt 9pt; }}
p, li {{ orphans: 3; widows: 3; }}
@page {{
  size: {pg['size']};
  margin: {pg['margin-top']} {pg['margin-outer']} {pg['margin-bottom']} {pg['margin-inner']};
}}
@page :right {{ margin: {pg['margin-top']} {pg['margin-outer']} {pg['margin-bottom']} {pg['margin-inner']}; }}
@page :left  {{ margin: {pg['margin-top']} {pg['margin-inner']} {pg['margin-bottom']} {pg['margin-outer']}; }}
"""


def epub_css(t: dict) -> str:
    p = t["type"]["print"]
    return f"""/* GENERATED from kit/design/brand.tokens.json v{t['version']}. Do not edit by hand. */
:root {{ --oe-teal: {flat_colors(t)['teal']}; --oe-navy: {flat_colors(t)['navy']}; --oe-ink: {flat_colors(t)['ink']};
  --oe-text-muted: {flat_colors(t)['text-muted']}; --oe-border: {flat_colors(t)['border']}; --oe-surface-alt: {flat_colors(t)['surface-alt']}; }}
body {{ font-family: {font_stack(t, 'body')}; color: var(--oe-ink); line-height: {p['line']}; }}
h1, h2, h3, h4 {{ font-family: {font_stack(t, 'heading')}; line-height: 1.25; page-break-after: avoid; }}
h1 {{ color: var(--oe-navy); }}
h2 {{ color: var(--oe-teal); border-top: 1px solid var(--oe-border); padding-top: .3em; margin-top: 1.6em; }}
a {{ color: var(--oe-teal); }}
table {{ border-collapse: collapse; width: 100%; font-size: .92em; }}
th, td {{ border-bottom: 1px solid var(--oe-border); padding: .25em .4em; text-align: left; vertical-align: top; }}
th {{ color: var(--oe-text-muted); }}
figure {{ margin: 1em 0; page-break-inside: avoid; }}
img {{ max-width: 100%; height: auto; }}
figcaption {{ font-size: .9em; color: var(--oe-text-muted); }}
blockquote {{ background: var(--oe-surface-alt); border-left: 3px solid var(--oe-teal); margin: 1em 0; padding: .4em .8em; }}
"""


def outputs(t: dict) -> dict[str, str]:
    flat = {"version": t["version"], "color": flat_colors(t),
            "font": {k: v["family"] for k, v in t["font"].items()}, "type": t["type"], "page": t["page"],
            "label": t["label"]}
    return {"brand.css": brand_css(t), "book.css": book_css(t), "epub.css": epub_css(t),
            "tokens.json": json.dumps(flat, indent=2) + "\n"}


def main() -> int:
    t = load()
    out = outputs(t)
    if "--check" in sys.argv:
        bad = [n for n, txt in out.items() if not (DIST / n).exists() or (DIST / n).read_text(encoding="utf-8") != txt]
        if bad:
            print("out of date:", ", ".join(bad), "- run kit/design/build_tokens.py")
            return 1
        print("design files are current")
        return 0
    DIST.mkdir(exist_ok=True)
    for n, txt in out.items():
        (DIST / n).write_text(txt, encoding="utf-8", newline="\n")
    print("wrote", ", ".join(out), "to", DIST)
    return 0


if __name__ == "__main__":
    sys.exit(main())

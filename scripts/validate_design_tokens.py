#!/usr/bin/env python3
"""Guard the additive-only compatibility contract on design-system/tokens.css.

conceptbase/app links tokens.css live from GitHub Pages with no version pin
(see design-system/README.md's "Versioning and the compatibility contract").
That means a rename or re-value of any token that existed before the
2026-09-15 expansion ships to that production app the moment it lands on
main, with zero chance to coordinate a migration first. This script is the
automated backstop the README promises but nothing previously enforced.

It freezes the exact name/value of every property that existed in each of
the three theme blocks (:root, the prefers-color-scheme dark media block,
and :root[data-theme="dark"]) as of 2026-09-15, and fails if any of them is
missing or has changed value in the current file. New properties, and new
blocks, are unaffected -- this only pins the pre-existing ones.

Exit code 0 on success, 1 if any pinned token is missing/changed. Intended
to run as a required PR status check against `main`.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKENS_PATH = ROOT / "design-system" / "tokens.css"

# Frozen 2026-09-15 baseline. Do not edit these values -- add new tokens to
# tokens.css instead. If a value below is ever intentionally changed, that is
# itself the signal this script exists to catch; treat it as a breaking
# change requiring a coordinated migration, not a quiet fix here.
BASELINE = {
    ":root": {
        "surface-1": "#fcfcfb",
        "surface-2": "#ffffff",
        "page-plane": "#f9f9f7",
        "text-primary": "#0b0b0b",
        "text-secondary": "#52514e",
        "text-muted": "#898781",
        "gridline": "#e1e0d9",
        "baseline": "#c3c2b7",
        "border": "rgba(11, 11, 11, 0.10)",
        "border-strong": "rgba(11, 11, 11, 0.18)",
        "series-a": "#2a78d6",
        "series-b": "#008300",
        "good": "#0ca30c",
        "warning": "#fab219",
        "serious": "#ec835a",
        "critical": "#d03b3b",
        "radius": "8px",
        "radius-sm": "5px",
        "font": 'system-ui, -apple-system, "Segoe UI", sans-serif',
    },
    ':root:where(:not([data-theme="light"]))': {
        "surface-1": "#1a1a19",
        "surface-2": "#212120",
        "page-plane": "#0d0d0d",
        "text-primary": "#ffffff",
        "text-secondary": "#c3c2b7",
        "text-muted": "#898781",
        "gridline": "#2c2c2a",
        "baseline": "#383835",
        "border": "rgba(255, 255, 255, 0.10)",
        "border-strong": "rgba(255, 255, 255, 0.18)",
        "series-a": "#3987e5",
        "series-b": "#008300",
    },
    ':root[data-theme="dark"]': {
        "surface-1": "#1a1a19",
        "surface-2": "#212120",
        "page-plane": "#0d0d0d",
        "text-primary": "#ffffff",
        "text-secondary": "#c3c2b7",
        "text-muted": "#898781",
        "gridline": "#2c2c2a",
        "baseline": "#383835",
        "border": "rgba(255, 255, 255, 0.10)",
        "border-strong": "rgba(255, 255, 255, 0.18)",
        "series-a": "#3987e5",
        "series-b": "#008300",
    },
}

DECL_RE = re.compile(r"--([\w-]+)\s*:\s*([^;]+);")


def parse_blocks(css_text: str) -> dict[str, dict[str, str]]:
    """Split CSS into {selector: {var: value}}, by brace depth (no nesting-aware
    selector composition needed -- this file never nests a var declaration two
    levels deep, so each block's own content is exactly its own declarations)."""
    blocks: dict[str, dict[str, str]] = {}
    stack: list[str] = []
    buf: list[str] = []
    for ch in css_text:
        if ch == "{":
            last_line = "".join(buf).rstrip().rsplit("\n", 1)[-1].strip()
            stack.append(last_line)
            buf = []
        elif ch == "}":
            selector = stack.pop() if stack else ""
            content = "".join(buf)
            decls = dict(DECL_RE.findall(content))
            decls = {k: v.strip() for k, v in decls.items()}
            if decls:
                blocks.setdefault(selector, {}).update(decls)
            buf = []
        else:
            buf.append(ch)
    return blocks


def main() -> int:
    if not TOKENS_PATH.exists():
        print(f"No tokens file found at {TOKENS_PATH}")
        return 1

    css_text = TOKENS_PATH.read_text(encoding="utf-8")
    current = parse_blocks(css_text)

    errors: list[str] = []
    checked = 0

    for selector, pinned in BASELINE.items():
        current_block = current.get(selector)
        if current_block is None:
            errors.append(f"block '{selector}' is missing entirely from tokens.css")
            continue
        for name, pinned_value in pinned.items():
            checked += 1
            if name not in current_block:
                errors.append(f"{selector} {{ --{name} }}: removed (was '{pinned_value}')")
            elif current_block[name] != pinned_value:
                errors.append(
                    f"{selector} {{ --{name} }}: value changed "
                    f"('{pinned_value}' -> '{current_block[name]}')"
                )

    if errors:
        print(f"FAILED: {len(errors)} of {checked} pinned pre-2026-09-15 token(s) violated\n")
        for e in errors:
            print(f"  - {e}")
        print(
            "\nThese tokens are relied on live (no version pin) by conceptbase/app. "
            "If this change is intentional, it is a breaking change to an external "
            "consumer, not a fix -- see design-system/README.md's compatibility "
            "contract before proceeding."
        )
        return 1

    print(f"OK: {checked} pinned pre-2026-09-15 token(s) across {len(BASELINE)} block(s) unchanged")
    return 0


if __name__ == "__main__":
    sys.exit(main())

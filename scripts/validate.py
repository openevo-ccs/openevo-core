#!/usr/bin/env python3
"""Structurally validate ontologies/core_v1.yaml.

This repo stores no entity instances (see README), so there is no
records/*.yaml corpus to schema-validate the way the Foundational Repos
that consume this ontology do. What can break here is the shared upper
ontology itself: a class or property missing a required field, or a
domain/range pointing at an oe: class that was never declared.

Checks:
  1. Required fields present on every entry in `classes`, `entityProperties`,
     `properties`, and `reserved`
  2. `status` values come from the lifecycle vocabulary documented on
     oe:status in entityProperties (see GOVERNANCE.md)
  3. Every oe:-prefixed domain/range/subClassOf/inverseOf reference resolves
     to a class or property actually declared somewhere in this file (or to
     `reserved`, which is allowed to be forward-referenced pre-RFC)

Exit code 0 on success, 1 if any check fails. Intended to run as a required
PR status check against `main` -- see .github/workflows/validate.yml.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ONTOLOGY_PATH = ROOT / "ontologies" / "core_v1.yaml"

STATUS_VALUES = {"proposed", "accepted", "stable", "deprecated", "superseded", "retracted"}


def _oe_refs(value):
    """Every oe:-prefixed string found in a scalar, list, or single value."""
    if isinstance(value, str):
        return [value] if value.startswith("oe:") else []
    if isinstance(value, list):
        return [v for v in value if isinstance(v, str) and v.startswith("oe:")]
    return []


def main() -> int:
    if not ONTOLOGY_PATH.exists():
        print(f"No ontology file found at {ONTOLOGY_PATH}")
        return 1

    with ONTOLOGY_PATH.open(encoding="utf-8") as f:
        doc = yaml.safe_load(f)

    classes = doc.get("classes", {}) or {}
    entity_props = doc.get("entityProperties", {}) or {}
    properties = doc.get("properties", {}) or {}
    reserved = doc.get("reserved", []) or []

    known_names = set(classes) | set(entity_props) | set(properties)
    known_names |= {r["iri"] for r in reserved if isinstance(r, dict) and "iri" in r}

    errors: list[str] = []

    for name, entry in classes.items():
        entry = entry or {}
        for field in ("label", "status", "definition"):
            if field not in entry:
                errors.append(f"classes.{name}: missing required field '{field}'")
        if entry.get("status") not in STATUS_VALUES:
            errors.append(f"classes.{name}: status '{entry.get('status')}' not in {sorted(STATUS_VALUES)}")
        for ref in _oe_refs(entry.get("subClassOf")):
            if ref not in known_names:
                errors.append(f"classes.{name}: subClassOf '{ref}' does not resolve to any declared class")

    for group_name, group in (("entityProperties", entity_props), ("properties", properties)):
        for name, entry in group.items():
            entry = entry or {}
            for field in ("label", "domain", "range", "status", "definition"):
                if field not in entry:
                    errors.append(f"{group_name}.{name}: missing required field '{field}'")
            if entry.get("status") not in STATUS_VALUES:
                errors.append(f"{group_name}.{name}: status '{entry.get('status')}' not in {sorted(STATUS_VALUES)}")
            for field in ("domain", "range", "inverseOf"):
                for ref in _oe_refs(entry.get(field)):
                    if ref not in known_names:
                        errors.append(f"{group_name}.{name}: {field} '{ref}' does not resolve to any declared class/property")

    for i, entry in enumerate(reserved):
        entry = entry or {}
        for field in ("iri", "plannedPhase"):
            if field not in entry:
                errors.append(f"reserved[{i}]: missing required field '{field}'")

    if errors:
        print(f"FAILED: {len(errors)} issue(s)\n")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(
        f"OK: {len(classes)} class(es), {len(entity_props)} entity property(ies), "
        f"{len(properties)} object property(ies), {len(reserved)} reserved IRI(s), 0 issues"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

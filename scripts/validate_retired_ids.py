#!/usr/bin/env python3
"""Structurally validate registry/retired-ids.yaml.

The table lists ids that were renamed or moved, and where each one went. This script checks the shape of the table and
that its entries agree with each other. It does not check the sources an entry names; a person does that.

Checks:
  1. Every entry has id, status, retired_on (an ISO date), reason and verified_against
  2. Every id looks like an OpenEvo id, and no id appears twice
  3. status is one of aliased, moved, retired; `aliased` has a successor, `retired` has none
  4. A successor looks like an OpenEvo id, is not the old id, and does not point back at an alias chain loop
  5. verification is named-in-source or derived-from-source on entries that name a pair
  6. Each rule has an id, a match of exact or prefix, a status, and for `moved` a now_lives_in

Exit code 0 on success, 1 if any check fails. Runs as a required PR status check, see .github/workflows/validate.yml.
"""
from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TABLE_PATH = ROOT / "registry" / "retired-ids.yaml"

ID_SHAPE = re.compile(r"^OE-[A-Z][A-Z0-9]*-[A-Za-z0-9][A-Za-z0-9_.-]*$")
PREFIX_SHAPE = re.compile(r"^OE-[A-Z][A-Z0-9]*-[A-Za-z0-9][A-Za-z0-9_.-]*-$")
STATUSES = {"aliased", "moved", "retired"}
VERIFICATIONS = {"named-in-source", "derived-from-source"}
MATCHES = {"exact", "prefix"}


def is_date(text) -> bool:
    try:
        date.fromisoformat(str(text))
    except ValueError:
        return False
    return True


def check_entries(entries) -> list[str]:
    errors: list[str] = []
    seen: dict[str, int] = {}
    successors: dict[str, str] = {}
    for position, entry in enumerate(entries, start=1):
        label = f"entry {position}"
        if not isinstance(entry, dict):
            errors.append(f"{label}: not a mapping")
            continue
        identifier = entry.get("id", "")
        label = f"entry {position} ({identifier})"
        for field in ("id", "status", "retired_on", "reason", "verified_against"):
            if not entry.get(field):
                errors.append(f"{label}: missing {field}")
        if identifier and not ID_SHAPE.match(identifier):
            errors.append(f"{label}: id does not look like an OpenEvo id")
        if identifier in seen:
            errors.append(f"{label}: id already listed in entry {seen[identifier]}")
        seen[identifier] = position
        status = entry.get("status")
        if status and status not in STATUSES:
            errors.append(f"{label}: status {status!r} is not one of {sorted(STATUSES)}")
        if entry.get("retired_on") and not is_date(entry["retired_on"]):
            errors.append(f"{label}: retired_on is not an ISO date")
        successor = entry.get("successor")
        if status == "aliased":
            if not successor:
                errors.append(f"{label}: aliased needs a successor")
            elif not ID_SHAPE.match(successor):
                errors.append(f"{label}: successor does not look like an OpenEvo id")
            elif successor == identifier:
                errors.append(f"{label}: successor is the id itself")
            else:
                successors[identifier] = successor
        elif successor:
            errors.append(f"{label}: only an aliased entry has a successor")
        if status == "moved" and not entry.get("now_lives_in"):
            errors.append(f"{label}: moved needs now_lives_in")
        if entry.get("verification") and entry["verification"] not in VERIFICATIONS:
            errors.append(f"{label}: verification {entry['verification']!r} is not one of {sorted(VERIFICATIONS)}")
        if status == "aliased" and entry.get("verification") is None:
            errors.append(f"{label}: aliased needs verification")
    for start in successors:
        walked, here = {start}, successors[start]
        while here in successors:
            if here in walked:
                errors.append(f"{start}: alias chain loops back to {here}")
                break
            walked.add(here)
            here = successors[here]
    return errors


def check_rules(rules) -> list[str]:
    errors: list[str] = []
    for position, rule in enumerate(rules, start=1):
        label = f"rule {position} ({rule.get('id', '') if isinstance(rule, dict) else ''})"
        if not isinstance(rule, dict):
            errors.append(f"{label}: not a mapping")
            continue
        for field in ("id", "match", "status", "reason", "verified_against"):
            if not rule.get(field):
                errors.append(f"{label}: missing {field}")
        if rule.get("match") and rule["match"] not in MATCHES:
            errors.append(f"{label}: match {rule['match']!r} is not one of {sorted(MATCHES)}")
        if rule.get("match") == "prefix" and rule.get("id") and not PREFIX_SHAPE.match(rule["id"]):
            errors.append(f"{label}: a prefix rule must end with '-'")
        if rule.get("match") == "exact" and rule.get("id") and not ID_SHAPE.match(rule["id"]):
            errors.append(f"{label}: id does not look like an OpenEvo id")
        if rule.get("status") not in STATUSES:
            errors.append(f"{label}: status {rule.get('status')!r} is not one of {sorted(STATUSES)}")
        if rule.get("status") == "moved" and not rule.get("now_lives_in"):
            errors.append(f"{label}: moved needs now_lives_in")
    return errors


def main() -> int:
    if not TABLE_PATH.exists():
        print(f"No table found at {TABLE_PATH}")
        return 1
    with TABLE_PATH.open(encoding="utf-8") as handle:
        document = yaml.safe_load(handle) or {}
    entries = document.get("entries") or []
    rules = document.get("rules") or []
    errors = check_entries(entries) + check_rules(rules)
    if errors:
        print(f"{len(errors)} problem(s) in {TABLE_PATH.name}:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"{TABLE_PATH.name}: {len(entries)} entries and {len(rules)} rules are well formed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

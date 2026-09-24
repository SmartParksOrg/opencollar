#!/usr/bin/env python3
"""Validate the YAML data files against their JSON schemas and check cross-references.

Usage: python scripts/validate_data.py
Exit code 1 on any problem. Run by the build workflow before mkdocs build.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SCHEMAS = ROOT / "scripts" / "schemas"


def load(name: str) -> dict:
    with open(DATA / f"{name}.yml", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def validate_schema(name: str, doc: dict, errors: list[str]) -> None:
    with open(SCHEMAS / f"{name}.schema.json", encoding="utf-8") as fh:
        schema = json.load(fh)
    validator = jsonschema.Draft202012Validator(schema)
    for err in sorted(validator.iter_errors(doc), key=lambda e: list(e.path)):
        path = "/".join(str(p) for p in err.path) or "(root)"
        errors.append(f"{name}.yml: {path}: {err.message}")


def main() -> int:
    errors: list[str] = []
    repos_doc, devices_doc, tools_doc = load("repositories"), load("devices"), load("tools")
    validate_schema("repositories", repos_doc, errors)
    validate_schema("devices", devices_doc, errors)
    validate_schema("tools", tools_doc, errors)
    if errors:
        print("\n".join(errors))
        return 1

    repos = {r["name"]: r for r in repos_doc["repositories"]}
    devices = {d["id"]: d for d in devices_doc["devices"]}
    tools = {t["id"]: t for t in tools_doc["tools"]}

    def check_unique(items, key, label):
        seen = set()
        for item in items:
            if item[key] in seen:
                errors.append(f"{label}: duplicate {key} {item[key]!r}")
            seen.add(item[key])

    check_unique(repos_doc["repositories"], "name", "repositories.yml")
    check_unique(devices_doc["devices"], "id", "devices.yml")
    check_unique(tools_doc["tools"], "id", "tools.yml")

    for r in repos.values():
        for d in r["devices"]:
            if d not in devices:
                errors.append(f"repositories.yml: {r['name']}: unknown device {d!r}")
        for rel in r["related"]:
            if rel not in repos:
                errors.append(f"repositories.yml: {r['name']}: unknown related repository {rel!r}")

    for d in devices.values():
        rp = d["repositories"]
        for name in [rp["docs"], *rp["hardware"], *rp["mechanics"]]:
            if name is not None and name not in repos:
                errors.append(f"devices.yml: {d['id']}: unknown repository {name!r}")
        for name in [*d["tools"].get("configure", []), *d["tools"].get("decode", [])]:
            if name not in tools:
                errors.append(f"devices.yml: {d['id']}: unknown tool {name!r}")
        if d["based_on"] is not None and d["based_on"] not in devices:
            errors.append(f"devices.yml: {d['id']}: unknown based_on {d['based_on']!r}")

    for t in tools.values():
        if t["repo"] is not None and t["repo"] not in repos:
            errors.append(f"tools.yml: {t['id']}: unknown repository {t['repo']!r}")

    if errors:
        print("\n".join(errors))
        return 1
    print(f"OK: {len(repos)} repositories, {len(devices)} devices, {len(tools)} tools")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Fetch the latest release and tag of every tracked repository into data/generated/releases.json.

Usage: GITHUB_TOKEN=... python scripts/sync_releases.py
Only repositories with releases.track: true in data/repositories.yml are queried. The output is
deterministic (sorted keys) so that the sync workflow only commits when something changed.
A token is optional for public repositories but avoids rate limits; in GitHub Actions the
built-in GITHUB_TOKEN is enough. Private repositories are skipped unless the token can read them.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "generated" / "releases.json"
API = "https://api.github.com"
ORG = "SmartParksOrg"


def api_get(path: str, token: str | None):
    req = urllib.request.Request(f"{API}{path}", headers={
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "opencollar-hub-sync",
        **({"Authorization": f"Bearer {token}"} if token else {}),
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp), resp.status
    except urllib.error.HTTPError as err:
        if err.code == 404:
            return None, 404
        raise


def fetch_repo(name: str, token: str | None) -> dict | None:
    meta, status = api_get(f"/repos/{ORG}/{name}", token)
    if meta is None:
        print(f"  {name}: not accessible (404), skipped", file=sys.stderr)
        return None
    release, _ = api_get(f"/repos/{ORG}/{name}/releases/latest", token)
    tags, _ = api_get(f"/repos/{ORG}/{name}/tags?per_page=1", token)
    entry = {
        "pushed_at": meta.get("pushed_at"),
        "default_branch": meta.get("default_branch"),
        "archived": meta.get("archived", False),
        "open_issues": meta.get("open_issues_count", 0),
        "latest_tag": tags[0]["name"] if tags else None,
        "latest_release": None,
    }
    if release:
        entry["latest_release"] = {
            "tag": release["tag_name"],
            "name": release.get("name") or release["tag_name"],
            "published_at": release.get("published_at"),
            "url": release["html_url"],
            "prerelease": release.get("prerelease", False),
            "assets": [
                {"name": a["name"], "url": a["browser_download_url"], "size": a["size"]}
                for a in release.get("assets", [])
            ],
        }
    return entry


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    with open(ROOT / "data" / "repositories.yml", encoding="utf-8") as fh:
        repos = yaml.safe_load(fh)["repositories"]
    tracked = [r["name"] for r in repos if r["releases"].get("track")]
    previous = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {"repositories": {}}
    result = {"generated_at": None, "repositories": {}}
    for name in tracked:
        print(f"fetching {name}", file=sys.stderr)
        entry = fetch_repo(name, token)
        if entry is not None:
            result["repositories"][name] = entry
    # Keep the previous timestamp when nothing but the timestamp would change.
    if result["repositories"] == previous.get("repositories"):
        print("no changes", file=sys.stderr)
        return 0
    result["generated_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(result['repositories'])} repositories)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

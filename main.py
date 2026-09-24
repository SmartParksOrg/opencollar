"""mkdocs-macros entry point: exposes the YAML data files as variables and rendering macros.

All content comes from data/*.yml and data/generated/releases.json. Pages call the macros
below (for example {{ device_page('rangeredge') }}) so that device specifications, repository
tables and release information are written once and rendered everywhere.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
ORG_URL = "https://github.com/SmartParksOrg"

STATUS_LABEL = {
    "current": "current", "maintained": "maintained", "legacy": "legacy", "experimental": "experimental",
    "archived": "archived", "private": "private source",
}


def _load_yaml(name: str) -> dict:
    with open(DATA / f"{name}.yml", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _load_releases() -> dict:
    path = DATA / "generated" / "releases.json"
    if not path.exists():
        return {"generated_at": None, "repositories": {}}
    return json.loads(path.read_text(encoding="utf-8"))



def _version_key(tag: str) -> tuple:
    """Sort key for tags like v1.43, V1.13.1, 0.5: numeric parts, then the raw string."""
    nums = tuple(int(n) for n in re.findall(r"\d+", tag or ""))
    return (nums, tag or "")


def _badge(text: str, kind: str) -> str:
    return f'<span class="oc-badge oc-badge--{kind}">{text}</span>'


def _md_escape(text: str) -> str:
    return str(text).replace("|", "\\|")


def _join(items, sep=", ") -> str:
    return sep.join(str(i) for i in items) if items else "—"


def define_env(env):
    repos_doc = _load_yaml("repositories")
    devices_doc = _load_yaml("devices")
    tools_doc = _load_yaml("tools")
    releases = _load_releases()

    repos = {r["name"]: r for r in repos_doc["repositories"]}
    devices = {d["id"]: d for d in devices_doc["devices"]}
    tools = {t["id"]: t for t in tools_doc["tools"]}

    env.variables["repositories"] = repos_doc["repositories"]
    env.variables["devices"] = devices_doc["devices"]
    env.variables["tools"] = tools_doc["tools"]
    env.variables["releases"] = releases
    env.variables["releases_generated_at"] = (releases.get("generated_at") or "never")[:10]

    # ---- helpers -------------------------------------------------------------------------
    def repo_url(name: str) -> str:
        return repos[name]["links"]["repo"] if name in repos else f"{ORG_URL}/{name}"

    def repo_link(name: str, label: str | None = None) -> str:
        if name not in repos:
            return f"[{label or name}]({ORG_URL}/{name})"
        r = repos[name]
        return f"[{label or r['display_name']}]({r['links']['repo']})"

    def release_of(name: str) -> dict | None:
        return releases.get("repositories", {}).get(name)

    def latest_release(name: str, with_date: bool = True) -> str:
        entry = release_of(name)
        if not entry:
            return "—"
        rel = entry.get("latest_release")
        tag = entry.get("latest_tag")
        if rel:
            text = f"[{rel['tag']}]({rel['url']})"
            if with_date and rel.get("published_at"):
                text += f" ({rel['published_at'][:10]})"
            # Some repositories tag more often than they publish releases; show a newer tag too.
            if tag and tag != rel["tag"] and _version_key(tag) > _version_key(rel["tag"]):
                text += f", tag {tag}"
            return text
        if tag:
            return f"tag {tag}"
        return "—"

    def device_link(dev_id: str, prefix: str = "") -> str:
        d = devices[dev_id]
        return f"[{d['display_name']}]({prefix}{dev_id}.md)"

    def tool_link(tool_id: str) -> str:
        t = tools[tool_id]
        return f"[{t['display_name']}]({t['url']})"

    env.macro(repo_link)
    env.macro(latest_release)
    env.macro(device_link)
    env.macro(tool_link)

    # ---- repositories ----------------------------------------------------------------------
    @env.macro
    def repo_table(category=None, status=None, device=None, audience=None, columns=("purpose", "status", "license", "latest")):
        rows = []
        for r in repos_doc["repositories"]:
            if category and r["category"] not in (category if isinstance(category, (list, tuple)) else [category]):
                continue
            if status and r["status"] not in (status if isinstance(status, (list, tuple)) else [status]):
                continue
            if device and device not in r["devices"]:
                continue
            if audience and audience not in r["audience"]:
                continue
            rows.append(r)
        if not rows:
            return "_No repositories match._"
        head = ["Repository"] + [c.capitalize() for c in columns]
        out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
        for r in rows:
            cells = [f"[`{r['name']}`]({r['links']['repo']})"]
            for c in columns:
                if c == "purpose":
                    cells.append(_md_escape(r["display_name"]))
                elif c == "status":
                    cells.append(_badge(STATUS_LABEL.get(r["status"], r["status"]), r["status"]))
                elif c == "license":
                    cells.append(_md_escape(r["license"]))
                elif c == "latest":
                    cells.append(latest_release(r["name"]))
                elif c == "devices":
                    cells.append(_join(devices[d]["display_name"] for d in r["devices"] if d in devices))
                elif c == "app":
                    cells.append(f"[open]({r['links']['app']})" if r["links"].get("app") else "—")
                elif c == "description":
                    cells.append(_md_escape(r["description"] or r["notes"]))
            out.append("| " + " | ".join(cells) + " |")
        return "\n".join(out)

    @env.macro
    def repo_count(category=None):
        return sum(1 for r in repos_doc["repositories"] if not category or r["category"] == category)

    # ---- devices --------------------------------------------------------------------------
    @env.macro
    def device_matrix(family=None, status=None, prefix=""):
        rows = [d for d in devices_doc["devices"]
                if (not family or d["family"] == family) and (not status or d["status"] == status)]
        if not rows:
            return "_No devices match._"
        out = ["| Device | Status | Board | Positioning | Connectivity | Power | Confidence |", "|---|---|---|---|---|---|---|"]
        for d in rows:
            fw = d["firmware"]
            board = f"`{fw['board']}`" if fw.get("board") else "—"
            power = d["power"].get("batteries") or d["power"].get("type") or "—"
            out.append("| " + " | ".join([
                device_link(d["id"], prefix),
                _badge(d["status"], d["status"]),
                board,
                _md_escape(_join(d["positioning"])),
                _md_escape(_join(d["connectivity"])),
                _md_escape(power),
                _badge(d["confidence"], d["confidence"]) if d["confidence"] != "high" else "high",
            ]) + " |")
        return "\n".join(out)

    @env.macro
    def device_page(dev_id: str):
        d = devices[dev_id]
        fw, pw, ph, rp = d["firmware"], d["power"], d["physical"], d["repositories"]
        parts = []
        parts.append(f"{_badge(d['status'], d['status'])} {_badge('availability: ' + d['availability'], 'availability')}"
                     + (f" {_badge('verification: ' + d['confidence'], d['confidence'])}" if d["confidence"] != "high" else ""))
        parts.append("")
        if d.get("image"):
            parts.append(f'<img class="oc-device-image" src="{d["image"]}" alt="{d["display_name"]}">')
            parts.append("")
        parts.append(d["summary"])
        parts.append("")
        if d.get("use_cases"):
            parts.append(f"**Typical use:** {_join(d['use_cases'])}.")
            parts.append("")
        if d.get("variants"):
            parts.append("**Variants:** " + _join(d["variants"], "; ") + ".")
            parts.append("")
        if d["confidence"] == "low":
            parts.append('!!! warning "Partly unverified"')
            parts.append(f"    {d['notes']}")
            parts.append("")
        parts.append("## Specifications")
        parts.append("")
        dims = " x ".join(str(v) for v in ph["dimensions_mm"]) + " mm" if ph.get("dimensions_mm") else "—"
        spec = [
            ("Positioning", _join(d["positioning"])),
            ("Connectivity", _join(d["connectivity"])),
            ("Sensors", _join(d["sensors"])),
            ("Power", " / ".join(str(x) for x in [pw.get("type"), pw.get("batteries"),
                                                 f"{pw['capacity_ah']} Ah" if pw.get("capacity_ah") else None] if x)
                      + (f"; charging: {_join(pw['charging'])}" if pw.get("charging") else "") or "—"),
            ("Dimensions", dims),
            ("Weight", f"{ph['weight_g']} g" if ph.get("weight_g") else "—"),
            ("Enclosure", ph.get("enclosure") or "—"),
        ]
        parts.append("| | |\n|---|---|")
        for k, v in spec:
            parts.append(f"| **{k}** | {_md_escape(v)} |")
        parts.append("")
        parts.append("## Firmware")
        parts.append("")
        if fw.get("board"):
            fwrows = [
                ("Firmware board", f"`{fw['board']}`"),
                ("Tracker type", f"`{fw['tracker_type']}`" + (f" (value {fw['tracker_type_value']})" if fw.get("tracker_type_value") is not None else "")),
                ("Hardware revisions supported", _join(fw["hardware_revisions"])),
            ]
            if fw.get("special_builds"):
                fwrows.append(("Special builds", _join(f"`{b}`" for b in fw["special_builds"])))
            fwrows.append(("Latest firmware", latest_release("smartparks-opencollar-edge-fw-public")))
            parts.append("| | |\n|---|---|")
            for k, v in fwrows:
                parts.append(f"| **{k}** | {v} |")
            parts.append("")
            parts.append("Runs the shared [OpenCollar Edge firmware](../firmware/index.md); see [supported hardware](../firmware/supported-hardware.md) for revision groups and the [releases](../firmware/releases.md) page for downloads.")
        else:
            parts.append("This device does not run the OpenCollar Edge firmware.")
        parts.append("")
        if d.get("based_on"):
            parts.append(f"Based on {device_link(d['based_on'])}.")
            parts.append("")
        parts.append("## Repositories")
        parts.append("")
        lines = []
        if rp.get("docs"):
            lines.append(f"- **Documentation, BOM and assembly:** {repo_link(rp['docs'])}")
        for h in rp.get("hardware", []):
            lines.append(f"- **Electronics:** {repo_link(h)} (latest: {latest_release(h)})")
        for m in rp.get("mechanics", []):
            lines.append(f"- **Mechanics:** {repo_link(m)} (latest: {latest_release(m)})")
        parts.append("\n".join(lines) if lines else "_No dedicated repositories. See the notes below._")
        parts.append("")
        parts.append("## Tools")
        parts.append("")
        tl = []
        if d["tools"].get("configure"):
            tl.append("- **Configure and update:** " + _join(tool_link(t) for t in d["tools"]["configure"]))
        if d["tools"].get("decode"):
            tl.append("- **Decode data:** " + _join(tool_link(t) for t in d["tools"]["decode"]))
        parts.append("\n".join(tl) if tl else "—")
        parts.append("")
        ext = d.get("external_links", {})
        links = [("Smart Parks Wiki", ext.get("wiki")), ("Datasheet", ext.get("datasheet")), ("Smart Parks catalog", ext.get("catalog"))]
        links = [(k, v) for k, v in links if v]
        if links:
            parts.append("## External links")
            parts.append("")
            parts.extend(f"- [{k}]({v})" for k, v in links)
            parts.append("")
        if d.get("notes") and d["confidence"] != "low":
            parts.append('!!! note')
            parts.append(f"    {d['notes']}")
            parts.append("")
        return "\n".join(parts)

    @env.macro
    def device_cards(family: str, prefix: str = ""):
        rows = [d for d in devices_doc["devices"] if d["family"] == family]
        out = ['<div class="grid cards" markdown>', ""]
        for d in rows:
            out.append(f"-   **{d['display_name']}** {_badge(d['status'], d['status'])}")
            out.append("")
            out.append(f"    ---")
            out.append("")
            out.append(f"    {d['summary']}")
            out.append("")
            out.append(f"    [:octicons-arrow-right-24: Details]({prefix}{d['id']}.md)")
            out.append("")
        out.append("</div>")
        return "\n".join(out)

    # ---- tools ----------------------------------------------------------------------------
    @env.macro
    def tool_cards(task=None, status=None):
        rows = [t for t in tools_doc["tools"]
                if (not task or task in t["tasks"]) and (not status or t["status"] in (status if isinstance(status, (list, tuple)) else [status]))]
        if not rows:
            return "_No tools match._"
        out = ['<div class="grid cards" markdown>', ""]
        for t in rows:
            out.append(f"-   **{t['display_name']}** {_badge(t['status'], t['status'])}")
            out.append("")
            out.append("    ---")
            out.append("")
            out.append(f"    {t['description']}")
            out.append("")
            out.append(f"    Platform: {t['platform']}. Firmware: {t.get('supported_firmware', '—')}.")
            out.append("")
            out.append(f"    [:octicons-arrow-right-24: Open]({t['url']})" + (f" · [source]({repo_url(t['repo'])})" if t.get("repo") else ""))
            out.append("")
        out.append("</div>")
        return "\n".join(out)

    # ---- releases -------------------------------------------------------------------------
    @env.macro
    def release_assets(name: str, pattern_prefix: str | None = None):
        entry = release_of(name)
        if not entry or not entry.get("latest_release"):
            return "_No release information synchronised yet._"
        rel = entry["latest_release"]
        out = [f"**{rel['name']}** published {rel.get('published_at', '')[:10]} — [release page]({rel['url']})", ""]
        assets = [a for a in rel["assets"] if not pattern_prefix or a["name"].startswith(pattern_prefix)]
        if assets:
            out.append("| Asset | Size |\n|---|---|")
            for a in assets:
                size = f"{a['size'] / 1_000_000:.1f} MB" if a["size"] > 1_000_000 else f"{a['size'] / 1000:.0f} kB"
                out.append(f"| [{a['name']}]({a['url']}) | {size} |")
        return "\n".join(out)

    @env.macro
    def releases_table(category=None):
        rows = [r for r in repos_doc["repositories"] if r["releases"].get("track") and (not category or r["category"] == category)]
        out = ["| Repository | Category | Latest release | Latest tag | Last push |", "|---|---|---|---|---|"]
        for r in rows:
            e = release_of(r["name"]) or {}
            out.append("| " + " | ".join([
                f"[`{r['name']}`]({r['links']['repo']})", r["category"], latest_release(r["name"]),
                e.get("latest_tag") or "—", (e.get("pushed_at") or "—")[:10],
            ]) + " |")
        return "\n".join(out)

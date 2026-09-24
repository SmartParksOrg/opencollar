# OpenCollar

**Open-source wildlife tracking technology by [Smart Parks](https://www.smartparks.org/opencollar-io/).**

This repository is the central entry point for the OpenCollar ecosystem and the source of the documentation site at **https://smartparksorg.github.io/opencollar/**. It links the firmware, hardware, mechanics, tools and protocol documentation that live in their own repositories in the [SmartParksOrg](https://github.com/SmartParksOrg) organization; it does not contain them.

## What is here

| Path | Content |
|---|---|
| `docs/` | The site pages (Markdown, MkDocs Material) |
| `data/devices.yml` | Device inventory: boards, tracker types, specifications, repositories, links |
| `data/repositories.yml` | Repository index: purpose, category, status, licence, links |
| `data/tools.yml` | User and developer tools |
| `data/generated/releases.json` | Latest releases and tags, refreshed weekly by a workflow (do not edit) |
| `scripts/` | Data validation and release synchronisation |
| `main.py` | MkDocs macros that render the data files into pages |
| `DISCOVERY-REPORT.md` | The September 2026 discovery report and implementation plan |

## Working on the site

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python scripts/validate_data.py
mkdocs serve
```

Refresh release metadata locally with `GH_TOKEN=$(gh auth token) python scripts/sync_releases.py`. Every push to `main` validates the data, builds the site with `mkdocs build --strict` and deploys it to GitHub Pages.

## Licence

Documentation is licensed under CC BY-SA 4.0 and the scripts and workflows under MIT; see [LICENSE](LICENSE). Smart Parks, OpenCollar, CollarEdge and the other *Edge names are trademarks of Smart Parks.

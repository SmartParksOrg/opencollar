# Contributing

## Reporting problems

- **This site**: open an issue or pull request on [SmartParksOrg/opencollar](https://github.com/SmartParksOrg/opencollar/issues). Device specifications live in `data/devices.yml`, repository descriptions in `data/repositories.yml`, tools in `data/tools.yml`; pages under `docs/` are Markdown.
- **Tools**: each tool repository has its own issue tracker, for example [ble-settings-app](https://github.com/SmartParksOrg/ble-settings-app/issues) and [raw_logs_decoder](https://github.com/SmartParksOrg/raw_logs_decoder/issues).
- **Firmware**: the public repository is a release mirror. Until issues are enabled there, report firmware problems on this repository and mention the firmware version, hardware type and revision shown by the app.
- **Hardware**: issues on the relevant `-hardware`, `-mechanics` or `-master` repository.

## Editing this site

```bash
git clone https://github.com/SmartParksOrg/opencollar
cd opencollar
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python scripts/validate_data.py
mkdocs serve
```

`mkdocs serve` previews the site at http://127.0.0.1:8000 with live reload. The validator checks the YAML data files against their schemas and cross-references. The build workflow runs both on every pull request; `mkdocs build --strict` fails on broken links.

To refresh release information locally: `GH_TOKEN=$(gh auth token) python scripts/sync_releases.py`.

## Style

Write for the reader named at the top of each section: users on device and tool pages, developers on firmware, protocol and repository pages. Use product names (RangerEdge, CollarEdge Free) in prose and repository names only in links and tables. Mark anything unverified.

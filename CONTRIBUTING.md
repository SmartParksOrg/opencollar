# Contributing

Thank you for helping keep the OpenCollar documentation accurate.

- **Commits**: a short imperative first line, a blank line, then why the change is needed. No co-author or generated-by trailers. Install the hook that strips them once per clone: `git config core.hooksPath .githooks`.
- **Branches**: work on `main`; ask before opening a branch.

- **Device or repository facts** (specifications, status, links): edit `data/devices.yml`, `data/repositories.yml` or `data/tools.yml`. Run `python scripts/validate_data.py` before opening a pull request; the schemas are in `scripts/schemas/`.
- **Pages**: edit the Markdown under `docs/`. Device pages are generated from the data files through the macros in `main.py`; add prose below the macro call if a device needs it.
- **Release information** is generated. Do not edit `data/generated/releases.json` by hand; run `scripts/sync_releases.py` or wait for the weekly workflow.
- **Problems with a device, tool or firmware** belong on that repository's issue tracker; see https://smartparksorg.github.io/opencollar/developers/contributing/.

Pull requests are built with `mkdocs build --strict`, so broken links fail the check. Keep unverified statements marked as such.

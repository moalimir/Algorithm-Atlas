# Maintenance guide

## What belongs in Git

| Files | Purpose | Published to Pages? |
| --- | --- | --- |
| Four HTML entry files | Learning map, complexity lesson, two bundled atlases | Yes |
| `assets/`, `complexity-review.svg`, `complexity-review.png` | Figures, review sheet, preview image | Yes |
| `scripts/` | Verification, plotting, site staging, repository packaging | No |
| `notes/` | Original complexity material, coverage record, mathematical assumptions | No |
| `docs/`, contribution templates, dependency file | Maintainer and contributor instructions | No |
| `LICENSE`, `THIRD_PARTY_NOTICES.md`, `licenses/` | Project and third-party licensing | Yes |
| `repository.json` | Project name, description, topic metadata | No |
| `dist/`, virtual environments, caches | Reproducible local outputs | No; ignored by Git |

Commit both the figures' generator and their exported SVG/PNG files. Readers should not need Python packages to view a chart. The original source note is also a fixture for the example-preservation check. Avoid removing it without replacing that contract.

## Tooling

- Site runtime: a modern browser; static hosting only.
- Checks and packaging: Python 3.13 and Node.js 24, both using their standard libraries.
- Plot authoring: Python 3.13 with the pinned packages in `requirements-dev.txt`.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/generate_precision_figures.py
python scripts/check_complexity.py
node scripts/check_complexity.js
```

The requirements pin the direct plotting dependencies, not every transitive package. Update pins deliberately and inspect the regenerated images and model manifest. Do not claim bit-for-bit identical PNG output across platforms.

## Editing sources

`index.html` and `foundations.html` are directly editable HTML with embedded CSS, JavaScript, and fonts. The complexity models and their static fallback renderings must agree. The SVG summary is the selectable-text master; render its PNG from that master and retain its dimensions.

`data-structures/index.html` and `algorithms/index.html` arrived as self-contained bundles. They are currently the canonical delivered lesson files. This repository has no original React components, original package lock, or original bundler configuration. Installing React or Vite here would not recreate those missing sources. Do not run a formatter over the compiled bundle.

For substantial future lab work, first recover the original project sources and exact dependencies, add their reproducible build, and compare the rebuilt lab routes and behavior with these bundles. Until then, keep bundle edits narrow, record the affected routes, and test them in the browser. New standalone lessons can be authored as readable HTML and linked from the map; update site staging, packaging, and link checks when adding a page.

## Checks and their scope

```sh
python3 scripts/check_complexity.py
node scripts/check_complexity.js
```

The Python check executes 26 examples, compares visible output, preserves 20 supplied function bodies, checks memory/edge cases and local routes, and inverts exported quadratic SVG coordinates. The Node check verifies model values and actual SVG geometry, including axes, bar heights, loop cells, tree edges, and retained characters.

These checks are focused regression evidence, not a full audit of all 82 algorithm labs. Before merging UI work, inspect relevant controls, keyboard behavior, mobile overflow, and navigation in an actual browser.

## GitHub Pages

The public entry point is <https://moalimir.github.io/Algorithm-Atlas/>.

`.github/workflows/pages.yml` runs the checks on pull requests and pushes to `main`. It builds `dist/site/` with `scripts/build_site.py`. Deployment runs only after successful checks on `main`, using the `github-pages` environment and GitHub's Pages artifact actions. PRs validate and stage the site but do not deploy. CI also installs the pinned optional plotting dependencies and regenerates figures in the temporary contributor copy, then checks their mathematical coordinates; approved source exports are left untouched.

The repository's Pages source must be **GitHub Actions**. Deployment uses relative URLs so the `/Algorithm-Atlas/` project prefix is preserved. In the repository's Actions tab, inspect the latest **Check and publish** run to diagnose a failed check or deployment. A merged revert to a known good commit triggers a new deployment.

To inspect exactly what will be published:

```sh
python3 scripts/build_site.py
python3 -m http.server 8000 --directory dist/site
```

Staging uses an explicit file list, so documentation, source fixtures, scripts, and Git internals are not uploaded. Third-party notices remain available to site users.

## Repository archive

```sh
python3 scripts/build_standalone.py
```

This copies the complete contributor package to `dist/algorithm-atlas/`, verifies it, and creates `dist/algorithm-atlas.zip`. It preserves the edited README, docs, workflows, and dependency file. It never rewrites source files or includes `.git`, installed dependencies, or previous build outputs.

## Useful next refinements

- Recover the original atlas component sources and lockfiles before major lab development.
- Extend regression checks to inherited labs as those labs change.
- Add browser automation around specific interactions when a regression justifies it.
- Keep new lessons linked to prerequisites and practice; preserve stable route IDs.

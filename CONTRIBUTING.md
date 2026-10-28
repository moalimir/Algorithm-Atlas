# Contributing

Help students understand why an algorithm works. Small corrections and focused improvements are welcome.

## Get started

1. Fork the repository and create a branch for your change.
2. Install Python 3.13 and Node.js 24 for the checks. Reading the site only needs a browser and a static server.
3. Run `python3 -m http.server 8000` and open <http://localhost:8000>.

There is no npm package installation. Only figure regeneration needs the optional Python dependencies in [requirements-dev.txt](requirements-dev.txt).

## Where to edit

| Change | File |
| --- | --- |
| Learning path, prerequisites, checkpoint problems | `index.html` |
| Complexity explanation, examples, interactions | `foundations.html` |
| Bundled data-structure lessons | `data-structures/index.html` |
| Bundled algorithm, AI, and ML labs | `algorithms/index.html` |
| Static mathematical plots | `scripts/generate_precision_figures.py` |
| Summary poster | `complexity-review.svg` and its matching PNG preview |
| Source coverage and mathematical assumptions | `notes/` |

The two atlases are bundled HTML, including embedded lesson data and compiled JavaScript. Original component sources and their bundler configuration are not in this repository. Avoid broad formatting or minified-code rewrites. Make a focused edit and document the affected lesson. See the [maintenance guide](docs/maintenance.md) for safe refinement and source-recovery priorities.

## Teaching and visual standards

- Explain prerequisites and define symbols before using them.
- Keep runnable examples small and show the expected output.
- Name the input variables, cost model, and case for complexity claims.
- Use computed geometry for quantitative visuals; label units, axes, domains, and scale. Provide a text or table equivalent.
- Give practice problems independent, initially closed worked solutions.
- Preserve existing URLs and anchors, keyboard operation, visible focus, and reduced-motion support.
- Keep source/example coverage notes current when changing the complexity lesson. Correcting an original example also requires a documented reason and updating its preservation check.
- Do not add copied content or assets without permission and attribution. Preserve font and library notices.

## Check your change

```sh
python3 scripts/check_complexity.py
node scripts/check_complexity.js
python3 scripts/build_site.py
```

For UI changes, inspect the affected pages and controls in a browser at desktop and narrow widths. Follow the learning map into each affected atlas and back; test changed anchors, disclosures, and interactions. Include a screenshot when it helps a reviewer.

The automated checks cover the complexity lesson and shared navigation. They do not prove every inherited lab is correct. Add a focused check for new mathematical behavior or a bug when practical; report exactly what you checked.

## Open a pull request

Explain the student-facing problem, the change, and how you checked it. For mathematical corrections, include a derivation, counterexample, or primary reference. Keep unrelated changes in separate PRs. An issue is useful for larger course changes before implementation; small fixes can go directly to a PR.

Be respectful, give constructive feedback, and protect other people's private information. By contributing original work, you agree to publish it under the repository's MIT license. Third-party material retains its own license and must be identified.

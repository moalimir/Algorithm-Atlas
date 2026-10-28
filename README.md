<!-- Generated from scripts/build_standalone.py and repository.json. -->
# Algorithm Atlas

Visual, interactive tutorials for data structures, algorithms, complexity analysis, AI, and machine learning—with Python examples, precise mathematical figures, and guided practice.

![Algorithm Atlas learning map and its core route](assets/algorithm-atlas-preview.png)

## Start exploring

- [Learning map](index.html): the shared route, prerequisites, checkpoints, and optional branches.
- [Complexity analysis](foundations.html): bounds, loop counts, live memory, recurrences, and amortized costs.
- [Data Structures](data-structures/index.html): arrays, linked lists, stacks, queues, hashing, trees, heaps, Union-Find, matrices, graphs, and suffix arrays/BWT. The ADT-to-CPU lesson is a separate foundation note.
- [Algorithms, AI & ML](algorithms/index.html): 82 working labs across 14 subject areas, including sorting, searching, graph algorithms, dynamic programming, strings, planning, probability, learning, and language.

The roadmap connects overlapping topics: learn the structure, then investigate the algorithm that uses it. AI and ML are optional branches with their own mathematical prerequisites.

## Run locally

No application build or JavaScript package installation is needed. From this folder:

```sh
python3 -m http.server 8000
```

Open [http://localhost:8000](http://localhost:8000). Python is used only to serve these static files. The learning map and analysis lesson use embedded fonts and scripts; they do not need a CDN.

## Learn by tracing

1. Predict the next state before stepping through a visual.
2. Change an input and explain which invariant stays true.
3. State the input variables, cost model, and case before naming a complexity.
4. Solve the roadmap checkpoints and complexity problems before expanding the worked solutions.
5. Use the [selectable complexity summary](complexity-review.svg) to connect the ideas after practice.

## Mathematical figures

Figures distinguish function plots, discrete operation counts, and structural diagrams:

- The [bounds plot](assets/figures/asymptotic-bounds.svg) uses `f(N) = 3N² + 5N + 12`, `c₁ = 3`, `c₂ = 5`, and `N₀ = 4`, with an algebraic proof beside it.
- Growth comparisons mark exact integer inputs; zero-valued points are explicitly omitted on logarithmic axes. The [reference export](assets/figures/growth-models.svg) uses the same formulas.
- Loop cells represent individual executions. Append bars count writes and copied references on a fixed vertical scale. Memory cells represent individual retained characters.
- Recursion-tree labels encode subproblem sizes; circle areas are not quantitative. Edge endpoints are computed from node centers and radii.

The [mathematical model manifest](assets/figures/mathematical-models.json) records domains, formulas, scales, and export precision. The lesson preserves 20 supplied Python examples, adds visible sample outputs, and corrects the source's bounds/cases and memory-analysis errors. See the [coverage record](notes/complexity-update.md).

## Verification

```sh
python3 scripts/check_complexity.py
node scripts/check_complexity.js
```

These checks cover source-example preservation, actual versus displayed outputs, boundary behavior, local routes, static fallback states, and the values **and coordinates** of the mathematical visuals. They are scoped to the new lesson and shared navigation; they do not certify every pre-existing lab implementation.

To regenerate the static mathematical plots, use Python with Matplotlib and NumPy installed:

```sh
python3 scripts/generate_precision_figures.py
```

Tested authoring versions are recorded in the generated model manifest. Plot generation also inverts the exported SVG coordinates to check them against the formulas.

## Repository layout

```text
algorithm-atlas/
├── index.html                  # Unified learning map
├── foundations.html            # Complexity analysis
├── data-structures/index.html   # 12 bundled lessons and foundation note
├── algorithms/index.html        # 82 labs across CS, AI, and ML
├── assets/                     # README preview and numerical plot exports
├── complexity-review.svg       # Selectable module summary
├── complexity-review.png
├── notes/                      # Source coverage and mathematical assumptions
├── scripts/                    # Verification, plot regeneration, packaging
└── repository.json             # Suggested GitHub name, description, and topics
```

## Build a standalone repository package

```sh
python3 scripts/build_standalone.py
```

This creates `dist/algorithm-atlas/` and `dist/algorithm-atlas.zip`, including both atlases, the learning map, analysis lesson, visual assets, source notes, and verification scripts. The directory is ready to use as the contents of a new repository.

**Suggested repository name:** `algorithm-atlas`

**Suggested GitHub description:** Visual, interactive tutorials for data structures, algorithms, complexity analysis, AI, and machine learning—with Python examples, precise mathematical figures, and guided practice.

Font copyright and license notices are preserved in the relevant HTML and SVG files. The original supplied tutorial and correction notes are kept with the authoring sources.

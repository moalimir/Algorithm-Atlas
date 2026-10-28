# Mathematical precision and standalone packaging — 28 October 2026

## Decisions

The user selected **Algorithm Atlas** and repository slug **algorithm-atlas**, then explicitly selected a standalone package containing only this tutorial series. The source checkout belongs to the broader Master-Tech repository. No remote rename, repository creation, commit, or push is part of this packaging operation.

`repository.json` holds the chosen name, title, description, and proposed GitHub topics. The source and packaged READMEs are generated from `scripts/build_standalone.py`, using the same description and their respective relative layouts. The README preview is an actual screenshot of the renamed entry page, not an illustrative mockup.

## Mathematical audit and repairs

| Figure | Original limitation | Current encoding and check |
| --- | --- | --- |
| Asymptotic bounds | The schematic's curves and threshold had no specified functions/constants | f(N)=3N²+5N+12, g(N)=N², c₁=3, c₂=5, N₀=4. Both the curves and shaded boundaries are analytic quadratic Bézier paths. The proof is 5N²−f(N)=(N−4)(2N+3) and f(N)−3N²=5N+12. |
| Growth spectrum | Straight segments connected integer samples and could be read as continuous curves | Discrete markers only, for integer N. No interpolation. Linear and log axes are explicitly labeled. Both zero-valued models at N=1 are omitted only on the log axis. Integer counts are displayed in full; irrational decimal approximations carry ≈. |
| Polynomial contribution | Rounded percentages alone obscured the exact share | SVG widths are numerator/total times a common width. Text reports the exact fraction before the rounded percent. |
| Append costs | The vertical range rescaled to the selected maximum | A common 0–20 unit vertical scale for all 1–32 append inputs. Each write/copy segment has a height proportional to its exact operation count. Averages show the exact quotient before a decimal approximation. |
| Recursive split tree | Its labels were correct, but geometry was manually positioned | Nodes are generated from the binary split rule. Edge endpoints intersect the node-circle boundaries, checked numerically. Per-level sizes sum to N. Node areas are explicitly nonquantitative. |
| Retained suffixes | Percentage bars were rounded and could be distorted by CSS layout | One equal-sized rectangle per retained character. Six input cells and fifteen copied cells for banana. This measures characters, not allocator bytes. |
| Loop shapes | Counts were already formula-based | Preserved. Square, triangular, and bounded-band counts are checked over every supported size, with one equal cell per execution. |
| Memory ledger / three-step recursion explanation | Boxes could be mistaken for proportional diagrams | Explicitly categorical/structural explanations. Their areas do not encode quantities. |

## Reproducible numerical tooling

`python3 scripts/generate_precision_figures.py` uses Matplotlib for axes, labels, layout, and raster exports, with NumPy for the mathematical data. The bounds SVG's sampled polynomial strokes are then replaced by their exact analytic quadratic Bézier representation. The shaded boundaries receive the same treatment. The PNG uses the same mathematical functions rendered by Matplotlib.

The bounds SVG encodes each polynomial exactly algebraically, subject to ordinary floating-point coordinate representation. The generator checks 3,603 parameter values; maximum floating-point discrepancy in the recorded run was about 4×10⁻¹³ work units. `check_complexity.py` independently parses the exported SVG, reads its actual clipping rectangle, inverts its coordinates, and checks 3,845 points across curves and band boundaries.

`node scripts/check_complexity.js` checks **8,261** values and graphical encodings: inverse axes, marker coordinates, fixed-scale stacked-bar heights, exact integer counts, proportion widths, recursion edges, and unit-cell counts. For very small values on a large linear domain, normalized coordinate tolerances account for floating-point conditioning; the underlying integer data remain exact.

The generator exports SVG/PNG reference plots and `assets/figures/mathematical-models.json`, which records domains, formulas, constants, rendering method, and Matplotlib/NumPy versions. No measured runtimes are fabricated. The dynamic-array plot remains an explicitly stated doubling-array teaching model, not CPython's exact allocation policy.

## Package layout

`scripts/build_standalone.py` assembles:

- `index.html`: unified learning map.
- `data-structures/index.html`: the bundled structure lessons and foundation note.
- `algorithms/index.html`: the algorithm/AI/ML bundle.
- `foundations.html`: complexity analysis.
- `assets/`, review SVG/PNG, README, source notes, verification scripts, and repository metadata.

All relevant hrefs and compiled navigation links are rewritten to the standalone layout. Internal lesson hash routes remain the same. The package carries `.nojekyll` for straightforward static hosting. It does not contain a Git directory or account credentials.

The output directory and ZIP live under ignored `dist/`. The builder runs the actual copied Python/Node checks from the packaged directory and resolves every local README link before creating the archive. It can rebuild from either the development layout or a standalone checkout without copying its own output recursively.

## Browser verification

The standalone package was served over HTTP and exercised through learning map → Data Structures → ADT-to-CPU lesson → map → Algorithm Labs → binary search → map → Complexity Analysis. All return links resolved within the package.

The map, analysis page, Data Structures home, algorithm home, category, and lesson were checked at a 320px browser size (305px content width). None produced page-level horizontal overflow. Plot and code containers retain their own local scrolling. Desktop views and actual SVG/image loading were inspected. The fresh package tab produced no console errors.

The original 20 supplied Python function bodies and 26 displayed outputs remain checked, along with boundary cases, legacy anchors, summary images, and local navigation. The current source and exported layouts both pass the same checks. Direct file-protocol browser automation remains unavailable under the browser's URL policy, so file mode is not reported as browser-tested.

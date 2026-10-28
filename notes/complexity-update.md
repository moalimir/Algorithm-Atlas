# Complexity lesson update — 28 October 2026

## Scope and source

Expanded the existing `foundations.html` reading page in place. The preserved URL and anchors `#cost`, `#space`, `#recursion`, `#invariant`, and `#practice` remain valid. Both atlas bundles retain their established routes. The roadmap and DSA home now identify this material as **Complexity analysis**.

The complete user-supplied text is retained in `complexity-source.md` (20 Python examples, including eight analysis problems). All 20 function bodies are preserved, verified by Python AST comparison. Comments and surrounding explanations may be corrected. Existing `contains`, bounded-neighbor loop, `triangle`, running-total, and recursive-sum examples remain; a visible joining alternative is added. Every example has a small sample call and explicit output.

This is one coherent analysis lesson with an ordered contents rail. The original introduction's recursion/invariant material supports the analysis rather than becoming a second course. Existing atlas library/search features are outside this revision; navigation and new lesson interactions are integrated.

## Coverage map

| Source item/example | Destination | Treatment |
| --- | --- | --- |
| Clock time, hardware, interpreter, background work | `#cost` | Preserved, with explicit cost-model assumptions and benchmarking distinction |
| O / Ω / Θ | `#bounds` | Corrected definitions; computed polynomial witness and algebraic proof; retained linear-search example |
| Constants, dominant terms | `#simplify` | Preserved formulas; interactive polynomial-share bar |
| Seven growth classes and examples | `#spectrum` | Preserved hierarchy; logarithmic/linear discrete growth graph and data table; output-size and quicksort qualifications |
| 1: `sequential_steps` | `#iteration` | Preserved, visible output and addition count |
| 2: `nested_loops` | `#iteration` | Preserved, visible output and square count |
| 3: `dependent_loops` | `#iteration` | Preserved, triangular sum and interactive cell grid |
| 4: `logarithmic_loop` | `#iteration` | Preserved code; corrected N=8 output to 1,2,4 |
| 5: `conditional_branch` | `#iteration` | Preserved; analyzed by case and input distribution |
| 6: `constant_space` | `#space` | Preserved; working words versus Python integer bits clarified |
| 7: `linear_space` | `#space` | Preserved; returned set/output convention explicit |
| 8: `quadratic_space` | `#space` | Preserved; independent rows and reference-slot count explained |
| 9: `recursive_countdown` | `#recursion` | Preserved; N+1 frames including base case; prior triangle trace retained |
| Merge-sort recursion tree | `#recurrences` | Drawn tree, 15 calls versus 4 active frames for N=8; merge buffer counted |
| Master Theorem | `#recurrences` | Conditions, polynomial gaps, regularity, valid three-case examples; limitations explicit |
| Dynamic-array amortization | `#amortized` | Doubling teaching model; cost spikes, full geometric sum, total below 3N; CPython policy distinguished |
| 10: `print_two_lists` | `#multiple-inputs` | Preserved; A+B and independent input dimensions |
| 11: `match_elements` | `#multiple-inputs` | Preserved; A·B positive-input shorthand, empty-inner-loop overhead noted |
| Native operation table | `#hidden-costs` | Preserved Python/JS operation analogies, but Python bounds qualified; slice length and hashing assumptions explicit |
| 12: `build_word` | `#hidden-costs` | Function body preserved; inaccurate unconditional-copy comment qualified; visible join alternative added |
| Small inputs and locality | `#reality` | Preserved; no universal crossover, Python reference layout qualified |
| 13: `find_all_pairs` | `#problem-1` | Preserved; renamed from “sliding window” to pair enumeration |
| 14: `get_intersection` | `#problem-2` | Preserved; K≤B matching occurrences can exceed A; separate O(Ua) working storage and O(K) output |
| 15: `count_operations` | `#problem-3` | Preserved; N+floor(N/2)+…<2N; empty input checked |
| 16: `reverse_string` | `#problem-4` | Preserved; corrected peak auxiliary character storage to Θ(N²) for copied CPython suffixes |
| 17: `calculate_fibonacci` | `#problem-5` | Preserved; O(2^N) upper bound versus Θ(phi^N) tight call growth; O(N) stack |
| 18: `binary_search` | `#problem-6` | Preserved; sorted-input assumption, empty array, immediate hit and worst case |
| 19: `search_matrix` | `#problem-7` | Preserved; R·C for positive rectangular dimensions; row overhead and ragged inputs distinguished |
| 20: `first_unique_character` | `#problem-8` | Preserved; 26 lowercase / 128 ASCII; alphabet and count-bit assumptions explicit |
| Prior recursive-sum practice | `#problem-recursion` | Retained as ninth task with independently folded solution |
| Module review | `#review` | Single selectable SVG master and matching browser-rendered PNG; no exercises included |

## Material corrections

- Bounds do not select best/worst cases; Θ does not assert those cases coincide.
- `while i < 8`, starting at one and doubling, executes three times.
- Ordinary copied string slices can remain live in waiting frames; peak storage is not just frame count.
- Intersection preserves repeated occurrences from B; its output can exceed `min(A,B)`.
- ASCII is 128 code points; 256 describes a byte's possible values.
- The Master Theorem needs its stated conditions. Balanced quicksort belongs to the equal-work example, not the root-dominant example.
- Doubling-array sequences may contain several resizes. Writes plus copied references total below 3N; a single-resize approximation is not the proof.
- Python's list growth policy is not exact doubling; the visual is explicitly an educational model.
- `+=` string behavior can be optimized by a runtime. The general copying model motivates joining without promising one timing curve for every implementation.
- Hash lookup is expected constant time under normal assumptions; quicksort's worst case, output materialization, large integer costs, and comparator costs are stated.
- Conversational transition prompts in the source were omitted; teaching content and all code examples were retained.

## Visuals and fallback

Five bounded interactive figures: polynomial dominance, growth curves, loop-cell shapes, one active recursion chain, and dynamic-array append spikes. Native range/select/checkbox controls support the keyboard. No animation or arbitrary code execution is used. Static SVG/cell states, tables, and captions remain in the HTML without JavaScript; controls are revealed only after initialization. Growth has a labeled logarithmic scale (zero omitted) and an explicit linear alternative.

Static teaching visuals: eventual-bound sandwich, input/working/output memory ledger, descending/returning call trace, retained-suffix bars, and the module review. Figures that need readable labels scroll inside their container on narrow screens. Text and code remain selectable. The embedded font pairing matches the learning map; licenses are preserved in the page and summary.

The summary is `complexity-review.svg`, 1400×1900. Its PNG is captured from the SVG in the browser with the embedded font, then encoded as PNG from the browser's JPEG screenshot export. A temporary sharp render was replaced by this browser render to keep the font/layout consistent. Panel text bounds were checked against each panel.

## Source checks

Primary references consulted for corrections:

- [NIST Master Theorem template](https://xlinux.nist.gov/dads/HTML/mastertheorm.html)
- [NYU Master Theorem conditions](https://cs.nyu.edu/~yap/classes/funAlgo/02f/hw/LectureNotes/master.pdf)
- [Yale recurrence expansion notes](https://www.cs.yale.edu/homes/aspnes/pinewiki/SolvingRecurrences.html)
- [Python programming FAQ: string concatenation](https://docs.python.org/3/faq/programming.html#what-is-the-most-efficient-way-to-concatenate-many-strings-together)
- [Python design FAQ: immutable strings](https://docs.python.org/3.13/faq/design.html#why-are-python-strings-immutable)

## Reproducible checks

- `python3 scripts/check_complexity.py`: Python 3.13.5; all 20 supplied function bodies, 26 displayed outputs, 29 boundary/retention assertions, 96 local links, legacy anchors, SVG validity, and PNG dimensions.
- `node scripts/check_complexity.js`: Node 24.16.0; 8,261 value and rendered-geometry assertions across chart inputs/scales, every loop pattern, and 1–32 appends.
- `git diff --check`: no whitespace errors.
- Browser checks: input boundaries, growth-scale changes, polynomial shares, active-path toggling, independent practice/solution disclosure states, and deep links opening enclosing disclosures. Verified at 320×720 and 1280×800 browser sizes (305px and 1265px content widths with scrollbars), with no page-level horizontal overflow. A fresh load, range interaction, and review deep link produced no console errors.
- Direct `file://` browsing is blocked by the browser's URL policy. The lesson has inline fonts/scripts and no runtime data fetch, but direct-file mode is not claimed as browser-tested. No complete audit of the existing 82 algorithm labs was performed as part of this revision.

## Precision and repository revision

The subsequent mathematical-precision review replaced the schematic band with a concrete polynomial witness, exact quadratic SVG paths, and a proof of N₀=4. Growth plots now use discrete integer markers, and all quantitative geometry is checked against its numerical model. See [precision and packaging](precision-and-packaging.md) for the updated method, naming decision, and standalone repository layout.

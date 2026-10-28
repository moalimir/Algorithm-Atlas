"""Build the dedicated algorithm-atlas repository package from either source layout.
Run: python3 scripts/build_standalone.py
Produces dist/algorithm-atlas/ and dist/algorithm-atlas.zip. Does not touch GitHub.
"""
from pathlib import Path
import json
import shutil
import zipfile
import subprocess
import sys
import re

ROOT = Path(__file__).resolve().parents[1]
META = json.loads((ROOT / 'repository.json').read_text())
STANDALONE = (ROOT / 'data-structures/index.html').exists()
DSA = ROOT / ('data-structures/index.html' if STANDALONE else 'index.html')
ALGORITHMS = ROOT / 'algorithms/index.html' if STANDALONE else ROOT.parent / 'Algorithms-Tutorial/index.html'
ENTRY = ROOT / ('index.html' if STANDALONE else 'roadmap.html')
DIST = ROOT / 'dist'
DEST = DIST / META['name']


def readme(standalone):
    entry = 'index.html' if standalone else 'roadmap.html'
    dsa = 'data-structures/index.html' if standalone else 'index.html'
    algorithms = 'algorithms/index.html' if standalone else '../Algorithms-Tutorial/index.html'
    command = 'python3 -m http.server 8000' if standalone else 'python3 -m http.server 8000 --directory ..'
    url = 'http://localhost:8000' if standalone else 'http://localhost:8000/DSA-Tutorial/roadmap.html'
    layout = '''algorithm-atlas/
├── index.html                  # Unified learning map
├── foundations.html            # Complexity analysis
├── data-structures/index.html   # 12 bundled lessons and foundation note
├── algorithms/index.html        # 82 labs across CS, AI, and ML
├── assets/                     # README preview and numerical plot exports
├── complexity-review.svg       # Selectable module summary
├── complexity-review.png
├── notes/                      # Source coverage and mathematical assumptions
├── scripts/                    # Verification, plot regeneration, packaging
└── repository.json             # Suggested GitHub name, description, and topics''' if standalone else '''DSA-Tutorial/
├── roadmap.html                # Unified learning map
├── foundations.html            # Complexity analysis
├── index.html                  # 12 bundled data-structure lessons
├── assets/                     # README preview and numerical plot exports
├── complexity-review.svg
├── complexity-review.png
├── notes/
├── scripts/
└── repository.json
Algorithms-Tutorial/index.html   # Sibling algorithm, AI, and ML bundle'''
    source_note = '' if standalone else '''\nThese development sources sit in the broader `Master-Tech` repository. The package builder combines only this series into a dedicated `algorithm-atlas` repository layout; it does not rename or modify the remote repository.\n'''
    return f'''<!-- Generated from scripts/build_standalone.py and repository.json. -->
# {META['title']}

{META['description']}

![Algorithm Atlas learning map and its core route](assets/algorithm-atlas-preview.png)

## Start exploring

- [Learning map]({entry}): the shared route, prerequisites, checkpoints, and optional branches.
- [Complexity analysis](foundations.html): bounds, loop counts, live memory, recurrences, and amortized costs.
- [Data Structures]({dsa}): arrays, linked lists, stacks, queues, hashing, trees, heaps, Union-Find, matrices, graphs, and suffix arrays/BWT. The ADT-to-CPU lesson is a separate foundation note.
- [Algorithms, AI & ML]({algorithms}): 82 working labs across 14 subject areas, including sorting, searching, graph algorithms, dynamic programming, strings, planning, probability, learning, and language.

The roadmap connects overlapping topics: learn the structure, then investigate the algorithm that uses it. AI and ML are optional branches with their own mathematical prerequisites.

## Run locally

No application build or JavaScript package installation is needed. From this folder:

```sh
{command}
```

Open [{url}]({url}). Python is used only to serve these static files. The learning map and analysis lesson use embedded fonts and scripts; they do not need a CDN.

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
{layout}
```
{source_note}
## Build a standalone repository package

```sh
python3 scripts/build_standalone.py
```

This creates `dist/{META['name']}/` and `dist/{META['name']}.zip`, including both atlases, the learning map, analysis lesson, visual assets, source notes, and verification scripts. The directory is ready to use as the contents of a new repository.

**Suggested repository name:** `{META['name']}`

**Suggested GitHub description:** {META['description']}

Font copyright and license notices are preserved in the relevant HTML and SVG files. The original supplied tutorial and correction notes are kept with the authoring sources.
'''


def package():
    assert DSA.is_file() and ALGORITHMS.is_file() and ENTRY.is_file()
    assert (ROOT / 'assets/algorithm-atlas-preview.png').is_file(), 'Create the README preview first'
    (ROOT / 'README.md').write_text(readme(STANDALONE))
    # Rebuild only the named generated output directory, never the source checkout.
    if DEST.exists(): shutil.rmtree(DEST)
    DEST.mkdir(parents=True)
    (DEST / 'data-structures').mkdir()
    (DEST / 'algorithms').mkdir()
    for name in ['assets','notes','scripts']:
        shutil.copytree(ROOT / name, DEST / name, ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    for name in ['complexity-review.svg','complexity-review.png','repository.json','.gitignore']:
        shutil.copy2(ROOT / name, DEST / name)
    if STANDALONE:
        (DEST / 'index.html').write_text(ENTRY.read_text())
        (DEST / 'foundations.html').write_text((ROOT / 'foundations.html').read_text())
        (DEST / 'data-structures/index.html').write_text(DSA.read_text())
        (DEST / 'algorithms/index.html').write_text(ALGORITHMS.read_text())
    else:
        entry=ENTRY.read_text().replace('href="index.html','href="data-structures/index.html').replace('../Algorithms-Tutorial/index.html','algorithms/index.html')
        foundation=(ROOT/'foundations.html').read_text().replace('href="index.html','href="data-structures/index.html').replace('href="roadmap.html','href="index.html').replace('../Algorithms-Tutorial/index.html','algorithms/index.html')
        dsa=DSA.read_text().replace('href="roadmap.html','href="../index.html').replace('href="foundations.html','href="../foundations.html')
        algorithms=ALGORITHMS.read_text().replace('../DSA-Tutorial/roadmap.html','../index.html')
        (DEST/'index.html').write_text(entry)
        (DEST/'foundations.html').write_text(foundation)
        (DEST/'data-structures/index.html').write_text(dsa)
        (DEST/'algorithms/index.html').write_text(algorithms)
    (DEST/'README.md').write_text(readme(True))
    (DEST/'.nojekyll').write_text('')
    subprocess.run([sys.executable,str(DEST/'scripts/check_complexity.py')],check=True)
    subprocess.run(['node',str(DEST/'scripts/check_complexity.js')],check=True)
    # Every relative README link must resolve inside the package.
    for link in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',(DEST/'README.md').read_text()):
        if not link.startswith(('http:','https:')): assert (DEST/link.split('#')[0]).is_file(),link
    archive=DIST/(META['name']+'.zip')
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for file in sorted(DEST.rglob('*')):
            if file.is_file(): z.write(file,Path(META['name'])/file.relative_to(DEST))
    print('Standalone package:',DEST)
    print('ZIP:',archive)

if __name__=='__main__': package()

"""Archive the complete contributor package without changing its source files.
Run: python3 scripts/build_standalone.py
Produces dist/algorithm-atlas/ and dist/algorithm-atlas.zip.
"""
from pathlib import Path
import json
import re
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
META = json.loads((ROOT / 'repository.json').read_text())
# The repository slug is metadata, never an arbitrary output path.
assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', META['name'])
DIST = ROOT / 'dist'
DEST = DIST / META['name']
FILES = (
    'index.html', 'foundations.html', 'complexity-review.svg', 'complexity-review.png',
    'README.md', 'CONTRIBUTING.md', 'LICENSE', 'THIRD_PARTY_NOTICES.md',
    'requirements-dev.txt', 'repository.json', '.gitignore', '.nojekyll',
)
DIRS = ('data-structures', 'algorithms', 'assets', 'notes', 'scripts', 'docs', '.github', 'licenses')


def package():
    for name in (*FILES, *DIRS):
        if not (ROOT / name).exists():
            raise FileNotFoundError(ROOT / name)
    # Rebuild only this generated directory; never rewrite the maintained README.
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True)
    for name in FILES:
        shutil.copy2(ROOT / name, DEST / name)
    for name in DIRS:
        shutil.copytree(ROOT / name, DEST / name,
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store'))
    subprocess.run([sys.executable, str(DEST / 'scripts/check_complexity.py')], check=True)
    subprocess.run(['node', str(DEST / 'scripts/check_complexity.js')], check=True)
    # Check local documentation destinations in the delivered package.
    for doc in [DEST / 'README.md', DEST / 'CONTRIBUTING.md', DEST / 'THIRD_PARTY_NOTICES.md', *sorted((DEST / 'docs').glob('*.md'))]:
        for link in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', doc.read_text()):
            if not link.startswith(('http:', 'https:', '#')):
                assert (doc.parent / link.split('#')[0]).is_file(), (doc, link)
    archive = DIST / (META['name'] + '.zip')
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for file in sorted(DEST.rglob('*')):
            if file.is_file():
                z.write(file, Path(META['name']) / file.relative_to(DEST))
    print('Contributor package:', DEST)
    print('ZIP:', archive)


if __name__ == '__main__':
    package()

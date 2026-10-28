"""Stage only public site files for GitHub Pages. No third-party packages needed."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'dist/site'
PUBLIC_FILES = (
    'index.html', 'foundations.html', 'data-structures/index.html',
    'algorithms/index.html', 'complexity-review.svg', 'complexity-review.png',
    'LICENSE', 'THIRD_PARTY_NOTICES.md', '.nojekyll',
)
PUBLIC_DIRS = ('assets', 'licenses')


def stage_site():
    # Validate before replacing only this generated staging directory.
    for name in (*PUBLIC_FILES, *PUBLIC_DIRS):
        if not (ROOT / name).exists():
            raise FileNotFoundError(ROOT / name)
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True)
    for name in PUBLIC_FILES:
        target = DEST / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / name, target)
    for name in PUBLIC_DIRS:
        shutil.copytree(ROOT / name, DEST / name)
    files = [p for p in DEST.rglob('*') if p.is_file()]
    assert not any(p.is_symlink() for p in DEST.rglob('*'))
    assert not any((DEST / name).exists() for name in ('scripts', 'notes', '.git', 'docs', '.github'))
    print(f'PASS: staged {len(files)} public files in {DEST}')


if __name__ == '__main__':
    stage_site()

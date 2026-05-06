#!/usr/bin/env python3
"""Export Stratos static assets into ./public for Vercel Output Directory."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'public'

INCLUDE_FILES = [
    'index.html',
    'app.js',
    'styles.css',
    'STRATOS_PREMIUM_REBUILD_BLUEPRINT.md',
    'HIGGSFIELD_CREATIVE_STUDIO.md',
    'PREMIUM_GPT_IMAGE_2_OAUTH_ASSETS.md',
]
INCLUDE_DIRS = [
    'data',
    'demos',
    'public-site',
    'close-rooms',
    'pitch-kits',
    'briefings',
    'dist',
    'marketing-assets/gpt-image-2-oauth',
    'marketing-assets/stratos-gpt2-premium-content-series',
    'n8n',
    'operations',
    'vertical-demos',
    'marketing-assets/vertical-demo-sites',
]
IGNORE_NAMES = {'.DS_Store'}
IGNORE_PARTS = {'.git', '__pycache__', '.vercel'}

if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)

copied = []
for rel in INCLUDE_FILES:
    src = ROOT / rel
    if not src.exists():
        raise SystemExit(f'missing required file: {rel}')
    shutil.copy2(src, OUT / rel)
    copied.append(rel)

for rel in INCLUDE_DIRS:
    src = ROOT / rel
    if not src.exists():
        continue
    dst = OUT / rel
    for path in src.rglob('*'):
        path_rel = path.relative_to(src)
        if path.name in IGNORE_NAMES or IGNORE_PARTS & set(path_rel.parts):
            continue
        target = dst / path_rel
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif path.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            copied.append(str(Path(rel) / path_rel))

# Add a tiny marker so Vercel/build logs make the selected output obvious.
(OUT / 'STRATOS_DEPLOY_READY.txt').write_text(
    'Stratos AI static export ready. Entry: index.html\n'
)
copied.append('STRATOS_DEPLOY_READY.txt')
print(f'Exported {len(copied)} files to {OUT}')

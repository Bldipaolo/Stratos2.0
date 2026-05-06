#!/usr/bin/env python3
"""Prepare a static deploy manifest for Vercel/static hosting."""
from pathlib import Path
import json, time
ROOT=Path(__file__).resolve().parents[1]
dist=ROOT/'dist'; dist.mkdir(exist_ok=True)
assets=set()
for folder in ['.', 'data', 'demos', 'pitch-kits', 'public-site', 'close-rooms', 'briefings', 'n8n', 'operations']:
    base=ROOT/folder
    if not base.exists():
        continue
    for p in base.rglob('*'):
        rel = p.relative_to(ROOT)
        ignored_parts = {'.git', 'dist', 'public', '__pycache__', '.vercel'}
        ignored_names = {'.DS_Store'}
        if p.is_file() and not (ignored_parts & set(rel.parts)) and p.name not in ignored_names:
            assets.add(str(rel))
manifest={
    'name':'Stratos AI Hermes Command Center',
    'generatedAt':time.strftime('%Y-%m-%dT%H:%M:%S'),
    'entrypoints':['index.html','public-site/index.html'],
    'assetCount':len(assets),
    'assets':sorted(assets),
    'deployNotes':['Static/Vercel-friendly: no server required for dashboard/public site.', 'Local scripts are dev/operator utilities and do not need to run in Vercel.']
}
(dist/'stratos-site-manifest.json').write_text(json.dumps(manifest, indent=2))
print(f"Wrote deploy manifest with {len(assets)} assets")

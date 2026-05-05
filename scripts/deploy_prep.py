#!/usr/bin/env python3
"""Prepare a static deploy manifest for Vercel/static hosting."""
from pathlib import Path
import json, time
ROOT=Path(__file__).resolve().parents[1]
dist=ROOT/'dist'; dist.mkdir(exist_ok=True)
assets=[]
for folder in ['.', 'data', 'demos', 'pitch-kits', 'public-site', 'close-rooms', 'briefings']:
    base=ROOT/folder
    if not base.exists():
        continue
    for p in base.rglob('*'):
        if p.is_file() and '.git' not in p.parts:
            assets.append(str(p.relative_to(ROOT)))
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

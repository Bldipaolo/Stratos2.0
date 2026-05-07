#!/usr/bin/env python3
"""Ruflo status snapshot for Stratos. No side effects beyond reading local clone and npx version."""
from pathlib import Path
import json, subprocess, shutil
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'data'/'stratos_ruflo_system.json').read_text())
print('STRATOS × RUFLO STATUS')
print('Source:', data['source']['repo'])
print('Local:', data['source']['localPath'])
print('Pinned head:', data['source']['summary'])
try:
    live=subprocess.check_output(['git','log','--oneline','-1'],cwd=data['source']['localPath'],text=True).strip()
    print('Live clone:', live)
except Exception as e:
    print('Live clone: unavailable', e)
print('npx:', 'available' if shutil.which('npx') else 'missing')
try:
    ver=subprocess.check_output(['npx','--yes','ruflo@latest','--version'],cwd=ROOT,text=True,stderr=subprocess.STDOUT,timeout=120).strip().splitlines()[-1]
    print('Ruflo npm:', ver)
except Exception as e:
    print('Ruflo npm: check failed', str(e)[:160])
print('\nDaily rhythm:')
for item in data['dailyRhythm']:
    print(f"- {item['slot']}: {item['command']}")

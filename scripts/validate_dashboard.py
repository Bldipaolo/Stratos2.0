#!/usr/bin/env python3
"""Deterministic Stratos dashboard validator: no model calls."""
from pathlib import Path
import json, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
errors=[]
def need(cond,msg):
    if not cond: errors.append(msg)
html=(ROOT/'index.html').read_text(); js=(ROOT/'app.js').read_text(); css=(ROOT/'styles.css').read_text()
leads=json.loads((ROOT/'data'/'leads.json').read_text()); autos=json.loads((ROOT/'data'/'automations.json').read_text())
for label in ['Boca Lead War Room','Usage Saver','Client Close Room','Strategy OS']:
    need(label in js, f'missing module label {label}')
for l in leads:
    for key in ['id','business','industry','score','weaknesses','offer','angle','demo','estBookings','avgValue']:
        need(key in l, f"lead {l.get('business','?')} missing {key}")
    need(isinstance(l.get('weaknesses'), list) and len(l['weaknesses'])>=2, f"lead {l.get('business')} needs weaknesses")
    need((ROOT/l['demo'].lstrip('/')).exists(), f"demo missing: {l['demo']}")
    need((ROOT/'close-rooms'/f"{l['id']}.html").exists(), f"close room missing: {l['id']}")
need(len(leads)>=10, 'expected >=10 leads')
need(len(autos)==8, 'expected 8 automations')
need('app.js' in html and 'styles.css' in html, 'index missing assets')
need('.usage-card' in css and '.quota-log' in css, 'missing usage saver CSS')
need('.strategy-hero' in css and '.ops-lane' in css, 'missing Strategy OS CSS')
for rel in ['public/index.html','public/app.js','public/styles.css','public/public-site/index.html','public/close-rooms/glamor-medical.html','public/STRATOS_DEPLOY_READY.txt','public-site/index.html','briefings/latest.md','dist/stratos-site-manifest.json','STRATOS_OPERATING_SYSTEM.md','STRATOS_RUNBOOK.md','DEPLOYMENT_CHECKLIST.md']:
    need((ROOT/rel).exists(), f'missing {rel}')
node = subprocess.run(['node','test-dashboard.js'], cwd=ROOT, text=True, capture_output=True)
need(node.returncode==0, 'node dashboard test failed: '+(node.stderr or node.stdout)[:500])
if errors:
    print('VALIDATION FAILED')
    for e in errors: print('-', e)
    sys.exit(1)
print(f"VALIDATION PASSED: {len(leads)} leads, {len(autos)} automations, Strategy OS + Usage Saver wired.")

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
growth=json.loads((ROOT/'data'/'stratos_growth_system.json').read_text())
premium=json.loads((ROOT/'data'/'stratos_premium_ops.json').read_text())
ops=json.loads((ROOT/'data'/'stratos_ops_library.json').read_text())
demo_system=json.loads((ROOT/'data'/'stratos_demo_site_system.json').read_text())
ruflo=json.loads((ROOT/'data'/'stratos_ruflo_system.json').read_text())
arena=json.loads((ROOT/'data'/'stratos_ruflo_arena.json').read_text())
for label in ['Command Intelligence','Sales War Room v2','Today Action Board','Offer Ladder','Outreach Vault','Client Audit Generator','Close Room Templates','Content Repurposing','Case Study Templates','Usage Saver','Client Close Room','Strategy OS','n8n Automation Library','Ops Logistics','Persistent CRM Board','Vertical Demo Sites','Pricing / Scope Calculator','School-Safe Launch Page','Ruflo Orchestration','Swarm Arena']:
    need(label in js, f'missing module label {label}')
for l in leads:
    for key in ['id','business','industry','score','weaknesses','offer','angle','demo','estBookings','avgValue']:
        need(key in l, f"lead {l.get('business','?')} missing {key}")
    need(isinstance(l.get('weaknesses'), list) and len(l['weaknesses'])>=2, f"lead {l.get('business')} needs weaknesses")
    need((ROOT/l['demo'].lstrip('/')).exists(), f"demo missing: {l['demo']}")
    need((ROOT/'close-rooms'/f"{l['id']}.html").exists(), f"close room missing: {l['id']}")
need(len(leads)>=10, 'expected >=10 leads')
need(len(autos)==8, 'expected 8 automations')
need(len(growth.get('offerLadder',[]))==4, 'expected 4 offer ladder packages')
need(len(growth.get('todayMoves',[]))>=6, 'expected daily action board moves')
need(len(growth.get('caseStudies',[]))>=3, 'expected transparent case study templates')
need(len(premium.get('operatingSystem',[]))>=5, 'expected premium operating lanes')
need(len(premium.get('dealPackets',[]))>=4, 'expected premium vertical deal packets')
need(len(premium.get('higgsfieldStudio',{}).get('promptBank',[]))>=4, 'expected Higgsfield prompt bank')
need(len(ops.get('n8nGuides',[]))>=4, 'expected >=4 n8n guides')
need(len(ops.get('templates',[]))>=4, 'expected >=4 ops templates')
need(len(demo_system.get('verticals',[]))==5, 'expected 5 premium vertical demos')
need(len(ruflo.get('dailyRhythm',[]))>=4, 'expected Ruflo daily rhythm')
need(len(arena.get('agents',[]))>=6 and len(arena.get('phases',[]))>=5, 'expected Ruflo Swarm Arena agents/phases')
need('Ruflo' in js and 'function ruflo()' in js and any('ruflo_daily.py' in c.get('cmd','') for c in ruflo.get('safeCommands',[])), 'missing Ruflo dashboard wiring')
for v in demo_system.get('verticals',[]):
    need((ROOT/v['demoPath'].lstrip('./')).exists(), f"vertical demo missing: {v.get('slug')}")
    need((ROOT/v['heroImage'].lstrip('./')).exists(), f"vertical hero missing: {v.get('slug')}")
need('0 credits' in json.dumps(premium.get('higgsfieldStudio',{})), 'Higgsfield blocker/status must be explicit')
need('app.js' in html and 'styles.css' in html, 'index missing assets')
need('.usage-card' in css and '.quota-log' in css, 'missing usage saver CSS')
need('.strategy-hero' in css and '.ops-lane' in css, 'missing Strategy OS CSS')
need('.intel-hero' in css and '.lane-grid' in css, 'missing Command Intelligence CSS')
need('.vertical-demo-grid' in css and '.crm-board' in css and '.pricing-lab' in css, 'missing premium demo/CRM/pricing CSS')
need('.ruflo-hero' in css and '.ruflo-rhythm' in css, 'missing Ruflo CSS')
need('.arena-stage' in css and '.agent-pod' in css, 'missing Swarm Arena CSS')
for rel in ['public/index.html','public/app.js','public/styles.css','public/public-site/index.html','public/close-rooms/glamor-medical.html','public/STRATOS_DEPLOY_READY.txt','public-site/index.html','briefings/latest.md','dist/stratos-site-manifest.json','STRATOS_OPERATING_SYSTEM.md','STRATOS_RUNBOOK.md','DEPLOYMENT_CHECKLIST.md','STRATOS_TODAY_ACCELERATION.md','STRATOS_PREMIUM_REBUILD_BLUEPRINT.md','HIGGSFIELD_CREATIVE_STUDIO.md','data/stratos_growth_system.json','data/stratos_premium_ops.json','data/stratos_ops_library.json','n8n/README.md','operations/README.md','operations/DELIVERY_QA_CHECKLIST.md','data/stratos_demo_site_system.json','scripts/generate_vertical_demo_sites.py','vertical-demos/medspa.html','marketing-assets/vertical-demo-sites/medspa-hero.png','public/vertical-demos/medspa.html','public/marketing-assets/vertical-demo-sites/medspa-hero.png','data/stratos_ruflo_system.json','scripts/ruflo_daily.py','scripts/ruflo_status.py','ruflo/README.md','ruflo/DAY_TO_DAY_PROCESS.md','public/data/stratos_ruflo_system.json','public/ruflo/README.md','data/stratos_ruflo_arena.json','scripts/ruflo_arena.py','ruflo/SWARM_ARENA.md','public/data/stratos_ruflo_arena.json','public/ruflo/SWARM_ARENA.md']:
    need((ROOT/rel).exists(), f'missing {rel}')
node = subprocess.run(['node','test-dashboard.js'], cwd=ROOT, text=True, capture_output=True)
need(node.returncode==0, 'node dashboard test failed: '+(node.stderr or node.stdout)[:500])
if errors:
    print('VALIDATION FAILED')
    for e in errors: print('-', e)
    sys.exit(1)
print(f"VALIDATION PASSED: {len(leads)} leads, {len(autos)} automations, Strategy OS + Usage Saver + n8n/Ops wired.")

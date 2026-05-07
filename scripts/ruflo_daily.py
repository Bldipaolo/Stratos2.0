#!/usr/bin/env python3
"""Generate/optionally run Ruflo coordination commands for Stratos daily ops."""
from pathlib import Path
import argparse, json, subprocess, shlex, datetime
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'data'/'stratos_ruflo_system.json').read_text())
parser=argparse.ArgumentParser(description='Stratos Ruflo day-to-day coordinator')
parser.add_argument('mode', choices=['morning','build','qa','close','commands'])
parser.add_argument('--objective', default='advance Stratos AI operating system')
parser.add_argument('--note', default='Stratos pattern captured')
parser.add_argument('--run', action='store_true', help='Actually run safe Ruflo npx commands. Default prints commands only.')
args=parser.parse_args()

def emit(label, cmd):
    print(f"\n## {label}\n{cmd}")
    if args.run:
        subprocess.run(cmd, cwd=ROOT, shell=True, check=False)

print('Stratos × Ruflo routine:', args.mode)
print('Rule: Ruflo coordinates; Hermes/Codex executes the work immediately after.')
if args.mode=='morning':
    emit('Search memory for Stratos patterns', 'npx --yes ruflo@latest memory search --query "Stratos AI daily operating patterns lead demo proof" || true')
    emit('Initialize lightweight coordination swarm', 'npx --yes ruflo@latest swarm init --topology hierarchical --max-agents 5 || true')
    emit('Spawn coordinator/researcher records', 'npx --yes ruflo@latest agent spawn -t coordinator --name stratos-daily-coordinator || true; npx --yes ruflo@latest agent spawn -t researcher --name stratos-market-researcher || true')
elif args.mode=='build':
    q=shlex.quote(args.objective)
    emit('Create build swarm', f'npx --yes ruflo@latest swarm init --topology hierarchical --max-agents 8 || true')
    emit('Spawn build team records', 'npx --yes ruflo@latest agent spawn -t architect --name stratos-architect || true; npx --yes ruflo@latest agent spawn -t coder --name stratos-builder || true; npx --yes ruflo@latest agent spawn -t tester --name stratos-tester || true')
    emit('Create tracked task', f'npx --yes ruflo@latest task create --type implementation --description {q} || true')
elif args.mode=='qa':
    q=shlex.quote(args.objective)
    emit('Create QA swarm', 'npx --yes ruflo@latest swarm init --topology mesh --max-agents 4 || true')
    emit('Spawn reviewer/tester records', 'npx --yes ruflo@latest agent spawn -t tester --name stratos-qa || true; npx --yes ruflo@latest agent spawn -t reviewer --name stratos-reviewer || true')
    print('\n## Required Stratos execution after Ruflo coordination\nnode --check app.js && node test-dashboard.js && python3 scripts/run_all.py')
elif args.mode=='close':
    note=shlex.quote(args.note)
    key='stratos-closeout-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    emit('Store closeout pattern', f'npx --yes ruflo@latest memory store --key {key} --value {note} --namespace stratos-patterns || true')
    print('\n## Required closeout\ngit status --short && python3 scripts/validate_dashboard.py')
elif args.mode=='commands':
    for row in data['safeCommands']:
        print(f"- {row['label']}: {row['cmd']}")

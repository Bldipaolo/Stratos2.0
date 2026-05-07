#!/usr/bin/env python3
"""Ruflo Swarm Arena: generate a Stratos mission packet and optionally register Ruflo coordination records."""
from pathlib import Path
import argparse, json, subprocess, datetime, shlex
ROOT=Path(__file__).resolve().parents[1]
arena=json.loads((ROOT/'data'/'stratos_ruflo_arena.json').read_text())
parser=argparse.ArgumentParser(description='Stratos Ruflo Swarm Arena')
parser.add_argument('action', choices=['mission','deck','status'])
parser.add_argument('--mode', default='ambush', choices=[m['id'] for m in arena['modes']])
parser.add_argument('--objective', default=arena['defaultObjective'])
parser.add_argument('--run-ruflo', action='store_true', help='Actually call Ruflo npx coordination commands')
args=parser.parse_args()

def sh(cmd):
    print('$', cmd)
    if args.run_ruflo:
        subprocess.run(cmd, cwd=ROOT, shell=True, check=False)

def mission():
    mode=next(m for m in arena['modes'] if m['id']==args.mode)
    stamp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    out=ROOT/'ruflo'/'missions'; out.mkdir(parents=True, exist_ok=True)
    packet={
        'missionId': f"ruflo-{args.mode}-{stamp}",
        'createdAt': datetime.datetime.now().isoformat(timespec='seconds'),
        'mode': mode,
        'objective': args.objective,
        'truthLabel': arena['truthLabel'],
        'agents': arena['agents'],
        'phases': arena['phases'],
        'executionOrder': [
            'Coordinate with Ruflo first; do not wait for it to build.',
            'Hermes/Codex executes files, scripts, browser QA, commit, and push.',
            'Only call outputs real when validators/browser/git prove them.'
        ],
        'rufloCommands': [
            'npx --yes ruflo@latest memory search --query "Stratos AI revenue demo proof automation" || true',
            'npx --yes ruflo@latest swarm init --topology hierarchical --max-agents 8 || true',
            'npx --yes ruflo@latest agent spawn -t coordinator --name queen-coordinator || true',
            'npx --yes ruflo@latest agent spawn -t researcher --name boca-signal-hunter || true',
            'npx --yes ruflo@latest agent spawn -t architect --name offer-architect || true',
            'npx --yes ruflo@latest agent spawn -t coder --name hermes-builder || true',
            'npx --yes ruflo@latest agent spawn -t tester --name proof-tester || true',
            f"npx --yes ruflo@latest task create --type implementation --description {shlex.quote(args.objective)} || true"
        ]
    }
    for cmd in packet['rufloCommands']:
        sh(cmd)
    path=out/f"{packet['missionId']}.json"
    path.write_text(json.dumps(packet,indent=2))
    latest=out/'latest.json'; latest.write_text(json.dumps(packet,indent=2))
    print('\nMISSION PACKET:', path)
    print('MODE:', mode['name'])
    print('OBJECTIVE:', args.objective)
    print('NEXT: execute the actual Stratos task, then run python3 scripts/run_all.py')

def deck():
    print('RUFLO SWARM ARENA COMMAND DECK')
    for cmd in arena['commandDeck']:
        print('-', cmd)

def status():
    latest=ROOT/'ruflo'/'missions'/'latest.json'
    print('Arena:', arena['name'])
    print('Latest mission:', latest if latest.exists() else 'none yet')
    print('Modes:', ', '.join(m['id'] for m in arena['modes']))

{'mission': mission, 'deck': deck, 'status': status}[args.action]()

#!/usr/bin/env python3
"""Generate local AI outreach drafts via Ollama without spending Codex quota."""
from pathlib import Path
import argparse
import json
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = 'qwen3.5:9b'

def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

def ollama(prompt, model, max_tokens=420):
    payload = {
        'model': model,
        'prompt': prompt,
        'stream': False,
        'options': {'temperature': 0.55, 'num_predict': max_tokens, 'top_p': 0.9},
    }
    req = urllib.request.Request(
        'http://127.0.0.1:11434/api/generate',
        data=json.dumps(payload).encode(),
        headers={'Content-Type': 'application/json'},
    )
    try:
        return json.loads(urllib.request.urlopen(req, timeout=180).read().decode()).get('response', '').strip()
    except Exception as e:
        raise SystemExit(f'Ollama draft failed. Is Ollama running? {e}')

def main():
    ap = argparse.ArgumentParser(description='Local Ollama Stratos draft generator')
    ap.add_argument('--lead', default='glamor-medical', help='lead id from data/leads.json or all')
    ap.add_argument('--model', default=DEFAULT_MODEL)
    ap.add_argument('--mode', choices=['email', 'sms', 'dm', 'call', 'all'], default='all')
    args = ap.parse_args()

    leads = json.loads((ROOT / 'data' / 'leads.json').read_text())
    selected = leads if args.lead == 'all' else [next((l for l in leads if l['id'] == args.lead or slug(l['business']) == args.lead), None)]
    selected = [l for l in selected if l]
    if not selected:
        raise SystemExit(f'No lead found for {args.lead}')

    out = ROOT / 'local-ai-drafts'
    out.mkdir(exist_ok=True)
    for lead in selected:
        modes = ['email', 'sms', 'dm', 'call'] if args.mode == 'all' else [args.mode]
        sections = []
        for mode in modes:
            prompt = f"""You are Bradley at Stratos AI, a Boca Raton agency selling premium websites plus AI automations to local businesses. Draft a concise, human, non-spammy {mode} outreach message. Be specific and useful. Do not mention that AI wrote this.

Lead: {lead['business']}
Industry: {lead['industry']}
Offer: {lead['offer']}
Angle: {lead['angle']}
Weaknesses: {'; '.join(lead['weaknesses'])}

Write only the {mode} message, ready to copy."""
            draft = ollama(prompt, args.model)
            sections.append(f"## {mode.upper()} · {args.model}\n\n{draft}\n")
        path = out / f"{slug(lead['business'])}-ollama.md"
        path.write_text(f"# Local Ollama Drafts — {lead['business']}\n\n" + '\n'.join(sections))
        print(f'Wrote {path}')

if __name__ == '__main__':
    main()

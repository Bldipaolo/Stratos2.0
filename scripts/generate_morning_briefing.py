#!/usr/bin/env python3
"""Generate a deterministic morning briefing from the current lead board."""
from pathlib import Path
from datetime import datetime
import json
ROOT=Path(__file__).resolve().parents[1]
leads=json.loads((ROOT/'data'/'leads.json').read_text())
out=ROOT/'briefings'; out.mkdir(exist_ok=True)
top=sorted(leads, key=lambda l:l['score'], reverse=True)[:5]
lines=["# Stratos AI Morning Briefing", "", f"Generated: {datetime.now().isoformat(timespec='seconds')}", "", "## Top targets"]
for i,l in enumerate(top,1):
    upside=l['estBookings']*l['avgValue']
    lines += [f"{i}. **{l['business']}** — {l['industry']} · Score {l['score']} · projected upside ${upside:,}/mo", f"   - Move: {l['angle']}", f"   - Asset: {l['demo']} and close-rooms/{l['id']}.html"]
lines += ["", "## Today’s zero-model action queue", "- Run `python3 scripts/run_all.py` after lead data changes.", "- Open `http://localhost:8790/#strategy` for the operating path.", "- Use `hermes -p stratos-local` for rough drafts; save Codex for final review.", "- Send one high-specificity pitch kit before building any new speculative feature."]
text='\n'.join(lines)+'\n'
(out/'latest.md').write_text(text)
(out/f"briefing-{datetime.now().strftime('%Y%m%d')}.md").write_text(text)
print(f"Generated briefing: {out/'latest.md'}")

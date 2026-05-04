#!/usr/bin/env python3
"""Build deterministic outreach pitch kits from data/leads.json with zero model calls."""
from pathlib import Path
import json, re
ROOT=Path(__file__).resolve().parents[1]
leads=json.loads((ROOT/'data'/'leads.json').read_text())
out=ROOT/'pitch-kits'; out.mkdir(exist_ok=True)
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def kit(l):
    weaknesses='\n'.join(f"- {w}" for w in l['weaknesses'])
    upside=l['estBookings']*l['avgValue']
    return f"""# {l['business']} Pitch Kit\n\nIndustry: {l['industry']}\nScore: {l['score']}\nPhone: {l['phone']}\nWebsite: {l.get('website') or 'Not listed'}\nAddress: {l['address']}\n\n## Angle\n{l['angle']}\n\n## Recommended Offer\n{l['offer']}\n\n## Why it fits\n{weaknesses}\n\n## Email\nSubject: Quick {l['industry'].lower()} growth idea for {l['business']}\n\nHey {l['business']} team — I noticed an opportunity to capture more qualified leads with {l['offer']}. The main gap is: {l['weaknesses'][0].lower()}.\n\nStratos AI builds premium local-business websites with AI booking, missed-call recovery, review automation, and follow-up systems. For {l['business']}, I’d recommend: {l['angle']}\n\nIf useful, I can send a quick preview/mockup showing what this would look like with your brand.\n\n— Bradley\nStratos AI\n\n## SMS / DM\nSaw a couple ways {l['business']} could capture more {l['industry'].lower()} leads with AI booking + follow-up. Want me to send the quick preview?\n\n## Call opener\nI’m local to Boca and built a quick growth-system concept for {l['business']}. The main idea is {l['angle']}\n\n## ROI line\nIf this creates even {max(1, round(1500/l['avgValue']))} extra bookings, it pays for the monthly system. Estimated upside from current assumptions: ${upside:,}/mo.\n"""
for l in leads:
    (out/f"{slug(l['business'])}.md").write_text(kit(l))
print(f"Built {len(leads)} pitch kits in {out}")

#!/usr/bin/env python3
"""Generate private close-room pages for every lead with zero model calls."""
from pathlib import Path
import html, json
ROOT=Path(__file__).resolve().parents[1]
leads=json.loads((ROOT/'data'/'leads.json').read_text())
autos=json.loads((ROOT/'data'/'automations.json').read_text())
out=ROOT/'close-rooms'; out.mkdir(exist_ok=True)
auto_list=''.join(f"<li>{html.escape(a['name'])} — ${a['price']}/mo</li>" for a in autos[:5])
for l in leads:
    upside=l['estBookings']*l['avgValue']
    weaknesses=''.join(f"<li>{html.escape(w)}</li>" for w in l['weaknesses'])
    page=f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{html.escape(l['business'])} — Stratos Close Room</title><style>body{{margin:0;background:#07080d;color:#f6f7fb;font:16px Inter,system-ui,sans-serif}}main{{max-width:1040px;margin:auto;padding:34px 20px}}.hero,.card{{border:1px solid #20283a;border-radius:28px;padding:26px;background:linear-gradient(135deg,rgba(124,131,255,.18),rgba(66,211,255,.06));margin:16px 0}}h1{{font-size:clamp(38px,7vw,78px);line-height:.92;letter-spacing:-.06em}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}}.metric b{{display:block;font-size:34px;color:#42d3ff}}li{{margin:10px 0;color:#c7d0e5}}a,button{{display:inline-block;border:1px solid #33405f;border-radius:999px;padding:12px 15px;color:#f6f7fb;text-decoration:none;background:#151b2a}}.muted{{color:#9aa4b7}}</style></head><body><main><section class='hero'><p class='muted'>Private proposal room · prepared by Stratos AI</p><h1>{html.escape(l['business'])}</h1><p>{html.escape(l['angle'])}</p><a href='../index.html#pitch'>Generate outreach pack</a> <a href='../{l['demo'].lstrip('/')}'>View demo</a></section><section class='grid'><div class='card metric'><span>Projected upside</span><b>${upside:,}/mo</b></div><div class='card metric'><span>Recommended offer</span><b>{html.escape(l['offer'])}</b></div><div class='card metric'><span>Starting investment</span><b>$2.5K + $1.5K/mo</b></div></section><section class='card'><h2>What we found</h2><ul>{weaknesses}</ul></section><section class='grid'><div class='card'><h2>Launch plan</h2><ol><li>48-hour audit and conversion map</li><li>7-day demo/proposal page</li><li>14-day site + AI capture launch</li><li>30-day optimization/reporting loop</li></ol></div><div class='card'><h2>Automation stack</h2><ul>{auto_list}</ul></div></section></main></body></html>"""
    (out/f"{l['id']}.html").write_text(page)
print(f"Generated {len(leads)} close rooms in {out}")

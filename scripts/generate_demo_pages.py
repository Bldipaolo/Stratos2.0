#!/usr/bin/env python3
"""Generate Stratos demo pages from data/leads.json with zero model calls."""
from pathlib import Path
import html, json
ROOT = Path(__file__).resolve().parents[1]
leads = json.loads((ROOT/'data'/'leads.json').read_text())
out = ROOT/'demos'; out.mkdir(exist_ok=True)
TEMPLATE = """<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>{business} — Stratos AI Demo</title><style>body{{margin:0;background:#07080d;color:#f6f7fb;font:16px Inter,system-ui,sans-serif}}main{{max-width:1060px;margin:auto;padding:44px 22px}}.hero,.card{{border:1px solid #20283a;border-radius:28px;background:linear-gradient(135deg,rgba(124,131,255,.18),rgba(66,211,255,.06));padding:28px;margin:16px 0}}h1{{font-size:clamp(36px,6vw,72px);line-height:.95;margin:10px 0}}.pill{{display:inline-block;border:1px solid #33405f;border-radius:999px;padding:8px 12px;margin:5px;background:#111827}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}}a,button{{color:#07080d;background:#42d3ff;border:0;border-radius:999px;padding:12px 16px;text-decoration:none;font-weight:800}}.muted{{color:#9aa4b7}}</style></head><body><main><section class=\"hero\"><p class=\"muted\">Private Stratos AI concept demo</p><h1>{business}</h1><p>{angle}</p><a href=\"../index.html#close\">Open full close room</a></section><section class=\"grid\"><div class=\"card\"><h2>What we would fix</h2>{weaknesses}</div><div class=\"card\"><h2>Recommended offer</h2><p class=\"pill\">{offer}</p><p class=\"muted\">Projected upside: {bookings} new bookings/mo × ${value} avg value.</p></div><div class=\"card\"><h2>Conversion modules</h2><span class=\"pill\">AI booking</span><span class=\"pill\">Missed-call recovery</span><span class=\"pill\">Review automation</span><span class=\"pill\">Lead follow-up</span></div></section></main></body></html>"""
count=0
for lead in leads:
    filename = lead.get('demo','').split('/')[-1] or f"{lead['id']}.html"
    weaknesses = ''.join(f"<p class='pill'>{html.escape(w)}</p>" for w in lead['weaknesses'])
    page = TEMPLATE.format(business=html.escape(lead['business']), angle=html.escape(lead['angle']), weaknesses=weaknesses, offer=html.escape(lead['offer']), bookings=lead['estBookings'], value=lead['avgValue'])
    (out/filename).write_text(page)
    count += 1
print(f"Generated {count} demo pages in {out}")

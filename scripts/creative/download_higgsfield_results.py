#!/usr/bin/env python3
"""Download result media URLs from a Higgsfield --wait --json job file.

This is intentionally generic because Higgsfield job JSON shape can vary by model.
It walks the JSON, finds http(s) media-looking URLs, and downloads them with stable names.
"""
from __future__ import annotations
from pathlib import Path
import json, re, sys, urllib.request

MEDIA_RE = re.compile(r'https?://[^\s"\']+\.(?:png|jpg|jpeg|webp|mp4|mov)(?:\?[^\s"\']*)?', re.I)

def walk(obj):
    if isinstance(obj, dict):
        for v in obj.values():
            yield from walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk(v)
    elif isinstance(obj, str):
        for m in MEDIA_RE.finditer(obj):
            yield m.group(0)

if len(sys.argv) != 3:
    raise SystemExit('usage: download_higgsfield_results.py <job.json> <output-dir>')

job = Path(sys.argv[1])
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
data = json.loads(job.read_text())
urls = []
for url in walk(data):
    if url not in urls:
        urls.append(url)

if not urls:
    raise SystemExit(f'no media URLs found in {job}')

for i, url in enumerate(urls, 1):
    clean = url.split('?', 1)[0]
    suffix = Path(clean).suffix or '.bin'
    target = out / f'{job.stem}-{i:02d}{suffix}'
    print(f'downloading {url} -> {target}')
    urllib.request.urlretrieve(url, target)
print(f'downloaded {len(urls)} file(s)')

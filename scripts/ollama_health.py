#!/usr/bin/env python3
"""Check local Ollama availability and installed models. Zero Codex usage."""
import json
import sys
import urllib.request

URL = 'http://127.0.0.1:11434/api/tags'
try:
    data = json.loads(urllib.request.urlopen(URL, timeout=5).read().decode())
except Exception as e:
    print(f'OLLAMA OFFLINE: {e}')
    sys.exit(1)

models = data.get('models', [])
print('OLLAMA ONLINE')
for m in models:
    details = m.get('details', {})
    print(f"- {m.get('name')} · {details.get('parameter_size', '?')} · {round(m.get('size', 0)/1e9, 1)} GB")
if not models:
    sys.exit('No Ollama models installed')

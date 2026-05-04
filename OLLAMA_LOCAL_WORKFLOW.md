# Stratos Local Ollama Workflow

Ollama is the local/cheap AI lane for Stratos. It does not spend Codex quota.

## Detected local models

- `qwen3.5:9b` — best current local general drafting/reasoning model.
- `qwen2.5-coder:7b` — local coding helper.

## Commands

Check Ollama:

```bash
python3 scripts/ollama_health.py
```

Generate local outreach drafts for one lead:

```bash
python3 scripts/ollama_draft.py --lead glamor-medical --mode all
```

Generate local outreach drafts for every lead:

```bash
python3 scripts/ollama_draft.py --lead all --mode all
```

Use the coder model when needed:

```bash
python3 scripts/ollama_draft.py --lead glamor-medical --mode email --model qwen2.5-coder:7b
```

Outputs go to `local-ai-drafts/`.

## Routing rule

- Deterministic repeated assets: scripts, no model.
- Draft copy and quick variants: Ollama.
- Architecture, difficult debugging, final design/code review: Codex/GPT-5.5.

## Optional Hermes local profile

A separate Hermes profile is already configured and verified:

```bash
hermes -p stratos-local chat -Q -t terminal,file --max-turns 3 -q 'Reply with exactly: STRATOS LOCAL ONLINE'
```

Profile config path:

```text
/Users/bradleydipaolo/.hermes/profiles/stratos-local/config.yaml
```

It uses:

```text
provider: ollama-local
base_url: http://127.0.0.1:11434/v1
model: qwen3.5:9b
```

Keep the normal/default profile on Codex for premium review.
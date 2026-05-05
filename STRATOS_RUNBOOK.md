# Stratos AI Runbook

## Daily startup

```bash
cd /Users/bradleydipaolo/stratos-ai/hermes-command-center
python3 scripts/run_all.py
python3 scripts/free_port_server.py --start 8790
```

Open the printed local URL, usually:

```text
http://localhost:8790
```

## Main operator path

1. Open **Strategy OS**.
2. Review the top three money moves.
3. Open **Boca Lead War Room**.
4. Select the highest-score lead.
5. Open their demo and close room.
6. Use **One-Click Outreach Packs** or the generated `pitch-kits/*.md` file.
7. If copy needs variation, use local Ollama:

```bash
python3 scripts/ollama_draft.py --lead glamor-medical --mode all
```

or Hermes local:

```bash
hermes -p stratos-local chat -t terminal,file -q "Using /Users/bradleydipaolo/stratos-ai/hermes-command-center, draft three concise outreach variants for Glamor Medical and save them under local-ai-drafts/."
```

## Full rebuild/test

```bash
python3 scripts/run_all.py
```

This runs:

- demo generation
- pitch-kit generation
- close-room generation
- public-site generation
- morning briefing generation
- deploy-manifest prep
- dashboard validation

## Validation only

```bash
python3 scripts/validate_dashboard.py
node test-dashboard.js
```

## Local AI health

```bash
python3 scripts/ollama_health.py
```

Expected local models:

- `qwen3.5:9b`
- `qwen2.5-coder:7b`

## Deploy prep

```bash
python3 scripts/deploy_prep.py
```

Then inspect:

```text
dist/stratos-site-manifest.json
```

For Vercel/static hosting, the app is static. The key entrypoints are:

- `index.html`
- `public-site/index.html`

## Premium-model rule

Do not use Codex for repetitive generation. Use Codex only when the next decision requires premium judgment or a tricky multi-file debugging pass.

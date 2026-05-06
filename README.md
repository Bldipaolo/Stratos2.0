# Stratos AI Hermes Command Center

A new ClawPort-free, Hermes-native static dashboard for Stratos AI.

## Run locally

```bash
cd /Users/bradleydipaolo/stratos-ai/hermes-command-center
python3 -m http.server 8790
```

Open: http://localhost:8790

## Modules, in descending importance

0. Strategy OS
1. Boca Lead War Room
2. Hyper-Specific Demo Sites
3. One-Click Outreach Packs
4. Audit → Demo → Pitch Workflow
5. MedSpa Domination Pack
6. Revenue Forecast Simulator
7. Morning Briefing
8. Proof Vault
9. Public Portfolio Page
10. Client Close Room
11. Usage Saver

## Data

- `data/leads.json`: seeded real Boca-area leads from the blueprint.
- `data/automations.json`: Stratos automation catalog.

## Design posture

Modeled after the useful parts of ClawPort — command-center density, sidebar navigation, modular pages — but not dependent on ClawPort/OpenClaw code, packages, or gateway assumptions.


## Zero-model commands

These run locally and do not spend Codex quota:

```bash
python3 scripts/generate_demo_pages.py
python3 scripts/build_pitch_kits.py
python3 scripts/validate_dashboard.py
python3 scripts/free_port_server.py --start 8790
python3 scripts/ollama_health.py
python3 scripts/ollama_draft.py --lead glamor-medical --mode all
```

## Usage Saver policy

Codex/GPT-5.5 is reserved for architecture, hard debugging, high-taste UI/product direction, and final review. Repeated demo generation, pitch kits, local validation, and server port selection should run through scripts first.

## Ollama local AI commands

These use local Ollama and do not spend Codex quota:

```bash
python3 scripts/ollama_health.py
python3 scripts/ollama_draft.py --lead glamor-medical --mode all
python3 scripts/ollama_draft.py --lead all --mode all
```

Outputs are saved in `local-ai-drafts/`. See `OLLAMA_LOCAL_WORKFLOW.md`.

## Hermes local profile

A separate local Hermes profile is configured for Ollama:

```bash
hermes -p stratos-local chat -t terminal,file -q "Draft three Stratos outreach variants for Glamor Medical and save them under local-ai-drafts/."
```

Use this for local/cheap drafts and summaries. Keep the default Codex profile for premium architecture, hard debugging, and final review. See `HERMES_LOCAL_PROFILE.md`.


## Full integrated rebuild

Run the entire zero-model build/test pipeline:

```bash
python3 scripts/run_all.py
```

This regenerates:

- `demos/*.html`
- `pitch-kits/*.md`
- `close-rooms/*.html`
- `public-site/index.html`
- `briefings/latest.md`
- `dist/stratos-site-manifest.json`

## Integrated strategy docs

- `STRATOS_OPERATING_SYSTEM.md` — the agency operating system.
- `STRATOS_RUNBOOK.md` — daily commands and operator workflow.
- `DEPLOYMENT_CHECKLIST.md` — static/Vercel deployment checklist.

## Main URLs after serving locally

- Command Center: `http://localhost:8790`
- Strategy OS: `http://localhost:8790/#strategy`
- Usage Saver: `http://localhost:8790/#usage`
- Public site: `http://localhost:8790/public-site/index.html`
- Example close room: `http://localhost:8790/close-rooms/glamor-medical.html`


## Vercel output directory fix

Vercel should use:

- Build command: `python3 scripts/run_all.py`
- Output directory: `public`

The build command runs `scripts/export_vercel_public.py`, which creates `public/` with the command center, data, demos, public site, close rooms, briefings, and deploy manifest.

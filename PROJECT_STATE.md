# Stratos AI Command Center — Project State

Current app: Hermes-native static dashboard at `/Users/bradleydipaolo/stratos-ai/hermes-command-center`.

## Current modules
- Boca Lead War Room
- Hyper-Specific Demo Sites
- One-Click Outreach Packs
- Audit → Demo → Pitch
- MedSpa Domination Pack
- Revenue Forecast Simulator
- Morning Briefing
- Proof Vault
- Public Portfolio Page
- Client Close Room
- Usage Saver

## Data
- `data/leads.json`: seeded Boca-area leads. Static, not yet live-scraped.
- `data/automations.json`: Stratos automation catalog.

## Zero-model scripts
- `scripts/generate_demo_pages.py` — rebuild all demo pages from `data/leads.json`.
- `scripts/build_pitch_kits.py` — generate Markdown outreach kits in `pitch-kits/`.
- `scripts/validate_dashboard.py` — deterministic validation.
- `scripts/free_port_server.py --start 8790` — run local static server on first free port.

## Usage policy
Use scripts for repeatable generation and validation. Reserve Codex/GPT-5.5 for architecture, complex debugging, and final review.

## Local Ollama
- Ollama is running on `127.0.0.1:11434` on Bradley's machine.
- Installed models during implementation: `qwen3.5:9b`, `qwen2.5-coder:7b`.
- Use `scripts/ollama_health.py` and `scripts/ollama_draft.py` for local cheap drafting without Codex quota.

## Hermes local profile
- Profile `stratos-local` exists and is configured for Ollama via `ollama-local` provider at `http://127.0.0.1:11434/v1`.
- Default model for that profile: `qwen3.5:9b`; coder model available via `-m qwen2.5-coder:7b`.
- Verified command: `hermes -p stratos-local chat -Q -t terminal,file --max-turns 3 -q 'Reply with exactly: STRATOS LOCAL ONLINE'`.
- Default Hermes profile remains Codex/GPT-5.5 for premium review.

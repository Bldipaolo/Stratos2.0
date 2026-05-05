# Stratos AI Operating System

This is the blueprint for running Stratos as a local-business AI agency from one Hermes-native hub.

## Core thesis

Stratos sells premium websites plus AI automations to Boca Raton local businesses. The product is not a website alone; it is a lead-capture operating system: audit, demo, pitch, close room, launch, proof, and ongoing automation.

## Default workflow

1. **Absorb** — collect lead facts, site observations, offer fit, and proof assets.
2. **Improve** — turn raw lead data into stronger demo pages, pitch kits, close rooms, and public positioning.
3. **Integrate** — keep every asset wired into the Command Center instead of creating standalone silos.
4. **Test** — run deterministic validators before spending premium-model calls.
5. **Ship** — prepare static/Vercel-friendly assets and send one specific pitch at a time.

## Operating lanes

- **Command Center:** `index.html`, `app.js`, `styles.css`.
- **Public website:** `public-site/index.html`.
- **Demo websites:** `demos/*.html`.
- **Private close rooms:** `close-rooms/*.html`.
- **Pitch kits:** `pitch-kits/*.md`.
- **Briefings:** `briefings/latest.md`.
- **Deploy prep:** `dist/stratos-site-manifest.json`.
- **Local AI drafts:** `local-ai-drafts/*.md`.

## Usage policy

- Tier 0: zero-model scripts for generation, validation, deploy prep, and local serving.
- Tier 1: local Ollama / `stratos-local` for rough drafts, lead summaries, and content variants.
- Tier 2: default Codex/GPT profile only for architecture, hard debugging, high-taste review, and final decisions.

## Money path

The command center should always bias toward actions that can create sales conversations:

1. Work top lead.
2. Open demo and close room.
3. Send tailored pitch kit.
4. Log response manually until CRM integration exists.
5. Convert response into proposal, proof, and next asset.

## Current caveats

- Lead data is static/semi-real-looking and not live-scraped yet.
- Outreach sending, CRM persistence, email, calendar, and payment are not connected yet.
- Public site is static and ready for Vercel-style hosting, but no remote deployment was performed in this run.

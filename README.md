# Stratos AI Hermes Command Center

A new ClawPort-free, Hermes-native static dashboard for Stratos AI.

## Run locally

```bash
cd /Users/bradleydipaolo/stratos-ai/hermes-command-center
python3 -m http.server 8787
```

Open: http://localhost:8787

## Modules, in descending importance

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

## Data

- `data/leads.json`: seeded real Boca-area leads from the blueprint.
- `data/automations.json`: Stratos automation catalog.

## Design posture

Modeled after the useful parts of ClawPort — command-center density, sidebar navigation, modular pages — but not dependent on ClawPort/OpenClaw code, packages, or gateway assumptions.

# Endless-Feeling Hermes / Codex Usage Strategy

Goal: make Stratos work feel effectively endless without burning premium Codex quota on low-value loops.

## The core idea
Use Codex/GPT-5.5 only as the executive architect and final reviewer. Move bulk execution, repeated edits, file generation, scraping, formatting, tests, and static builds into deterministic scripts, local tooling, cheap models, cron jobs, or smaller scoped sessions.

## Tiers

### Tier 0 — No model calls
Use for anything deterministic.
- File generation from templates
- Bulk JSON/CSV transforms
- Repeated find/replace
- Running tests/builds
- Starting local servers
- Screenshot/console verification
- Lead scoring from already-collected data

Implementation: Python scripts, npm scripts, Makefile commands, static JSON data, reusable templates.

### Tier 1 — Cheap/fast model
Use for drafting, classification, summarization, extraction, lead blurbs, first-pass outreach, and bulk content.
Potential providers: OpenRouter cheap models, Gemini Flash, DeepSeek, local Ollama models.

### Tier 2 — Premium Codex/GPT-5.5
Use only for:
- Architecture decisions
- Complex debugging
- Final code review
- High-taste UI direction
- Multi-file refactors
- Strategy decisions

## Workflow rules

1. Batch big asks into one explicit spec.
2. Do not ask the premium model to inspect huge folders repeatedly.
3. Maintain project state in short files: README, STRATEGY, TODO, DATA_SCHEMA, CHANGELOG.
4. Prefer static/Vercel-friendly builds first, then add backend only when needed.
5. Use scripts to generate repeated assets instead of asking the model to hand-write each file.
6. Verify with deterministic checks before asking the model to reason.
7. Keep browser verification to one smoke pass unless UI broke.
8. Use Hermes skills/memory so we do not re-explain the same constraints.
9. Use `/new` or separate sessions for unrelated work to avoid dragging old context.
10. Use lower toolsets for cheap sessions: file+terminal only, no browser/web unless needed.

## Commands to consider

### Create a cheap profile later
When an API key is available, create a profile for low-cost work:

```bash
hermes profile create stratos-cheap --clone
hermes profile use stratos-cheap
hermes model
```

Pick a cheaper provider/model for drafts and bulk work.

### Keep premium profile for architecture/review

```bash
hermes profile create stratos-premium --clone
```

Use premium only for hard tasks.

### Restrict tools for cheap runs

```bash
hermes chat -q "Do the deterministic task..." --toolsets terminal,file
```

### Use scripts before model calls
Put repeatable operations into scripts under:

```text
/Users/bradleydipaolo/stratos-ai/scripts/
```

Examples:
- generate_demo_pages.py
- score_leads.py
- build_pitch_kits.py
- validate_dashboard.py
- export_vercel_static.py

## Stratos-specific endless loop

1. Lead scan script populates `data/leads.json`.
2. Lead scoring script computes scores and suggested offers.
3. Template script generates demo pages and pitch packs.
4. Hermes/Codex reviews only the top 3 outputs.
5. Browser smoke test checks only homepage + one demo + one close room.
6. Commit and deploy.

This makes one premium turn produce many assets.

## Immediate next build
Create a Stratos control panel called "Usage Saver" with:
- Task mode selector: Free Script / Cheap Draft / Premium Review
- Estimated quota burn before running
- Buttons to generate leads, demos, pitches, and snapshots locally
- A running log of which steps used model calls vs zero-model scripts

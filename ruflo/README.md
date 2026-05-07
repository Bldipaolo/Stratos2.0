# Ruflo Integration for Stratos AI

Ruflo source repo cloned locally at:

`/Users/bradleydipaolo/stratos-ai/external/ruflo`

Upstream: `https://github.com/ruvnet/ruflo.git`  
Current head: `addb5cd3f fix(release): hotfix 3.7.0-alpha.11 — strip workspace: protocol leak (#1825) (#1827)`

## How Stratos uses Ruflo

Ruflo is integrated as the **day-to-day orchestration ledger** for Stratos, not as a replacement for Hermes/Codex execution.

- Ruflo coordinates swarms, agents, tasks, hooks, and memory.
- Hermes/Codex still writes files, runs scripts, validates, commits, and pushes.
- Every Ruflo routine should end in actual Stratos actions: CRM movement, demo build, n8n workflow, proof update, validation, or deployment prep.

## Daily commands

```bash
python3 scripts/ruflo_status.py
python3 scripts/ruflo_daily.py morning
python3 scripts/ruflo_daily.py build --objective "build the next Stratos growth asset"
python3 scripts/ruflo_daily.py qa --objective "validate Stratos command center export"
python3 scripts/ruflo_daily.py close --note "validated and shipped Stratos update"
```

## Safety rule

Do not wait for Ruflo to do the work. Treat it as coordination + memory. After a Ruflo command, immediately execute the actual Stratos task and validate it with:

```bash
python3 scripts/run_all.py
```

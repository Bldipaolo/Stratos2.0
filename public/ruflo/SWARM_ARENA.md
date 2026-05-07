# Ruflo Swarm Arena

A crazy Stratos experiment: an interactive agency war-game layer where Ruflo creates coordination records for a specialized swarm and Hermes/Codex does the actual work.

## Commands

```bash
python3 scripts/ruflo_arena.py deck
python3 scripts/ruflo_arena.py mission --mode ambush --objective "48-hour Boca medspa revenue ambush"
python3 scripts/ruflo_arena.py mission --mode ambush --objective "48-hour Boca medspa revenue ambush" --run-ruflo
```

## Truth label

The browser arena is deterministic/interactive. Ruflo coordination becomes real when the script is run with `--run-ruflo`. Implementation is only real after files, validators, browser checks, git commit, and push exist.

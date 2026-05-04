# Hermes Stratos Local Profile

A separate Hermes profile named `stratos-local` is configured for local Ollama use. It does not change the default Codex profile.

## Profile

- Name: `stratos-local`
- Provider: `ollama-local`
- Base URL: `http://127.0.0.1:11434/v1`
- Default model: `qwen3.5:9b`
- Secondary local model available: `qwen2.5-coder:7b`
- Hermes config path: `/Users/bradleydipaolo/.hermes/profiles/stratos-local/config.yaml`

## Verified command

```bash
hermes -p stratos-local chat -Q -t terminal,file --max-turns 3 -q 'Reply with exactly: STRATOS LOCAL ONLINE'
```

Verified output:

```text
STRATOS LOCAL ONLINE
```

## Use it for cheap/local Stratos work

```bash
hermes -p stratos-local chat -t terminal,file -q "Using the Stratos project at /Users/bradleydipaolo/stratos-ai/hermes-command-center, draft three outreach variants for the top medspa lead. Save output to local-ai-drafts/."
```

## Use coder model for local coding help

```bash
hermes -p stratos-local chat --provider ollama-local -m qwen2.5-coder:7b -t terminal,file -q "Review app.js for simple bugs and summarize only. Do not edit files."
```

## Rules

- Use `stratos-local` for drafts, summaries, copy variants, light file analysis, and low-risk local work.
- Keep default Hermes/Codex for premium architecture, hard debugging, final code review, and major refactors.
- Prefer `-t terminal,file` to avoid loading unnecessary tool overhead.
- Start new local sessions for unrelated work to keep context small.

## Important implementation note

Hermes requires a 64K context declaration. The local profile sets `context_length: 65536` as an override even though the local Ollama model metadata reports a smaller native window. Keep local prompts focused and avoid dumping huge files into this profile.

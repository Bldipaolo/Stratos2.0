# GitHub Repo Setup — Stratos2.0

Target repo name:

```text
Stratos2.0
```

Expected GitHub URL:

```text
https://github.com/Bldipaolo/Stratos2.0
```

## One-time auth

The local `gh` CLI is installed but not currently logged in. Run:

```bash
gh auth login
```

Choose:

- GitHub.com
- HTTPS
- Authenticate with browser
- Set up Git credentials: yes

## Create and push

After login:

```bash
cd /Users/bradleydipaolo/stratos-ai/hermes-command-center
gh repo create Stratos2.0 --public --source . --push
```

If the repo already exists:

```bash
cd /Users/bradleydipaolo/stratos-ai/hermes-command-center
git push -u origin main
```

## Vercel import

Import this GitHub repo into Vercel:

```text
Bldipaolo/Stratos2.0
```

Settings:

- Framework: Other
- Root directory: project root
- Build command: `python3 scripts/run_all.py`
- Output directory: leave blank / project root

## Public URLs after Vercel deploy

If Vercel gives:

```text
https://stratos2-0.vercel.app
```

Then:

- Command Center: `https://stratos2-0.vercel.app/`
- Strategy OS: `https://stratos2-0.vercel.app/#strategy`
- Usage Saver: `https://stratos2-0.vercel.app/#usage`
- Public site: `https://stratos2-0.vercel.app/public-site/`
- Demo example: `https://stratos2-0.vercel.app/demos/glamor-medical.html`
- Close room example: `https://stratos2-0.vercel.app/close-rooms/glamor-medical.html`

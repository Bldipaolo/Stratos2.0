# Deployment Checklist

## Current deployment shape

The Stratos command center is static and can be hosted on Vercel or any static web host.

## Pre-deploy commands

```bash
cd /Users/bradleydipaolo/stratos-ai/hermes-command-center
python3 scripts/run_all.py
```

Confirm these pass:

```bash
python3 scripts/validate_dashboard.py
node test-dashboard.js
```

## Entry points

- Operator command center: `index.html`
- Public Stratos site: `public-site/index.html`
- Demo pages: `demos/*.html`
- Client close rooms: `close-rooms/*.html`

## Files to include

Include these folders/files:

- `index.html`
- `app.js`
- `styles.css`
- `data/`
- `demos/`
- `public-site/`
- `close-rooms/`
- `pitch-kits/`
- `briefings/`
- `dist/stratos-site-manifest.json`
- docs as desired

Scripts are useful locally but not required at runtime on static hosting.

## Do not deploy as production secrets

No API keys, PATs, OAuth tokens, `.env` files, or Hermes profile secrets should be deployed.

## Vercel note

Because this is static HTML/CSS/JS, it can deploy without a framework. If setting up Vercel manually, point the project root to:

```text
/Users/bradleydipaolo/stratos-ai/hermes-command-center
```

Build command can be empty, or if a local prebuild is desired:

```bash
python3 scripts/run_all.py
```

Output directory can be the project root for static hosting.

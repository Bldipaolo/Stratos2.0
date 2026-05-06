# Stratos Higgsfield Creative Studio

Status from latest local check: Higgsfield CLI is installed and authenticated, but the account is currently on the free plan with **0 credits**. That means I cannot honestly generate new Higgsfield images/videos right now. This file is the ready-to-run studio plan for when credits are available.

## Quality rules

1. Use Higgsfield for premium source imagery/video, not final Stratos typography.
2. Composite Stratos logo, headlines, CTAs, and captions locally after generation.
3. Inspect every generated result before publishing.
4. Reject warped text, fake UI labels, malformed objects, repeated blobs, and tiny unreadable copy.
5. Prefer 4 excellent assets over 40 mediocre templates.

## Bootstrap

```bash
command -v higgsfield
higgsfield account status
higgsfield model list --json > /tmp/stratos_higgs_models.json
```

If auth expires:

```bash
higgsfield auth login
```

## Campaign 1 — Medspa AI Consult Concierge key art

Purpose: reusable hero/background for medspa close rooms, Instagram, and public site.

```bash
higgsfield generate create gpt_image_2 \
  --prompt "Premium editorial ad key art for Stratos AI, boutique medspa front desk after hours, elegant dark forest-green and warm-white palette, a phone showing a consult request routed into an AI concierge workflow, cinematic lighting, realistic luxury clinic details, no fake logos, no readable tiny text, high-end agency aesthetic, space for headline overlay." \
  --aspect_ratio 9:16 \
  --resolution 2k \
  --wait \
  --wait-timeout 20m \
  --json > creative/higgsfield/jobs/medspa-consult-concierge.json
```

## Campaign 2 — Disconnected systems brand visual

Purpose: flagship Stratos “tools should talk to each other” brand ad.

```bash
higgsfield generate create gpt_image_2 \
  --prompt "Premium B2B operations visual for Stratos AI: fragmented local business tools represented as separate dark glass panels slowly connecting into one clean command flow, forest green signal lines, black and off-white palette, no clutter, no fake brand marks, dramatic but minimal, room for typography overlay." \
  --aspect_ratio 1:1 \
  --resolution 2k \
  --wait \
  --wait-timeout 20m \
  --json > creative/higgsfield/jobs/disconnected-systems.json
```

## Campaign 3 — UGC founder pitch video

Purpose: vertical Reel/TikTok/Story ad for Stratos itself.

```bash
higgsfield generate create marketing_studio_video \
  --prompt "A confident young agency founder explains that most local businesses do not need another generic website; they need their website, missed calls, forms, and follow-up connected into one revenue system. Premium but natural, direct-to-camera, Boca Raton local-business context, clear CTA: DM 'front desk' for a quick audit." \
  --mode ugc \
  --duration 15 \
  --resolution 720p \
  --aspect_ratio 9:16 \
  --generate-audio true \
  --wait \
  --wait-timeout 30m \
  --json > creative/higgsfield/jobs/ugc-founder-pitch.json
```

## Campaign 4 — TV spot: website is the front desk

Purpose: polished ad concept for public site and pitch material.

```bash
higgsfield generate create marketing_studio_video \
  --prompt "Polished commercial for Stratos AI showing a local business losing after-hours leads, then switching to a premium website plus AI intake and follow-up system. Modern forest-green/black/white brand mood, serious, high-trust, no hype, end with: Your website should act like your best operator." \
  --mode tv_spot \
  --duration 15 \
  --resolution 720p \
  --aspect_ratio 9:16 \
  --generate-audio true \
  --wait \
  --wait-timeout 30m \
  --json > creative/higgsfield/jobs/tv-spot-front-desk.json
```

## Download pattern

After a job completes, inspect JSON for result URLs and download with names like:

```bash
mkdir -p creative/higgsfield/source creative/higgsfield/final creative/higgsfield/jobs
python3 scripts/creative/download_higgsfield_results.py creative/higgsfield/jobs/medspa-consult-concierge.json creative/higgsfield/source/
```

## QA checklist

- brand spelling exact if any generated text appears
- no warped logo/text in source image
- no fake dashboards where details are meant to be read
- strong phone readability after local overlay
- consistent Stratos green/black/white system
- final asset exported with manifest entry

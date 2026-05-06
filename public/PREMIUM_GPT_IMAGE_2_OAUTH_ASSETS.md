# Stratos Premium GPT Image 2 OAuth Asset Upgrade

Generated on 2026-05-06 through the Hermes `openai-codex` image generation provider, using ChatGPT/Codex OAuth rather than a paid OpenAI Images API key.

## Status

- Provider: `openai-codex`
- Model tier used: `gpt-image-2-medium`
- Successful medium renders: 3
- Blocker encountered: 4th medium render returned `usage_limit_reached` on the Plus/Codex account.
- Integration: source images and locally-composited HTML creative gallery are committed into the repo and exported to `public/`.

## Why this is better than the prior Higgsfield-only plan

The previous creative studio was honest but blocked: Higgsfield was authenticated with 0 credits. The OAuth route gives Stratos direct GPT Image 2 creative production without adding a paid OpenAI API key. The new standard is:

1. Generate source/key art through GPT Image 2 OAuth.
2. Avoid final generated text/logos inside the image.
3. Composite Stratos logo, headlines, CTAs, and claims locally for exact spelling and layout control.
4. Use generated assets as proof of premium visual direction, not as fake client results.
5. Keep every usage-limit/cost caveat visible.

## Assets shipped

### 1. Command Room Hero

- Source: `marketing-assets/gpt-image-2-oauth/source/command-room-hero.png`
- Gallery: `marketing-assets/gpt-image-2-oauth/index.html`
- Best use: public website hero, Command Intelligence page, pitch deck opener, LinkedIn banner.
- Overlay headline: “Your website should act like your best operator.”

### 2. Medspa Concierge

- Source: `marketing-assets/gpt-image-2-oauth/source/medspa-concierge-portrait.png`
- Best use: medspa wedge campaign, Instagram story/Reel cover, medspa close rooms.
- Overlay headline: “Consult intent should not wait until morning.”

### 3. Disconnected Systems

- Source: `marketing-assets/gpt-image-2-oauth/source/disconnected-systems-square.png`
- Best use: flagship brand ad, carousel opener, “why Stratos” section.
- Overlay headline: “Disconnected tools leak revenue.”

### 4. Outcome Discipline derivative

- Uses the Command Room source as a second local composition.
- Best use: proof/retainer positioning.
- Overlay headline: “Less dashboard. More booked action.”

## QA notes

Vision QA was attempted, but the same Plus/Codex usage limit also blocked image-analysis calls immediately after generation. To keep shipping moving, the publishable layer was designed defensively:

- generated assets are used as background/key art only;
- all readable Stratos text is local HTML/CSS;
- no generated client claims are made;
- the gallery notes the successful renders and usage-limit blocker;
- the next pass should perform visual QA after the reset before expanding the pack.

## Next generation queue after reset

1. Legal urgent-intake command room, portrait.
2. Home-service emergency job recovery visual, portrait.
3. Founder/UGC-style still frame for Stratos personal-brand ads.
4. Dental new-patient capture key art.
5. Dedicated 16:9 public-site hero with more negative space on the left.

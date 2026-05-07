# Stratos × Ruflo Day-to-Day Process

## 1. Morning

1. Run `python3 scripts/ruflo_daily.py morning`.
2. Open Command Center `#today`, `#war`, and `#crm`.
3. Pick one money task: outreach, demo, proof, automation, or close room.
4. Search memory/patterns before starting.

## 2. Build block

1. Run `python3 scripts/ruflo_daily.py build --objective "..."`.
2. Hermes/Codex executes the real work.
3. Keep outputs inside the Command Center system: data, scripts, docs, public export, validation.

## 3. QA block

1. Run `python3 scripts/ruflo_daily.py qa --objective "..."`.
2. Run `node --check app.js`, `node test-dashboard.js`, `python3 scripts/validate_dashboard.py`, and `python3 scripts/run_all.py`.
3. Browser-check at least one operational route and one public/demo route.

## 4. Closeout

1. Run `python3 scripts/ruflo_daily.py close --note "what shipped"`.
2. Move CRM statuses if real outreach happened.
3. Update proof vault only with transparent labels.
4. Commit and push after validation.

## Important

Ruflo coordinates. Hermes/Codex executes. Never claim Ruflo completed implementation unless files/tests/browser proof show it.

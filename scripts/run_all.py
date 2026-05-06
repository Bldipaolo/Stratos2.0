#!/usr/bin/env python3
"""Run the full zero-model Stratos build pipeline."""
from pathlib import Path
import subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
steps=[
    ['Generate demo pages', ['python3','scripts/generate_demo_pages.py']],
    ['Generate premium vertical demo sites', ['python3','scripts/generate_vertical_demo_sites.py']],
    ['Build pitch kits', ['python3','scripts/build_pitch_kits.py']],
    ['Generate close rooms', ['python3','scripts/generate_close_rooms.py']],
    ['Build public website', ['python3','scripts/build_public_site.py']],
    ['Generate morning briefing', ['python3','scripts/generate_morning_briefing.py']],
    ['Prepare deploy manifest', ['python3','scripts/deploy_prep.py']],
    ['Export Vercel public directory', ['python3','scripts/export_vercel_public.py']],
    ['Validate dashboard', ['python3','scripts/validate_dashboard.py']],
]
for label, cmd in steps:
    print(f"\n==> {label}")
    proc=subprocess.run(cmd, cwd=ROOT, text=True)
    if proc.returncode:
        print(f"FAILED: {label}", file=sys.stderr)
        sys.exit(proc.returncode)
print("\nSTRATOS FULL PIPELINE PASSED")

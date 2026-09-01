"""Regenerates every referral print asset from refer/config.json.

Run this after editing the bonus amounts or payout timing in refer/config.json,
or after changing any of the gen_*.py scripts.
"""
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent

for script in ["gen_qr.py", "gen_dashboard_sticker.py", "gen_poster.py", "gen_wallet_card.py"]:
    print(f"--- {script} ---")
    subprocess.run([sys.executable, str(SCRIPTS_DIR / script)], check=True)

print("\nAll print assets regenerated in print-assets/")

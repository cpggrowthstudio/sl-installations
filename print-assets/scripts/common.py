import json
import os

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(SCRIPTS_DIR))
FONTS_DIR = os.path.join(SCRIPTS_DIR, "fonts")
OUTPUT_DIR = os.path.join(REPO_ROOT, "print-assets")
LOGO_PATH = os.path.join(REPO_ROOT, "logo-horizontal.png")
CONFIG_PATH = os.path.join(REPO_ROOT, "refer", "config.json")

URL = "https://slinstallations.ca/refer"

RED = (0xD1 / 255, 0x00 / 255, 0x00 / 255)
BLACK = (0x0D / 255, 0x0D / 255, 0x0D / 255)
WHITE = (1, 1, 1)


def load_config():
    """Reads refer/config.json (the same file the live web page fetches) so every
    print asset always shows the same bonus amounts and payout timing as the site."""
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    cfg["bonusLine"] = "{startAmount} {startTiming}. {milestoneAmount} {milestoneTiming}.".format(**cfg)
    return cfg

# Referral print asset generator

Regenerates `qr-code.png`, `dashboard-sticker.svg`, `warehouse-poster.pdf`, and
`wallet-card.pdf` in the parent `print-assets/` folder from a single config file.

## To change the bonus amount or payout timing

1. Edit `refer/config.json` at the repo root. This same file is also read live
   by `refer/index.html`, so editing it updates the website immediately after
   you push, with no other changes needed.
2. Run the generator (see below) to rebuild the print assets so they match.
3. Reprint anything you already handed out.

## Running it

```
cd print-assets/scripts
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 generate_all.py
```

Fonts (Bebas Neue, Barlow) are bundled in `fonts/` so this works offline.

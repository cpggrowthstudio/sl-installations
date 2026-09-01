import base64

from common import FONTS_DIR, LOGO_PATH, OUTPUT_DIR, URL, load_config
from qr_matrix import get_qr_matrix, qr_svg_group

cfg = load_config()

with open(LOGO_PATH, "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode()
with open(f"{FONTS_DIR}/bebasneue.ttf", "rb") as f:
    bebas_b64 = base64.b64encode(f.read()).decode()
with open(f"{FONTS_DIR}/barlow-semibold.ttf", "rb") as f:
    barlow_b64 = base64.b64encode(f.read()).decode()
with open(f"{FONTS_DIR}/barlow-bold.ttf", "rb") as f:
    barlow_bold_b64 = base64.b64encode(f.read()).decode()

matrix = get_qr_matrix()

# Sized for an interior sticker (dashboard, visor, glovebox lid), read up close
# rather than a large exterior decal.
W, H = 4, 5  # inches

logo_w = 2.3
logo_h = logo_w * (360 / 1200)
logo_x = (W - logo_w) / 2
logo_y = 0.25  # logo spans 0.25 -> 0.94

qr_size = 1.85
qr_x = (W - qr_size) / 2
qr_y = 2.6  # QR spans 2.6 -> 4.45

qr_group = qr_svg_group(matrix, qr_x, qr_y, qr_size, dark="#0d0d0d", light="#ffffff", quiet_modules=3)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}in" height="{H}in" viewBox="0 0 {W} {H}">
  <defs>
    <style>
      @font-face {{
        font-family:"Bebas Neue";
        src:url(data:font/ttf;base64,{bebas_b64}) format("truetype");
      }}
      @font-face {{
        font-family:"Barlow SemiBold";
        src:url(data:font/ttf;base64,{barlow_b64}) format("truetype");
      }}
      @font-face {{
        font-family:"Barlow Bold";
        src:url(data:font/ttf;base64,{barlow_bold_b64}) format("truetype");
      }}
      .headline {{ font-family:"Bebas Neue","Arial Narrow",Arial,sans-serif; }}
      .body {{ font-family:"Barlow SemiBold","Barlow",Arial,sans-serif; }}
      .bold {{ font-family:"Barlow Bold","Barlow",Arial,sans-serif; }}
    </style>
  </defs>

  <rect x="0" y="0" width="{W}" height="{H}" fill="#0d0d0d"/>

  <image href="data:image/png;base64,{logo_b64}" x="{logo_x}" y="{logo_y}" width="{logo_w}" height="{logo_h}"/>

  <text x="{W/2}" y="1.28" class="headline" font-size="0.42" fill="#ffffff" text-anchor="middle" letter-spacing="0.01">KNOW SOMEONE</text>
  <text x="{W/2}" y="1.73" class="headline" font-size="0.42" fill="#D10000" text-anchor="middle" letter-spacing="0.01">GOOD?</text>

  <text x="{W/2}" y="2.05" class="body" font-size="0.15" fill="#ffffff" text-anchor="middle">Refer an installer. Get paid.</text>

  <rect x="{W/2 - 0.3}" y="2.24" width="0.6" height="0.02" fill="#D10000"/>

  <text x="{W/2}" y="2.42" class="bold" font-size="0.155" fill="#D10000" text-anchor="middle">{cfg['bonusLine']}</text>

  <g>
    {qr_group}
  </g>

  <text x="{W/2}" y="4.73" class="headline" font-size="0.19" fill="#ffffff" text-anchor="middle" letter-spacing="0.02">SLINSTALLATIONS.CA/REFER</text>
</svg>
'''

out_path = f"{OUTPUT_DIR}/dashboard-sticker.svg"
with open(out_path, "w") as f:
    f.write(svg)
print("wrote", out_path, "encodes:", URL, "| bonus:", cfg["bonusLine"])

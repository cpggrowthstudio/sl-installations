from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from common import FONTS_DIR, LOGO_PATH, OUTPUT_DIR, RED, BLACK, WHITE, URL, load_config
from qr_matrix import get_qr_matrix, draw_qr_pdf

pdfmetrics.registerFont(TTFont("BebasNeue", f"{FONTS_DIR}/bebasneue.ttf"))
pdfmetrics.registerFont(TTFont("Barlow", f"{FONTS_DIR}/barlow-regular.ttf"))
pdfmetrics.registerFont(TTFont("Barlow-SemiBold", f"{FONTS_DIR}/barlow-semibold.ttf"))
pdfmetrics.registerFont(TTFont("Barlow-Bold", f"{FONTS_DIR}/barlow-bold.ttf"))

cfg = load_config()


def centered_text(c, text, cx, y, font, size, color):
    c.setFont(font, size)
    c.setFillColorRGB(*color)
    w = pdfmetrics.stringWidth(text, font, size)
    c.drawString(cx - w / 2, y, text)


def crop_marks(c, trim_w, trim_h, mark_len=0.2 * inch, offset=0.125 * inch):
    """Marks at each trim-box corner, extending outward into the page margin.
    Caller must leave >= offset+mark_len of margin around the trim box."""
    c.setLineWidth(0.5)
    c.setStrokeColorRGB(0, 0, 0)
    corners = [(0, 0), (trim_w, 0), (0, trim_h), (trim_w, trim_h)]
    for cx, cy in corners:
        dx = -1 if cx == 0 else 1
        dy = -1 if cy == 0 else 1
        c.line(cx + dx * offset, cy, cx + dx * (offset + mark_len), cy)
        c.line(cx, cy + dy * offset, cx, cy + dy * (offset + mark_len))


TRIM_W, TRIM_H = 11 * inch, 17 * inch
BLEED = 0.125 * inch
MARGIN = 0.5 * inch  # room outside the trim box for crop marks
PAGE_W, PAGE_H = TRIM_W + 2 * MARGIN, TRIM_H + 2 * MARGIN
matrix = get_qr_matrix()

c = canvas.Canvas(f"{OUTPUT_DIR}/warehouse-poster.pdf", pagesize=(PAGE_W, PAGE_H))
c.translate(MARGIN, MARGIN)  # (0,0) is now the trim-box origin

W, H = TRIM_W, TRIM_H

c.setFillColorRGB(*BLACK)
c.rect(-BLEED, -BLEED, W + 2 * BLEED, H + 2 * BLEED, stroke=0, fill=1)

cx = W / 2

logo = ImageReader(LOGO_PATH)
logo_w = 6.5 * inch
logo_h = logo_w * (360 / 1200)
c.drawImage(logo, cx - logo_w / 2, H - 2.35 * inch, width=logo_w, height=logo_h, mask='auto')

centered_text(c, "KNOW SOMEONE", cx, H - 3.35 * inch, "BebasNeue", 1.15 * inch, WHITE)
centered_text(c, "GOOD?", cx, H - 4.55 * inch, "BebasNeue", 1.15 * inch, RED)

centered_text(c, "Refer an installer. Get paid.", cx, H - 5.35 * inch, "Barlow-SemiBold", 0.42 * inch, WHITE)

c.setFillColorRGB(*RED)
c.rect(cx - 0.9 * inch, H - 5.75 * inch, 1.8 * inch, 0.05 * inch, stroke=0, fill=1)

qr_size = 6.2 * inch
qr_x = cx - qr_size / 2
qr_y = H - 13.1 * inch
draw_qr_pdf(c, matrix, qr_x, qr_y, qr_size)

centered_text(c, "SLINSTALLATIONS.CA/REFER", cx, qr_y - 0.65 * inch, "BebasNeue", 0.55 * inch, WHITE)

bullet_y = qr_y - 1.65 * inch
bullets = [
    "Scan the code. That's the only step.",
    "We call your referral the same day. They don't apply, we call them.",
    cfg["bonusLine"],
]
c.setFillColorRGB(*RED)
bx = 1.3 * inch
for i, line in enumerate(bullets):
    by = bullet_y - i * 0.62 * inch
    c.circle(bx, by + 0.11 * inch, 0.05 * inch, stroke=0, fill=1)
    c.setFillColorRGB(*WHITE)
    c.setFont("Barlow-SemiBold", 0.3 * inch)
    c.drawString(bx + 0.25 * inch, by, line)
    c.setFillColorRGB(*RED)

crop_marks(c, W, H)
c.showPage()
c.save()
print("wrote warehouse-poster.pdf, QR encodes:", URL, "| bonus:", cfg["bonusLine"])

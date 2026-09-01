from reportlab.lib.pagesizes import letter
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
logo = ImageReader(LOGO_PATH)
matrix = get_qr_matrix()


def centered_text(c, text, cx, y, font, size, color):
    c.setFont(font, size)
    c.setFillColorRGB(*color)
    w = pdfmetrics.stringWidth(text, font, size)
    c.drawString(cx - w / 2, y, text)


CARD_W, CARD_H = 3.5 * inch, 2 * inch
COLS, ROWS = 2, 5  # 10-up on a letter sheet
GUTTER = 0.15 * inch

grid_w = COLS * CARD_W + (COLS - 1) * GUTTER
grid_h = ROWS * CARD_H + (ROWS - 1) * GUTTER
margin_x = (letter[0] - grid_w) / 2
margin_y = (letter[1] - grid_h) / 2


def draw_front(c, ox, oy):
    c.saveState()
    c.translate(ox, oy)
    c.setFillColorRGB(*BLACK)
    c.rect(0, 0, CARD_W, CARD_H, stroke=0, fill=1)
    c.setStrokeColorRGB(*RED)
    c.setLineWidth(1)
    c.rect(0.04 * inch, 0.04 * inch, CARD_W - 0.08 * inch, CARD_H - 0.08 * inch, stroke=1, fill=0)

    qr_size = 1.15 * inch
    qr_x = 0.22 * inch
    qr_y = CARD_H / 2 - qr_size / 2
    draw_qr_pdf(c, matrix, qr_x, qr_y, qr_size)

    tx = qr_x + qr_size + 0.22 * inch
    c.setFont("BebasNeue", 0.24 * inch)
    c.setFillColorRGB(*WHITE)
    c.drawString(tx, CARD_H - 0.5 * inch, "REFER AN")
    c.setFillColorRGB(*RED)
    c.drawString(tx, CARD_H - 0.74 * inch, "INSTALLER")
    c.setFont("Barlow-SemiBold", 0.11 * inch)
    c.setFillColorRGB(*WHITE)
    c.drawString(tx, CARD_H - 0.98 * inch, "Scan to send")
    c.drawString(tx, CARD_H - 1.12 * inch, "their name and number")
    c.setFont("BebasNeue", 0.13 * inch)
    c.drawString(tx, 0.22 * inch, "SLINSTALLATIONS.CA")

    c.restoreState()


def draw_back(c, ox, oy):
    c.saveState()
    c.translate(ox, oy)
    c.setFillColorRGB(*BLACK)
    c.rect(0, 0, CARD_W, CARD_H, stroke=0, fill=1)
    c.setStrokeColorRGB(*RED)
    c.setLineWidth(1)
    c.rect(0.04 * inch, 0.04 * inch, CARD_W - 0.08 * inch, CARD_H - 0.08 * inch, stroke=1, fill=0)

    logo_w = 1.7 * inch
    logo_h = logo_w * (360 / 1200)
    c.drawImage(logo, CARD_W / 2 - logo_w / 2, CARD_H - logo_h - 0.14 * inch, width=logo_w, height=logo_h, mask='auto')

    lines = [
        "1. Scan the code.",
        "2. We call your referral today.",
        "3. Get paid when they stick.",
    ]
    y = CARD_H - logo_h - 0.42 * inch
    for line in lines:
        c.setFont("Barlow-SemiBold", 0.115 * inch)
        c.setFillColorRGB(*WHITE)
        c.drawCentredString(CARD_W / 2, y, line)
        y -= 0.19 * inch

    c.setStrokeColorRGB(*RED)
    c.setLineWidth(0.75)
    c.line(CARD_W / 2 - 0.55 * inch, y - 0.04 * inch, CARD_W / 2 + 0.55 * inch, y - 0.04 * inch)
    y -= 0.24 * inch

    centered_text(c, cfg["bonusLine"], CARD_W / 2, y, "Barlow-Bold", 0.105 * inch, RED)

    c.restoreState()


def draw_sheet_page(c, draw_fn, label):
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.setFont("Barlow", 8)
    c.drawString(0.25 * inch, letter[1] - 0.35 * inch, f"SL Installations - Referral Wallet Cards - {label} (10-up, 3.5 x 2 in, cut on dotted lines)")
    for row in range(ROWS):
        for col in range(COLS):
            ox = margin_x + col * (CARD_W + GUTTER)
            oy = letter[1] - margin_y - (row + 1) * CARD_H - row * GUTTER
            draw_fn(c, ox, oy)
            c.setStrokeColorRGB(0.75, 0.75, 0.75)
            c.setLineWidth(0.4)
            c.setDash(2, 2)
            c.rect(ox, oy, CARD_W, CARD_H, stroke=1, fill=0)
            c.setDash()
    c.showPage()


c = canvas.Canvas(f"{OUTPUT_DIR}/wallet-card.pdf", pagesize=letter)
draw_sheet_page(c, draw_front, "FRONT")
draw_sheet_page(c, draw_back, "BACK")
c.save()
print("wrote wallet-card.pdf, QR encodes:", URL, "| bonus:", cfg["bonusLine"])

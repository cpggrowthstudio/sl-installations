import qrcode
from qrcode.constants import ERROR_CORRECT_H

from common import URL


def get_qr_matrix():
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, border=0)
    qr.add_data(URL)
    qr.make(fit=True)
    return qr.get_matrix()  # list of lists of bool, True = dark module


def qr_svg_group(matrix, x, y, size, dark="#000000", light=None, quiet_modules=4):
    """Returns SVG <rect> markup for a QR code, positioned in the SAME coordinate
    units as the parent viewBox (no "in"/"px" suffix on the numbers)."""
    n = len(matrix)
    total_modules = n + quiet_modules * 2
    module_size = size / total_modules
    parts = []
    if light:
        parts.append(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="{light}"/>')
    for r, row in enumerate(matrix):
        for c, dark_cell in enumerate(row):
            if not dark_cell:
                continue
            mx = x + (c + quiet_modules) * module_size
            my = y + (r + quiet_modules) * module_size
            parts.append(f'<rect x="{mx:.4f}" y="{my:.4f}" width="{module_size:.4f}" height="{module_size:.4f}" fill="{dark}"/>')
    return "\n".join(parts)


def draw_qr_pdf(c, matrix, x, y, size, dark=(0.05, 0.05, 0.05), light=(1, 1, 1), quiet_modules=3):
    """Draws a QR code directly on a ReportLab canvas as native vector rects
    (PDF y-axis is bottom-up, unlike SVG)."""
    n = len(matrix)
    total = n + quiet_modules * 2
    module = size / total
    c.setFillColorRGB(*light)
    c.rect(x, y, size, size, stroke=0, fill=1)
    c.setFillColorRGB(*dark)
    for r, row in enumerate(matrix):
        for col, dark_cell in enumerate(row):
            if not dark_cell:
                continue
            mx = x + (col + quiet_modules) * module
            my = y + size - (r + quiet_modules + 1) * module
            c.rect(mx, my, module, module, stroke=0, fill=1)

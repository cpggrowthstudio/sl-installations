import qrcode
from PIL import Image
from qrcode.constants import ERROR_CORRECT_H

from common import OUTPUT_DIR, URL

if __name__ == "__main__":
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    img = img.resize((2000, 2000), resample=Image.NEAREST)
    out = f"{OUTPUT_DIR}/qr-code.png"
    img.save(out)
    print("wrote", out, img.size, "encodes:", URL)

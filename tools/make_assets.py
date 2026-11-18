"""Regenerate the site's images from the app's source assets.

Run from the Website folder:  python tools/make_assets.py
Needs Pillow. Reads the source images in tools/source/ and writes to assets/img/.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent.parent
SRC = HERE / "tools" / "source"
ICON = SRC / "icon.png"
OUT = HERE / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)

NAVY, GREEN, BG = (36, 43, 51), (22, 163, 74), (255, 255, 255)  # text, accent, background: the app palette

icon = Image.open(ICON).convert("RGB")
icon.resize((512, 512), Image.LANCZOS).save(OUT / "icon-512.png", optimize=True)
icon.resize((180, 180), Image.LANCZOS).save(OUT / "apple-touch-icon.png", optimize=True)
icon.resize((192, 192), Image.LANCZOS).save(OUT / "icon-192.png", optimize=True)
icon.resize((32, 32), Image.LANCZOS).save(OUT / "favicon-32.png", optimize=True)
icon.resize((96, 96), Image.LANCZOS).save(OUT / "logo-96.webp", quality=90, method=6)

# Social preview 1200x630
W, H = 1200, 630
card = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(card)
d.rectangle([0, 0, 14, H], fill=GREEN)
logo = icon.resize((360, 360), Image.LANCZOS)
card.paste(logo, (90, 135))
def font(name, size):
    return ImageFont.truetype(f"C:/Windows/Fonts/{name}", size)
d.text((510, 170), "Yaaddi", font=font("segoeuib.ttf", 112), fill=NAVY)
d.text((514, 310), "Free learning app with", font=font("segoeui.ttf", 44), fill=(60, 60, 60))
d.text((514, 366), "ready-made courses", font=font("segoeui.ttf", 44), fill=(60, 60, 60))
d.text((514, 470), "No ads. No account. Works offline.", font=font("segoeuisb.ttf", 34) if Path("C:/Windows/Fonts/segoeuisb.ttf").exists() else font("segoeui.ttf", 34), fill=GREEN)
card.save(OUT / "og-image.png", optimize=True)

# Screenshots -> webp, 480 wide
for src, dst in [("library.png", "shot-library.webp"),
                 ("course-map.png", "shot-course-map.webp"),
                 ("question.png", "shot-question.webp")]:
    im = Image.open(SRC / src).convert("RGB")
    h = round(im.height * 480 / im.width)
    im.resize((480, h), Image.LANCZOS).save(OUT / dst, quality=82, method=6)
    print(dst, 480, h)
print("done")

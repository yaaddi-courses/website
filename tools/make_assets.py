"""Regenerate the site's images from the app's source assets.

Run from the Website folder:  python tools/make_assets.py
Needs Pillow. Reads the app icon and the screenshots listed below; writes to assets/img/.
Only the generated files are committed, so the site repo needs none of the sources.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent.parent
YAADDI = HERE.parent
ICON = YAADDI / "app" / "assets" / "icon.png"
SHOTS = Path("D:/MRM/ai/MKT/Posts/001-text-yaaddi-introduction/screenshots")
OUT = HERE / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)

NAVY, GREEN, BG = (13, 47, 127), (22, 163, 74), (250, 250, 247)

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
for src, dst in [("02-course-library.png", "shot-library.webp"),
                 ("04-course-map.png", "shot-course-map.webp"),
                 ("06-answer-feedback.png", "shot-question.webp")]:
    im = Image.open(SHOTS / src).convert("RGB")
    h = round(im.height * 480 / im.width)
    im.resize((480, h), Image.LANCZOS).save(OUT / dst, quality=82, method=6)
    print(dst, 480, h)
print("done")

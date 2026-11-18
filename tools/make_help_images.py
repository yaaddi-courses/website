"""Convert the help-page screenshots (tools/source/help/*.png) to 480-wide WebP in assets/img/help/.

Capture the PNGs first with tools/capture_help_shots.cjs. Run from the Website folder:
    python tools/make_help_images.py
"""
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent.parent
SRC = HERE / "tools" / "source" / "help"
OUT = HERE / "assets" / "img" / "help"
OUT.mkdir(parents=True, exist_ok=True)

for png in sorted(SRC.glob("*.png")):
    im = Image.open(png).convert("RGB")
    h = round(im.height * 480 / im.width)
    target = OUT / f"{png.stem}.webp"
    im.resize((480, h), Image.LANCZOS).save(target, quality=82, method=6)
    print(target.name, 480, h, f"{target.stat().st_size // 1024} KB")

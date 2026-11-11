#!/usr/bin/env python3
"""Apply Cinderfall v2 pixel art to Emerald tiles, keeping all map/collision data.

The repo asset is zlib-compressed 4-bit palette-index art for the 46 original
16x16 Cinderfall metatiles. This *only* updates their 184 hardware 8x8 images.
"""
from pathlib import Path
from PIL import Image
import base64, hashlib, sys, zlib

project = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
asset = Path(__file__).resolve().parents[1] / "assets/cinderfall_polished_metatile_pixels_v2.txt"
pixels = zlib.decompress(base64.b64decode(asset.read_text().strip(), validate=True))
assert len(pixels) == 46 * 4 * 64, len(pixels)
assert hashlib.sha256(pixels).hexdigest() == "9a4faa17b9df12926a2b28c0716cbcf23ba99107da5384c5c225c57fe964a352", "Pixel art data mismatch"

root = project / "data/tilesets/secondary/petalburg"
palette = [(0,0,0), (22,20,31), (46,41,50), (86,76,79),
           (127,108,99), (184,150,121), (65,43,45), (124,65,56),
           (208,85,47), (249,149,59), (255,215,109), (27,24,30),
           (88,97,113), (151,153,157), (178,151,82), (232,216,178)]
(root / "palettes/12.pal").write_text(
    "JASC-PAL\n0100\n16\n" + "".join(f"{r} {g} {b}\n" for r,g,b in palette),
    encoding="utf-8")

source = root / "tiles.png"
image = Image.open(source).convert("P")
assert image.width == 128 and image.height >= 176
assert (root / "metatiles.bin").stat().st_size > 144 * 16
for n in range(46 * 4):
    index = 160 + n
    x = index % 16 * 8
    y = index // 16 * 8
    tile = Image.frombytes("P", (8, 8), pixels[n*64:(n+1)*64])
    image.paste(tile,(x,y))
image.save(source)
print("Cinderfall v2 graphics: 46 enhanced 16x16 metatiles, no collision or warp changes")

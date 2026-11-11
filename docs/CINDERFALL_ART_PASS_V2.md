# Cinderfall Town — Pixel-Art Polish v2

**Status:** Source art pack committed and automatically applied in GitHub GBA builds. Emulator smoke test not yet completed for this v2 revision.

## Why v1 looked rough
It used 46 quickly generated 16×16 map metatiles: flat front-facing houses, little shading, repetitive road tiles, and uniform fire holes. Enlarging the native GBA image makes those shortcuts apparent.

## What changed in v2
- Original hand-authored, GBA-compatible 16-color indexed pixel-art pass for 46 metatiles (184 8×8 hardware graphics tiles)
- Pitched-looking roof edges, individual shingles, darker broken roof cavities and stronger eaves
- Staggered stone/brick work, shadows under rooftops and more detailed boarded windows
- Lit windows/clinic detail, differentiated slate relief center, weathered crimson/rust palette
- Less checkerboard-looking roads, improved rubble, scrap, banners, barrels, ground and flames
- Town layout, collisions, seven interior entrances, Rook event script and starter script preserved

**Asset:** `assets/cinderfall_polished_metatile_pixels_v2.txt` — zlib-compressed palette-index art (binary graphic data encoded as text for GitHub source control). 
**Integration:** `scripts/apply_cinderfall_polish_v2.py` applies the asset after town/layout/interior generation.
**Preview:** A complete map tile render was created, but map renders and sprites must be verified in the compiled ROM.

## Art direction limitations and next stage
A GBA game displays only 240×160 pixels at native resolution; a large 1300-pixel mockup will look more intricate than actual on-console gameplay. For quality closer to our original cinematic Cinderfall concept, we need a larger **hand-drawn modular tileset** with many more unique building silhouettes, front-facing facades, damaged roof variants, animated fire/smoke objects, terrain transitions, and custom NPC/character sprites. Merely upscaling sprites will not achieve that.

## Build
The GitHub workflow fetches pinned pokeemerald-expansion source, applies gameplay/story patches, generates the existing Cinderfall map and interiors, injects polished art, and builds a `.gba`. The compiled GBA must be tested independently in mGBA/Pizza Boy.

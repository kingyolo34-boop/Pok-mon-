# Cinderfall Town Alpha — actual GBA map (2026-11-10)

## Successful source build and emulator test
- **GitHub Actions (SUCCESS):** https://github.com/kingyolo34-boop/Pok-mon-/actions/runs/42948791988
- **ROM SHA-256:** `b70ec479af971ed15adeda6fd761a507d4d016011f617fccb1cb829d2bb3dc0b`
- ROM size: **33,554,432 bytes (32 MiB)**. GBA header `FALLEN ASHE`, game code `BPEE`, valid checksum.
- **mGBA runtime check:** ROM boots; the actual modified town renders with dark ground, burned roofs, fallen ash and Mom/truck introduction. This is no longer a story-only or text-only alpha.
- **Not yet fully playtested:** all door warps, four new landmark interactions, complete Rook scene, saves and late-game events.

## What's genuinely new
- **Cinderfall is a real 28 × 29 metatile town** (original Littleroot was 20 × 20).
- 46 new, original, GBA-compatible 16 × 16 metatiles, generated into the Petalburg secondary tileset; reserved palette slot 12 avoids modifying upstream building palettes.
- Seven recognizable sites: Mom's burned house, frightened family home, Cinderfall Relief Clinic, Supply Depot, Garrick's Shelter, Abandoned House, and Trade Post.
- Burned roofs with holes and fires, dry grass, cracked ash roads, charred stumps, scrap, sandbags, warning signs, crates, fences, and barricades.
- Original two house warps and relief lab warp deliberately preserved at (5,8), (14,8), (7,16).
- Four new exterior signs with lore dialogue; **these new houses have no interiors yet**.
- Updated visible-intro and Rook/chapter-one script are applied *before* the new map generator.
- Pathfinding source check verified streets reach the main northern exit and all building-front locations.

## How to play the build
Download the `Fallen-Ashe-GBA-Cinderfall-Town-Alpha` artifact from the successful Actions run. Extract the ZIP, rename `pokeemerald.gba` to `Pokemon_Fallen_Ashe_Cinderfall_Town_Alpha_v1.gba`, and open it in Pizza Boy A Pro or My Boy! using **New Game**. Continue past the still-placeholder Emerald moving-truck introduction. The first actual outdoor scene is now the real rebuilt Cinderfall map.

Please avoid loading old save states: map sizes and tileset IDs changed, so use a fresh save slot when testing.

## Limitations / what's next
- The moving truck, character designs and home interiors still include substantial original Emerald content.
- Rooftop fire is static map art for now, and art is simplified into authentic GBA-resolution tiles. Dynamic smoke and flame effects can be added later.
- Custom starter battle sprites, Rook/Dane overworld sprites and full prologue still need visual integration.
- Wren's 2× EXP Struggle-only Blissey farm remains tracked as issue #1.
- The protagonist eventually killing Rook remains locked narrative canon, **not yet in this compiled Chapter One**.

## Developer source
`scripts/apply_cinderfall_map.py` generates this map deterministically as a standalone source transformation. The complete readable generator and a Porymap-compatible asset overlay are available as attachments from the project development conversation. Do **not** commit copyrighted ROM images to this repository.

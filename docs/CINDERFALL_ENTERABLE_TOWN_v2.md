# Cinderfall Enterable Town v2 — Build milestone

**GitHub Actions:** https://github.com/kingyolo34-boop/Pok-mon-/actions/runs/42957307321
**Status:** SUCCESS — complete 32 MiB `.gba` compiled and cartridge checksum validated.
**SHA-256:** `5d9d19a55b13d83f5d2235d0c36e1539d25ce8eac3e3eabd68aca6e62b4c127a`

## What's in this build
- 28x29 Cinderfall town using original ash/cracked-road/fire/rubble/boarded-window GBA-compatible metatiles.
- Seven enterable buildings: two original homes, the relief-lab entrance, plus four NEW interior maps (Supply House, Garrick's Shelter, Abandoned House, Trade Depot).
- Two-way warp mapping for all seven; statically checked town path reachability including Route 101 northern exit.
- NPC dialogue and a real basic-item Pokémart in the Trade Depot.
- Existing Fallen Ashe Ashvale/Danes intro and coded Chapter One Rook scene carried forward.
- Starters use placeholder original Hoenn sprites in existing species slots.

## Validation and limitations
- GitHub ARM toolchain compilation and ROM header passed.
- A 13,000-frame mGBA libretro standalone emulator smoke test ran to completion without crashing.
- **Not yet verified:** entering/exiting EACH of seven doors by hand, actual shop purchase, Rook battle story progression, and save/reload. A long unattended frame test is NOT equivalent to a complete gameplay walkthrough.
- **Still placeholders:** original Emerald moving-truck intro, standard indoor tile art, extra NPC animations, actual new starter battle sprites, Wren Blissey farm and later story arc.

## Android installation
See [Android troubleshooting](ANDROID_TROUBLESHOOTING.md). Users must extract the archive or download the `.gba` directly, open it in Pizza Boy A Pro/My Boy!, and start a NEW GAME. Report the exact screen where a problem occurs.

### Source patch
[apply_cinderfall_interiors.py](../scripts/apply_cinderfall_interiors.py) adds four interior maps/scripts and self-checks the seven-door town layout; the build workflow applies it after town generation.

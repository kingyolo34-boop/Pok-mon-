# Pokémon Fallen Ashe — Development Status

## Goal
Build a playable Pokémon Emerald-based fan game featuring an original, darker story in the Ashvale region. Target: standard GBA emulators, including Pizza Boy A Pro and My Boy!.

## Core story
The Danes attack the protagonist's mother in Cinderfall. Three Poké Balls fall, and the player chooses one of three original starters. Rook kills the mother, the player battles Rook, and the adventure begins. The story grows into a tale of grief, survival, and redemption.

## Priority creatures
- Grass Dragon: Verdrake → Leafdrake → Grovedrake
- Water Unicorn: Aqualye → Tidalcorn → Abysscorn
- Fire Griffin: Embergryph → Flaregryph → Inferngryph
- Legendary companions: Deku (Fighting/Steel, Warpath) and Asta (Normal/Fighting), each tied to *The Last Guardians of Cinderfall* side quest
- World legendaries: Shadowvile, Smokerdile, and secret Veylith

## Gameplay goals
- Burnt, ruined Cinderfall with an actual opening sequence and Rook battle
- Functional original starter species and evolutions with proper GBA sprites
- Wren's repeatable Blissey training battles inside Pokémon Centers (Struggle only; 2× EXP)
- Memorable dog-legendary rescue quest and legendary storyline
- Polished Emerald-style world and battle presentation, stable saving and emulator compatibility

## Current status
**Chapter One source build compiled successfully** in GitHub Actions: https://github.com/kingyolo34-boop/Pok-mon-/actions/runs/42922008393. The 32 MiB ROM passed GBA-header and checksum checks. See [Chapter One playtest instructions](CHAPTER_ONE_PLAYTEST.md). The Cinderfall attack, starter selection, mother-death flag, and new Rook trainer event now have source-code implementations, while major visuals remain placeholders. Emulator playthrough has **not yet been verified**. The repository builds from pinned upstream expansion source with our local Python modifiers; it does **not** yet vendor the entire upstream source tree.

## Repository hygiene
Do not commit commercial ROMs (`*.gba`) or saves (`*.sav`, `*.srm`), BIOS files, secrets, or keys. Preserve upstream credits and licenses when importing the expansion source.

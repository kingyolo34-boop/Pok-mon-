# Fallen Ashe — Visual Alpha v2 (first on-screen-verified changes)

**GitHub Actions build:** https://github.com/kingyolo34-boop/Pok-mon-/actions/runs/42925417653
**Build:** SUCCESS. ROM: 33,554,432 bytes. GBA header title: `FALLEN ASHE`.
**SHA-256:** `7c534d41bb36799902f865a6ba471fc45fc8e3bcdd21936f4497804c7ea9fe7f`
**Emulator smoke test:** mGBA libretro core 0.10.5 successfully booted the ROM and displayed the new story intro. Full playthrough, Rook battle, save/reload and map event logic are not yet verified.

## How to tell you are playing the new build
1. Save the new `.gba` under a **distinct filename**, not as `pokeemerald.gba` or an overwritten previous ROM.
2. In your emulator, open the **new file specifically**. Start a **New Game**; don't load an old save state.
3. The first introduction text must say **POKéMON FALLEN ASHE**, **ASHVALE REGION**, and describe **the DANES**. If it says **"Hi! Sorry to keep you waiting!"**, it is the older build.
4. On arriving in the town, the map section name should say **CINDERFALL**. Mom's arrival dialogue now says you're hiding from the Dane blockade.
5. The town has a preliminary dry/ash palette, but the houses and roads are **still Emerald's original map geometry**.
6. Follow the tutorial to the Route 101 ambush for the scripted mother/Rook sequence. **This sequence has not been playtested to completion in an emulator.**

## This is a corrective development milestone, NOT the full Fallout-style town
Done: real in-ROM Ashvale prologue text, native GBA cartridge title, town/region labels, revised Mom & NPC dialogue, preliminary outdoor stone/ash palette, earlier Rook scripted trainer code.
Not done: original title screen graphic, moving truck removal, actual ruined Cinderfall tiles and map redesign, new starter species sprite graphics, custom Dane/Rook sprites, Wren 2x EXP training, and Black Rain/endgame. **Do not advertise this as a finished Cinderfall chapter.**

Our next milestone must use **custom tile graphics and distinct original starter sprites**, with screenshots from an emulator *before* claiming the visuals are delivered.

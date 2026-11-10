# Fallen Ashe — Chapter One GBA test build

**GitHub Actions build:** https://github.com/kingyolo34-boop/Pok-mon-/actions/runs/42922008393

**Status:** source compilation succeeded and the generated 32 MiB .gba header and checksum were verified. Actual emulator playthrough is **not yet verified**.

## How to test this alpha
1. Extract the artifact ZIP from the successful workflow (downloadable on the Actions run).
2. Open **pokeemerald.gba** in **Pizza Boy A Pro, My Boy!, or mGBA**.
3. Start a **New Game**; do not reuse save states from earlier Fallen Ashe tests.
4. The **early Emerald moving-truck/tutorial scene is still a placeholder**. Proceed through it.
5. Walk **north out of Littleroot Town** (temporarily Cinderfall) to **Route 101**.
6. Watch for falling volcanic ash and the **Mom-versus-Dane** ambush using temporary Mom and Team Magma sprites.
7. Interact with the dropped starter bag, choose **Verdrake, Aqualye, or Embergryph**, and confirm the selection.
8. The native wild Zigzagoon battle should be **skipped**. A temporary Maxie-sprite Rook should enter, reveal the Eclipse Mark, kill Mom in a fade-to-black scene, then battle you with a **level 3 Poochyena**.
9. After defeating Rook, he threatens to hunt you. Your character should be sent to the lab as a temporary shelter. Verify saving, reloading, and moving around.

## What is implemented
- Dedicated new **TRAINER_FALLEN_ASHE_ROOK** (distinct trainer flag and party)
- Scripted early Dane attack, Mom's death flag, and Rook confrontation
- Native starter selector (three starter species families supplied by the companion source modifier)
- Starter callback changed to return to the cutscene rather than fight wild Zigzagoon
- Temporary volcanic ash weather in Littleroot and Route 101
- One-shot event progression (starter bag hides; Rook removed after battle)

## Still in development
- Original custom overworld sprite art and burn-scarred Cinderfall map tiles
- Original starter **battle sprites** (old Hoenn graphics currently show in their replacement species slots)
- Fully custom title screen, custom introduction before the truck/tutorial, and a redesigned laboratory shelter
- Later Rook hunt encounters, Black Rain consequences and the eventual **death of Rook by the protagonist** (locked story canon, NOT implemented yet)
- Deku, Asta, Shadowvile, Smokerdile and Veylith story and original species sprites
- **Wren's Blissey training room** (GitHub issue #1)

## Troubleshooting
If it hangs at starter selection, battle, or scene transition, save a screenshot and tell us **exactly what was on screen just before the problem**. We have compiler validation, not yet an in-game emulator test.

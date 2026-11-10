# Fallen Ashe: Cinderfall opening (source patch v1)

## What this adds
The Danes attack the player's mother on Route 101 (our temporary Cinderfall attack scene). A Dane grunt replaces the fleeing wild Zigzagoon sprite. Three dropped Poké Balls lead into Emerald's **native starter chooser**: Verdrake (Grass Dragon), Aqualye (Water Unicorn), or Embergryph (Fire Griffin). Rook enters using a temporary Maxie sprite, kills the mother in a fade-to-black/text-led sequence, fights the player using a Level 4 Poochyena, and leaves. The player returns to the lab as a temporary safehouse.

This patch is built against the **previously modified Fallen Ashe pokeemerald-expansion source**, not the unmodified upstream checkout. The earlier custom starter species definitions and sprite assets are required.

## Use
Apply `patches/opening-chapter-v1.patch` from the root of the modified source with:

```bash
git apply --check opening-chapter-v1.patch
git apply opening-chapter-v1.patch
python3 fallen_ashe/qa_checks.py
```

If using a direct download, place the patch at a known path and substitute that path above.

## Validation
Source-only checks passed for event ordering, starter names and choice order, Rook object, saved mother-death flag, trainer party, and starter assets. **A complete GBA compilation and runtime test have NOT passed**; do not call this a downloadable playable ROM yet. The full opening is not animated, the three dropped balls currently use the native three-ball menu rather than separate overworld sprites, and Cinderfall's custom burnt map still needs implementation.

## Next
1. Import the customized expansion source (without copyrighted ROMs).
2. Make GitHub Actions compile it and capture errors.
3. Test starter choice → Rook encounter → escape → save on emulator.
4. Replace temporary Rook and Dane sprites and rebuild the ruined town.

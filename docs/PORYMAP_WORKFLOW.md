# Editing Fallen Ashe maps with Porymap

The user-provided `pokeemerald-expansion-master (1).zip` was checked and contains the Emerald source needed by Porymap 6.3.1. A separate Porymap starter project archive was prepared in the conversation, with our nine starter-species data changes and volcanic-ash weather enabled on the temporary opening maps.

## Windows workflow

1. Extract the full project archive; do not open the ZIP directly.
2. Launch `porymap.exe`.
3. Use **Open Project** and choose the extracted project root, the folder that has `Makefile`, `data`, `graphics`, `src`, and `include`.
4. Load `LittlerootTown` for the temporary Cinderfall village and `Route101` for the attack site.
5. Use the event/warp and tileset views to edit. Save your work.
6. Upload the edited `data/maps`, `data/layouts`, and any changed `data/tilesets` files for integration, or export the edited project as a ZIP.

## Architecture

The GitHub Actions job currently checks out a **pinned upstream source revision** and applies `scripts/apply_fallen_ashe.py`; it does **not** automatically pick up Porymap edits from a local computer. To turn Porymap changes into a ROM, we must commit corresponding source file changes or apply a controlled override step in the GitHub workflow. Avoid overwriting unrelated files with a newer upstream snapshot.

## Not yet complete

The editor project is a scene-building starting point, **not** a tested version of the full opening. The custom Dane, mother, Rook and starter graphics, event scripts, and final Cinderfall tilesets still need implementation and runtime testing.

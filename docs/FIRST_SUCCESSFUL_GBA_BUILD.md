# Fallen Ashe GBA build milestone — successful

**Build workflow:** https://github.com/kingyolo34-boop/Pok-mon-/actions/runs/42754819982
**Workflow result:** Success (November 10, 2026 UTC)
**Output:** pokeemerald.gba (33,554,432 bytes, 32 MiB)
**GBA game code:** BPEE
**SHA-256:** 42e11605312c20ad2bc508581a09547ddc9803a666da2efd31771f894f82f326

The GitHub Action installed arm-none-eabi tools, checked out pinned pokeemerald-expansion commit be3b089fc121143b7ccf6503ea1385b8abe05b8c, applied scripts/apply_fallen_ashe.py, and compiled with make -j2 modern. The cartridge header and checksum passed validation.

**Implemented in this first source build:** nine original starter species NAMES, stats, types, and level-18/36 evolutions, using temporary replacements of the three Hoenn starter families. Starter selector order is Grass Dragon / Water Unicorn / Fire Griffin. The intro starter message has changed.

**NOT IMPLEMENTED IN THE COMPILED ROM:** original creature battle sprites, custom Cinderfall town art, the animated attack/Rook battle sequence, Wren's Blissey farm, and Deku/Asta/Shadowvile/Smokerdile/Veylith. Those existing plans and separate prototype assets still require integration.

**Caution:** Compilation and cartridge-header checks passed. This particular ROM has not yet been run inside Pizza Boy A Pro or My Boy!, so an Android emulator test is still needed.

The success artifact is available in GitHub Actions as Fallen-Ashe-GBA-Starter-Test (7-day retention). No commercial base ROM was committed to this repository.

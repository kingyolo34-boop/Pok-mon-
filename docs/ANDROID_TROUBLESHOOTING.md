# Fallen Ashe on Android — playtest troubleshooting

## Installing a new test ROM
1. Download the direct **.gba** file if available. If you downloaded a ZIP, open it in Android Files / My Files and select **Extract** first.
2. Confirm the extracted ROM ends in **.gba**, not **.zip** or **.gba.zip**. The file should be about **32 MB**.
3. Move it to a folder such as `Downloads/FallenAshe/` so you can find it.
4. Open **Pizza Boy A Pro** or **My Boy!**, use the app's **Open/Load ROM** option and select the **new named .gba** file.
5. Choose **New Game** for a new build. Do **not** load an old emulator save state or rename an older ROM over the new one.
6. A working Fallen Ashe build should show an Ashvale/Danes introduction, then reach the ruined Cinderfall town after the original Emerald opening/truck portion.

## What “can't play” might mean
- **Couldn't download the file:** Try the ZIP download instead or a browser download, then extract it with Android's My Files app.
- **The emulator can't see the file:** Check the file extension, directory permission, and that it's uncompressed.
- **The emulator opens to a blank/black screen:** Force close and relaunch; verify the 32-MB file finished downloading; test a known-working ROM to rule out emulator issues.
- **The game opens but gets stuck:** Note the screen and the most recent action (intro, truck, town door, starter chooser, Rook encounter) and provide a screenshot. This identifies a game-engine bug rather than a file-opening problem.
- **Looks unchanged:** Open the new distinctly named file and start New Game rather than loading a previous save state.

## Build confidence vs game completeness
The GitHub Action checks source patch application, ARM compilation, and the GBA cartridge header/checksum. It does NOT prove a complete story playthrough. A launch test and door/shop interactions must be tested in an emulator. Report issues by the exact step; do not assume every compile success means playable.

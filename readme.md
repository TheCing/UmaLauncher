# Uma Launcher (Global Mod)

A companion tool for Uma Musume (Global/Steam) that adds training analytics, a skill buy optimizer, race logging, and quality-of-life features.

> Fork of [qwcan/UmaLauncher](https://github.com/qwcan/UmaLauncher) with additional features for the Global version.

For questions and feedback, join the Discord: [![Discord](https://discordapp.com/api/guilds/1416044589877559497/widget.png?style=shield)](https://discord.gg/xd4EbvKBaf)

---

## Quick Start

### 1. Install Hachimi + CarrotBlender

Most features require **CarrotBlender** (reads the game's network data). It runs through **Hachimi**.

1. Install [Hachimi-Edge](https://github.com/kairusds/Hachimi-Edge/releases/latest) (use the installer `.exe`, restart your PC if needed).
2. Get the CarrotBlender `.dll` from the [Discord server](https://discord.gg/xd4EbvKBaf).
3. Copy the `.dll` into the `hachimi` folder inside your game's install directory.
4. Open `config.json` in that same folder and add it to `load_libraries`:
   ```json
   "load_libraries": ["hachimi\\carrotblender.dll"]
   ```

### 2. Download & Run Uma Launcher

1. Download **`UmaLauncher-Global.exe`** from the [latest release](https://github.com/TheCing/UmaLauncher/releases/latest).
2. Put it somewhere convenient (Desktop, game folder, wherever).
3. Run it. It will ask for admin privileges (needed to interact with the game window).
4. A horseshoe icon appears in your system tray (bottom-right of your taskbar, near the clock).

That's it. Launch Uma Musume through Steam as normal and Uma Launcher will detect it automatically.

### Troubleshooting

| Problem | Check |
|---------|-------|
| Uma Launcher won't start / crashes on launch | Make sure you're running Windows 10 or 11. Try running as Administrator. |
| "Could not bind to 127.0.0.1:17229" | Another instance is already running. Close it from the tray icon, or kill all instances in PowerShell: `Get-Process \| Where-Object { $_.ProcessName -like '*UmaLauncher*' } \| Stop-Process -Force` |
| No training event helper / no features working | You need **CarrotBlender** installed (see Step 1 above). Without it, Uma Launcher can't read game data. |
| Event helper not showing up | Make sure "Enable CarrotJuicer" is checked in Preferences. Also check that your browser (Edge/Chrome/Firefox) is working. |
| Game install path wrong / game not detected | Right-click tray icon > Preferences > set **Game install path** to the folder containing `umamusume.exe`. |
| "Recommend skill buys" says no data | You need to be inside a training run. The game must have sent at least one packet — navigate through a turn first. |
| "Export Account Data" says no data | Go to the home screen in-game first. Uma Launcher captures it from the home screen packet. |
| Training logs not being saved | Make sure **Track trainings** is enabled in Preferences. |
| Training viewer won't load `.gz` files | Old `.gz` log format has browser compatibility issues. Start a new run (saves as `.json`) or use **Export Training CSV** from the tray menu. |
| Connection error about umapyoi.net | Safe to ignore on Global. English translations from umapyoi.net are optional — everything still works, some text may show in Japanese. |

---

## Features

### Training Event Helper *(CarrotBlender required)*
Automatically opens a browser with your current character + support cards on [GameTora](https://gametora.com/umamusume/training-event-helper), scrolling to the right event choice when one comes up.

### Skill Buy Recommender *(CarrotBlender required)*
At the end-of-career skill screen, right-click the tray icon and choose **Recommend skill buys**. It calculates the optimal set of skills to buy to maximize your horse's rating, accounting for hint discounts, aptitude multipliers, and skill point budget.

### Training Logs & Viewer *(CarrotBlender required)*
With "Track trainings" enabled in Preferences, every training run is saved to the `training_logs` folder. You can:
- **Export Training CSV** from the tray menu to analyze in Excel/Sheets.
- Open `training_viewer.html` in your browser and drag-and-drop `.json` log files (or `.csv` exports) for an interactive dashboard with charts and turn-by-turn breakdowns.

[CSV column reference](Training_Analyzer_Documentation.md)

### Race Logging *(CarrotBlender required)*
Standalone races (Room Match, Champions Meet, etc.) are automatically saved to `appdata/race_logs/` as JSON + CSV.

### Account Export *(CarrotBlender required)*
Right-click tray icon > **Export Account Data** to save your full account info (characters, support cards, etc.) to a JSON file. Visit the home screen at least once first so the data can be captured.

### Discord Rich Presence
Shows your current training details in Discord.

### Window Management
- Lock and remember game window position (portrait and landscape separately).
- Auto-resize the game window to fill your screen.
- Screenshot to clipboard.

---

## Tray Menu Reference

Right-click the horseshoe in the system tray:

| Option | What it does |
|--------|-------------|
| Preferences | Open settings |
| Maximize + center game | Resize game window to fill screen |
| Copy screenshot to clipboard | Capture the game window |
| Export Training CSV | Convert training logs to spreadsheet |
| Export Account Data | Save account info to JSON |
| Recommend skill buys | Optimal skill purchase advice |
| Close | Exit Uma Launcher |

---

## Disclaimer

Uma Launcher is not associated with Cygames, Inc. or any related companies. It reads publicly available game data to enhance the player experience.

## License

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This code is available under the GNU GPLv3 license. Credits for included libraries are in [CREDITS.txt](CREDITS.txt).

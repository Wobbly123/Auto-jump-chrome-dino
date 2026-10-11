# Chrome Dino Bot

A small Python bot that plays the Chrome Dino game (`chrome://dino`) on its own.
It watches a thin strip of the screen in front of the dino and presses **space**
whenever a cactus gets close. The look-ahead distance grows over time, because
the game speeds up.

## How it works

1. You hover the mouse over the front of the dino (at belly height) for calibration.
2. The bot repeatedly grabs a small strip of the screen ahead of the dino.
3. If enough pixels differ strongly from the background, it counts as an obstacle.
4. It presses space, waits a moment, and keeps watching.

Nothing is saved to disk; every screenshot is held in memory and overwritten.

## Run from source

Requires Python 3.9+ on Windows.

```
python -m pip install -r requirements.txt
python dino_en.py
```

## Build a standalone .exe

```
python -m pip install pyinstaller
python -m PyInstaller --onefile dino_en.py
```

The result is in `dist/dino_en.exe`. Do not use `--noconsole`, because calibration
happens in the console window.

## Usage

1. Open `chrome://dino` in Chrome.
2. Start the program.
3. Hover the mouse over the front of the dino, at belly height (not the feet), and press Enter in the console.
4. Within 5 seconds, click the game window and press space to start the game.
5. Stop the bot with Ctrl+C.

## Settings

Edit the constants at the top of `dino_en.py`:

| Setting | Meaning |
|---|---|
| `LOOKAHEAD_START` | How far ahead (px) the bot looks at the start |
| `LOOKAHEAD_GROWTH` | How fast the look-ahead grows (px/s) |
| `THRESHOLD` | How much a pixel must differ from the background |
| `MIN_PIXELS` | How many differing pixels count as an obstacle |
| `JUMP_COOLDOWN` | Pause after each jump (seconds) |

If it jumps too late, increase `LOOKAHEAD_START` or `LOOKAHEAD_GROWTH`.
If it jumps for no reason, increase `MIN_PIXELS`.

## Limitations

- Only jumps; it does not duck under flying birds.
- Does not restart the game after losing.
- Tuned for the default game size; screen scaling may need adjustments.

## About

This is my first project ever. Feedback and suggestions are welcome!

## License

MIT

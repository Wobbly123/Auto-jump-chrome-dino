"""
Bot for the Google Dino game (chrome://dino).
Install:  python -m pip install mss numpy pyautogui
Run:      python dino_en.py
"""
import time

import mss
import numpy as np
import pyautogui

pyautogui.PAUSE = 0

# ---- Settings (tweak if needed) ----
LOOKAHEAD_START = 70   # how many px ahead of the dino we look at the start
LOOKAHEAD_GROWTH = 4   # how many px/s the lookahead grows (the game speeds up)
MAX_LOOKAHEAD = 300    # maximum lookahead distance in px
THRESHOLD = 100        # how much a pixel must differ from the background (clouds and pebbles are weaker)
MIN_PIXELS = 40        # how many such pixels at once count as a cactus (ignores small noise)
STRIP_HEIGHT = 30      # height of the scanned strip at cactus level in px
JUMP_COOLDOWN = 0.15   # seconds - avoids jumping several times at one cactus
# ------------------------------------


def calibrate():
    print("CALIBRATION")
    print("1. Open chrome://dino and start the game (space), then wait for the start screen.")
    print("2. Hover the mouse over the very FRONT of the dino, at the height of its BELLY (not the feet!).")
    input("3. Don't move the mouse and press Enter here in the console... ")
    x, y = pyautogui.position()
    print(f"Saved position: {x}, {y}")
    return x, y


def main():
    x, y = calibrate()

    region = {
        "left": x + 25,
        "top": y - STRIP_HEIGHT // 2,
        "width": MAX_LOOKAHEAD,
        "height": STRIP_HEIGHT,
    }

    print("Starting in 5 seconds - click the game window and press space to start the game!")
    time.sleep(5)
    t0 = time.time()

    with mss.mss() as sct:
        while True:
            frame = np.array(sct.grab(region))[:, :, :3]
            gray = frame.mean(axis=2)
            background = np.median(gray)  # background colour = median of the whole strip

            lookahead = int(LOOKAHEAD_START + (time.time() - t0) * LOOKAHEAD_GROWTH)
            lookahead = min(lookahead, MAX_LOOKAHEAD)

            if (np.abs(gray[:, :lookahead] - background) > THRESHOLD).sum() >= MIN_PIXELS:
                pyautogui.press("space")
                time.sleep(JUMP_COOLDOWN)

            time.sleep(0.005)  # lighter CPU load


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Stopped.")

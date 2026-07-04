#!/usr/bin/env python3

# Automates one FF8 Card command retry cycle in RetroArch:
# load state, skip turns with Circle, save state, then select Card.
# Press Enter between attempts and Ctrl-C to stop.

import sys

from raspberrypi_hid.config import load_config

runtime = load_config()
keyboard = runtime.keyboard
pad = runtime.pad
timing = runtime.timing

print("This script runs one FF8 Card retry cycle each time you press Enter.")
print("It will load state, skip turns with Circle, save state, then select Card.")
print("Use F2 to save while the Card command is highlighted before starting.")
print("If the attempt fails, press Enter on this keyboard to try again.")
print("Press Ctrl-C to stop. Press Enter to begin.")
sys.stdin.readline()
print("Beginning...")
try:
    while True:
        keyboard.tap(pad.load_state, delay=timing.medium)
        keyboard.tap(pad.circle, delay=timing.medium)
        # If two characters are alive:
        keyboard.tap(pad.circle, delay=timing.medium)
        # If three characters are alive:
        # keyboard.tap(pad.circle, delay=timing.medium)
        keyboard.tap(pad.save_state, delay=timing.medium)
        keyboard.tap(pad.cross, delay=timing.medium)
        keyboard.tap(pad.cross, delay=timing.medium)
        keyboard.release_all()

        print("Waiting for enter...")
        sys.stdin.readline()
except KeyboardInterrupt:
    print("\nStopped by Ctrl-C.")
finally:
    keyboard.release_all()

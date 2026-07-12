#!/usr/bin/env python3

# Alternates Square and Circle for the FF9 Hippaul racing minigame.
# Start the script at the starting line when Hippaul's mother says "Get set,"
# then press Ctrl-C when Vivi reaches the finish line.

from raspberrypi_hid.config import load_config

runtime = load_config()
keyboard = runtime.keyboard
pad = runtime.pad

print("This script will alternate Square and Circle until you stop it with Ctrl-C.")

try:
    while True:
        keyboard.tap(pad.square)
        keyboard.tap(pad.circle)
except KeyboardInterrupt:
    print("\nStopped by Ctrl-C.")
finally:
    keyboard.release_all()

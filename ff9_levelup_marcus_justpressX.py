#!/usr/bin/env python3

import argparse

from raspberrypi_hid.config import load_config
from raspberrypi_hid.duration import add_hours_argument, run_repeated_tap


parser = argparse.ArgumentParser()
add_hours_argument(parser, default=1)
args = parser.parse_args()

runtime = load_config()
keyboard = runtime.keyboard
pad = runtime.pad
timing = runtime.timing

def pause_game():
    keyboard.tap(pad.start, delay=timing.select_long)


run_repeated_tap(keyboard, pad.cross, timing, "Cross", args.hours)
pause_game()

# Release all keys
keyboard.release_all()

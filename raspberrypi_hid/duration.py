"""Helpers for duration-based repeated button scripts."""

import argparse
from fractions import Fraction


def add_hours_argument(parser: argparse.ArgumentParser, default=1) -> None:
    """Add a shared --hours option to a script argument parser."""

    parser.add_argument(
        "--hours",
        type=parse_run_hours,
        default=default,
        help=(
            'Hours to run, such as "1", "0.5", or "1/60". '
            'Use "none" to run until Ctrl-C. Default: %(default)s.'
        ),
    )


def parse_run_hours(value):
    """Parse --hours values, including fractions and 'none'."""

    if value.lower() == "none":
        return None
    try:
        hours = float(Fraction(value))
    except (ValueError, ZeroDivisionError) as exc:
        raise argparse.ArgumentTypeError(
            '--hours must be a positive number like "1", "0.5", or "1/60", '
            'or "none" to run until Ctrl-C.'
        ) from exc
    if hours <= 0:
        raise argparse.ArgumentTypeError(
            '--hours must be positive, or "none" to run until Ctrl-C.'
        )
    return hours


def run_repeated_tap(keyboard, button, timing, button_name: str, run_hours) -> None:
    """Press one button repeatedly for a duration, or until Ctrl-C."""

    if run_hours is None:
        print(f"This script will press {button_name} until you stop it with Ctrl-C.")
        try:
            while True:
                keyboard.tap(button, delay=timing.rapid)
        except KeyboardInterrupt:
            pass
        return

    seconds_per_loop = timing.button_hold + timing.rapid
    runloops = max(1, int((60 * 60 * run_hours) / seconds_per_loop))
    print(
        f"This script will press {button_name} for about "
        f"{run_hours:g} hour(s), using {runloops} taps. Stop with Ctrl-C."
    )
    for num_passes in range(1, runloops + 1):
        keyboard.tap(button, delay=timing.rapid)


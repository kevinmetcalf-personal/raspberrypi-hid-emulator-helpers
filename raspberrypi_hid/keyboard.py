"""Low-level Raspberry Pi USB HID keyboard writer."""

import os
import signal
import sys
import time
from typing import Optional, Union

from .keys import Key, key
from .timing import TimingProfile


KeyLike = Union[str, Key]


class Keyboard:
    """Write keyboard reports to a Linux USB HID gadget device."""

    def __init__(
        self,
        device: str = "/dev/hidg0",
        hold_time: Optional[float] = None,
        require_root: bool = True,
        timing_profile: Optional[TimingProfile] = None,
        timing_speed: int = 5,
    ) -> None:
        """Create a keyboard writer.

        When a timing profile is supplied, timing_speed adjusts the emulator
        timing rhythm as a group: key hold time, rapid repeat gaps, menu
        movement, select/confirm pauses, and medium/long waits.
        """

        self.device = device
        self.timing = timing_profile.at_speed(timing_speed) if timing_profile else None
        self.hold_time = hold_time if hold_time is not None else (
            self.timing.button_hold if self.timing else 0.03
        )
        if require_root:
            self._check_root()
        self._check_device()

    def install_exit_handler(self) -> None:
        """Release all keys when the user presses Ctrl-C."""

        def handler(sig, frame):
            print("You pressed Ctrl-C. Releasing all keys.")
            self.release_all()
            sys.exit(0)

        signal.signal(signal.SIGINT, handler)

    def tap(
        self,
        key_to_press: KeyLike,
        delay: float = 0.0,
        hold_time: Optional[float] = None,
    ) -> None:
        """Press and release one key, then optionally pause."""

        self.press(key_to_press)
        time.sleep(self.hold_time if hold_time is None else hold_time)
        self.release_all()
        if delay:
            time.sleep(delay)

    def press(self, key_to_press: KeyLike) -> None:
        """Press one key without releasing it."""

        resolved = self._resolve_key(key_to_press)
        self.write_report(bytes([resolved.modifier, 0, resolved.code, 0, 0, 0, 0, 0]))

    def release_all(self) -> None:
        """Release every key currently held by the virtual keyboard."""

        self.write_report(bytes(8))

    def write_report(self, report: bytes) -> None:
        """Write one raw 8-byte HID report."""

        with open(self.device, "rb+") as fd:
            fd.write(report)

    def _resolve_key(self, key_to_press: KeyLike) -> Key:
        if isinstance(key_to_press, Key):
            return key_to_press
        return key(key_to_press)

    def _check_root(self) -> None:
        if hasattr(os, "geteuid") and os.geteuid() != 0:
            raise SystemExit(
                "This script writes to /dev/hidg0 and usually must run as root.\n"
                "Try one of these:\n"
                "  sudo python3 your_script.py\n"
                "  sudo su -\n"
                "Then rerun the command from this project folder."
            )

    def _check_device(self) -> None:
        if not os.path.exists(self.device):
            raise SystemExit(
                f"Could not find {self.device}.\n"
                "Make sure the Raspberry Pi USB HID gadget is configured and enabled."
            )

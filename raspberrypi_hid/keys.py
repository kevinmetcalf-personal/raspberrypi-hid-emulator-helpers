"""USB HID keyboard key codes used by the automation scripts.

The key codes come from the USB HID Usage Tables keyboard/keypad page.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Key:
    """A single keyboard key that can be sent as a USB HID report."""

    name: str
    code: int
    modifier: int = 0


KEYS: Dict[str, Key] = {
    "a": Key("a", 4),
    "b": Key("b", 5),
    "c": Key("c", 6),
    "d": Key("d", 7),
    "e": Key("e", 8),
    "f": Key("f", 9),
    "g": Key("g", 10),
    "h": Key("h", 11),
    "i": Key("i", 12),
    "j": Key("j", 13),
    "k": Key("k", 14),
    "l": Key("l", 15),
    "m": Key("m", 16),
    "n": Key("n", 17),
    "o": Key("o", 18),
    "p": Key("p", 19),
    "q": Key("q", 20),
    "r": Key("r", 21),
    "s": Key("s", 22),
    "t": Key("t", 23),
    "u": Key("u", 24),
    "v": Key("v", 25),
    "w": Key("w", 26),
    "x": Key("x", 27),
    "y": Key("y", 28),
    "z": Key("z", 29),
    "enter": Key("enter", 40),
    "space": Key("space", 44),
    "right": Key("right", 79),
    "left": Key("left", 80),
    "down": Key("down", 81),
    "up": Key("up", 82),
    "f2": Key("f2", 59),
    "f4": Key("f4", 61),
}


def key(name: str) -> Key:
    """Return a named key, raising a helpful error for unknown names."""

    try:
        return KEYS[name.lower()]
    except KeyError as exc:
        known = ", ".join(sorted(KEYS))
        raise ValueError(f"Unknown key {name!r}. Known keys: {known}") from exc


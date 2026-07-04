"""Controller profiles mapping emulator keyboard keys to PlayStation buttons."""

from dataclasses import dataclass
from typing import Optional

from .keys import Key, key


@dataclass(frozen=True)
class PlayStationProfile:
    """Keyboard mapping for PlayStation-style emulator controls."""

    name: str
    square: Key
    triangle: Key
    circle: Key
    cross: Key
    start: Key
    up: Key
    down: Key
    left: Key
    right: Key
    save_state: Optional[Key] = None
    load_state: Optional[Key] = None


RETROARCH_PSX = PlayStationProfile(
    name="RetroArch PSX",
    square=key("a"),
    triangle=key("s"),
    circle=key("x"),
    cross=key("z"),
    start=key("enter"),
    up=key("up"),
    down=key("down"),
    left=key("left"),
    right=key("right"),
    save_state=key("f2"),
    load_state=key("f4"),
)

OPENEMU_PSX = PlayStationProfile(
    name="OpenEmu PSX",
    square=key("a"),
    triangle=key("s"),
    circle=key("z"),
    cross=key("x"),
    start=key("enter"),
    up=key("up"),
    down=key("down"),
    left=key("left"),
    right=key("right"),
)

CONTROLLER_PROFILES = {
    "retroarch_psx": RETROARCH_PSX,
    "openemu_psx": OPENEMU_PSX,
}

"""Runtime configuration loader for HID automation scripts."""

import configparser
import os
from dataclasses import dataclass
from typing import Optional

from .keyboard import Keyboard
from .profiles import CONTROLLER_PROFILES, PlayStationProfile
from .timing import TIMING_PROFILES, TimingProfile


DEFAULT_CONFIG = {
    "hid": {
        "device": "/dev/hidg0",
        "require_root": "yes",
        "install_exit_handler": "yes",
    },
    "emulator": {
        "controller_profile": "retroarch_psx",
        "timing_profile": "retroarch_psx",
        "timing_speed": "5",
    },
}


@dataclass(frozen=True)
class RuntimeConfig:
    """Ready-to-use objects for an automation script."""

    keyboard: Keyboard
    pad: PlayStationProfile
    timing: TimingProfile
    config_path: Optional[str]


def load_config(config_path: Optional[str] = None) -> RuntimeConfig:
    """Load config.ini and return the configured keyboard, pad, and timing."""

    parser = configparser.ConfigParser()
    parser.read_dict(DEFAULT_CONFIG)
    resolved_path = _resolve_config_path(config_path)
    if resolved_path:
        parser.read(resolved_path)

    controller_name = parser.get("emulator", "controller_profile")
    timing_name = parser.get("emulator", "timing_profile")
    timing_speed = parser.getint("emulator", "timing_speed")
    device = parser.get("hid", "device")
    require_root = parser.getboolean("hid", "require_root")
    install_exit_handler = parser.getboolean("hid", "install_exit_handler")

    pad = _get_named(CONTROLLER_PROFILES, controller_name, "controller profile")
    timing_profile = _get_named(TIMING_PROFILES, timing_name, "timing profile")
    try:
        keyboard = Keyboard(
            device=device,
            require_root=require_root,
            timing_profile=timing_profile,
            timing_speed=timing_speed,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    if install_exit_handler:
        keyboard.install_exit_handler()

    return RuntimeConfig(
        keyboard=keyboard,
        pad=pad,
        timing=keyboard.timing,
        config_path=resolved_path,
    )


def _resolve_config_path(config_path: Optional[str]) -> Optional[str]:
    if config_path:
        return _required_config_path(config_path)

    env_path = os.environ.get("RASPBERRYPI_HID_CONFIG")
    if env_path:
        return _required_config_path(env_path)

    candidates = [
        os.path.join(os.getcwd(), "config.ini"),
        os.path.join(_project_root(), "config.ini"),
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
    return None


def _required_config_path(path: str) -> str:
    resolved = os.path.abspath(os.path.expanduser(path))
    if not os.path.exists(resolved):
        raise SystemExit(f"Config file not found: {resolved}")
    return resolved


def _project_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _get_named(registry, name: str, label: str):
    try:
        return registry[name]
    except KeyError as exc:
        known = ", ".join(sorted(registry))
        raise SystemExit(f"Unknown {label} {name!r}. Known values: {known}") from exc

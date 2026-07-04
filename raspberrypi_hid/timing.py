"""Named delay profiles for emulator automation scripts."""

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class TimingProfile:
    """Delay values, in seconds, for one emulator/input setup."""

    button_hold: float = 0.0275
    rapid: float = 0.025
    tap_gap: float = 0.03
    quantity: float = 0.075
    menu_arrow: float = 0.090
    menu_page: float = 0.175
    select_short: float = 0.100
    select_medium: float = 0.200
    select_long: float = 0.750
    medium: float = 0.875
    long: float = 2.500

    def at_speed(self, speed: int) -> "TimingProfile":
        """Return this profile adjusted to a user-friendly speed from 1 to 10.

        Speed 5 keeps the measured baseline timings. Lower is safer/slower.
        Higher is faster, but may cause missed input if the emulator cannot keep up.
        """

        if speed < 1 or speed > 10:
            raise ValueError("Speed must be between 1 and 10.")

        multiplier = _speed_multiplier(speed)
        return replace(
            self,
            button_hold=max(0.02, self.button_hold * multiplier),
            rapid=max(0.01, self.rapid * multiplier),
            tap_gap=max(0.01, self.tap_gap * multiplier),
            quantity=max(0.02, self.quantity * multiplier),
            menu_arrow=max(0.03, self.menu_arrow * multiplier),
            menu_page=max(0.05, self.menu_page * multiplier),
            select_short=max(0.04, self.select_short * multiplier),
            select_medium=max(0.08, self.select_medium * multiplier),
            select_long=max(0.25, self.select_long * multiplier),
            medium=max(0.30, self.medium * multiplier),
            long=max(1.00, self.long * multiplier),
        )


def _speed_multiplier(speed: int) -> float:
    if speed == 5:
        return 1.0
    if speed < 5:
        return 1.0 + ((5 - speed) * 0.15)
    return 1.0 - ((speed - 5) * 0.08)


RETROARCH_PSX_TIMING = TimingProfile()

TIMING_PROFILES = {
    "retroarch_psx": RETROARCH_PSX_TIMING,
}

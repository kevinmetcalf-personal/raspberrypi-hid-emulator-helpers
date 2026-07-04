# Raspberry Pi HID Emulator Helpers

This project contains Raspberry Pi USB HID keyboard scripts for automating repetitive emulator inputs. The original use case was reducing wrist strain while playing PlayStation games in an emulator, especially repetitive Final Fantasy VIII and IX tasks.

The Raspberry Pi pretends to be a USB keyboard. The emulator sees ordinary keyboard input, and the scripts send those keys through `/dev/hidg0`.

## Hardware And Runtime

This was built around a Raspberry Pi that supports USB gadget mode, such as a Raspberry Pi Zero or Zero W.

Expected environment:

- Raspberry Pi configured as a USB HID keyboard gadget
- Linux device file available at `/dev/hidg0`
- Python 3.7 or newer
- Root access for writing to `/dev/hidg0`

The active refactored scripts use only Python standard library modules:

- `argparse`
- `configparser`
- `dataclasses`
- `datetime`
- `os`
- `signal`
- `sys`
- `time`
- `typing`

No third-party Python packages are required.

## Configuration

Copy the example config before running scripts:

```sh
cp config.example.ini config.ini
```

Then edit `config.ini` for your setup. The file is commented and is meant to be self-documenting. Local `config.ini` is ignored by git.

The default config uses:

- HID device: `/dev/hidg0`
- controller profile: `retroarch_psx`
- timing profile: `retroarch_psx`
- timing speed: `5`

You can also point to a different config file with:

```sh
RASPBERRYPI_HID_CONFIG=/path/to/config.ini sudo python3 ff9_hippaul_retroarch.py
```

## Running Scripts

Most systems require root privileges to write to `/dev/hidg0`. If you run a script as a normal user, the shared keyboard helper will stop and remind you to use root.

Run a script with `sudo`:

```sh
sudo python3 ff9_hippaul_retroarch.py
```

Or switch to a root shell first:

```sh
sudo su -
cd /home/pi/raspberrypi-hid
python3 ff9_hippaul_retroarch.py
```

Press `Ctrl-C` to stop a running script. The shared keyboard helper tries to release all keys before exiting.

Some repeated-button scripts accept `--hours`:

```sh
sudo python3 ff9_levelup_marcus_justpressX.py --hours=1/60
sudo python3 ff9_fossilroo_justpressquare.py --hours=none
```

Use a number of hours, a fraction such as `1/60`, or `none` to run until `Ctrl-C`.

The FF8 Esthar stat-up farming script accepts a few task-specific options:

```sh
sudo python3 ff8_esthar_stat_up_farm.py --passes=1
sudo python3 ff8_esthar_stat_up_farm.py --use-existing-gil
sudo python3 ff8_esthar_stat_up_farm.py --current-hp-ups=1 --max-hp-ups=20
```

Use `--use-existing-gil` if you already have enough Gil and want to skip the money loop.

## Project Layout

- `raspberrypi_hid/keyboard.py`: writes raw keyboard reports to `/dev/hidg0`, checks for root, and releases keys on exit.
- `raspberrypi_hid/keys.py`: maps keyboard names like `a`, `z`, `enter`, and `f2` to USB HID key codes.
- `raspberrypi_hid/profiles.py`: maps PlayStation-style buttons to emulator keyboard bindings.
- `raspberrypi_hid/timing.py`: maps user-friendly speed levels to measured emulator delays.
- `raspberrypi_hid/config.py`: loads `config.ini` and returns ready-to-use `keyboard`, `pad`, and `timing` objects.
- `raspberrypi_hid/duration.py`: shared `--hours` parsing and repeated-button helpers.
- `config.example.ini`: commented configuration template.
- `ff8_esthar_stat_up_farm.py`: farms FF8 stat-up items through Esthar shop/refine loops.
- `ff8_retroarch_f4_triangle_triangle_f2_x.py`: repeats an FF8 Card command retry cycle.
- `ff9_fossilroo_justpressquare.py`: repeatedly presses Square for the FF9 Fossil Roo mining minigame.
- `ff9_hippaul_retroarch.py`: alternates Square and Circle for the FF9 Hippaul racing minigame.
- `ff9_levelup_marcus_justpressX.py`: repeatedly presses Cross for FF9 Marcus/Eiko leveling.

## Emulator Mappings

Task scripts should talk in PlayStation buttons: `cross`, `circle`, `square`, `triangle`, `start`, and directions. Emulator-specific keyboard choices live in `raspberrypi_hid/profiles.py`.

For example, the RetroArch profile currently maps:

```python
RETROARCH_PSX = PlayStationProfile(
    square=key("a"),
    triangle=key("s"),
    circle=key("x"),
    cross=key("z"),
    start=key("enter"),
    save_state=key("f2"),
    load_state=key("f4"),
)
```

If your emulator uses different keyboard controls, set `controller_profile` in `config.ini`. If none of the built-in profiles match, add or edit a profile in `raspberrypi_hid/profiles.py`.

## Timing And Speed

Set timing speed in `config.ini`:

```ini
[emulator]
timing_profile = retroarch_psx
timing_speed = 5
```

Use a value from `1` to `10`:

- `1` is slowest and safest.
- `5` keeps the original measured timings.
- `10` is fastest, but may cause missed inputs if the emulator cannot keep up.

`timing_speed` is applied by the shared keyboard helper. It scales the emulator timing profile as a group:

- key hold time
- rapid repeat gaps
- menu movement waits
- select/confirm pauses
- medium waits
- long waits, such as menus opening

The timing profile keeps different kinds of waits separate. Quick repeat actions use `timing.rapid`; menu navigation uses values like `timing.menu_arrow`, `timing.select_short`, and `timing.long`. This lets a script read like a task recipe while still allowing the whole rhythm to be tuned for a specific emulator/computer.

## Copying To The Pi

One simple workflow is to edit on your main computer and copy the project to the Pi:

```sh
scp -r raspberrypi-hid pi@raspberrypi.local:~/raspberrypi-hid
```

Replace `raspberrypi.local` with your Pi hostname or IP address. If your SSH key is installed for the `pi` user, this should not require a password.

## Notes

These scripts are examples, not a general-purpose game automation framework yet. The intent is to keep the low-level HID code reusable while making each task script read like a small walkthrough recipe.

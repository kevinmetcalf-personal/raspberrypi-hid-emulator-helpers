#!/usr/bin/env python3

# Automates the Esthar shop/refine loops used to farm FF8 stat-up items
# while keeping character levels low. The money loop buys Tents and Cottages,
# refines them into Mega-Potions, sells those Mega-Potions, then uses the
# resulting Gil to buy and refine stat-up materials.
#
# Before starting:
# 1. Clear the first three item slots in inventory.
# 2. Put 1 or more Mega-Potion in slot 1. This cannot be zero.
# 3. Put any Tents in slot 2 and Cottages in slot 3.
# 4. Exit to the world map.

import argparse
from datetime import datetime

from raspberrypi_hid.config import load_config

def positive_int(value):
  try:
    number = int(value)
  except ValueError as exc:
    raise argparse.ArgumentTypeError("must be a positive whole number") from exc
  if number < 1:
    raise argparse.ArgumentTypeError("must be a positive whole number")
  return number

parser = argparse.ArgumentParser()
parser.add_argument(
  "--passes",
  help="Number of full stat-up farming passes to run. Default: %(default)s.",
  dest="runloops",
  type=positive_int,
  default=1,
)
parser.add_argument(
  "--numtimes",
  help=argparse.SUPPRESS,
  dest="runloops",
  type=positive_int,
  default=argparse.SUPPRESS,
)
parser.add_argument(
  "--current-hp-ups",
  help="Starting number of HP Up items, to avoid overflowing the 100 item limit. Default: %(default)s.",
  dest="current_hps",
  type=positive_int,
  default=1,
)
parser.add_argument(
  "--curhps",
  help=argparse.SUPPRESS,
  dest="current_hps",
  type=positive_int,
  default=argparse.SUPPRESS,
)
parser.add_argument(
  "--max-hp-ups",
  help="Maximum number of HP Up items to allow, to avoid overflowing the 100 item limit. Default: %(default)s.",
  dest="max_hps",
  type=positive_int,
  default=1,
)
parser.add_argument(
  "--maxhps",
  help=argparse.SUPPRESS,
  dest="max_hps",
  type=positive_int,
  default=argparse.SUPPRESS,
)
parser.add_argument(
  "--use-existing-gil",
  help="Spend existing Gil instead of running the money loop first.",
  action="store_true",
)
parser.add_argument(
  "--usegil",
  help=argparse.SUPPRESS,
  choices=("0", "1"),
)
args = parser.parse_args()
runloops = args.runloops
use_existing_gil = args.use_existing_gil or args.usegil == "1"
max_hps = args.max_hps
current_hps = args.current_hps
setup_complete = False

runtime = load_config()
keyboard = runtime.keyboard
pad = runtime.pad
timing = runtime.timing


def tap(button, delay):
  hold_time = timing.button_hold if setup_complete else timing.button_hold * 2
  keyboard.tap(button, delay=delay, hold_time=hold_time)

def tap_repeated(button, count, delay):
  for _ in range(count):
    tap(button, delay)

def return_to_ability_menu():
  tap_repeated(pad.triangle, 3, timing.medium)

# Open the menu and anchor the cursor on Call Shop. Later re-anchors are kept
# intentionally because this workflow depends on remembered menu positions.
def initial_setup():
  global setup_complete
  tap(pad.circle,timing.long)		# Circle (enter menu) ; NOTE: IT TAKES 3-4 SECONDS FOR THE MENU TO OPEN!
  tap_repeated(pad.down, 5, timing.menu_arrow) # Down Arrow (place cursor on Ability)
  tap(pad.cross,timing.medium)	# Cross (select Ability)
  tap_repeated(pad.down, 3, timing.menu_arrow) # Down Arrow (place cursor on Call Shop)
  setup_complete = True

def money_loop(max_count):
  if use_existing_gil:
    return
  reset_shop()
  for count in range(max_count):
    tap(pad.cross,timing.select_long)	# Cross (select Call Shop)
    if count == 0:					# ONLY NEED TO DO THIS FOR THE FIRST PASS
      tap_repeated(pad.up, 2, timing.menu_arrow) # Up Arrow (place cursor on Esthar Shop!!!)
    tap(pad.cross,timing.medium)	# Cross (select Esthar Shop!!!)
    tap(pad.cross,timing.select_long)	# Cross (select Buy)
    tap(pad.right,timing.menu_page) # Right Arrow (select next page in menu)
    tap_repeated(pad.up, 2, timing.menu_arrow) # Up Arrow (place cursor Cottage)
    tap(pad.cross,timing.select_short)	# Cross (select Cottage)
    tap_repeated(pad.up, 10, timing.quantity) # Up Arrow (Select the maximum of 100 Cottages)
    tap(pad.cross,timing.select_short)	# Cross (buy 100 Cottages)
    tap(pad.up,timing.menu_arrow)	# Up Arrow (place cursor on Tent)
    tap(pad.cross,timing.select_short)	# Cross (select Tent)
    tap_repeated(pad.up, 10, timing.quantity) # Up Arrow (Select the maximum of 100 Tents)
    tap(pad.cross,timing.select_medium)	# Cross (buy 100 Tents)
    tap(pad.triangle,timing.select_long)	# Triangle (exit to menu)
    tap(pad.right,timing.menu_arrow) # Right Arrow (place curson on sell)
    tap(pad.cross,timing.select_long)	# Cross (select sell)
    tap(pad.cross,timing.select_short)	# Cross (select Mega-Potion)
    tap_repeated(pad.up, 8, timing.quantity) # Up Arrow (select all items)
    tap(pad.cross,timing.select_short)	# Cross (sell Mega-Potions)
    return_to_ability_menu()
    tap(pad.right,timing.menu_page) # Right Arrow (Next page of Ability Menu)
    tap(pad.up,timing.menu_arrow)	# Up Arrow (place cursor on Recov Med-RF)
    tap(pad.cross,timing.medium)	# Cross (select Recov Med-RF)
    tap(pad.down,timing.menu_arrow) # Down Arrow (place cursor on Tent)
    tap(pad.cross,timing.select_medium)	# Cross (select Tent)
    tap_repeated(pad.down, 3, timing.quantity) # Down Arrow (select all tents)
    tap(pad.cross,timing.select_short)	# Cross (Refine all tents)
    tap(pad.down,timing.menu_arrow) # Down Arrow (place cursor on Cottage)
    tap(pad.cross,timing.select_short)	# Cross (select Cottage)
    tap_repeated(pad.down, 5, timing.quantity) # Down Arrow (select all Cottages)
    tap(pad.cross,timing.select_short)	# Cross (Refine all Cottages)
    tap(pad.triangle,timing.medium)	# Triangle (exit to Ability Menu)
    tap(pad.left,timing.menu_page) # Left Arrow (back to first page of ability menu)
    tap(pad.down,timing.menu_arrow) # Down Arrow (place cursor over call shop)

def reset_shop():
  tap(pad.triangle,timing.medium)     # Triangle: Exit to Main Menu
  tap(pad.cross,timing.medium)     # Cross: Return to Ability Menu
  tap_repeated(pad.down, 3, timing.menu_arrow) # Down Arrow (place cursor on Call Shop)

def exit_to_map():
  tap(pad.triangle,timing.medium)	# Triangle: Exit to Main Menu
  tap(pad.triangle,timing.long)	# Triangle: Exit to map

def pause_game():
  tap(pad.start,timing.select_long) # Start Button: Pause game

def get_stat_up(stat_type,num_want):
  global current_hps
  if stat_type=='HP':
    money_loop(5)
    reset_shop()
    current_hps += 10
    if current_hps > max_hps:
      return
    item_location=4
  elif stat_type=='Str':
    money_loop(5)
    reset_shop()
    item_location=3
  elif stat_type=='Spr':
    money_loop(5)
    reset_shop()
    item_location=2
  elif stat_type=='Mag':
    money_loop(5)
    reset_shop()
    item_location=1
  elif stat_type=='Vit':
    money_loop(11)
    reset_shop()
    for count in range(num_want):
      for count2 in range(5):				# NOTE - YOU NEED TO CYCLE THROUGH THIS FIVE TIMES!
        tap(pad.cross,timing.select_long)	# Cross (select Call Shop)
        if (count == 0) and (count2 == 0):		# ONLY NEED TO DO THIS FOR THE FIRST PASS
          tap_repeated(pad.up, 4, timing.menu_arrow) # Up Arrow (place cursor on Esthar Pet Shop)
        tap(pad.cross,timing.medium)	# Cross (select Esthar Pet Shop)
        tap(pad.cross,timing.select_long)	# Cross (select Buy)
        tap(pad.up,timing.menu_arrow) # Up Arrow (place cursor over appropriate item)
        tap(pad.cross,timing.select_short)	# Cross (select item)
        tap_repeated(pad.up, 10, timing.quantity) # Up Arrow (Select the maximum of 100 items)
        tap(pad.cross,timing.select_medium)      # Cross (Purchase Item)
        return_to_ability_menu()
        tap(pad.right,timing.menu_page) # Right Arrow (Next page of abilities)
        tap_repeated(pad.down, 5, timing.menu_arrow) # Down Arrow (Cursor over GFAbl Med-RF)
        tap(pad.cross,timing.medium)     # Cross (select GFAbl Med-RF)
        tap(pad.down,timing.menu_arrow) # Down Arrow (Cursor over item to refine)
        tap(pad.cross,timing.medium)     # Cross (select item to refine)
        tap(pad.down,timing.menu_arrow) # Down Arrow (Choose quantity 10 items to refine)
        tap(pad.cross,timing.medium)     # Cross (refine)
        if count2 == 4:
          tap(pad.down,timing.menu_arrow) # Down Arrow (Cursor over item to refine)
          tap(pad.cross,timing.medium)     # Cross (select item to refine)
          tap(pad.down,timing.menu_arrow) # Down Arrow (Choose quantity 10 items to refine)
          tap(pad.cross,timing.medium)     # Cross (refine)
          tap(pad.triangle,timing.medium) # Triangle to return to ability menu
          tap_repeated(pad.up, 2, timing.menu_arrow) # Up Arrow (Cursor over Forbid Med-RF)
          tap(pad.cross,timing.medium)     # Cross (select Forbid Med-RF)
          tap(pad.down,timing.menu_arrow) # Down Arrow (Cursor over item to refine)
          tap(pad.cross,timing.medium)     # Cross (Select Item)
          tap(pad.down,timing.menu_arrow) # Down Arrow (In case this is HP up, we'll need 10)
          tap(pad.cross,timing.medium)     # Cross (Refine Item)
          tap(pad.triangle,timing.medium) # Triangle to return to ability menu
          tap(pad.left,timing.menu_page)   # Left Arrow (previous page of abilities)
          tap_repeated(pad.up, 3, timing.menu_arrow) # Up Arrow (Cursor over Call Shop)
        else:
          tap(pad.triangle,timing.medium) # Triangle to return to ability menu
          tap(pad.left,timing.menu_page)   # Left Arrow (previous page of abilities)
          tap_repeated(pad.up, 5, timing.menu_arrow) # Up Arrow (Cursor over Call Shop)
    return
  for count in range(num_want):
    tap(pad.cross,timing.select_long)     # Cross (select Call Shop)
    if count == 0:                                    # ONLY NEED TO DO THIS FOR THE FIRST PASS
      tap_repeated(pad.up, 4, timing.menu_arrow) # Up Arrow (place cursor on Esthar Pet Shop)
    tap(pad.cross,timing.medium)     # Cross (select Esthar Pet Shop)
    tap(pad.cross,timing.select_long)	# Cross (select Buy)
    tap(pad.right,timing.menu_page) # Right Arrow (select next page in menu)
    tap_repeated(pad.up, item_location, timing.menu_arrow)   # Up Arrow (place cursor over appropriate item)
    tap(pad.cross,timing.select_short)      # Cross (select item)
    tap_repeated(pad.up, 10, timing.quantity) # Up Arrow (Select the maximum of 100 items)
    tap(pad.cross,timing.select_medium)      # Cross (Purchase Item)
    return_to_ability_menu()
    tap(pad.right,timing.menu_page) # Right Arrow (Next page of abilities)
    tap_repeated(pad.down, 5, timing.menu_arrow) # Down Arrow (Cursor over GFAbl Med-RF)
    tap(pad.cross,timing.medium)     # Cross (select GFAbl Med-RF)
    tap(pad.down,timing.menu_arrow) # Down Arrow (Cursor over item to refine)
    tap(pad.cross,timing.medium)     # Cross (select item to refine)
    tap(pad.down,timing.menu_arrow) # Down Arrow (Choose quantity 10 items to refine)
    tap(pad.cross,timing.medium)     # Cross (refine)
    tap(pad.triangle,timing.medium) # Triangle to return to ability menu
    tap_repeated(pad.up, 2, timing.menu_arrow) # Up Arrow (Cursor over Forbid Med-RF)
    tap(pad.cross,timing.medium)     # Cross (select Forbid Med-RF)
    tap_repeated(pad.down, 2, timing.menu_arrow) # Down Arrow (Cursor over item to refine)
    tap(pad.cross,timing.medium)     # Cross (Select Item)
    tap(pad.down,timing.menu_arrow) # Down Arrow (In case this is HP up, we'll need 10)
    tap(pad.cross,timing.medium)     # Cross (Refine Item)
    tap(pad.triangle,timing.medium) # Triangle to return to ability menu
    tap(pad.left,timing.menu_page)   # Left Arrow (previous page of abilities)
    tap_repeated(pad.up, 3, timing.menu_arrow) # Up Arrow (Cursor over Call Shop)

print(f"""This script automates FF8 Esthar stat-up farming.

It will run {runloops} full farming pass(es).
It will {"spend existing Gil instead of running the money loop first" if use_existing_gil else "run the money loop before buying stat-up materials"}.

Optional arguments:
--passes=N             Number of full stat-up farming passes.
--current-hp-ups=N     Current HP Up count, to avoid overflowing 100 items.
--max-hp-ups=N         Maximum HP Up count to allow.
--use-existing-gil     Spend existing Gil instead of earning Gil first.

Before starting, make sure the first page of your item list looks like this:
1: 1 or more Mega-Potion
2: Zero or more Tent
3: Zero or more Cottage
4: 1 HP up
5: 1 Str Up
6: 1 Spr Up
7: 1 Mag Up
8: 1 Vit Up
Second, make sure you do not have any of the following in your inventory \
(sell them if you have to!): Giant's Ring, Gaea's Ring, Power Wrist, Hyper Wrist, \
Force Armlet, Magic Armlet, Hypno Crown, Royal Crown, Vit-J Scroll, Orihalcon, Adamantine

Stop the script with Ctrl-C.

Running now...""")


try:
  initial_setup()
  for num_passes in range(1,runloops+1):
    print("Beginning Pass: ", num_passes, " at ", datetime.now())
    get_stat_up('HP',1)
    get_stat_up('Str',1)
    get_stat_up('Spr',1)
    get_stat_up('Mag',1)
    get_stat_up('Vit',1)
  exit_to_map()
  pause_game()
except KeyboardInterrupt:
  print("\nStopped by Ctrl-C.")
finally:
  keyboard.release_all()

#!/usr/bin/env python3
"""
Interactive Combat Sandbox — test combat scenarios in isolation.
Pick a class, pick enemies, optionally equip gear, fight the real combat loop.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.engine import GameEngine, EQUIPMENT_DATABASE, CYAN, YELLOW, GREEN, RED, RESET, BOLD
from src.moves import get_moves_for_class
from src.bestiary import ALL_ENEMIES, get_enemy_by_name

CLASS_OPTIONS = {
    '1': ('Kira Nightwind', 'void_mage'),
    '2': ('Theron Ashford', 'knight'),
    '3': ('Vex Shadowstep', 'shadow'),
    '4': ('Elara Vance', 'merchant'),
    '5': ('Asha Ironheart', 'warden'),
}

CLASS_BASE_STATS = {
    'void_mage': {'strength': 4, 'dexterity': 6, 'intelligence': 8, 'charisma': 5,
                  'void_magic': 7, 'combat': 3, 'stealth': 4, 'influence': 2},
    'knight':    {'strength': 8, 'dexterity': 6, 'intelligence': 5, 'charisma': 6,
                  'void_magic': 0, 'combat': 9, 'stealth': 3, 'influence': 4},
    'shadow':    {'strength': 5, 'dexterity': 9, 'intelligence': 7, 'charisma': 6,
                  'void_magic': 0, 'combat': 4, 'stealth': 10, 'influence': 5},
    'merchant':  {'strength': 4, 'dexterity': 5, 'intelligence': 9, 'charisma': 8,
                  'void_magic': 0, 'combat': 2, 'stealth': 4, 'influence': 8},
    'warden':    {'strength': 7, 'dexterity': 6, 'intelligence': 5, 'charisma': 5,
                  'void_magic': 0, 'combat': 5, 'stealth': 3, 'influence': 2,
                  'nature_magic': 7, 'survival': 8},
}

EQUIP_SLOT_ORDER = ['weapon', 'armor', 'accessory']


def pick_class():
    print(f"\n{BOLD}{CYAN}═══ COMBAT SANDBOX ═══{RESET}")
    print(f"{'─' * 40}")
    print("Pick a character class:\n")
    for key, (name, cls) in CLASS_OPTIONS.items():
        moves = get_moves_for_class(cls)
        move_names = ", ".join(m.name for m in moves.values())
        print(f"  {YELLOW}[{key}]{RESET} {name:22} ({cls})")
        print(f"       Moves: {move_names}")
    print()
    while True:
        choice = input("Class [1-5]: ").strip()
        if choice in CLASS_OPTIONS:
            return CLASS_OPTIONS[choice]
        print(f"{RED}Pick 1-5.{RESET}")


def pick_enemies():
    enemies_list = []
    print(f"\n{BOLD}Available enemies:{RESET}\n")
    sorted_names = sorted(ALL_ENEMIES.keys(), key=lambda n: ALL_ENEMIES[n].hp)
    for i, key in enumerate(sorted_names, 1):
        en = ALL_ENEMIES[key]
        moves_str = ""
        if en.moves:
            moves_str = f" | moves: {', '.join(m.get('name', '?') for m in en.moves)}"
        print(f"  {YELLOW}[{i:2}]{RESET} {en.name:22} HP:{en.hp:3} ATK:{en.damage:2} "
              f"gold:{en.gold_drop:2}{moves_str}")

    print(f"\n  {YELLOW}[D]{RESET} Done selecting enemies")
    print("  (Pick 1-3 enemies from the list)\n")
    while len(enemies_list) < 3:
        choice = input(f"Enemy #{len(enemies_list) + 1}: ").strip().upper()
        if choice == 'D':
            break
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(sorted_names):
                key = sorted_names[idx]
                en = ALL_ENEMIES[key]
                enemies_list.append(en)
                print(f"  {GREEN}✓ Added {en.name}{RESET}")
            else:
                print(f"{RED}Invalid number.{RESET}")
        else:
            print(f"{RED}Enter a number or D to finish.{RESET}")

    if not enemies_list:
        print(f"{RED}No enemies selected, exiting.{RESET}")
        sys.exit(0)

    return enemies_list


def equip_items(engine):
    equip_keys = list(EQUIPMENT_DATABASE.keys())
    print(f"\n{BOLD}Available equipment:{RESET}\n")
    for i, key in enumerate(equip_keys, 1):
        eq = EQUIPMENT_DATABASE[key]
        bonus_str = ", ".join(f"+{v} {k}" for k, v in eq.bonuses.items())
        print(f"  {YELLOW}[{i:2}]{RESET} {eq.name:22} ({eq.slot:10}) {bonus_str}")
    print(f"\n  {YELLOW}[S]{RESET} Skip equipment")
    print(f"  {YELLOW}[D]{RESET} Done equipping\n")

    while True:
        choice = input("Item to equip [1-{}], S, D: ".format(len(equip_keys))).strip().upper()
        if choice == 'S' or choice == 'D':
            break
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(equip_keys):
                key = equip_keys[idx]
                engine.inventory.append(key)
                engine.equip_item(key)
            else:
                print(f"{RED}Invalid number.{RESET}")


def setup_engine(char_name, char_class):
    engine = GameEngine()
    engine.player = char_name
    engine.stats = CLASS_BASE_STATS[char_class].copy()
    return engine


def main():
    char_name, char_class = pick_class()
    enemies = pick_enemies()

    engine = setup_engine(char_name, char_class)

    eq_choice = input(f"\nEquip items? [Y/n]: ").strip().upper()
    if eq_choice != 'N':
        equip_items(engine)

    surprise_choice = input(f"\nSurprise round (enemies go first)? [y/N]: ").strip().upper()
    surprise = surprise_choice == 'Y'

    eff_stats = engine.get_effective_stats()
    print(f"\n{BOLD}{CYAN}═══ FINAL SETUP ═══{RESET}")
    print(f"  Character: {char_name} ({char_class})")
    print(f"  HP: {engine.health}/{engine.max_hp}  |  Mana: {engine.mana}/50")
    print(f"  STR:{eff_stats.get('strength',0)} DEX:{eff_stats.get('dexterity',0)} "
          f"INT:{eff_stats.get('intelligence',0)} CHA:{eff_stats.get('charisma',0)}")
    print(f"  Enemies: {', '.join(en.name for en in enemies)}")
    print(f"  Surprise: {'YES' if surprise else 'No'}")
    print(f"{'─' * 40}")

    input(f"\n{BOLD}Press ENTER to start combat!{RESET}")

    result = engine.combat_encounter(enemies, char_class, surprise=surprise)

    print(f"\n{BOLD}{GREEN if result else RED}═══ COMBAT {'VICTORY' if result else 'DEFEAT'} ═══{RESET}")
    if result:
        gold_str = f" | Gold earned: {getattr(engine, 'gold_earned', 0)}" if getattr(engine, 'gold_earned', 0) else ""
        print(f"  HP remaining: {engine.health}/{engine.max_hp}{gold_str}")

    retry = input(f"\nFight again? [Y/n]: ").strip().upper()
    if retry != 'N':
        print(f"{CYAN}Restarting...{RESET}")
        main()


if __name__ == '__main__':
    main()

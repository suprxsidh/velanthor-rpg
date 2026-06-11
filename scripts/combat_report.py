#!/usr/bin/env python3
"""
Combat Status Report — prints all combat encounters, enemies, gold, surprise flags.
Read-only; no game data modified.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.bestiary import ALL_ENEMIES, get_enemy_by_name
from src.moves import STATUS_EFFECTS


def get_enemy_status_effects(enemy):
    effects = set()
    for move in getattr(enemy, 'moves', []):
        eff = move.get('effect')
        if eff and eff in STATUS_EFFECTS:
            effects.add(eff)
    return effects


def main():
    BATTLE_ENEMY_MAP = {
        'KIRA_CH1_BANDITS': ['Bandit', 'Bandit'],
        'KIRA_CH1_WATCH_TRIAL': 'Watch Mercenary',
        'KIRA_CH1_CIRCLE_TRIAL': 'Circle Initiate',
        'KIRA_CH1_WASTELAND_BATTLE': 'Void Creature',
        'KIRA_CH1_BANDIT_AMBUSH': 'Cult Enforcer',
        'KIRA_CH1_GUARD_POST': 'Border Guard',
        'KIRA_CH1_SHADOW_WATCH': 'Hollow Knight',
        'KIRA_CH1_WASTELAND_STAND': 'Void Creature',
        'KIRA_CH2_BATTLE': 'Hollow Knight',
        'KIRA_CH2_PALACE_SURPRISE': 'Royal Guard',
        'KIRA_CH2_CATACOMB_GUARDIAN': 'Ancient Guardian',
        'KIRA_CH2_GUILD_INFILTRATE': 'Guild Enforcer',
        'KIRA_CH2_MAGE_TOWER': 'Corrupted Mage',
        'KIRA_CH2_STREET_FIGHT': 'Cult Priest',
        'KIRA_CH2_SHADOW_SQUAD': 'Hollow Knight',
        'KIRA_CH2_PALACE_ESCAPE': 'Royal Guard',
        'KIRA_CH3_TEMPLE_GUARDS': 'Hollow Knight',
        'KIRA_CH3_PRIESTS': 'Cult Priest',
        'KIRA_CH3_VESPERA_FIGHT': 'Vespera',
        'KIRA_CH3_FINAL_GUARDIAN': 'The Hollow King',
        'KIRA_CH3_BEAST': 'Void Beast',
        'KIRA_CH3_ALTAR_GUARDIANS': 'Void Golem',
        'KIRA_CH3_TEMPLE_ENTRANCE': 'Cultist Sentinel',
        'KIRA_CH2_PALACE_ENTER': 'Royal Guard',
        'THERON_CH1_AMBUSH': ['bandit', 'bandit'],
        'THERON_CH1_JOURNEY': 'bandit',
        'THERON_CH2_COMPANION': 'watch_mercenary',
        'THERON_CH2_BATTLE': 'cultist',
        'THERON_CH3_BATTLE': 'hollow_knight',
        'THERON_CH1_TAVERN_BRAWL': 'cultist',
        'THERON_CH1_STREET_AMBUSH': 'cultist',
        'THERON_CH1_WATCH_PATROL': 'watch_mercenary',
        'THERON_CH1_CULT_HUNTERS': 'cult_leader',
        'THERON_CH1_BORDER_SKIRMISH': 'watch_mercenary',
        'THERON_CH1_TAVERN_FIGHT': 'cultist',
        'THERON_CH1_NIGHT_ASSAULT': 'street_thug',
        'THERON_CH1_CULT_ENCOUNTER': 'cultist',
        'THERON_CH2_TEMPLE_ASSAULT': 'cultist',
        'THERON_CH2_PRIEST_FIGHT': 'cult_leader',
        'THERON_CH2_ESCORT_MISSION': 'cultist',
        'THERON_CH2_GUARD_POST': 'watch_mercenary',
        'THERON_CH2_AMBUSH_COUNTER': 'cultist',
        'THERON_CH2_PRISON_BREAK': 'hollow_guard',
        'THERON_CH2_RITUAL_INTERRUPT': 'cultist',
        'THERON_CH2_CULT_VANGUARD': 'hollow_knight',
        'THERON_CH3_TEMPLE_ENTRY': 'void_rat',
        'THERON_CH3_WARRIORS': 'hollow_knight',
        'THERON_CH3_VESPERA_DUEL': 'vespera',
        'THERON_CH3_FINAL_STAND': 'the_hollow_king',
        'THERON_CH3_BEAST_BATTLE': 'the_hollow_king',
        'VEX_CH1_DOCKS': ['guild_enforcer', 'street_thug'],
        'VEX_CH1_AMBUSH': 'Guild Enforcer',
        'VEX_CH2_SURRENDER': 'Guard',
        'VEX_CH2_FIGHT': 'Guild Enforcer',
        'VEX_CH1_DOCKS_CHASE': 'guild_enforcer',
        'VEX_CH1_GANG_ENCOUNTER': 'street_thug',
        'VEX_CH1_GUARD_PATROL': 'city_watch',
        'VEX_CH1_SMUGGLER_BATTLE': 'smuggler',
        'VEX_CH1_PICKPOCKET_GONE_WRONG': 'guild_enforcer',
        'VEX_CH1_ROOFTOP_ESCAPE': 'guild_enforcer',
        'VEX_CH1_STREET_AMBUSH': 'guild_enforcer',
        'VEX_CH1_WATCH_CHASE': 'city_watch',
        'VEX_CH1_FINAL_ESCAPE': 'guild_enforcer',
        'VEX_CH2_GUILD_HALL': 'guild_enforcer',
        'VEX_CH2_ASSASSIN_MISSION': 'guild_lieutenant',
        'VEX_CH2_RIVAL_THIEF': 'rival_thief',
        'VEX_CH2_WATCH_INFILTRATE': 'city_watch',
        'VEX_CH2_CULT_ROUTE': 'cultist',
        'VEX_CH2_SECRET_PASSAGE': 'guild_guard',
        'VEX_CH2_GUILD_ASSAULT': 'guild_enforcer',
        'VEX_CH3_TREASURE_HOUSE': 'shadowmaster',
        'VEX_CH3_GUILD_WAR': 'guild_enforcer',
        'VEX_CH3_BETRAYAL': 'corvus',
        'VEX_CH3_FINAL_THIEF': 'royal_guard',
        'VEX_CH3_SHADOW_FIGHT': 'vance_hunter',
        'ELARA_CH1_STRIKE': ['Watch Mercenary', 'Cultist'],
        'ELARA_CH2_MEETING': 'Cultist',
        'ELARA_CH2_ATTACK': 'Watch Mercenary',
        'ELARA_CH1_ESTATE_ASSAULT': 'Hollow Knight',
        'ELARA_CH1_GUARD_FIGHT': 'Watch Mercenary',
        'ELARA_CH1_CULT_INFILTRATE': 'Cultist',
        'ELARA_CH1_MERCHANT_WAR': 'Street Thug',
        'ELARA_CH1_ASSASSIN_ENCOUNTER': 'Cult Enforcer',
        'ELARA_CH2_NETWORK_BATTLE': 'Cultist',
        'ELARA_CH2_CIRCLE_ASSAULT': 'Hollow Knight',
        'ELARA_CH2_CULT_SURPRISE': 'Cult Enforcer',
        'ELARA_CH2_VAULT_HEIST': 'Void Golem',
        'ELARA_CH2_BETRAYAL': 'Cultist',
        'ELARA_CH2_CULT_VAULT': 'Hollow Knight',
        'ELARA_CH3_VAULT_BATTLE': 'Hollow Knight',
        'ELARA_CH3_FINAL_ASSULT': 'Cultist',
        'ELARA_CH3_VESPERA_CONFRONT': 'Vespera',
        'ELARA_CH3_CROWN_FIGHT': 'Vespera',
        'ELARA_CH3_VICTORY_BATTLE': 'Vespera',
        'ASHA_CH1_WOLF_ATTACK': 'Ashen Wolf',
        'ASHA_CH1_CULT_PURSUIT': ['Cultist', 'Cultist'],
        'ASHA_CH1_CORRUPTED_TREANT': 'Corrupted Treant',
        'ASHA_CH1_WASTES_BORDER': 'Wastes Scorpion',
        'ASHA_CH1_ESCAPE': 'Hollow Guard',
        'ASHA_CH2_INFILTRATE': 'Cultist',
        'ASHA_CH2_SCOUT': 'Watch Mercenary',
        'ASHA_CH2_AMBUSH': 'Hollow Guard',
        'ASHA_CH2_VOID_SERPENT': 'Void Serpent',
        'ASHA_CH2_TEMPLE_ASSAULT': 'Hollow Sentinel',
        'ASHA_CH3_FINAL_APPROACH': 'Hollow Knight',
        'ASHA_CH3_CULT_VANGUARD': 'Cult Leader',
        'ASHA_CH3_VESPERA_CONFRONT': 'Vespera',
        'ASHA_CH3_HOLLOW_KING': 'The Hollow King',
        'ASHA_CH4_GUARDIAN_TRIAL': 'Guardian of the North',
        'ASHA_CH4_FINAL_STAND': 'The Hollow King',
    }

    SURPRISE_ENCOUNTERS = {
        'THERON_CH1_AMBUSH',
        'VEX_CH1_DOCKS',
        'ASHA_CH1_WOLF_ATTACK',
    }

    CYAN = "\033[1;36m"
    YELLOW = "\033[1;33m"
    GREEN = "\033[1;32m"
    RED = "\033[1;31m"
    BOLD = "\033[1m"
    RESET = "\033[0m"
    MAGENTA = "\033[1;35m"

    def resolve_enemies(entry):
        if isinstance(entry, list):
            return entry
        return [entry]

    def get_enemy_info(name):
        return get_enemy_by_name(name)

    print(f"\n{BOLD}{CYAN}═══ COMBAT ENCOUNTER REPORT ═══{RESET}\n")

    total_encounters = len(BATTLE_ENEMY_MAP)
    multi_count = 0
    surprise_count = len(SURPRISE_ENCOUNTERS)
    total_gold = 0
    all_effects = set()
    enemies_seen = set()

    prev_char = ""
    for scene_id in sorted(BATTLE_ENEMY_MAP.keys()):
        char = scene_id.split('_')[0]
        if char != prev_char:
            if prev_char:
                print()
            print(f" {BOLD}{YELLOW}{char}{RESET}")
            prev_char = char

        raw = BATTLE_ENEMY_MAP[scene_id]
        names = resolve_enemies(raw)
        count = len(names)
        if count > 1:
            multi_count += 1

        detected_enemies = []
        total_gold_here = 0
        effects_here = set()
        has_aoe = False

        for name in names:
            en = get_enemy_info(name)
            if en:
                detected_enemies.append(en)
                total_gold_here += getattr(en, 'gold_drop', 0)
                enemies_seen.add(en.name)
                for move in getattr(en, 'moves', []):
                    eff = move.get('effect')
                    if eff and eff in STATUS_EFFECTS:
                        all_effects.add(eff)
                        effects_here.add(eff)

                aoe_moves_here = [m for m in getattr(en, 'moves', []) if m.get('aoe')]
                if aoe_moves_here:
                    has_aoe = True

        is_surprise = scene_id in SURPRISE_ENCOUNTERS
        sur_tag = f" {RED}[SURPRISE]{RESET}" if is_surprise else ""
        multi_tag = f" {MAGENTA}[MULTI x{count}]{RESET}" if count > 1 else ""

        eff_tags = ""
        if effects_here:
            eff_tags = f" {GREEN}[{','.join(sorted(effects_here))}]{RESET}"

        gold_tag = f" {YELLOW}[{total_gold_here}g]{RESET}" if total_gold_here > 0 else ""
        total_gold += total_gold_here

        name_str = " + ".join(n.name for n in detected_enemies) if detected_enemies else " + ".join(names)
        padded = f"  {scene_id:45} {name_str:30}{multi_tag}{gold_tag}{sur_tag}{eff_tags}"
        print(padded)

    print(f"\n{BOLD}{CYAN}{'═' * 72}{RESET}")
    print(f"  Total encounters: {total_encounters}")
    print(f"  Multi-enemy:      {multi_count}")
    print(f"  Surprise rounds:  {surprise_count}")
    print(f"  Unique enemies:   {len(enemies_seen)}")
    print(f"  Total gold pool:  {total_gold}")
    print(f"  Status effects:   {', '.join(sorted(all_effects)) if all_effects else 'None (enemy-applied)'}")

    print(f"\n{BOLD}Status effect definitions:{RESET}")
    for name, data in sorted(STATUS_EFFECTS.items()):
        penalty = f", stat: {data['stat_penalty']}" if data.get('stat_penalty') else ""
        print(f"  {name:10} | dmg/turn: {data['damage']} | turns: {data['turns']}{penalty}")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Velanthor RPG - Main Entry Point
A dark fantasy choice-based terminal RPG.
"""

import sys
import os
import json
import random

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.engine import GameEngine, CYAN, YELLOW, GREEN, RED, RESET, BOLD
from scripts.intro import display_intro, get_characters, show_character_selection
from src.bestiary import get_enemy_by_name

# Character class mapping (from intro.py choice letters)
CHAR_CLASS_MAP = {
    'A': 'void_mage',  # Kira
    'B': 'knight',    # Theron
    'C': 'shadow',    # Vex
    'D': 'merchant',  # Elara
    'E': 'warden',    # Asha
}

# Full character data for game creation (not in intro.py)
CHARACTER_DATA = {
    'A': {
        'name': 'Kira Nightwind',
        'class': 'void_mage',
        'stats': {'strength': 4, 'dexterity': 6, 'intelligence': 8, 'charisma': 5, 'void_magic': 7, 'combat': 3, 'stealth': 4, 'influence': 2},
        'inventory': ["void spellbook", "mother's locket"],
        'start_scene': 'KIRA_CH1_THORNWICK',
        'mana': 40
    },
    'B': {
        'name': 'Theron Ashford',
        'class': 'knight',
        'stats': {'strength': 8, 'dexterity': 6, 'intelligence': 5, 'charisma': 6, 'void_magic': 0, 'combat': 9, 'stealth': 3, 'influence': 4},
        'inventory': ['rusty sword', 'old shield'],
        'start_scene': 'THERON_CH1_TAVERN',
        'mana': 30
    },
    'C': {
        'name': 'Vex Shadowstep',
        'class': 'shadow',
        'stats': {'strength': 5, 'dexterity': 9, 'intelligence': 7, 'charisma': 6, 'void_magic': 0, 'combat': 4, 'stealth': 10, 'influence': 5},
        'inventory': ['lockpicking tools', 'crown piece'],
        'start_scene': 'VEX_CH1_DOCKS',
        'mana': 25
    },
    'D': {
        'name': 'Elara Vance',
        'class': 'merchant',
        'stats': {'strength': 4, 'dexterity': 5, 'intelligence': 9, 'charisma': 8, 'void_magic': 0, 'combat': 2, 'stealth': 4, 'influence': 8},
        'inventory': ['trading ledger', 'letter of credit'],
        'start_scene': 'ELARA_CH1_ESTATE',
        'mana': 35
    },
    'E': {
        'name': 'Asha Ironheart',
        'class': 'warden',
        'stats': {'strength': 7, 'dexterity': 6, 'intelligence': 5, 'charisma': 5, 'void_magic': 0, 'combat': 5, 'stealth': 3, 'influence': 2, 'nature_magic': 7, 'survival': 8},
        'inventory': ['druid staff', 'ancient talisman'],
        'start_scene': 'ASHA_CH1_VILLAGE',
        'mana': 40
    },
}

# Battle scene to enemy mapping
BATTLE_ENEMY_MAP = {
    'KIRA_CH1_BANDITS': 'Bandit',
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
    'THERON_CH1_AMBUSH': 'bandit',
    'THERON_CH1_JOURNEY': 'bandit',
    'THERON_CH2_COMPANION': 'watch_mercenary',
    'THERON_CH2_BATTLE': 'cultist',
    'THERON_CH3_BATTLE': 'hollow_knight',
    # New Theron Chapter 1 Battle Scenes
    'THERON_CH1_TAVERN_BRAWL': 'cultist',
    'THERON_CH1_STREET_AMBUSH': 'cultist',
    'THERON_CH1_WATCH_PATROL': 'watch_mercenary',
    'THERON_CH1_CULT_HUNTERS': 'cult_leader',
    'THERON_CH1_BORDER_SKIRMISH': 'watch_mercenary',
    'THERON_CH1_TAVERN_FIGHT': 'cultist',
    'THERON_CH1_NIGHT_ASSAULT': 'street_thug',
    'THERON_CH1_CULT_ENCOUNTER': 'cultist',
    # New Theron Chapter 2 Battle Scenes
    'THERON_CH2_TEMPLE_ASSAULT': 'cultist',
    'THERON_CH2_PRIEST_FIGHT': 'cult_leader',
    'THERON_CH2_ESCORT_MISSION': 'cultist',
    'THERON_CH2_GUARD_POST': 'watch_mercenary',
    'THERON_CH2_AMBUSH_COUNTER': 'cultist',
    'THERON_CH2_PRISON_BREAK': 'hollow_guard',
    'THERON_CH2_RITUAL_INTERRUPT': 'cultist',
    'THERON_CH2_CULT_VANGUARD': 'hollow_knight',
    # New Theron Chapter 3 Battle Scenes
    'THERON_CH3_TEMPLE_ENTRY': 'void_rat',
    'THERON_CH3_WARRIORS': 'hollow_knight',
    'THERON_CH3_VESPERA_DUEL': 'vespera',
    'THERON_CH3_FINAL_STAND': 'the_hollow_king',
    'THERON_CH3_BEAST_BATTLE': 'the_hollow_king',
    'VEX_CH1_DOCKS': 'guild_enforcer',
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
    'ELARA_CH1_STRIKE': 'Watch Mercenary',
    'ELARA_CH2_MEETING': 'Cultist',
    'ELARA_CH2_ATTACK': 'Watch Mercenary',
    # New Elara Chapter 1 Battle Scenes
    'ELARA_CH1_ESTATE_ASSAULT': 'Hollow Knight',
    'ELARA_CH1_GUARD_FIGHT': 'Watch Mercenary',
    'ELARA_CH1_CULT_INFILTRATE': 'Cultist',
    'ELARA_CH1_MERCHANT_WAR': 'Street Thug',
    'ELARA_CH1_ASSASSIN_ENCOUNTER': 'Cult Enforcer',
    # New Elara Chapter 2 Battle Scenes
    'ELARA_CH2_NETWORK_BATTLE': 'Cultist',
    'ELARA_CH2_CIRCLE_ASSAULT': 'Hollow Knight',
    'ELARA_CH2_CULT_SURPRISE': 'Cult Enforcer',
    'ELARA_CH2_VAULT_HEIST': 'Void Golem',
    'ELARA_CH2_BETRAYAL': 'Cultist',
    'ELARA_CH2_CULT_VAULT': 'Hollow Knight',
    # New Elara Chapter 3 Battle Scenes
    'ELARA_CH3_VAULT_BATTLE': 'Hollow Knight',
    'ELARA_CH3_FINAL_ASSULT': 'Cultist',
    'ELARA_CH3_VESPERA_CONFRONT': 'Vespera',
    'ELARA_CH3_CROWN_FIGHT': 'Vespera',
    'ELARA_CH3_VICTORY_BATTLE': 'Vespera',
    # Asha (Warden) Chapter 1 Battle Scenes
    'ASHA_CH1_WOLF_ATTACK': 'Ashen Wolf',
    'ASHA_CH1_CULT_PURSUIT': 'Cultist',
    'ASHA_CH1_CORRUPTED_TREANT': 'Corrupted Treant',
    'ASHA_CH1_WASTES_BORDER': 'Wastes Scorpion',
    'ASHA_CH1_ESCAPE': 'Hollow Guard',
    # Asha Chapter 2 Battle Scenes
    'ASHA_CH2_INFILTRATE': 'Cultist',
    'ASHA_CH2_SCOUT': 'Watch Mercenary',
    'ASHA_CH2_AMBUSH': 'Hollow Guard',
    'ASHA_CH2_VOID_SERPENT': 'Void Serpent',
    'ASHA_CH2_TEMPLE_ASSAULT': 'Hollow Sentinel',
    # Asha Chapter 3 Battle Scenes
    'ASHA_CH3_FINAL_APPROACH': 'Hollow Knight',
    'ASHA_CH3_CULT_VANGUARD': 'Cult Leader',
    'ASHA_CH3_VESPERA_CONFRONT': 'Vespera',
    'ASHA_CH3_HOLLOW_KING': 'The Hollow King',
    # Asha Chapter 4 Battle Scenes
    'ASHA_CH4_GUARDIAN_TRIAL': 'Guardian of the North',
    'ASHA_CH4_FINAL_STAND': 'The Hollow King',
}

# Stealth-based bypass: scenes where high stealth can skip combat
STEALTH_BYPASS_SCENES = {
    'VEX_CH1_AMBUSH': {'dc': 12, 'stat': 'stealth', 'skip_scene': 'VEX_CH1_SISTER'},
    'VEX_CH2_FIGHT': {'dc': 14, 'stat': 'stealth', 'skip_scene': None},
}

# Influence-based alternatives for merchant class
INFLUENCE_ALTERNATIVES = {
    'ELARA_CH2_ATTACK': {
        'bribe': {'gold_cost': 20, 'skip_scene': 'ELARA_CH3_VAULT'},
        'intimidate': {'dc': 12, 'stat': 'charisma', 'skip_scene': 'ELARA_CH3_VAULT'},
    }
}


def get_character_class(engine):
    """Get character's combat class based on player name."""
    if not engine.player:
        return 'knight'
    name_lower = engine.player.lower()
    if 'kira' in name_lower:
        return 'void_mage'
    elif 'theron' in name_lower:
        return 'knight'
    elif 'vex' in name_lower:
        return 'shadow'
    elif 'elara' in name_lower:
        return 'merchant'
    elif 'asha' in name_lower:
        return 'warden'
    return 'knight'


def is_battle_scene(scene_id):
    """Check if scene ID indicates a battle/ambush/fight scene."""
    if not scene_id:
        return False
    scene_upper = scene_id.upper()
    # Check keywords OR if scene is in BATTLE_ENEMY_MAP
    return 'BATTLE' in scene_upper or 'AMBUSH' in scene_upper or '_FIGHT' in scene_upper or scene_id in BATTLE_ENEMY_MAP


def get_enemy_for_scene(scene_id):
    """Get enemy for a battle scene."""
    return BATTLE_ENEMY_MAP.get(scene_id)


def load_story_scenes():
    """Load story scenes from JSON."""
    try:
        with open('data/story.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{RED}Story data not found. Run story_parser.py first.{RESET}")
        return {}


def create_character(choice, engine):
    """Set up player based on character choice."""
    
    if choice not in CHARACTER_DATA:
        return None
    
    char = CHARACTER_DATA[choice]
    engine.player = char['name']
    engine.stats = char['stats'].copy()
    engine.inventory = char['inventory'].copy()
    engine.current_scene = char['start_scene']
    engine.mana = char.get('mana', 30)
    
    return engine


def display_scene(scene_data, engine):
    """Display a scene and handle choices."""
    print(f"\n{BOLD}{CYAN}{'─' * 60}{RESET}")
    
    # Show scene description
    description = scene_data.get('description', '').strip()
    if description:
        print(description)
    
    # Check for ending
    if 'ending' in scene_data:
        ending = scene_data['ending']
        print(f"\n{BOLD}{GREEN}═══ ENDING: {ending} ═══{RESET}")
        return 'ending'
    
    # Show choices - hide all technical tags from user
    choices = scene_data.get('choices', [])
    if choices:
        print(f"\n{BOLD}What do you do?{RESET}")
        for choice in choices:
            letter = choice['letter']
            text = choice['text']
            # Hide all technical tags - just show letter and text
            print(f"  {YELLOW}[{letter}]{RESET} {text}")
    else:
        # No choices - auto-advance immediately without prompting
        return 'auto'
    
    return 'continue'


def handle_choice(scene_data, choice_letter, engine, scenes):
    """Process player choice and navigate to next scene."""
    choices = scene_data.get('choices', [])
    
    # Find choice - exact match OR first available
    chosen_choice = None
    for choice in choices:
        if choice['letter'].upper() == choice_letter.upper():
            chosen_choice = choice
            break
    
    # If no exact match, use first available choice
    if not chosen_choice and choices:
        chosen_choice = choices[0]
        print(f"{YELLOW}Using {chosen_choice['letter']} instead.{RESET}")
    
    if chosen_choice:
        # Check requirements
        req = chosen_choice.get('requires')
        if req:
            meets_req, fail_msg = engine.check_requirements(req)
            if not meets_req:
                print(f"{RED}Cannot: {fail_msg}{RESET}")
                return engine.current_scene
        
        # Apply effects
        effects = chosen_choice.get('effects', {})
        for stat, value in effects.items():
            if stat in engine.stats:
                engine.stats[stat] += value
        
        # Navigate to next scene
        next_scene = chosen_choice.get('leads_to')
        if next_scene and next_scene in scenes:
            return next_scene
        elif next_scene:
            return None
    
    print(f"{YELLOW}Invalid choice.{RESET}")
    return scene_data.get('id', engine.current_scene)


def show_tutorial():
    """Show the tutorial."""
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════╗
║                      TUTORIAL                              ║
╚══════════════════════════════════════════════════════════════╝{RESET}

{YELLOW}MAKING CHOICES:{RESET}
  - Each scene presents choices labeled [A], [B], [C], [D]
  - Type the letter and press ENTER to choose
  - Some choices require certain stats (shown in {YELLOW}yellow{RESET})

{YELLOW}STATS:{RESET}
  - STR (Strength): Physical power, combat damage
  - DEX (Dexterity): Agility, stealth, dodging
  - INT (Intelligence): Knowledge, puzzle solving
  - CHA (Charisma): Persuasion, leadership
  - Class skills: Void Magic, Combat, Stealth, Influence

{YELLOW}COMBAT:{RESET}
  - [A] Attack: Roll STR + Combat vs enemy defense
  - [B] Defend: Reduce incoming damage
  - [C] Use Skill: Class-specific abilities
  - [D] Flee: Attempt to escape

{YELLOW}TIPS:{RESET}
  - Type {CYAN}stats{RESET} anytime to view your stats
  - Type {CYAN}inventory{RESET} to check your items
  - Type {CYAN}save{RESET} to save your progress
  - Type {CYAN}quit{RESET} to exit

{GREEN}Good luck, traveler. The fate of Velanthor rests with you.{RESET}
""")
    input("\nPress ENTER to begin...")


def main():
    """Main game loop."""
    # Load story data
    scenes = load_story_scenes()
    if not scenes:
        return
    
    engine = GameEngine()
    
    # Show intro
    display_intro()
    
    # Check for saved game and handle continuation
    import os
    save_exists = os.path.exists('savegame.json')
    should_continue = False
    
    if save_exists:
        print(f"\n{YELLOW}You have a saved game.{RESET}")
        print(f"  {YELLOW}[C]{RESET} Continue")
        print(f"  {YELLOW}[N]{RESET} New game")
        
        save_choice = input("\nChoice: ").strip().upper()
        
        if save_choice == 'C':
            engine = GameEngine()
            if engine.load_game('savegame.json'):
                should_continue = True
                print(f"{GREEN}Continuing your adventure as {engine.player}...{RESET}")
            else:
                print(f"{YELLOW}Save corrupted. Starting new game.{RESET}")
        elif save_choice == 'N':
            pass  # New game
        else:
            pass  # Default to new game
    
    if not should_continue:
        # Character selection
        characters = get_characters()
        choice = show_character_selection(characters)
        
        if choice not in characters:
            print(f"{RED}Invalid choice. Exiting.{RESET}")
            return
        
        # Create character
        create_character(choice, engine)
        
        print(f"\n{GREEN}You are now {engine.player}, a {characters[choice]['class']}.{RESET}")
        
        # Show tutorial only on new game
        show_tutorial()
    
    # Main game loop - story navigation
    while True:
        scene_id = engine.current_scene
        
        if not scene_id:
            print(f"\n{BOLD}{CYAN}THE END{RESET}")
            break
        
        if scene_id not in scenes:
            print(f"\n{RED}Scene not found: {scene_id}{RESET}")
            break
        
        scene_data = scenes[scene_id]
        
        # Check for battle scenes - trigger combat before description
        if is_battle_scene(scene_id):
            char_class = get_character_class(engine)
            
            # Check for stealth bypass (Vex with high stealth)
            if scene_id in STEALTH_BYPASS_SCENES and char_class == 'shadow':
                bypass_info = STEALTH_BYPASS_SCENES[scene_id]
                stealth_val = engine.stats.get(bypass_info['stat'], 0)
                stealth_roll = random.randint(1, 20) + stealth_val
                
                print(f"\n{CYAN}═══ STEALTH OPPORTUNITY ═══{RESET}")
                print(f"Your stealth prowess might allow you to bypass this encounter...")
                print(f"{YELLOW}[S]{RESET} Attempt stealth bypass (DC {bypass_info['dc']}, Roll: {stealth_roll})")
                print(f"{YELLOW}[F]{RESET} Engage in combat instead")
                
                bypass_choice = input("\nChoice: ").strip().upper()
                
                if bypass_choice == 'S' and stealth_roll >= bypass_info['dc']:
                    print(f"{GREEN}✓ You slip past undetected!{RESET}")
                    # Grant stealth stat bonus for bypassing
                    engine.stats['stealth'] = engine.stats.get('stealth', 0) + 1
                    if bypass_info['skip_scene']:
                        engine.current_scene = bypass_info['skip_scene']
                        continue
                else:
                    if bypass_choice == 'S':
                        print(f"{YELLOW}Stealth failed. Engaging combat...{RESET}")
                    else:
                        print(f"{YELLOW}You choose to fight.{RESET}")
            
            # Check for influence alternatives (Elara - merchant class)
            if scene_id in INFLUENCE_ALTERNATIVES and char_class == 'merchant':
                alt = INFLUENCE_ALTERNATIVES[scene_id]
                print(f"\n{CYAN}═══ ALTERNATIVE OPTIONS ═══{RESET}")
                print(f"{YELLOW}[C]{RESET} Combat")
                print(f"{YELLOW}[B]{RESET} Bribe (Cost: {alt['bribe']['gold_cost']} gold)")
                print(f"{YELLOW}[I]{RESET} Intimidate (DC {alt['intimidate']['dc']})")
                
                alt_choice = input("\nChoice: ").strip().upper()
                
                if alt_choice == 'B':
                    if engine.gold >= alt['bribe']['gold_cost']:
                        engine.gold -= alt['bribe']['gold_cost']
                        print(f"{GREEN}✓ You bribe your way through! (-{alt['bribe']['gold_cost']} gold){RESET}")
                        engine.stats['influence'] = engine.stats.get('influence', 0) + 1
                        engine.current_scene = alt['bribe']['skip_scene']
                        continue
                    else:
                        print(f"{RED}Not enough gold! ({engine.gold}/{alt['bribe']['gold_cost']}){RESET}")
                        print("Falling back to combat...")
                elif alt_choice == 'I':
                    cha_roll = random.randint(1, 20) + engine.stats.get('charisma', 0)
                    if cha_roll >= alt['intimidate']['dc']:
                        print(f"{GREEN}✓ Your presence strikes fear! You intimidate them into submission.{RESET}")
                        engine.stats['charisma'] = engine.stats.get('charisma', 0) + 1
                        engine.current_scene = alt['intimidate']['skip_scene']
                        continue
                    else:
                        print(f"{RED}✗ Intimidation failed!{RESET}")
                        print("Falling back to combat...")
                else:
                    print(f"{YELLOW}Choosing combat.{RESET}")
            
            enemy_name = get_enemy_for_scene(scene_id)
            if enemy_name:
                enemy = get_enemy_by_name(enemy_name)
                if enemy:
                    print(f"\n{RED}⚔ COMBAT ENCOUNTER: {enemy.name} ⚔{RESET}")
                    victory = engine.combat_encounter(enemy, char_class)
                    if not victory:
                        print(f"\n{RED}You have fallen in battle...{RESET}")
                        engine.current_scene = None
                        break
                    print(f"\n{GREEN}VICTORY! You defeated {enemy.name}!{RESET}")
        
        # Display scene
        result = display_scene(scene_data, engine)
        
        if result == 'ending':
            break
        
        # Auto-advance through scenes without choices - immediate, no prompt
        if result == 'auto':
            char_prefix = scene_id.split('_')[0]
            # Sort scenes properly
            all_scenes = sorted([s for s in scenes.keys() if s.startswith(char_prefix)],
                               key=lambda x: int(x.split('_CH')[1].split('_')[0]) if '_CH' in x else 0)
            
            current_idx = all_scenes.index(scene_id) if scene_id in all_scenes else 0
            
            # Find next scene with choices AFTER current
            next_scene = None
            for i in range(current_idx + 1, len(all_scenes)):
                sid = all_scenes[i]
                if len(scenes[sid].get('choices', [])) > 0:
                    next_scene = sid
                    break
            
            # If no next with choices, try ANY next scene (will auto-advance again)
            if not next_scene and current_idx + 1 < len(all_scenes):
                next_scene = all_scenes[current_idx + 1]
            
            if next_scene:
                engine.current_scene = next_scene
                continue
            else:
                print(f"\n{RED}End of story path.{RESET}")
                break
        
        # Get player choice
        choice_input = input(f"\n{RESET}> ").strip().upper()
        
        # Handle empty input
        if choice_input == '':
            continue
        
        if choice_input in ['QUIT', 'EXIT']:
            print(f"{YELLOW}Are you sure you want to quit? (y/n){RESET}")
            if input("> ").strip().lower() == 'y':
                break
        elif choice_input == 'STATS':
            engine.show_stats()
            continue
        elif choice_input == 'INVENTORY':
            engine.show_inventory()
            continue
        elif choice_input == 'EQUIP':
            engine.show_equipment()
            continue
        elif choice_input == 'ITEMS':
            engine.show_items()
            continue
        elif choice_input.startswith('EQUIP '):
            item_name = choice_input[5:].strip().lower().replace(' ', '_')
            engine.equip_item(item_name)
            continue
        elif choice_input.startswith('USE '):
            item_name = choice_input[4:].strip().lower().replace(' ', '_')
            engine.use_item(item_name)
            continue
        elif choice_input == 'HELP':
            show_tutorial()
            continue
        elif choice_input == 'SAVE':
            engine.save_game('savegame.json')
            continue
        elif choice_input == 'LOAD':
            if engine.load_game('savegame.json'):
                print(f"{GREEN}Game loaded.{RESET}")
            continue
        
        # Handle story choice
        next_scene = handle_choice(scene_data, choice_input, engine, scenes)
        
        # If leads_to scene doesn't exist OR leads_to is None, find next with choices
        if not next_scene or next_scene not in scenes:
            char_prefix = scene_id.split('_')[0]
            # Get all scenes for this character, sorted by chapter
            all_scenes = sorted([s for s in scenes.keys() if s.startswith(char_prefix)], 
                              key=lambda x: int(x.split('_CH')[1].split('_')[0]) if '_CH' in x else 0)
            
            current_idx = all_scenes.index(scene_id) if scene_id in all_scenes else 0
            
            # Find next scene AFTER current with choices
            next_scene = None
            for i in range(current_idx + 1, len(all_scenes)):
                sid = all_scenes[i]
                if len(scenes[sid].get('choices', [])) > 0:
                    next_scene = sid
                    break
            
            # If no next with choices, look for ANY next scene (will auto-advance)
            if not next_scene and current_idx + 1 < len(all_scenes):
                next_scene = all_scenes[current_idx + 1]
        
        engine.current_scene = next_scene
    
    print(f"\n{CYAN}Thanks for playing Velanthor!{RESET}")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Velanthor RPG - Core Game Engine
A terminal-based choice RPG with stats, inventory, and branching narratives.
"""

import json
import os
import sys
import random
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Dict, List
from src.moves import get_moves_for_class, Move, STATUS_EFFECTS
from src.bestiary import Enemy, get_enemy_by_name

# ANSI color codes
CYAN = "\033[1;36m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
GREEN = "\033[1;32m"
RESET = "\033[0m"
BOLD = "\033[1m"
MAGENTA = "\033[1;35m"


# ============== EQUIPMENT SYSTEM ==============

@dataclass
class Equipment:
    """Represents equippable gear."""
    name: str
    slot: str  # weapon, armor, accessory
    bonuses: Dict[str, int]  # stat bonuses
    description: str = ""
    
    def __repr__(self):
        bonus_str = ", ".join(f"+{v} {k}" for k, v in self.bonuses.items())
        return f"{self.name} ({self.slot}): {bonus_str}"


# Equipment Database
EQUIPMENT_DATABASE = {
    # Weapons
    "void_blade": Equipment(
        name="Void Blade",
        slot="weapon",
        bonuses={"void_magic": 2, "combat": 1},
        description="A blade forged from void energy. Increases void magic."
    ),
    "druid_staff": Equipment(
        name="Druid Staff",
        slot="weapon",
        bonuses={"nature_magic": 2, "intelligence": 1},
        description="A staff blessed by forest spirits. Enhances nature magic."
    ),
    "shadow_daggers": Equipment(
        name="Shadow Daggers",
        slot="weapon",
        bonuses={"stealth": 2, "dexterity": 2},
        description="Twin daggers that hide in shadow. Increases stealth."
    ),
    "knights_sword": Equipment(
        name="Knight's Sword",
        slot="weapon",
        bonuses={"combat": 3, "strength": 1},
        description="A well-balanced blade. Increases combat skill."
    ),
    "arcane_staff": Equipment(
        name="Arcane Staff",
        slot="weapon",
        bonuses={"intelligence": 2, "void_magic": 1},
        description="A staff of polished wood with an enchanted crystal."
    ),
    
    # Armor
    "knight_plate": Equipment(
        name="Knight Plate",
        slot="armor",
        bonuses={"health": 15, "defense": 2},
        description="Heavy plate armor. Provides significant protection."
    ),
    "ranger_cloak": Equipment(
        name="Ranger Cloak",
        slot="armor",
        bonuses={"dexterity": 2, "stealth": 1},
        description="A cloaked vestment favored by forest scouts."
    ),
    "warden_vestments": Equipment(
        name="Warden Vestments",
        slot="armor",
        bonuses={"nature_magic": 2, "survival": 1},
        description="Ceremonial garb of the Warden order."
    ),
    "leather_armor": Equipment(
        name="Leather Armor",
        slot="armor",
        bonuses={"health": 8, "dexterity": 1},
        description="Light leather armor. Good for mobility."
    ),
    "mage_robes": Equipment(
        name="Mage Robes",
        slot="armor",
        bonuses={"void_magic": 2, "intelligence": 1},
        description="Enchanted robes that enhance magical ability."
    ),
    
    # Accessories
    "ring_of_protection": Equipment(
        name="Ring of Protection",
        slot="accessory",
        bonuses={"defense": 1, "health": 5},
        description="A simple ring with minor protective enchantment."
    ),
    "amulet_of_healing": Equipment(
        name="Amulet of Healing",
        slot="accessory",
        bonuses={"health": 10},
        description="An amulet that slowly regenerates health."
    ),
    "charm_of_fortune": Equipment(
        name="Charm of Fortune",
        slot="accessory",
        bonuses={"charisma": 2, "luck": 1},
        description="A charm said to bring good luck to its wearer."
    ),
    "talisman_of_power": Equipment(
        name="Talisman of Power",
        slot="accessory",
        bonuses={"void_magic": 2, "nature_magic": 2},
        description="A powerful artifact channeling magical energy."
    ),
    "boots_of_swiftness": Equipment(
        name="Boots of Swiftness",
        slot="accessory",
        bonuses={"dexterity": 3},
        description="Enchanted boots that increase movement speed."
    ),
}


# ============== ITEMS SYSTEM ==============

@dataclass
class Item:
    """Represents a consumable item."""
    name: str
    item_type: str  # healing, mana, defensive, utility
    effect: Dict[str, int]  # effects like {"health": 25}
    description: str = ""
    uses: int = 1
    cost: int = 0  # gold value


# Item Database
ITEM_DATABASE = {
    # Healing Items
    "health_potion": Item(
        name="Health Potion",
        item_type="healing",
        effect={"health": 25},
        description="Restores 25 HP",
        uses=1,
        cost=15
    ),
    "healing_shard": Item(
        name="Healing Shard",
        item_type="healing",
        effect={"health": 50},
        description="Restores 50 HP",
        uses=1,
        cost=30
    ),
    "herbal_remedy": Item(
        name="Herbal Remedy",
        item_type="healing",
        effect={"health": 15, "clears_poison": 1},
        description="Restores 15 HP and cures poison",
        uses=1,
        cost=10
    ),
    
    # Mana Items
    "mana_crystal": Item(
        name="Mana Crystal",
        item_type="mana",
        effect={"mana": 20},
        description="Restores 20 Mana",
        uses=1,
        cost=12
    ),
    "essence_vial": Item(
        name="Essence Vial",
        item_type="mana",
        effect={"mana": 40},
        description="Restores 40 Mana",
        uses=1,
        cost=25
    ),
    
    # Defensive Items
    "cloak_of_defense": Item(
        name="Cloak of Defense",
        item_type="defensive",
        effect={"temp_defense": 3},
        description="Provides +3 defense for one battle",
        uses=1,
        cost=20
    ),
    "iron_ward": Item(
        name="Iron Ward",
        item_type="defensive",
        effect={"temp_health": 15},
        description="Provides +15 temporary HP",
        uses=1,
        cost=25
    ),
    
    # Utility Items
    "antidote": Item(
        name="Antidote",
        item_type="utility",
        effect={"clears_poison": 1},
        description="Cures poison status",
        uses=1,
        cost=8
    ),
    "flashbang": Item(
        name="Flashbang",
        item_type="utility",
        effect={"escape_bonus": 5},
        description="+5 to escape attempts",
        uses=1,
        cost=5
    ),
    "lockpick_set": Item(
        name="Lockpick Set",
        item_type="utility",
        effect={"unlocks": 1},
        description="One-time unlock bonus",
        uses=1,
        cost=10
    ),
}


# ============== STATUS EFFECTS ==============

@dataclass
class StatusEffect:
    """Represents a combat status effect."""
    name: str
    effect_type: str  # poison, bleed, stun, regen, barrier, void_corruption
    amount: int  # damage/heal per turn
    duration: int  # turns remaining
    description: str


# ============== GAME ENGINE ==============

class GameEngine:
    """Core game engine for Velanthor RPG."""
    
    def __init__(self):
        self.player = None
        self.stats = {
            "strength": 4,
            "dexterity": 4,
            "intelligence": 4,
            "charisma": 4,
            "void_magic": 0,
            "combat": 0,
            "stealth": 0,
            "influence": 0,
            "nature_magic": 0,
            "survival": 0,
            "defense": 0,
            "luck": 0
        }
        self.inventory = []
        self.equipped = {
            "weapon": None,
            "armor": None,
            "accessory": None
        }
        self.items = {}  # name -> count
        self.status_effects: List[StatusEffect] = []
        self.flags = {}
        self.current_scene = None
        self.humanity = 10
        self.health = 100
        self.mana = 50
        self.gold = 10
        self.relationships = {}
        self.story_data = {}
    
    def get_equipment_bonuses(self) -> Dict[str, int]:
        """Calculate total bonuses from equipped items."""
        total = {}
        for slot, equip in self.equipped.items():
            if equip:
                for stat, value in equip.bonuses.items():
                    total[stat] = total.get(stat, 0) + value
        return total
    
    def get_effective_stats(self) -> Dict[str, int]:
        """Get stats with equipment bonuses applied."""
        base = self.stats.copy()
        bonuses = self.get_equipment_bonuses()
        for stat, value in bonuses.items():
            if stat in base:
                base[stat] += value
        return base
    
    def equip_item(self, item_name: str) -> bool:
        """Equip an item from inventory."""
        if item_name not in EQUIPMENT_DATABASE:
            print(f"{RED}Unknown equipment: {item_name}{RESET}")
            return False
        
        equip = EQUIPMENT_DATABASE[item_name]
        
        if item_name not in self.inventory:
            print(f"{RED}You don't have {item_name}{RESET}")
            return False
        
        # Check if another item of same type is equipped
        if self.equipped[equip.slot]:
            old_equip = self.equipped[equip.slot]
            print(f"{YELLOW}Unequipping {old_equip.name}{RESET}")
        
        self.equipped[equip.slot] = equip
        print(f"{GREEN}✓ Equipped {equip.name}{RESET}")
        return True
    
    def unequip_item(self, slot: str) -> bool:
        """Unequip an item from a slot."""
        if slot not in self.equipped:
            print(f"{RED}Invalid slot: {slot}{RESET}")
            return False
        
        if self.equipped[slot] is None:
            print(f"{YELLOW}Nothing equipped in {slot} slot{RESET}")
            return False
        
        print(f"{YELLOW}Unequipped {self.equipped[slot].name}{RESET}")
        self.equipped[slot] = None
        return True
    
    def show_equipment(self):
        """Display currently equipped items."""
        print(f"\n{BOLD}{CYAN}═══ EQUIPPED ITEMS ═══{RESET}")
        for slot, equip in self.equipped.items():
            if equip:
                bonus_str = ", ".join(f"+{v} {k}" for k, v in equip.bonuses.items())
                print(f"  {slot.capitalize()}: {GREEN}{equip.name}{RESET} ({bonus_str})")
            else:
                print(f"  {slot.capitalize()}: {YELLOW}(empty){RESET}")
        
        bonuses = self.get_equipment_bonuses()
        if bonuses:
            print(f"\n{BOLD}Active Bonuses:{RESET}")
            for stat, value in bonuses.items():
                print(f"  +{value} {stat}")
    
    def add_item(self, item_name: str, count: int = 1):
        """Add an item to inventory."""
        if item_name not in ITEM_DATABASE:
            return
        self.items[item_name] = self.items.get(item_name, 0) + count
    
    def use_item(self, item_name: str, in_combat: bool = False) -> bool:
        """Use a consumable item."""
        if item_name not in self.items or self.items[item_name] <= 0:
            print(f"{RED}You don't have {item_name}{RESET}")
            return False
        
        if item_name not in ITEM_DATABASE:
            print(f"{RED}Unknown item: {item_name}{RESET}")
            return False
        
        item = ITEM_DATABASE[item_name]
        
        # Apply effects
        for effect_key, effect_value in item.effect.items():
            if effect_key == "health":
                old_hp = self.health
                self.health = min(100, self.health + effect_value)
                healed = self.health - old_hp
                print(f"{GREEN}Restored {healed} HP!{RESET}")
            elif effect_key == "mana":
                old_mana = self.mana
                self.mana = min(50, self.mana + effect_value)
                restored = self.mana - old_mana
                print(f"{CYAN}Restored {restored} Mana!{RESET}")
            elif effect_key == "clears_poison":
                self.clear_status_effect("poison")
                print(f"{GREEN}Cured poison!{RESET}")
            elif effect_key == "temp_defense":
                self.stats["defense"] += effect_value
                print(f"{CYAN}+{effect_value} defense for this battle{RESET}")
            elif effect_key == "temp_health":
                self.health += effect_value
                print(f"{GREEN}+{effect_value} temporary HP!{RESET}")
        
        # Decrease uses
        self.items[item_name] -= 1
        if self.items[item_name] <= 0:
            del self.items[item_name]
        
        return True
    
    def show_items(self):
        """Display inventory items."""
        print(f"\n{BOLD}{CYAN}═══ ITEMS ═══{RESET}")
        if not self.items:
            print("  (no items)")
            return
        
        for item_name, count in self.items.items():
            if item_name in ITEM_DATABASE:
                item = ITEM_DATABASE[item_name]
                print(f"  {item.name} x{count}: {item.description}")
    
    # Status Effects Methods
    def add_status_effect(self, effect_type: str, amount: int, duration: int, description: str):
        """Add a status effect to the player."""
        # Check if already has this effect - extend duration if so
        for effect in self.status_effects:
            if effect.effect_type == effect_type:
                effect.duration = max(effect.duration, duration)
                effect.amount = max(effect.amount, amount)
                print(f"{YELLOW}{effect.name} extended to {effect.duration} turns{RESET}")
                return
        
        effect_names = {
            "poison": "Poison",
            "bleed": "Bleed", 
            "stun": "Stunned",
            "regen": "Regeneration",
            "barrier": "Barrier",
            "void_corruption": "Void Corruption"
        }
        
        new_effect = StatusEffect(
            name=effect_names.get(effect_type, effect_type),
            effect_type=effect_type,
            amount=amount,
            duration=duration,
            description=description
        )
        self.status_effects.append(new_effect)
        print(f"{YELLOW}✦ {new_effect.name}: {description}{RESET}")
    
    def clear_status_effect(self, effect_type: str):
        """Clear a specific status effect."""
        self.status_effects = [e for e in self.status_effects if e.effect_type != effect_type]
    
    def process_status_effects(self, is_enemy_turn: bool = False):
        """Process status effects at the start of each turn."""
        damage_from_status = 0
        
        for effect in self.status_effects[:]:
            if effect.duration <= 0:
                continue
                
            if effect.effect_type == "poison":
                damage_from_status += effect.amount
                print(f"{YELLOW}Poison deals {effect.amount} damage{RESET}")
            elif effect.effect_type == "bleed":
                damage_from_status += effect.amount
                print(f"{YELLOW}Bleed deals {effect.amount} damage{RESET}")
            elif effect.effect_type == "regen":
                self.health = min(100, self.health + effect.amount)
                print(f"{GREEN}Regeneration restores {effect.amount} HP{RESET}")
            elif effect.effect_type == "barrier":
                print(f"{CYAN}Barrier absorbs 50% of damage{RESET}")
            elif effect.effect_type == "stun":
                if not is_enemy_turn:
                    print(f"{YELLOW}✦ You are stunned and skip your turn!{RESET}")
                    return True  # Return True to indicate player is stunned
        
        if damage_from_status > 0:
            self.health -= damage_from_status
        
        # Decrease durations
        for effect in self.status_effects:
            effect.duration -= 1
        
        # Remove expired effects
        self.status_effects = [e for e in self.status_effects if e.duration > 0]
        
        return False  # Not stunned
    
    def show_status_effects(self):
        """Display current status effects."""
        if not self.status_effects:
            return
        print(f"\n{YELLOW}Status Effects:{RESET}")
        for effect in self.status_effects:
            print(f"  • {effect.name}: {effect.description} ({effect.duration} turns)")
    
    def is_stunned(self) -> bool:
        """Check if player is stunned."""
        return any(e.effect_type == "stun" for e in self.status_effects)
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, text):
        print(f"\n{BOLD}{CYAN}{'=' * 60}{RESET}")
        print(f"{BOLD}{CYAN}{text:^60}{RESET}")
        print(f"{BOLD}{CYAN}{'=' * 60}{RESET}\n")
    
    def print_choice(self, letter, text, requirements=None):
        req_text = ""
        if requirements:
            req_text = f" {YELLOW}[{requirements}]{RESET}"
        print(f"  {YELLOW}[{letter}]{RESET} {text}{req_text}")
    
    def roll_dice(self, stat, dc=10):
        """Roll a stat check."""
        roll = random.randint(1, 20) + self.stats.get(stat, 0)
        return roll >= dc, roll
    
    def show_stats(self):
        """Display player stats."""
        print(f"\n{BOLD}STATS:{RESET}")
        print(f"  STR: {self.stats['strength']} | DEX: {self.stats['dexterity']} | "
              f"INT: {self.stats['intelligence']} | CHA: {self.stats['charisma']}")
        print(f"  HP: {GREEN}{self.health}{RESET}/100 | Mana: {CYAN}{self.mana}{RESET}/50 | "
              f"Gold: {YELLOW}{self.gold}{RESET} | Humanity: {self.humanity}")
    
    def show_inventory(self):
        """Display inventory."""
        print(f"\n{BOLD}INVENTORY:{RESET}")
        if self.inventory:
            for item in self.inventory:
                print(f"  - {item}")
        else:
            print("  (empty)")
    
    def parse_choice_effects(self, choice_text):
        """Parse effects from choice metadata."""
        effects = {}
        
        # Parse LEADS TO
        if "LEADS TO:" in choice_text:
            start = choice_text.find("LEADS TO:") + 9
            end = choice_text.find("}", start)
            if end > start:
                effects['next_scene'] = choice_text[start:end].strip()
        
        # Parse EFFECT
        if "EFFECT:" in choice_text:
            start = choice_text.find("EFFECT:") + 7
            end = choice_text.find("}", start)
            if end > start:
                effect_text = choice_text[start:end].strip()
                # Parse stat changes like "+1 INT"
                for part in effect_text.split(","):
                    part = part.strip()
                    if part.startswith("+"):
                        stat_name = part[2:].strip().lower()
                        if stat_name in self.stats:
                            self.stats[stat_name] += int(part[1])
                    elif part.startswith("-"):
                        stat_name = part[2:].strip().lower()
                        if stat_name in self.stats:
                            self.stats[stat_name] = max(0, self.stats[stat_name] + int(part[1]))
        
        # Parse REQUIRES
        if "REQUIRES:" in choice_text:
            start = choice_text.find("REQUIRES:") + 8
            end = choice_text.find("}", start)
            if end > start:
                effects['requires'] = choice_text[start:end].strip()
        
        return effects
    
    def check_requirements(self, req_text):
        """Check if player meets requirements."""
        if not req_text:
            return True, None
        
        # Check stat requirements
        req_parts = req_text.split(",")
        for part in req_parts:
            part = part.strip()
            # Handle "StatName Value" format
            parts = part.split()
            if len(parts) == 2:
                stat = parts[0].lower()
                value = int(parts[1])
                if stat in self.stats:
                    if self.stats[stat] < value:
                        return False, f"Requires {stat} {value}+"
            elif len(parts) == 3:  # "Item X" format
                if parts[0] == "Item":
                    item = parts[1].strip('"')
                    if item not in self.inventory:
                        return False, f"Requires item: {item}"
        
        return True, None
    
    def combat_encounter(self, enemy, char_class):
        """
        Turn-based combat encounter with move system, status effects, equipment bonuses, and combo system.
        
        Args:
            enemy: Enemy object from bestiary
            char_class: Character class string ("void_mage", "knight", "shadow", "merchant", "warden")
        """
        # Import combo functions
        from src.moves import get_combo_bonus, get_available_combos, apply_elemental_weakness
        
        # Clear any leftover status effects from previous combat
        self.status_effects = []
        
        enemy_name = enemy.name
        enemy_hp = enemy.hp
        enemy_damage = enemy.damage
        
        # Get effective stats with equipment bonuses
        effective_stats = self.get_effective_stats()
        
        # Get moves for character class
        class_moves = get_moves_for_class(char_class)
        
        # Track previous move for combos
        previous_move_key = None
        
        print(f"\n{RED}╔{'═'*56}╗{RESET}")
        print(f"{RED}║ {'⚔ COMBAT ENCOUNTER: ' + enemy_name.upper():^44} ║{RESET}")
        print(f"{RED}╚{'═'*56}╝{RESET}")
        print(f"\n  {YELLOW}Enemy Stats:{RESET} HP: {RED}{enemy_hp}{RESET} | ATK: {enemy_damage} | DEF: {enemy.str}")
        print(f"  {CYAN}Weak against:{RESET} {GREEN}{enemy.weak_against if enemy.weak_against else 'None'}{RESET}")
        print(f"  {MAGENTA}Strong against:{RESET} {RED}{enemy.strong_against if enemy.strong_against else 'None'}{RESET}")
        
        # Show status effects at start
        self.show_status_effects()
        
        while self.health > 0 and enemy_hp > 0:
            # Clear line for turn display
            print(f"\n{BOLD}{CYAN}━━━ YOUR TURN ━━━{RESET}")
            
            # Process status effects at start of turn (player turn)
            is_stunned = self.process_status_effects(is_enemy_turn=False)
            
            # Show stats with equipment bonuses
            print(f"\n  {GREEN}HP: {self.health}/100{RESET} | {CYAN}Mana: {self.mana}/50{RESET}")
            self.show_status_effects()
            
            if is_stunned:
                print(f"\n{YELLOW}You are stunned and cannot act!{RESET}")
            else:
                print(f"\n{BOLD}CHOOSE YOUR ACTION:{RESET}")
                
                # Display class moves with mana costs
                move_num = 1
                for move_key, move in class_moves.items():
                    mana_text = f"{CYAN}{move.mana_cost} mana{RESET}" if move.mana_cost > 0 else "Free"
                    dmg_text = f"{RED}{move.damage} dmg{RESET}" if move.damage > 0 else "-"
                    print(f"  {YELLOW}[{move_num}]{RESET} {move.name:20} | {mana_text:12} | {dmg_text:8} | DC {move.accuracy_dc}")
                    move_num += 1
                
                # Basic options + items
                print(f"\n  {YELLOW}[A]{RESET} Basic Attack (STR + combat)")
                print(f"  {YELLOW}[B]{RESET} Defend (-30% dmg taken)")
                print(f"  {YELLOW}[C]{RESET} Use Item")
                print(f"  {YELLOW}[D]{RESET} Flee")
                
                choice = input("\nAction: ").strip().upper()
                
                player_damage = 0
                player_hit = False
                
                # Process player action
                if choice.isdigit():
                    # Move selection
                    move_index = int(choice) - 1
                    move_keys = list(class_moves.keys())
                    
                    if 0 <= move_index < len(move_keys):
                        selected_move_key = move_keys[move_index]
                        selected_move = class_moves[selected_move_key]
                        
                        # Check mana
                        if self.mana >= selected_move.mana_cost:
                            self.mana -= selected_move.mana_cost
                            
                            # Roll accuracy with effective stats
                            stat_value = effective_stats.get(selected_move.stat_used, 0)
                            roll = random.randint(1, 20) + stat_value
                            player_hit = roll >= selected_move.accuracy_dc
                            
                            if player_hit:
                                player_damage = selected_move.damage
                                combo_bonus = 0
                                combo_effect = ""
                                
                                # Check for combo from previous move
                                if previous_move_key:
                                    combo_dmg, combo_eff, combo_desc = get_combo_bonus(char_class, previous_move_key, selected_move_key)
                                    if combo_dmg > 0:
                                        combo_bonus = combo_dmg
                                        combo_effect = combo_eff
                                        player_damage += combo_bonus
                                        print(f"\n{GREEN}🔥 COMBO! {combo_desc}{RESET}")
                                        print(f"   (+{combo_bonus} bonus damage)")
                                
                                # Apply equipment bonus to damage
                                if selected_move.stat_used in effective_stats:
                                    player_damage += effective_stats[selected_move.stat_used] // 2
                                
                                # Apply elemental weakness/strength
                                if selected_move.element:
                                    player_damage = apply_elemental_weakness(
                                        player_damage, 
                                        selected_move.element,
                                        enemy.weak_against,
                                        enemy.strong_against
                                    )
                                    if player_damage > selected_move.damage + combo_bonus:
                                        print(f"   {MAGENTA}✨ Elemental weakness exploited!{RESET}")
                                
                                # Critical hit on natural 20
                                if roll == 20:
                                    player_damage *= 2
                                    print(f"\n{GREEN}⚡ CRITICAL HIT!{RESET}")
                                
                                # Check for status effect from move
                                if selected_move.status_effect:
                                    self.add_status_effect(
                                        selected_move.status_effect,
                                        STATUS_EFFECTS.get(selected_move.status_effect, {}).get("damage", 0),
                                        selected_move.status_turns,
                                        f"+{selected_move.status_effect}"
                                    )
                                    print(f"   {CYAN}✦ Applied {selected_move.status_effect}{RESET}")
                                
                                # Apply combo effect
                                if combo_effect == "drain":
                                    heal = combo_bonus
                                    self.health = min(100, self.health + heal)
                                    print(f"   {GREEN}♥ Drained {heal} HP{RESET}")
                                
                                enemy_hp -= player_damage
                                print(f"\n{GREEN}✓ {selected_move.name} hits for {RED}{player_damage}{GREEN} damage!{RESET}")
                                print(f"   (Rolled {roll}, needed {selected_move.accuracy_dc})")
                            else:
                                print(f"\n{RED}✗ {selected_move.name} misses!{RESET}")
                                print(f"   (Rolled {roll}, needed {selected_move.accuracy_dc})")
                            
                            # Update previous move for next turn's combo
                            previous_move_key = selected_move_key
                            
                            # Show available combos for next turn
                            if previous_move_key:
                                available = get_available_combos(char_class, previous_move_key)
                                if available:
                                    print(f"\n   {YELLOW}▸ Combo available:{RESET}")
                                    for c in available:
                                        print(f"     [{move_keys.index(c['move_key'])+1}] {c['move_name']} (+{c['bonus_damage']} dmg)")
                        else:
                            print(f"\n{RED}Not enough mana! Need {selected_move.mana_cost}, have {self.mana}{RESET}")
                    else:
                        print(f"\n{RED}Invalid move number.{RESET}")
                
                elif choice == "A":
                    # Basic Attack with equipment bonuses
                    hit, roll = self.roll_dice("strength", 8)
                    if hit:
                        base_damage = random.randint(5, 10)
                        combat_bonus = effective_stats.get("combat", 0)
                        player_damage = base_damage + combat_bonus
                        enemy_hp -= player_damage
                        print(f"\n{GREEN}✓ Basic Attack hits for {RED}{player_damage}{GREEN} damage!{RESET}")
                    else:
                        print(f"\n{RED}✗ Basic Attack misses!{RESET}")
                
                elif choice == "B":
                    # Defend - reduce next damage
                    print(f"\n{CYAN}✓ You take a defensive stance! (-30% incoming damage){RESET}")
                    # Mark that we're defending (will be processed in enemy turn)
                    defending = True
                
                elif choice == "C":
                    # Use Item
                    if not self.items:
                        print(f"\n{RED}You have no items!{RESET}")
                        continue
                    print(f"\n{YELLOW}Available items:{RESET}")
                    for i, (item_name, count) in enumerate(self.items.items(), 1):
                        if item_name in ITEM_DATABASE:
                            item = ITEM_DATABASE[item_name]
                            print(f"  {YELLOW}[{i}]{RESET} {item.name} x{count}")
                    
                    item_choice = input("\nUse which item? ").strip()
                    if item_choice.isdigit():
                        item_idx = int(item_choice) - 1
                        item_names = list(self.items.keys())
                        if 0 <= item_idx < len(item_names):
                            self.use_item(item_names[item_idx], in_combat=True)
                
                elif choice == "D":
                    # Flee with equipment bonus
                    flee_bonus = effective_stats.get("dexterity", 0)
                    hit, roll = self.roll_dice("dexterity", 12)
                    if hit or (roll + flee_bonus >= 15):
                        print(f"\n{GREEN}✓ Escaped from combat!{RESET}")
                        return True
                    else:
                        print(f"\n{RED}✗ Failed to escape!{RESET}")
                        self.health -= enemy_damage
                        print(f"   {enemy_name} hits for {RED}{enemy_damage}{RESET} damage while you flee.")
                    defending = False
                
                else:
                    print(f"\n{RED}Invalid action. Choose a move number, A, B, C, or D.{RESET}")
                    continue
            
            # Enemy turn (if still alive)
            if enemy_hp > 0 and self.health > 0:
                print(f"\n{BOLD}{RED}━━━ ENEMY TURN ━━━{RESET}")
                
                # Process status effects at start of enemy turn
                self.process_status_effects(is_enemy_turn=True)
                
                if self.health <= 0:
                    break
                
                # Check if player was defending
                defending = False
                
                # Apply barrier if active
                has_barrier = any(e.effect_type == "barrier" for e in self.status_effects)
                
                # Enemy attacks
                enemy_roll = random.randint(1, 20) + enemy.str
                if enemy_roll >= 8:
                    enemy_dmg = enemy_damage + random.randint(-2, 2)
                    enemy_dmg = max(1, enemy_dmg)
                    
                    # Apply defense reduction if defending
                    if 'defending' in locals() and defending:
                        enemy_dmg = int(enemy_dmg * 0.7)
                        print(f"   (Defended: {enemy_damage} → {enemy_dmg})")
                    
                    # Apply barrier reduction
                    if has_barrier:
                        original_dmg = enemy_dmg
                        enemy_dmg = int(enemy_dmg * 0.5)
                        print(f"   (Barrier: {original_dmg} → {enemy_dmg})")
                    
                    self.health -= enemy_dmg
                    print(f"   {RED}{enemy_name} attacks for {enemy_dmg} damage!{RESET}")
                else:
                    print(f"   {GREEN}{enemy_name} attacks but misses.{RESET}")
        
        # Combat ended
        if self.health <= 0:
            print(f"\n{RED}💀 You have fallen in combat.{RESET}")
            return False
        
        # Clear status effects after combat
        self.status_effects = []
        
        # Post-battle regeneration (percentage of max)
        hp_restore = max(5, int(100 * 0.15))
        
        # Determine max mana based on class
        max_mana = 50
        if effective_stats.get('void_magic', 0) > 5:
            max_mana = 50
        elif effective_stats.get('combat', 0) > 5:
            max_mana = 40
        elif effective_stats.get('stealth', 0) > 5:
            max_mana = 35
        elif effective_stats.get('nature_magic', 0) > 5:
            max_mana = 40
        else:
            max_mana = 45
            
        mana_restore = max(5, int(max_mana * 0.20))
        
        self.health = min(100, self.health + hp_restore)
        self.mana = min(max_mana, self.mana + mana_restore)
        print(f"\n{CYAN}Rest & Recover:{RESET} +{GREEN}{hp_restore} HP{RESET}, +{CYAN}{mana_restore} Mana{RESET}")
        
        print(f"\n{GREEN}╔{'═'*54}╗{RESET}")
        print(f"{GREEN}║ {'⚔ VICTORY! ' + enemy_name.upper() + ' defeated!':^44} ║{RESET}")
        print(f"{GREEN}╚{'═'*54}╝{RESET}")
        
        # Random loot drop chance
        if random.random() < 0.3:  # 30% chance
            loot_options = list(EQUIPMENT_DATABASE.keys())
            loot = random.choice(loot_options)
            if loot not in self.inventory:
                self.inventory.append(loot)
                print(f"\n{YELLOW}★ Loot: Found {EQUIPMENT_DATABASE[loot].name}!{RESET}")
        
        return True
    
    def combat_encounter_simple(self, enemy_name, enemy_hp, enemy_damage):
        """Legacy simple combat encounter (backward compatibility)."""
        print(f"\n{RED}⚔ COMBAT: {enemy_name} ⚔{RESET}")
        print(f"Enemy HP: {enemy_hp}")
        
        while self.health > 0 and enemy_hp > 0:
            self.show_stats()
            print(f"\n{YELLOW}[A]{RESET} Attack")
            print(f"{YELLOW}[B]{RESET} Defend")
            print(f"{YELLOW}[C]{RESET} Use Skill")
            print(f"{YELLOW}[D]{RESET} Flee")
            
            choice = input("\nAction: ").strip().upper()
            
            if choice == "A":
                hit, roll = self.roll_dice("strength", 8)
                if hit:
                    damage = random.randint(5, 10) + self.stats.get("combat", 0)
                    enemy_hp -= damage
                    print(f"{GREEN}✓ Hit! {damage} damage{RESET}")
                else:
                    print(f"{RED}✗ Miss!{RESET}")
            
            elif choice == "B":
                print(f"{CYAN}You take a defensive stance.{RESET}")
                damage = max(0, enemy_damage - random.randint(1, 5))
                self.health -= damage
                print(f"Enemy hits for {damage} damage.")
            
            elif choice == "C":
                print(f"{CYAN}You use a special skill...{RESET}")
            
            elif choice == "D":
                print(f"{YELLOW}Attempting to flee...{RESET}")
                if random.randint(1, 20) + self.stats.get("dexterity", 0) > 12:
                    print(f"{GREEN}Escaped!{RESET}")
                    return True
                else:
                    print(f"{RED}Failed to escape!{RESET}")
                    damage = enemy_damage
                    self.health -= damage
                    print(f"Enemy hits for {damage} while you flee.")
            
            if enemy_hp > 0:
                enemy_dmg = random.randint(3, 8)
                self.health -= enemy_dmg
                print(f"{enemy_name} hits for {enemy_dmg} damage.")
        
        if self.health <= 0:
            print(f"\n{RED}You have fallen.{RESET}")
            return False
        
        print(f"\n{GREEN}Victory! {enemy_name} defeated!{RESET}")
        return True
    
    def load_story(self, story_file):
        """Load story data from JSON file."""
        try:
            with open(story_file, 'r') as f:
                self.story_data = json.load(f)
            return True
        except FileNotFoundError:
            print(f"{RED}Story file not found: {story_file}{RESET}")
            return False
    
    def save_game(self, save_file):
        """Save game state."""
        # Save equipped items as list of names
        equipped_items = []
        for slot, equip in self.equipped.items():
            if equip:
                equipped_items.append(equip.name)
        
        save_data = {
            "player": self.player,
            "stats": self.stats,
            "inventory": self.inventory,
            "equipped_items": equipped_items,
            "items": self.items,
            "flags": self.flags,
            "current_scene": self.current_scene,
            "humanity": self.humanity,
            "health": self.health,
            "mana": self.mana,
            "gold": self.gold
        }
        with open(save_file, 'w') as f:
            json.dump(save_data, f, indent=2)
        print(f"{GREEN}Game saved.{RESET}")
    
    def load_game(self, save_file):
        """Load game state."""
        try:
            with open(save_file, 'r') as f:
                save_data = json.load(f)
            self.player = save_data.get("player")
            self.stats = save_data.get("stats", self.stats)
            self.inventory = save_data.get("inventory", [])
            
            # Load equipped items
            equipped_names = save_data.get("equipped_items", [])
            self.equipped = {"weapon": None, "armor": None, "accessory": None}
            for name in equipped_names:
                for equip_name, equip in EQUIPMENT_DATABASE.items():
                    if equip.name == name:
                        self.equipped[equip.slot] = equip
                        break
            
            # Load items
            self.items = save_data.get("items", {})
            
            self.flags = save_data.get("flags", {})
            self.current_scene = save_data.get("current_scene")
            self.humanity = save_data.get("humanity", 10)
            self.health = save_data.get("health", 100)
            self.mana = save_data.get("mana", 50)
            self.gold = save_data.get("gold", 10)
            return True
        except FileNotFoundError:
            return False


def create_engine():
    """Create and return a new game engine."""
    return GameEngine()


if __name__ == "__main__":
    engine = create_engine()
    print(f"{CYAN}Velanthor Engine initialized.{RESET}")
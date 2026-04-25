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
from src.moves import get_moves_for_class, Move
from src.bestiary import Enemy, get_enemy_by_name

# ANSI color codes
CYAN = "\033[1;36m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
GREEN = "\033[1;32m"
RESET = "\033[0m"
BOLD = "\033[1m"


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
            "influence": 0
        }
        self.inventory = []
        self.flags = {}
        self.current_scene = None
        self.humanity = 10
        self.health = 100
        self.mana = 50
        self.gold = 10
        self.relationships = {}
        self.story_data = {}
        
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
        Turn-based combat encounter with move system.
        
        Args:
            enemy: Enemy object from bestiary
            char_class: Character class string ("void_mage", "knight", "shadow", "merchant")
        """
        enemy_name = enemy.name
        enemy_hp = enemy.hp
        enemy_damage = enemy.damage
        
        # Get moves for character class
        class_moves = get_moves_for_class(char_class)
        
        print(f"\n{RED}⚔ COMBAT: {enemy_name} ⚔{RESET}")
        print(f"Enemy HP: {enemy_hp} | Damage: {enemy_damage}")
        print(f"{CYAN}Weak against:{RESET} {enemy.weak_against if enemy.weak_against else 'None'}")
        print(f"{YELLOW}Strong against:{RESET} {enemy.strong_against if enemy.strong_against else 'None'}")
        
        while self.health > 0 and enemy_hp > 0:
            self.show_stats()
            print(f"\n{BOLD}YOUR MOVES:{RESET}")
            
            # Display class moves with mana costs
            move_num = 1
            for move_key, move in class_moves.items():
                mana_text = f"{CYAN}{move.mana_cost} mana{RESET}" if move.mana_cost > 0 else "Free"
                dmg_text = f"{RED}{move.damage} dmg{RESET}" if move.damage > 0 else "-"
                print(f"  {YELLOW}[{move_num}]{RESET} {move.name:20} | {mana_text:12} | {dmg_text:8} | DC {move.accuracy_dc}")
                move_num += 1
            
            # Basic options
            print(f"\n  {YELLOW}[A]{RESET} Basic Attack (STR + combat)")
            print(f"  {YELLOW}[B]{RESET} Defend (-30% dmg taken)")
            print(f"  {YELLOW}[C]{RESET} Flee")
            
            choice = input("\nAction: ").strip().upper()
            
            player_damage = 0
            player_hit = False
            
            # Process player action
            if choice.isdigit():
                # Move selection
                move_index = int(choice) - 1
                move_keys = list(class_moves.keys())
                
                if 0 <= move_index < len(move_keys):
                    selected_move = class_moves[move_keys[move_index]]
                    
                    # Check mana
                    if self.mana >= selected_move.mana_cost:
                        self.mana -= selected_move.mana_cost
                        
                        # Roll accuracy
                        stat_value = self.stats.get(selected_move.stat_used, 0)
                        roll = random.randint(1, 20) + stat_value
                        player_hit = roll >= selected_move.accuracy_dc
                        
                        if player_hit:
                            player_damage = selected_move.damage
                            # Critical hit on natural 20
                            if roll == 20:
                                player_damage *= 2
                                print(f"{GREEN}⚡ CRITICAL HIT!{RESET}")
                            enemy_hp -= player_damage
                            print(f"{GREEN}✓ {selected_move.name} hits for {player_damage} damage!{RESET} (rolled {roll})")
                        else:
                            print(f"{RED}✗ {selected_move.name} misses!{RESET} (rolled {roll})")
                    else:
                        print(f"{RED}Not enough mana! Need {selected_move.mana_cost}, have {self.mana}{RESET}")
                else:
                    print(f"{RED}Invalid move number.{RESET}")
            
            elif choice == "A":
                # Basic Attack
                hit, roll = self.roll_dice("strength", 8)
                if hit:
                    base_damage = random.randint(5, 10)
                    player_damage = base_damage + self.stats.get("combat", 0)
                    enemy_hp -= player_damage
                    print(f"{GREEN}✓ Basic Attack hits for {player_damage} damage!{RESET}")
                else:
                    print(f"{RED}✗ Basic Attack misses!{RESET}")
            
            elif choice == "B":
                # Defend - reduce next damage
                reduced_damage = int(enemy_damage * 0.7)
                self.health -= reduced_damage
                print(f"{CYAN}✓ You defend! Damage reduced from {enemy_damage} to {reduced_damage}.{RESET}")
            
            elif choice == "C":
                # Flee
                hit, roll = self.roll_dice("dexterity", 12)
                if hit:
                    print(f"{GREEN}✓ Escaped from combat!{RESET}")
                    return True
                else:
                    print(f"{RED}✗ Failed to escape!{RESET}")
                    self.health -= enemy_damage
                    print(f"{enemy_name} hits for {enemy_damage} damage while you flee.")
            
            else:
                print(f"{RED}Invalid action. Choose a move number, A, B, or C.{RESET}")
            
            # Enemy turn (if still alive)
            if enemy_hp > 0:
                # Enemy attacks
                enemy_roll = random.randint(1, 20) + enemy.str
                if enemy_roll >= 8:
                    enemy_dmg = enemy_damage + random.randint(-2, 2)
                    enemy_dmg = max(1, enemy_dmg)
                    self.health -= enemy_dmg
                    print(f"{RED}{enemy_name} attacks for {enemy_dmg} damage!{RESET}")
                else:
                    print(f"{GREEN}{enemy_name} attacks but misses.{RESET}")
        
        # Combat ended
        if self.health <= 0:
            print(f"\n{RED}💀 You have fallen in combat.{RESET}")
            return False
        
        print(f"\n{GREEN}⚔ VICTORY! {enemy_name} defeated!{RESET}")
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
        save_data = {
            "player": self.player,
            "stats": self.stats,
            "inventory": self.inventory,
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
#!/usr/bin/env python3
"""Tutorial system for Velanthor RPG - teaches new players game mechanics."""


class Tutorial:
    """Tutorial system for teaching game mechanics."""
    
    def __init__(self):
        self.shown_topics = set()
        self.player_stats = {
            "strength": 0,
            "dexterity": 0,
            "intelligence": 0,
            "charisma": 0,
        }
    
    def show_welcome(self):
        """Display welcome message and tutorial overview."""
        print("\n" + "=" * 50)
        print("           WELCOME TO VELANTHOR")
        print("=" * 50)
        print("""
  This is a choice-based RPG where your decisions
  shape the story. Before you begin, let's cover
  the basics.
        """)
        print("=" * 50)
        input("\n  [ Press any key to continue ]")
    
    def show_choices(self):
        """Explain how to make choices."""
        if "choices" in self.shown_topics:
            return
        
        self.shown_topics.add("choices")
        
        print("\n" + "─" * 40)
        print("  🎯 MAKING CHOICES")
        print("─" * 40)
        print("""
  Throughout your journey, you'll face decisions.
  Each choice is labeled with a letter (A, B, C, D).

  Example:
    [A] Attack the enemy
    [B] Try to negotiate
    [C] Search for clues
    [D] Flee from combat

  Type the letter and press Enter to select.
  
  Some choices may require certain stats or items.
  Others may have consequences later in the story.
        """)
        print("─" * 40)
        input("\n  [ Press any key to continue ]")
    
    def show_stats(self):
        """Explain character stats."""
        if "stats" in self.shown_topics:
            return
        
        self.shown_topics.add("stats")
        
        print("\n" + "─" * 40)
        print("  📊 CHARACTER STATS")
        print("─"  * 40)
        print("""
  Your character has EIGHT stats:

  ⚔️  STRENGTH (STR)
      Physical power. Used for combat damage,
      athletic checks, and lifting heavy objects.
      
  🏃 DEXTERITY (DEX)  
      Agility and reflexes. Used for stealth,
      lockpicking, dodging, and escaping.
      
  🧠  INTELLIGENCE (INT)
      Knowledge and logic. Used for puzzle solving,
      remembering lore, and magical aptitude.
      
  💬  CHARISMA (CHA)
      Persuasion and leadership. Used for dialogue,
      NPC reactions, and inspiring allies.
      
  ⚡  [CLASS SKILL]
      Unique skill based on your character:
      - VOID_MAGIC (Kira) - Void powers
      - COMBAT (Theron) - Sword fighting
      - STEALTH (Vex) - Shadow moves
      - INFLUENCE (Elara) - Business/money

  📈  HP / MANA / GOLD
      • HP (Health): Your life in battle (100 base)
      • Mana: Spell energy (25-40 based on class)
      • Gold: Money for bribes/items

  STATS IMPACT COMBAT:
      Higher stat = Better move accuracy!
      Class skill increases unique move damage.
        """)
        print("─" * 40)
        input("\n  [ Press any key to continue ]")
    
    def show_stat_checks(self):
        """Explain stat checks."""
        if "stat_checks" in self.shown_topics:
            return
        
        self.shown_topics.add("stat_checks")
        
        print("\n" + "─" * 40)
        print("  🎲 STAT CHECKS")
        print("─" * 40)
        print("""
  Some choices require passing a stat check.

  The game will show requirements like:
    [A] Persuade the guard
        {REQUIRES: Charisma 5}
  
  This means you need at least 5 Charisma
  to attempt this option.

  If you don't meet the requirement, you can
  still try—but you're more likely to fail.
  
  Success and failure both advance the story
  in different ways.
        """)
        print("─" * 40)
        input("\n  [ Press any key to continue ]")
    
    def show_combat(self):
        """Explain Pokemon-style combat."""
        if "combat" in self.shown_topics:
            return
        
        self.shown_topics.add("combat")
        
        print("\n" + "─" * 40)
        print("  ⚔️  POKEMON-STYLE COMBAT")
        print("─" * 40)
        print("""
  When you encounter enemies marked with ⚔️ or battle 
  scenes, combat begins!

  YOUR TURN:
    Choose a move (1-6) or use basic options (A-C):
    
    Moves use your CLASS SKILL - each character 
    has unique abilities:
    
    ╔════════════════════════════════════════╗
    ║  KIRA (Void Mage)  - Uses VOID_MAGIC    ║
    ║    • Void Burst (15 dmg, 8 mana)         ║
    ║    • Shadow Bolt (10 dmg, 5 mana)        ║
    ║    • Void Shield (defense)              ║
    ║    • Soul Drain (drain life)            ║
    ║    • Dark Pact (power)                ║
    ║    • Void Walk (escape)               ║
    ╠════════════════════════════════════════════════╣
    ║  THERON (Knight) - Uses COMBAT          ║
    ║    • Shield Bash (8 dmg, 3 mana)          ║
    ║    • Cleaving Strike (14 dmg, 6 mana)     ║
    ║    • Defensive Stance (defense)         ║
    ║    • Reckless Blow (high dmg)          ║
    ║    • Blade Storm (area)               ║
    ║    • Iron Will (buff)                 ║
    ╠════════════════════════════════════════════════╣
    ║  VEX (Shadow) - Uses STEALTH           ║
    ║    • Backstab (12 dmg, 4 mana)          ║
    ║    • Poison Blade (DoT, 5 mana)         ║
    ║    • Smoke Bomb (evade)              ║
    ║    • Fan of Knives (multi)           ║
    ║    • Shadow Step ( repositions)       ║
    ║    • Assassinate (finisher)           ║
    ╠════════════════════════════════════════════════╣
    ║  ELARA (Merchant) - Uses INFLUENCE    ║
    ║    • Coin Toss (5 dmg, 2 mana)         ║
    ║    • Sweet Talk (charm)               ║
    ║    • Intimidate (fear)                ║
    ║    • Call in Favor (summon)           ║
    ║    • Gold Syndrome (pay to win)        ║
    ║    • Business Ending (ultimate)        ║
    ╚══════════════════════════════════════════╝

  HOW COMBAT WORKS:
    1. Choose move (1-6) or basic (A-C)
    2. Roll: d20 + YOUR STAT vs ENEMY DC
    3. Hit = Deal damage shown
    4. Enemy attacks back
    5. Repeat until one falls!

  STATS MATTER:
    • Higher stat = better accuracy
    • Mana limits moves per battle
    • Watch enemy weaknesses!
        """)
        print("─" * 40)
        input("\n  [ Press any key to continue ]")
    
    def show_inventory(self):
        """Explain inventory system."""
        if "inventory" in self.shown_topics:
            return
        
        self.shown_topics.add("inventory")
        
        print("\n" + "─" * 40)
        print("  🎒 INVENTORY")
        print("─" * 40)
        print("""
  You'll collect items during your journey:
  - Weapons and armor
  - Quest items
  - Gold and resources
  - Key documents

  Items can:
  - Unlock new dialogue options
  - Provide combat bonuses
  - Help bypass obstacles
  - Be sold for gold

  Type 'inventory' or 'inv' anytime to view
  your current items.
        """)
        print("─" * 40)
        input("\n  [ Press any key to continue ]")
    
    def show_help(self):
        """Show help reminder and command list."""
        print("\n" + "─" * 40)
        print("  ❓ HELP COMMAND")
        print("─" * 40)
        print("""
  Type 'help' anytime to see available commands:
  
  ───────────────────────
  help    - Show this menu
  stats   - View your stats
  inventory / inv - View your items
  save    - Save your progress
  load    - Load a save
  quit    - Exit the game
  ───────────────────────

  Remember: Type 'help' anytime!
        """)
        print("─" * 40)
    
    def show_tips(self):
        """Show general gameplay tips."""
        if "tips" in self.shown_topics:
            return
        
        self.shown_topics.add("tips")
        
        print("\n" + "─" * 40)
        print("  💡 TIPS FOR YOUR JOURNEY")
        print("─" * 40)
        print("""
  • Explore all choices - each leads somewhere different
  • Talk to NPCs - they may have useful information
  • Check your stats - they affect what you can do
  • Watch your inventory - items unlock options
  • Save often - some choices are permanent
  • Type 'help' anytime for a reminder of commands

  Your decisions matter. Choose wisely.
  
  The world of Velanthor awaits.
        """)
        print("─" * 40)
        input("\n  [ Press any key to begin your journey ]")
    
    def run_full_tutorial(self):
        """Run the complete tutorial sequence."""
        self.show_welcome()
        self.show_choices()
        self.show_stats()
        self.show_stat_checks()
        self.show_combat()
        self.show_inventory()
        self.show_help()
        self.show_tips()
    
    def show_topic(self, topic):
        """Show a specific tutorial topic on demand."""
        topics = {
            "choices": self.show_choices,
            "stats": self.show_stats,
            "stat_checks": self.show_stat_checks,
            "combat": self.show_combat,
            "inventory": self.show_inventory,
            "help": self.show_help,
            "tips": self.show_tips,
        }
        if topic in topics:
            topics[topic]()


def create_tutorial():
    """Factory function to create a tutorial instance."""
    return Tutorial()


def run_tutorial():
    """Run the tutorial standalone."""
    tutorial = create_tutorial()
    tutorial.run_full_tutorial()


if __name__ == "__main__":
    run_tutorial()
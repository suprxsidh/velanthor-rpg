# Velanthor: The Crown of the Dead God

A dark fantasy choice-based terminal RPG with 5 playable characters, turn-based combat, equipment system, and branching narratives.

## Features

- **5 Playable Characters**: Kira, Theron, Vex, Elara, and Asha
- **Turn-Based Combat**: Class-specific moves, status effects, equipment bonuses
- **Equipment System**: Weapons, armor, and accessories with stat bonuses
- **Consumable Items**: Healing potions, mana crystals, defensive items
- **Status Effects**: Poison, Bleed, Stun, Regeneration, Barrier
- **Branching Story**: Multiple endings based on your choices

## Characters

| Character | Class | Description |
|-----------|-------|--------------|
| Kira Nightwind | Void Mage | Last of the Nightwind line, hunted by the Cult |
| Theron Ashford | Knight | Fallen knight seeking redemption |
| Vex Shadowstep | Shadow | Thief carrying impossible cargo |
| Elara Vance | Merchant | Merchant heiress seeking vengeance |
| Asha Ironheart | Warden | Druid guardian of the northern border |

## Commands

| Command | Action |
|---------|--------|
| `STATS` | View your stats |
| `INVENTORY` | View your inventory items |
| `EQUIP` | View equipped items |
| `EQUIP [item]` | Equip an item |
| `ITEMS` | View consumable items |
| `USE [item]` | Use an item |
| `SAVE` | Save your game |
| `LOAD` | Load a saved game |
| `HELP` | Show tutorial |

## How to Play

```bash
python3 main.py
```

## Game Mechanics

### Stats
- **STR** (Strength): Physical power, combat damage
- **DEX** (Dexterity): Agility, stealth, dodging
- **INT** (Intelligence): Knowledge, puzzle solving
- **CHA** (Charisma): Persuasion, leadership
- **Class Skills**: Void Magic, Combat, Stealth, Influence, Nature Magic, Survival

### Combat
- Choose moves (numbered 1-6) or basic actions (A/B/C/D)
- Equipment provides stat bonuses in combat
- Status effects can be applied by enemy attacks
- Defend (B) reduces incoming damage by 30%
- Use items (C) in combat for healing or buffs

### Equipment
Loot drops from enemies (30% chance). Equip items to gain stat bonuses:
- Weapons: +Combat, +Void Magic, +Stealth, etc.
- Armor: +Health, +Defense
- Accessories: Various bonuses

## Version History

### v1.1 (May 2026)
- Added 5th character: Asha Ironheart (Warden)
- Added Equipment System (15 items)
- Added Consumable Items (10 items)
- Added Status Effects in combat
- Improved combat display with turn order
- Added loot drops from enemies

### v1.0 (April 2026)
- Initial release with 4 characters
- Kira, Theron, Vex, Elara storylines
- Basic combat system

## Credits

Created with Python 3. A terminal-based RPG inspired by classic choose-your-own-adventure games.

---

*The world of Velanthor remembers the old ways. The crown calls. What legend will you carve?*
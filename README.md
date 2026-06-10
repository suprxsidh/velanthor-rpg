# Velanthor: The Crown of the Dead God

A dark fantasy choice-based terminal RPG with 5 playable characters, turn-based combat, equipment systems, and branching narratives.

**Current build:** 714 scenes, 2136 choices, 81 endings — all reachable, fully playable.

## Features

- **5 Playable Characters**: Kira, Theron, Vex, Elara, and Asha — each with unique storylines
- **81 Unique Endings**: Branching narratives with death endings, victory endings, and walkaway endings
- **5-Chapter Structure**: Each character progresses through 5 chapters with phase scenes (Prepare, Reflect, Search, Rest)
- **Turn-Based Combat**: Class-specific moves, status effects, equipment bonuses
- **Equipment System**: Weapons, armor, accessories with stat bonuses
- **Consumable Items**: Healing potions, mana crystals, defensive items
- **Status Effects**: Poison, Bleed, Stun, Regeneration, Barrier
- **Zero Dead Ends**: Every story path leads to a meaningful conclusion

## Characters

| Character | Class | Description | Endings |
|-----------|-------|-------------|---------|
| **Kira Nightwind** | Void Mage | Last of the Nightwind line, hunted by the Cult for her void magic. 139 scenes. | 24 |
| **Theron Ashford** | Fallen Knight | Broken knight carrying the void, seeking redemption. 152 scenes. | 17 |
| **Vex Shadowstep** | Shadow | Street thief navigating the criminal underworld, searching for her sister. 151 scenes. | 11 |
| **Elara Vance** | Merchant Heiress | Noble seeking vengeance for her murdered parents. 115 scenes. | 12 |
| **Asha Ironheart** | Warden | Druid guardian of the northern border, protector of nature's balance. 157 scenes. | 17 |

## How to Play

```bash
python3 main.py
```

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

## Story Structure

Each character's story follows a 5-chapter arc with phase scenes between major story beats:

- **MAIN scenes**: Central chapter hub — choose your path
- **Phase scenes** (Prepare, Reflect, Search, Rest): Narrative breathing room between action
- **TRANSITION scenes**: Chapter gates with atmospheric chapter titles
- **ALT scenes**: Side paths that rejoin the main story
- **EXTRA scenes**: Optional side content and character moments

## Verification

The game includes automated verification scripts:

```bash
python3 scripts/verify_story.py       # Structural integrity (broken refs, dead ends, duplicates)
python3 scripts/test_playability.py   # Playability (all characters can reach endings)
python3 scripts/replay_tracer.py      # Deep replay verification per character
```

## Version History

### v1.6 (June 2026)
- Full quality audit across all 5 characters
- Fixed 63 phase scene navigation issues (chapter skipping)
- Created 11 new VEX Chapter 1 scenes with divergent choice paths
- Wrote 26 proper ending descriptions (replacing placeholders)
- Connected all 81 endings to the story graph (0 unreachable)
- Expanded 40 scene descriptions from placeholders to immersive narrative
- Fixed 9 VEX and 4 ELARA ending types (were incorrectly typed as "story")
- Converted ASHA_CH4_ENDING_SELECTION from dead end to proper ending
- Removed ~120 duplicate choice texts
- Added verification and replay tracing scripts
- ASHA: 157 scenes, 17 endings
- VEX: 151 scenes, 11 endings
- KIRA: 139 scenes, 24 endings
- THERON: 152 scenes, 17 endings
- ELARA: 115 scenes, 12 endings

### v1.5.1 (May 2026)
- Fix direct-to-ending paths: require chapter progression, min 10+ turns to ending

### v1.5 (May 2026)
- Full connectivity fix: all 5 characters at 100% reachability, all paths lead to endings

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

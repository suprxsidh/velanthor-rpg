# Velanthor - Future Expansion Plans

*Document created: May 2026*
*Phase 1 Complete: Asha Ironheart (Warden)*

---

## Completed

### Phase 1: Asha Ironheart (Warden)
- 5th playable character added
- 4 chapters, ~60 scenes, 6 endings → expanded to 11 endings
- Warden class with nature magic
- New enemies: Ashen Wolf, Corrupted Treant, Void Serpent, etc.
- See: `main.py`, `src/moves.py`, `src/bestiary.py`, `data/story.json`

### Phase 2: Equipment System ✅ COMPLETE

**Implementation**:
- Equipment class in `src/engine.py` with 15 items (5 weapons, 5 armor, 5 accessories)
- `equip_item()`, `unequip_item()`, `show_equipment()` commands
- Equipment bonuses applied in combat
- Loot drops from enemies (30% chance)
- Save/load includes equipment

### Phase 3: Combat Improvements ✅ COMPLETE

**Implementation**:
- Status Effects: Poison, Bleed, Stun, Regen, Barrier
- Turn Order Display: "━━━ YOUR TURN ━━━" / "━━━ ENEMY TURN ━━━"
- Damage Numbers: Show exact damage dealt
- Enemy Weakness Display: Shows weak/strong against
- Visual Combat Feedback: Color-coded messages
- Fixed stun effect logic

---

## Planned Expansions

### 1. Equipment System

**Status**: COMPLETE (May 2026)

**Description**: Add weapons, armor, and accessories that provide stat bonuses.

**Implementation**:
- Add Equipment class to `src/engine.py`
- Create equipment inventory system
- Add equip/unequip commands
- Loot drops from enemies
- Optional: purchasable from merchants

**Equipment Types**:
| Type | Examples | Effects |
|------|----------|---------|
| Weapons | Void Blade, Druid Staff, Shadow Daggers | +Combat, +Void Magic, +Stealth |
| Armor | Knight Plate, Ranger Cloak, Warden Vestments | +Defense, +HP |
| Accessories | Ring of Protection, Amulet of Healing | Various bonuses |

---

### 2. Combat Improvements

**Status**: COMPLETE (May 2026)

**Description**: Enhanced combat experience based on modern RPG design.

**Features**:
- Status Effects: Poison, Bleed, Stun, Void Corruption, Regen, Barrier
- Turn Order Display: Clear "Your Turn" / "Enemy Turn" indicators
- Damage Numbers: Show exact damage dealt
- Enemy Weaknesses: Exploit with right attack type
- Visual Combat Feedback: Color-coded messages

**Status Effects Details**:
| Status | Effect | Duration | Cured By |
|--------|--------|----------|----------|
| Poison | -2 HP/turn | 3 turns | Antidote, Herbal Remedy |
| Bleed | -1 HP/turn, stacks | 2 turns | Bandage |
| Stun | Skip turn | 1 turn | Wait out |
| Void Corruption | -1 to all stats | Until healed | Circle of Mages |
| Regen | +3 HP/turn | 2 turns | - |
| Barrier | 50% damage reduction | 1 turn | - |

---

### 3. Items System

**Status**: Pending

**Description**: Usable items (healing, defensive, utility).

**Item Categories**:
| Category | Examples | Use |
|----------|----------|-----|
| Healing | Health Potion, Healing Shard, Herbal Remedy | Restore HP |
| Mana | Mana Crystal, Essence Vial | Restore Mana |
| Defensive | Cloak of Defense, Shield Scroll, Iron Ward | Temporary buffs |
| Utility | Antidote, Lockpick Set, Flashbang | Special uses |
| Quest | Crown Shard, Ancient Key | Story progression |

**Implementation**:
- Add Item class to `src/engine.py`
- Add `use [item]` command
- Integrate into combat and exploration
- Inventory display with uses remaining

---

### 4. Cross-Character Convergence Scenes

**Status**: Future (Postponed)

**Description**: Scenes where 2+ characters' paths intersect.

**Crossover Points** (Planned):
| Scene ID | Location | Characters | Description |
|----------|----------|------------|-------------|
| `CROSS_DUSTWALL_TAVERN` | Dustwall tavern | Theron + Vex | Vex sees Theron drinking |
| `CROSS_CROWNHAVEN_PALACE` | Crownhaven palace | Kira + Theron + Elara | All three at the Summit |
| `CROSS_TEMPLE_FINAL` | Cult Temple | All 5 | Final battle convergence |
| `CROSS_WASTES_BORDER` | Ashen Wastes edge | Asha + Kira | Both seek answers about the Void |
| `CROSS_MERCHANT_MEET` | Theris trade district | Elara + Vex | Old contacts, potential alliance |

**Implementation Notes**:
- Requires shared save state between characters
- Option A: Import previous save for crossovers
- Option B: Standalone "what-if" scenarios
- Option C: NPCs represent other characters in single playthrough

---

### 5. Advanced Move Combos

**Status**: Future

**Description**: Chain attacks and counter system.

**Features**:
- Combo system: Link moves together for bonus effects
- Counter attacks: React to enemy attacks
- Defensive counters: Parry then strike
- Timing-based bonuses

---

### 6. Multi-Enemy Encounters

**Status**: Future

**Description**: Fighting multiple opponents simultaneously.

**Features**:
- Group battles (2-4 enemies)
- Area-of-effect moves
- Priority targeting
- Swarm enemies (multiple weak enemies)

---

### 7. Boss Mechanics

**Status**: Future

**Description**: Enhanced boss battles with phases and special mechanics.

**Features**:
- Phase transitions at 50% HP
- Enrage timers (must defeat before time runs out)
- Summon minions during battle
- Unique boss abilities per boss

---

### 8. Skill Trees

**Status**: Future

**Description**: Branching skill trees per class.

**Implementation**:
- Create `src/skills.py` module
- Visual skill tree display
- Skill unlock requirements
- Multiple paths per class

**Example - Warden Skill Tree**:
```
Warden Skill Tree:
├── Path of the Guardian
│   ├── Shield Wall (requires: STR 6, Defense 5)
│   ├── Taunt (requires: CHA 4)
│   └── Last Stand (requires: Defense 8)
├── Path of the Beast
│   ├── Beast Call (requires: Nature Magic 5)
│   ├── Beast Form (requires: Nature Magic 7)
│   └── Beast Lord (requires: Nature Magic 9)
└── Path of the Wild
    ├── Healing Grove (requires: Nature Magic 4)
    ├── Root Entangle (requires: DEX 5)
    └── Nature's Wrath (requires: INT 6)
```

---

### 9. Companion System

**Status**: Future

**Description**: Allow other characters to join as AI companions.

**Features**:
- Combat: Companion fights alongside player
- Dialogue: Companion provides commentary
- Stats: Companion has their own stats and inventory
- Relationship mechanics

---

### 10. Faction Storylines

**Status**: Future

**Description**: Extended storylines for major factions.

**Factions**:
- The Silent Church
- The Cult of the Hollow
- The Circle of Mages
- The Shadow Guild
- The Watch

---

### 11. Hidden/Secret Paths

**Status**: Future

**Description**: Easter egg content and secret endings.

**Features**:
- Hidden scenes triggered by specific choices
- Secret endings for completing hidden objectives
- Special items that unlock secret dialogue

---

### 12. Prestige/New Game+

**Status**: Future

**Description**: Start new game with bonuses from previous playthrough.

**Features**:
- Carry over some stats/items
- Hard mode with new enemies
- Alternate timeline story branches

---

### 13. Quality of Life Improvements

**Status**: Future

**Features**:
- Combat animations/effects (text-based)
- Enemy name display
- Damage numbers
- Battle log/history
- Auto-battle mode
- Faster text display option

---

## Technical Debt

- Clean up temporary/debug files in root directory
- Document all new systems
- Add unit tests for new features
- Optimize JSON loading

---

*Last Updated: May 2026*
*Priority Order: Equipment → Combat Improvements → Items → Crossovers*
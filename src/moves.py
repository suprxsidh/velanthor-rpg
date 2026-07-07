"""
Velanthor RPG - Move System
All character class moves with damage, mana costs, and accuracy DCs.
"""

from dataclasses import dataclass


@dataclass
class Move:
    """Represents a combat move/ability."""
    name: str
    mana_cost: int
    damage: int
    accuracy_dc: int
    stat_used: str
    description: str
    element: str = ""  # fire, ice, lightning, void, nature
    status_effect: str = ""  # burn, freeze, bleed, mark, poison
    status_turns: int = 0
    aoe: bool = False  # area of effect flag


# Combo Chain - defines valid move combinations
@dataclass
class ComboChain:
    """Represents a combo between two moves."""
    first_move: str
    second_move: str
    bonus_damage: int = 0
    bonus_effect: str = ""
    description: str = ""


# Combo chains per character class
COMBO_CHAINS = {
    "void_mage": [
        ComboChain("void_burst", "shadow_bolt", 5, "mark", "Void cascade - leaves enemy marked"),
        ComboChain("shadow_bolt", "soul_drain", 8, "drain", "Shadow absorption - drains health"),
        ComboChain("void_burst", "dark_pact", 12, "wound", "Dark evolution - the wound deepens with every heartbeat"),
    ],
    "knight": [
        ComboChain("shield_bash", "cleaving_strike", 6, "stun", "Shield break - leaves vulnerable"),
        ComboChain("cleaving_strike", "blade_storm", 10, "bleed", "Storm blade - causes bleeding"),
        ComboChain("defensive_stance", "reckless_blow", 8, "focus", "Defensive fury - a measured strike from perfect footing"),
    ],
    "shadow": [
        ComboChain("backstab", "poison_blade", 7, "poison", "Deadly combination - venom seeps into the open cut"),
        ComboChain("fan_of_knives", "assassinate", 15, "mark", "Shadow execution - the mark glows where the knife will land"),
        ComboChain("smoke_bomb", "backstab", 5, "crit", "Stealth strike - they never saw the second blade"),
    ],
    "merchant": [
        ComboChain("coin_toss", "intimidate", 4, "terror", "Psychological warfare - fear does half the work"),
        ComboChain("intimidate", "business_ending", 10, "shatter", "Business destruction - their composure shatters like glass"),
        ComboChain("sweet_talk", "favor_call", 5, "charm", "Social manipulation - they want to help you now"),
    ],
    "warden": [
        ComboChain("root_entangle", "beast_call", 8, "immobilize", "Nature's trap - roots close like a fist"),
        ComboChain("beast_call", "natures_wrath", 12, "wound", "Beast fury - claws follow where the call leads"),
        ComboChain("healing_grove", "thorn_shield", 5, "regen", "Nature's blessing - green light knits the flesh"),
    ],
}


# Status Effects definitions
STATUS_EFFECTS = {
    "poison": {"damage": 2, "turns": 3, "stat_penalty": ""},
    "burn": {"damage": 3, "turns": 3, "stat_penalty": "defense"},
    "freeze": {"damage": 0, "turns": 2, "stat_penalty": "dexterity"},
    "bleed": {"damage": 2, "turns": 4, "stat_penalty": ""},
    "mark": {"damage": 0, "turns": 2, "stat_penalty": ""},  # next attack +50%
    "stun": {"damage": 0, "turns": 1, "stat_penalty": "all"},
    "terror": {"damage": 0, "turns": 2, "stat_penalty": "all"},
    "drain": {"damage": 3, "turns": 2, "stat_penalty": "strength"},
    "shield": {"damage": 0, "turns": 3, "stat_penalty": "", "temp_hp": 5},  # +5 temporary HP
}


# Void Mage Moves - Intelligence-based void magic
VOID_MAGE_MOVES = {
    "void_burst": Move(
        name="Void Burst",
        mana_cost=8,
        damage=15,
        accuracy_dc=12,
        stat_used="intelligence",
        description="Unleash a blast of void energy that tears through the target.",
        element="void",
        status_effect="mark",
        status_turns=2
    ),
    "shadow_bolt": Move(
        name="Shadow Bolt",
        mana_cost=5,
        damage=10,
        accuracy_dc=10,
        stat_used="intelligence",
        description="Hurl a bolt of corrupted shadow at your enemy.",
        element="void"
    ),
    "void_shield": Move(
        name="Void Shield",
        mana_cost=6,
        damage=0,
        accuracy_dc=8,
        stat_used="intelligence",
        description="Summon void energy to form a protective barrier.",
        status_effect="shield",
        status_turns=3
    ),
    "soul_drain": Move(
        name="Soul Drain",
        mana_cost=10,
        damage=12,
        accuracy_dc=14,
        stat_used="intelligence",
        description="Tear the soul from your enemy, dealing damage and healing yourself.",
        element="void",
        status_effect="drain",
        status_turns=2
    ),
    "dark_pact": Move(
        name="Dark Pact",
        mana_cost=15,
        damage=20,
        accuracy_dc=16,
        stat_used="void_magic",
        description="Channel forbidden void magic at great personal cost.",
        element="void",
        status_effect="terror",
        status_turns=2
    ),
    "void_walk": Move(
        name="Void Walk",
        mana_cost=12,
        damage=0,
        accuracy_dc=12,
        stat_used="void_magic",
        description="Step through the void to appear behind your enemy."
    ),
}


# Knight Moves - Strength-based melee combat
KNIGHT_MOVES = {
    "shield_bash": Move(
        name="Shield Bash",
        mana_cost=3,
        damage=8,
        accuracy_dc=10,
        stat_used="strength",
        description="Strike with your shield to stun and damage.",
        status_effect="stun",
        status_turns=1
    ),
    "cleaving_strike": Move(
        name="Cleaving Strike",
        mana_cost=6,
        damage=14,
        accuracy_dc=12,
        stat_used="strength",
        description="A powerful overhead swing that hits hard.",
        status_effect="bleed",
        status_turns=3
    ),
    "defensive_stance": Move(
        name="Defensive Stance",
        mana_cost=4,
        damage=0,
        accuracy_dc=8,
        stat_used="combat",
        description="Enter a defensive stance to reduce incoming damage.",
        status_effect="shield",
        status_turns=3
    ),
    "reckless_blow": Move(
        name="Reckless Blow",
        mana_cost=8,
        damage=18,
        accuracy_dc=14,
        stat_used="strength",
        description="An all-or-nothing strike of tremendous power."
    ),
    "blade_storm": Move(
        name="Blade Storm",
        mana_cost=12,
        damage=16,
        accuracy_dc=14,
        stat_used="combat",
        description="Spin and cut through multiple enemies.",
        status_effect="bleed",
        status_turns=2,
        aoe=True
    ),
    "iron_will": Move(
        name="Iron Will",
        mana_cost=5,
        damage=0,
        accuracy_dc=10,
        stat_used="strength",
        description="Channel your will to ignore pain and keep fighting."
    ),
}


# Shadow Moves - Dexterity-based stealth combat
SHADOW_MOVES = {
    "backstab": Move(
        name="Backstab",
        mana_cost=4,
        damage=12,
        accuracy_dc=12,
        stat_used="dexterity",
        description="Strike from the shadows for critical damage.",
        status_effect="bleed",
        status_turns=2
    ),
    "poison_blade": Move(
        name="Poison Blade",
        mana_cost=5,
        damage=8,
        accuracy_dc=10,
        stat_used="stealth",
        description="Coat your blade in deadly poison.",
        status_effect="poison",
        status_turns=3
    ),
    "smoke_bomb": Move(
        name="Smoke Bomb",
        mana_cost=6,
        damage=0,
        accuracy_dc=8,
        stat_used="stealth",
        description="Throw a smoke bomb to obscure vision and escape."
    ),
    "fan_of_knives": Move(
        name="Fan of Knives",
        mana_cost=8,
        damage=10,
        accuracy_dc=12,
        stat_used="dexterity",
        description="Throw multiple daggers in rapid succession.",
        status_effect="bleed",
        status_turns=2,
        aoe=True
    ),
    "shadow_step": Move(
        name="Shadow Step",
        mana_cost=7,
        damage=0,
        accuracy_dc=10,
        stat_used="stealth",
        description="Vanish into shadows and reappear behind an enemy."
    ),
    "assassinate": Move(
        name="Assassinate",
        mana_cost=15,
        damage=25,
        accuracy_dc=16,
        stat_used="dexterity",
        description="A lethal killing blow from stealth.",
        status_effect="mark",
        status_turns=2
    ),
}


# Merchant Moves - Charisma-based social combat
MERCHANT_MOVES = {
    "coin_toss": Move(
        name="Coin Toss",
        mana_cost=2,
        damage=5,
        accuracy_dc=8,
        stat_used="charisma",
        description="Distract with thrown coins and strike."
    ),
    "sweet_talk": Move(
        name="Sweet Talk",
        mana_cost=3,
        damage=0,
        accuracy_dc=10,
        stat_used="charisma",
        description="Charm and confuse your enemy with words.",
        status_effect="mark",
        status_turns=2
    ),
    "intimidate": Move(
        name="Intimidate",
        mana_cost=4,
        damage=0,
        accuracy_dc=12,
        stat_used="charisma",
        description="Scare your enemy into hesitation.",
        status_effect="terror",
        status_turns=2
    ),
    "favor_call": Move(
        name="Call in Favor",
        mana_cost=8,
        damage=0,
        accuracy_dc=14,
        stat_used="influence",
        description="Call in owed favors from your network."
    ),
    "gold_syndrome": Move(
        name="Gold Syndrome",
        mana_cost=10,
        damage=14,
        accuracy_dc=14,
        stat_used="influence",
        description="Bribe nearby enemies to turn on each other."
    ),
    "business_ending": Move(
        name="Business Ending",
        mana_cost=15,
        damage=18,
        accuracy_dc=16,
        stat_used="charisma",
        description="A devastating verbal assault on business rivals."
    ),
}


# Warden Moves - Nature Magic based druid/guardian combat
WARDEN_MOVES = {
    "root_entangle": Move(
        name="Root Entangle",
        mana_cost=5,
        damage=8,
        accuracy_dc=10,
        stat_used="dexterity",
        description="Summon roots to immobilize your enemy.",
        status_effect="freeze",
        status_turns=2
    ),
    "beast_call": Move(
        name="Beast Call",
        mana_cost=8,
        damage=10,
        accuracy_dc=12,
        stat_used="nature_magic",
        description="Call a wolf spirit to fight alongside you."
    ),
    "healing_grove": Move(
        name="Healing Grove",
        mana_cost=6,
        damage=0,
        accuracy_dc=8,
        stat_used="nature_magic",
        description="Channel nature's power to restore 15 HP."
    ),
    "thorn_shield": Move(
        name="Thorn Shield",
        mana_cost=4,
        damage=0,
        accuracy_dc=8,
        stat_used="nature_magic",
        description="Create a shield of thorns that reflects damage.",
        status_effect="shield",
        status_turns=3
    ),
    "natures_wrath": Move(
        name="Nature's Wrath",
        mana_cost=12,
        damage=18,
        accuracy_dc=14,
        stat_used="intelligence",
        description="Unleash the fury of the wild upon your enemy.",
        element="nature"
    ),
    "iron_bark": Move(
        name="Iron Bark",
        mana_cost=7,
        damage=0,
        accuracy_dc=10,
        stat_used="survival",
        description="Harden your skin like oak bark, reducing incoming damage."
    ),
}


def get_moves_for_class(char_class: str) -> dict:
    """Get the moves dictionary for a character class."""
    class_moves = {
        "void_mage": VOID_MAGE_MOVES,
        "knight": KNIGHT_MOVES,
        "shadow": SHADOW_MOVES,
        "merchant": MERCHANT_MOVES,
        "warden": WARDEN_MOVES,
    }
    return class_moves.get(char_class.lower(), {})


def get_move_by_name(char_class: str, move_name: str) -> Move:
    """Get a specific move by name for a character class."""
    moves = get_moves_for_class(char_class)
    for move in moves.values():
        if move.name.lower() == move_name.lower():
            return move


def get_combo_bonus(char_class: str, previous_move: str, current_move: str) -> tuple:
    """
    Check if two moves form a valid combo.
    Returns (bonus_damage, bonus_effect, description)
    """
    combos = COMBO_CHAINS.get(char_class.lower(), [])
    for combo in combos:
        if combo.first_move == previous_move and combo.second_move == current_move:
            return (combo.bonus_damage, combo.bonus_effect, combo.description)
    return (0, "", "")


def get_available_combos(char_class: str, previous_move: str) -> list:
    """Get list of moves that can combo from the previous move."""
    combos = COMBO_CHAINS.get(char_class.lower(), [])
    available = []
    for combo in combos:
        if combo.first_move == previous_move:
            # Get the move object for display
            moves = get_moves_for_class(char_class)
            if combo.second_move in moves:
                move = moves[combo.second_move]
                available.append({
                    "move_key": combo.second_move,
                    "move_name": move.name,
                    "bonus_damage": combo.bonus_damage,
                    "bonus_effect": combo.bonus_effect,
                    "description": combo.description
                })
    return available


def apply_elemental_weakness(base_damage: int, attack_element: str, enemy_weak: str, enemy_strong: str) -> int:
    """Apply elemental weakness/strength modifiers to damage."""
    if enemy_weak and attack_element.lower() == enemy_weak.lower():
        return int(base_damage * 1.5)
    elif enemy_strong and attack_element.lower() == enemy_strong.lower():
        return int(base_damage * 0.5)
    return base_damage
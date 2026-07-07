"""
Velanthor RPG - Enemy Bestiary
All enemies organized by tier with stats and weaknesses.
"""

from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Enemy:
    """Represents an enemy in the game."""
    name: str
    hp: int
    damage: int
    str: int
    dex: int
    int: int
    cha: int
    weak_against: str = ""
    strong_against: str = ""
    description: str = ""
    moves: List[dict] = field(default_factory=list)
    gold_drop: int = 0


# Tier 1 - Basic enemies (starting areas)
TIER_1 = {
    "bandit": Enemy(
        name="Bandit",
        hp=20,
        damage=6,
        str=3,
        dex=3,
        int=2,
        cha=2,
        weak_against="stealth",
        strong_against="charisma",
        description="A desperate outlaw preying on travelers.",
        moves=[{"name": "Dirty Strike", "tell": "shifts his weight to the back foot, blade held low", "damage": 10, "accuracy_dc": 12, "effect": None, "heal": 0, "cooldown": 2}],
        gold_drop=5
    ),
    "street_thug": Enemy(
        name="Street Thug",
        hp=25,
        damage=7,
        str=4,
        dex=3,
        int=2,
        cha=2,
        weak_against="strength",
        strong_against="void_magic",
        description="A rough fighter from the criminal underworld.",
        moves=[{"name": "Low Blow", "tell": "palms something short and heavy, eyes dropping to your knees", "damage": 12, "accuracy_dc": 14, "effect": "stun", "heal": 0, "cooldown": 3}],
        gold_drop=5
    ),
    "void_rat": Enemy(
        name="Void Rat",
        hp=15,
        damage=5,
        str=2,
        dex=4,
        int=1,
        cha=1,
        weak_against="void_magic",
        strong_against="strength",
        description="A corrupted creature tainted by void energy.",
        moves=[{"name": "Toxic Bite", "tell": "hisses, jaw unhinging wider than it should", "damage": 8, "accuracy_dc": 10, "effect": "poison", "heal": 0, "cooldown": 2}],
        gold_drop=5
    ),
}


# Tier 2 - Intermediate enemies (town threats)
TIER_2 = {
    "cultist": Enemy(
        name="Cultist",
        hp=30,
        damage=8,
        str=3,
        dex=3,
        int=4,
        cha=3,
        weak_against="void_magic",
        strong_against="charisma",
        description="A follower of forbidden void cults.",
        moves=[{"name": "Dark Prayer", "tell": "sinks to one knee, muttering into clasped hands", "damage": 0, "accuracy_dc": 0, "effect": None, "heal": 10, "cooldown": 3}],
        gold_drop=8
    ),
    "hollow_guard": Enemy(
        name="Hollow Guard",
        hp=35,
        damage=9,
        str=5,
        dex=3,
        int=2,
        cha=2,
        weak_against="stealth",
        strong_against="strength",
        description="A corrupted soldier serving the Hollow."
    ),
    "watch_mercenary": Enemy(
        name="Watch Mercenary",
        hp=40,
        damage=10,
        str=5,
        dex=4,
        int=3,
        cha=3,
        weak_against="dexterity",
        strong_against="charisma",
        description="A professional fighter hired by corrupt officials.",
        moves=[{"name": "Crossbow Shot", "tell": "steps back and levels the crossbow at your chest", "damage": 12, "accuracy_dc": 8, "effect": None, "heal": 0, "cooldown": 2}],
        gold_drop=8
    ),
    "royal_guard": Enemy(
        name="Royal Guard",
        hp=45,
        damage=12,
        str=6,
        dex=4,
        int=3,
        cha=3,
        weak_against="stealth",
        strong_against="strength",
        description="An elite palace guard protecting the royal family."
    ),
    "guard": Enemy(
        name="Guard",
        hp=30,
        damage=8,
        str=4,
        dex=3,
        int=2,
        cha=2,
        weak_against="stealth",
        strong_against="strength",
        description="A city guard or jailer.",
        moves=[{"name": "Shield Push", "tell": "squares up behind the shield, boots finding purchase", "damage": 8, "accuracy_dc": 10, "effect": "stun", "heal": 0, "cooldown": 2}],
        gold_drop=8
    ),
}


# Tier 3 - Advanced enemies (major threats)
TIER_3 = {
    "hollow_knight": Enemy(
        name="Hollow Knight",
        hp=50,
        damage=14,
        str=7,
        dex=4,
        int=3,
        cha=3,
        weak_against="void_magic",
        strong_against="strength",
        description="An armored warrior corrupted by the Hollow.",
        moves=[{"name": "Dark Cleave", "tell": "raises the greatsword high; void drips from its edge", "damage": 15, "accuracy_dc": 12, "effect": "bleed", "heal": 0, "cooldown": 2}],
        gold_drop=15
    ),
    "cult_leader": Enemy(
        name="Cult Leader",
        hp=45,
        damage=12,
        str=4,
        dex=4,
        int=6,
        cha=5,
        weak_against="void_magic",
        strong_against="charisma",
        description="The dark priest leading the cult faction.",
        moves=[{"name": "Void Bolt", "tell": "traces a sigil that hangs burning in the air", "damage": 12, "accuracy_dc": 10, "effect": "terror", "heal": 0, "cooldown": 2}, {"name": "Dark Benediction", "tell": "opens his arms wide; torn flesh begins to close", "damage": 0, "accuracy_dc": 0, "effect": None, "heal": 15, "cooldown": 3}]
    ),
    "guild_enforcer": Enemy(
        name="Guild Enforcer",
        hp=55,
        damage=15,
        str=6,
        dex=5,
        int=4,
        cha=4,
        weak_against="stealth",
        strong_against="strength",
        description="A muscle-bound enforcer for the thieves guild.",
        moves=[{"name": "Blackjack", "tell": "slips a weighted sap from his sleeve", "damage": 10, "accuracy_dc": 12, "effect": "stun", "heal": 0, "cooldown": 2}],
        gold_drop=12
    ),
}


# Tier 4 - Boss-tier enemies (major villains)
TIER_4 = {
    "vespera": Enemy(
        name="Vespera",
        hp=60,
        damage=16,
        str=5,
        dex=6,
        int=7,
        cha=6,
        weak_against="void_magic",
        strong_against="charisma",
        description="The enigmatic leader of the Shadow Guild.",
        moves=[{"name": "Shadow Lance", "tell": "gathers the dark into a point above her palm", "damage": 16, "accuracy_dc": 12, "effect": "mark", "heal": 0, "cooldown": 2}],
        gold_drop=25
    ),
    "shadowmaster": Enemy(
        name="Shadowmaster",
        hp=55,
        damage=18,
        str=4,
        dex=8,
        int=6,
        cha=5,
        weak_against="void_magic",
        strong_against="stealth",
        description="A master of shadows who commands darkness itself.",
        gold_drop=25
    ),
}


# Tier 5 - Final boss
TIER_5 = {
    "the_hollow_king": Enemy(
        name="The Hollow King",
        hp=80,
        damage=22,
        str=8,
        dex=6,
        int=8,
        cha=7,
        weak_against="void_magic",
        strong_against="charisma",
        description="The corrupted ruler who seeks to plunge the world into void.",
        moves=[{"name": "Void Nova", "tell": "the crown ignites; cold light floods the chamber", "damage": 20, "accuracy_dc": 14, "effect": "terror", "heal": 0, "cooldown": 3}, {"name": "Dark Restoration", "tell": "draws the void inward, knitting himself whole", "damage": 0, "accuracy_dc": 0, "effect": None, "heal": 25, "cooldown": 4}],
        gold_drop=25
    ),
}


# Warden-themed enemies (Ashen Wastes / Northreach)
WARDEN_ENEMIES = {
    "ashen_wolf": Enemy(
        name="Ashen Wolf",
        hp=25,
        damage=8,
        str=4,
        dex=5,
        int=2,
        cha=2,
        weak_against="nature_magic",
        strong_against="strength",
        description="A corrupted wolf tainted by void energy from the Wastes.",
        moves=[{"name": "Feral Bite", "damage": 9, "accuracy_dc": 10, "effect": "bleed", "heal": 0, "cooldown": 2}],
        gold_drop=5
    ),
    "corrupted_treant": Enemy(
        name="Corrupted Treant",
        hp=45,
        damage=12,
        str=7,
        dex=2,
        int=3,
        cha=3,
        weak_against="fire",
        strong_against="void_magic",
        description="A once-noble tree spirit twisted by void corruption.",
        moves=[{"name": "Bramble Whip", "damage": 10, "accuracy_dc": 10, "effect": "freeze", "heal": 0, "cooldown": 2}],
        gold_drop=12
    ),
    "void_serpent": Enemy(
        name="Void Serpent",
        hp=35,
        damage=14,
        str=4,
        dex=6,
        int=4,
        cha=3,
        weak_against="nature_magic",
        strong_against="dexterity",
        description="A serpent born from the darkness between worlds."
    ),
    "northreach_bear": Enemy(
        name="Northreach Bear",
        hp=50,
        damage=15,
        str=8,
        dex=4,
        int=2,
        cha=3,
        weak_against="dexterity",
        strong_against="strength",
        description="A massive bear from the northern forests, fierce and territorial."
    ),
    "wastes_scorpion": Enemy(
        name="Wastes Scorpion",
        hp=20,
        damage=10,
        str=3,
        dex=5,
        int=1,
        cha=1,
        weak_against="fire",
        strong_against="void_magic",
        description="A giant scorpion from the Ashen Wastes with a venomous stinger.",
        moves=[{"name": "Venom Sting", "tell": "arches its tail, venom beading at the barb", "damage": 12, "accuracy_dc": 12, "effect": "poison", "heal": 0, "cooldown": 2}]
    ),
    "hollow_sentinel": Enemy(
        name="Hollow Sentinel",
        hp=55,
        damage=16,
        str=7,
        dex=4,
        int=4,
        cha=4,
        weak_against="nature_magic",
        strong_against="strength",
        description="A corrupted guardian from the old world, serving the Hollow."
    ),
    "spirit_fox": Enemy(
        name="Spirit Fox",
        hp=30,
        damage=9,
        str=3,
        dex=7,
        int=4,
        cha=5,
        weak_against="void_magic",
        strong_against="stealth",
        description="A mystical fox spirit, guide to those who walk the wild."
    ),
    "guardian_north": Enemy(
        name="Guardian of the North",
        hp=65,
        damage=18,
        str=8,
        dex=5,
        int=6,
        cha=6,
        weak_against="nature_magic",
        strong_against="charisma",
        description="An ancient druid who has watched the border for centuries."
    ),
}


# Enemy Tiers dictionary
ENEMY_TIERS = {
    "tier_1": TIER_1,
    "tier_2": TIER_2,
    "tier_3": TIER_3,
    "tier_4": TIER_4,
    "tier_5": TIER_5,
}


# All enemies combined for lookup
ALL_ENEMIES = {}
for tier in ENEMY_TIERS.values():
    ALL_ENEMIES.update(tier)
ALL_ENEMIES.update(WARDEN_ENEMIES)


def get_enemy_by_name(name: str) -> Optional[Enemy]:
    """Get an enemy by name (case-insensitive)."""
    name_lower = name.lower().replace(" ", "_")
    return ALL_ENEMIES.get(name_lower)


def get_enemy_by_tier(tier: str) -> dict:
    """Get all enemies in a tier."""
    tier_lower = tier.lower()
    return ENEMY_TIERS.get(tier_lower, {})


def get_random_enemy(tier: str = "tier_1") -> Enemy:
    """Get a random enemy from a tier."""
    import random
    tier_enemies = get_enemy_by_tier(tier)
    if tier_enemies:
        enemy_list = list(tier_enemies.values())
        return random.choice(enemy_list)
    return None
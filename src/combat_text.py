"""Combat presentation helpers — pure functions, no game state.

All functions return strings (or None); engine.py decides when to print.
Pacing: beat() honors VELANTHOR_FAST so tests and scripted runs skip delays.
"""
import os
import time


def hp_bar(current, maximum, width=20):
    if maximum <= 0:
        return "░" * width
    filled = max(0, min(width, round(width * current / maximum)))
    return "▓" * filled + "░" * (width - filled)


def damage_line(attacker, move_name, damage, target_hp_after, target_max_hp, target="you"):
    frac = target_hp_after / target_max_hp if target_max_hp else 0
    if target_hp_after <= 0:
        if target == "you":
            return f"{attacker}'s {move_name} lands - {damage} - and the world tilts. You are down."
        return f"{attacker} takes {move_name} for {damage} and drops, finished."
    if frac <= 0.25:
        if target == "you":
            return f"{attacker}'s {move_name} tears through your guard - {damage}. You taste copper."
        return f"{move_name} rips into {attacker} for {damage} - it staggers, barely upright."
    if frac <= 0.5:
        if target == "you":
            return f"{attacker}'s {move_name} connects hard - {damage}. Your knees argue."
        return f"{move_name} slams {attacker} for {damage} - it is hurting now."
    if target == "you":
        return f"{attacker}'s {move_name} catches you - {damage}."
    return f"{move_name} strikes {attacker} for {damage}."


def enemy_tell(enemy_name, tell):
    return f"⚠ {enemy_name} {tell}"


def low_hp_warning(current, maximum, already_warned):
    frac = current / maximum if maximum else 0
    if frac <= 0.25 and "quarter" not in already_warned:
        already_warned.update({"half", "quarter"})
        return "Your vision narrows. One more mistake ends this."
    if frac <= 0.5 and "half" not in already_warned:
        already_warned.add("half")
        return "Blood on your grip. This is no longer going your way."
    return None


def beat(seconds=0.45):
    if not os.environ.get("VELANTHOR_FAST"):
        time.sleep(seconds)

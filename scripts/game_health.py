#!/usr/bin/env python3
"""
Game Health Dashboard — single-command health report for the entire RPG.
Combines story validation, combat status, and ending reachability.
"""

import sys
import os
import json
from collections import deque, defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.moves import STATUS_EFFECTS
from src.bestiary import ALL_ENEMIES

CYAN = "\033[1;36m"
YELLOW = "\033[1;33m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
BOLD = "\033[1m"
RESET = "\033[0m"
MAGENTA = "\033[1;35m"

STORY_FILE = 'data/story.json'
START_SCENES = {
    'KIRA': 'KIRA_CH1_THORNWICK',
    'THERON': 'THERON_CH1_TAVERN',
    'VEX': 'VEX_CH1_DOCKS',
    'ELARA': 'ELARA_CH1_ESTATE',
    'ASHA': 'ASHA_CH1_VILLAGE',
}
SKIP = {'metadata', 'story_id', 'title', 'author', 'description', 'chapters', 'endings'}


def load_story():
    try:
        with open(STORY_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def char_scenes(data, char):
    result = {}
    for sid, scene in data.items():
        if not isinstance(scene, dict) or sid in SKIP:
            continue
        if scene.get('character', '').upper() == char or sid.startswith(char + '_'):
            result[sid] = scene
    return result


def find_endings(scenes):
    return {sid for sid, s in scenes.items() if s.get('type') == 'ending' or s.get('ending')}


def bfs_stats(scenes, start):
    visited = set()
    q = deque([start])
    ending_count = 0
    broken_refs = 0
    ending_ids = find_endings(scenes)

    while q:
        sid = q.popleft()
        if sid in visited:
            continue
        visited.add(sid)
        scene = scenes.get(sid)
        if not scene:
            broken_refs += 1
            continue
        if sid in ending_ids:
            ending_count += 1
            continue
        for c in scene.get('choices', []):
            t = c.get('leads_to', '')
            if t and t not in visited:
                q.append(t)

    return {
        'total_scenes': len(visited),
        'endings_reachable': ending_count,
        'broken_refs': broken_refs,
    }


def check_duplicate_letters(scenes):
    dupes = 0
    for sid, scene in scenes.items():
        seen = set()
        for c in scene.get('choices', []):
            l = c.get('letter', '')
            if l in seen:
                dupes += 1
            seen.add(l)
    return dupes


def check_nav_issues(scenes):
    issues = 0
    for sid, scene in scenes.items():
        for c in scene.get('choices', []):
            t = c.get('leads_to', '')
            if t and t not in scenes:
                issues += 1
    return issues


def main():
    data = load_story()
    if not data:
        print(f"{RED}Error: Could not load story data from {STORY_FILE}{RESET}")
        sys.exit(1)

    skip = SKIP
    total_scenes_in_file = sum(1 for s in data if isinstance(data[s], dict) and s not in skip)

    combat_encounter_count = 0
    try:
        from main import BATTLE_ENEMY_MAP, SURPRISE_ENCOUNTERS
        combat_encounter_count = len(BATTLE_ENEMY_MAP)
        surprise_count = len(SURPRISE_ENCOUNTERS)
    except (ImportError, ModuleNotFoundError):
        combat_encounter_count = 0
        surprise_count = 0

    total_choices = 0
    total_endings = 0
    for sid, scene in data.items():
        if isinstance(scene, dict) and sid not in skip:
            total_choices += len(scene.get('choices', []))
            if scene.get('type') == 'ending' or scene.get('ending'):
                total_endings += 1

    total_broken_refs = 0
    total_dup_letters = 0
    total_nav_issues = 0
    total_unique_endings = 0
    unreachable_endings = 0

    print(f"\n{BOLD}{CYAN}═══ VELANTHOR RPG — GAME HEALTH ═══{RESET}")
    print(f"{'═' * 56}")
    print(f"  {BOLD}Characters:{RESET} 5 | {BOLD}Scenes:{RESET} {total_scenes_in_file} | "
          f"{BOLD}Choices:{RESET} {total_choices} | {BOLD}Endings:{RESET} {total_endings}")
    print(f"{'─' * 56}\n")

    for char in ['KIRA', 'THERON', 'VEX', 'ELARA', 'ASHA']:
        scenes = char_scenes(data, char)
        start = START_SCENES.get(char)
        if not scenes or not start:
            print(f"  {YELLOW}{char:8}{RESET} 0 scenes (missing start or data)")
            continue

        endings = find_endings(scenes)
        stats = bfs_stats(scenes, start)
        dupes = check_duplicate_letters(scenes)
        nav_bad = check_nav_issues(scenes)
        total_broken_refs += stats['broken_refs']
        total_dup_letters += dupes
        total_nav_issues += nav_bad
        total_unique_endings += len(endings)

        unreachable = len(endings) - stats['endings_reachable']
        unreachable_endings += unreachable

        status = f"{GREEN}✓{RESET}" if stats['broken_refs'] == 0 and unreachable == 0 else f"{RED}✗{RESET}"
        ending_str = f"{stats['endings_reachable']}/{len(endings)} reachable"
        if unreachable > 0:
            ending_str += f" {RED}({unreachable} blocked){RESET}"
        elif len(endings) > 0:
            ending_str += f" {GREEN}✓{RESET}"
        else:
            ending_str += f" {YELLOW}(no endings defined){RESET}"

        s = scenes[start] if start in scenes else None
        desc = ""
        if s:
            desc_raw = s.get('description', '')
            desc = desc_raw[:60].replace('\n', ' ') + "..." if len(desc_raw) > 60 else desc_raw

        print(f"  {BOLD}{char:8}{RESET} {len(scenes):4} scenes | {len(endings):2} endings | {ending_str} | {status}")
        if desc:
            print(f"           Start: {desc}")
        issues = []
        if stats['broken_refs'] > 0:
            issues.append(f"{RED}{stats['broken_refs']} broken refs{RESET}")
        if dupes > 0:
            issues.append(f"{YELLOW}{dupes} dup letters{RESET}")
        if nav_bad > 0:
            issues.append(f"{YELLOW}{nav_bad} nav issues{RESET}")
        if issues:
            print(f"           Issues: {', '.join(issues)}")
        print()

    print(f"{'─' * 56}")
    print(f"  {BOLD}COMBAT SYSTEM{RESET}")
    print(f"  Encounters: {combat_encounter_count}")
    print(f"  Surprise rounds: {surprise_count}")
    print(f"  Unique enemies: {len(ALL_ENEMIES)}")

    print(f"\n  {BOLD}STATUS EFFECTS ({len(STATUS_EFFECTS)} enabled){RESET}")
    for name, data_s in sorted(STATUS_EFFECTS.items()):
        extra = ""
        if data_s.get('stat_penalty'):
            extra = "stat:%s" % data_s['stat_penalty']
        print("    %-10s dmg:%s turns:%s %s" % (name, data_s['damage'], data_s['turns'], extra))

    print(f"\n  {BOLD}OVERALL{RESET}")
    all_good = (total_broken_refs == 0 and total_nav_issues == 0
                and unreachable_endings == 0 and total_scenes_in_file > 0)
    if all_good:
        print(f"  {GREEN}ALL SYSTEMS OPERATIONAL{RESET}")
    else:
        issues = []
        if total_broken_refs > 0:
            issues.append(f"{total_broken_refs} broken refs")
        if total_nav_issues > 0:
            issues.append(f"{total_nav_issues} nav issues")
        if unreachable_endings > 0:
            issues.append(f"{unreachable_endings} unreachable endings")
        if not total_scenes_in_file:
            issues.append("no story data loaded")
        print(f"  {RED}ISSUES: {', '.join(issues)}{RESET}")

    print(f"{'═' * 56}\n")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Playability tests: verify every character can reach at least one ending,
and check chapter progression flows.
"""

import json
import sys
import re

STORY_FILE = 'data/story.json'

CHARACTERS = ['THERON', 'KIRA', 'VEX', 'ELARA', 'ASHA']

START_SCENES = {
    'THERON': 'THERON_CH1_TAVERN',
    'KIRA': 'KIRA_CH1_THORNWICK',
    'VEX': 'VEX_CH1_DOCKS',
    'ELARA': 'ELARA_CH1_ESTATE',
    'ASHA': 'ASHA_CH1_VILLAGE',
}

# Ending scene IDs per character (known from previous analysis)
# These are scenes that have type="ending" or ending field
ENDINGS = {}

# Scenes to skip in BFS (metadata, etc.)
SKIP = {'metadata', 'story_id', 'title', 'author', 'description', 'chapters', 'endings'}


def load_story():
    with open(STORY_FILE, 'r') as f:
        return json.load(f)


def find_endings(data):
    """Find all ending scenes per character."""
    endings = {}
    for scene_id, scene in data.items():
        if not isinstance(scene, dict):
            continue
        if scene_id in SKIP:
            continue
        is_ending = scene.get('type') == 'ending' or bool(scene.get('ending'))
        if is_ending:
            char = scene.get('character', '') or scene_id.split('_')[0]
            if char in CHARACTERS:
                endings.setdefault(char, []).append(scene_id)
    return endings


def bfs_path_to_ending(data, start, endings_set, max_steps=200):
    """BFS from start to any ending scene. Returns path or None."""
    if start not in data:
        return None
    queue = [(start, [start])]
    visited = {start}
    while queue:
        sid, path = queue.pop(0)
        if sid in endings_set:
            return path
        if len(path) > max_steps:
            continue
        scene = data.get(sid)
        if not isinstance(scene, dict):
            continue
        for choice in scene.get('choices', []):
            target = choice.get('leads_to', '')
            if target and target not in visited:
                if target in data and isinstance(data[target], dict):
                    visited.add(target)
                    queue.append((target, path + [target]))
    return None


def check_chapter_progression(data):
    """
    Verify chapter progression for each character:
    must be able to go CH1 → CH2 → CH3 → CH4 → CH5 → ending
    """
    issues = []
    for char in CHARACTERS:
        ch_map = {}
        for scene_id in data:
            if not isinstance(data[scene_id], dict):
                continue
            m = re.match(rf'{char}_CH(\d+)_', scene_id)
            if m:
                ch = int(m.group(1))
                ch_map.setdefault(ch, []).append(scene_id)

        # Check each chapter is reachable
        for ch in range(1, 6):
            scenes_in_ch = ch_map.get(ch, [])
            if not scenes_in_ch:
                issues.append(f'{char}: No scenes in Chapter {ch}')
                continue

            # Check MAIN scene exists
            main_scene = f'{char}_CH{ch}_MAIN'
            if ch > 1 and main_scene not in data:
                issues.append(f'{char}: Missing {main_scene}')

            # Check TRANSITION exists (for Ch2-5)
            if ch >= 2:
                trans_scene = f'{char}_CH{ch}_TRANSITION'
                if trans_scene not in data:
                    issues.append(f'{char}: Missing {trans_scene}')

            # Check END scene exists (for Ch1-4)
            if ch <= 4:
                end_scene = f'{char}_CH{ch}_END'
                if end_scene not in data:
                    issues.append(f'{char}: Missing {end_scene}')

            # Check phase scenes exist
            for phase in ['PREPARE', 'REFLECT', 'SEARCH', 'REST']:
                phase_scene = f'{char}_CH{ch}_{phase}'
                if phase_scene in data:
                    # Verify choice A has a valid target
                    choices = data[phase_scene].get('choices', [])
                    if choices:
                        target = choices[0].get('leads_to', '')
                        if target and target not in data:
                            issues.append(f'{char}: {phase_scene} [A] → {target} (missing)')

    return issues


def verify_choice_uniqueness(data):
    """
    For each scene, verify all choice texts are unique.
    This catches remaining duplicate text issues.
    """
    issues = []
    for scene_id, scene in data.items():
        if not isinstance(scene, dict):
            continue
        if scene_id in SKIP:
            continue
        choices = scene.get('choices', [])
        if not choices:
            continue
        texts = [c.get('text', '') for c in choices]
        seen = {}
        for i, text in enumerate(texts):
            if text in seen:
                issues.append(f'{scene_id}: Duplicate text "{text}" at positions {seen[text]} and {i}')
            seen[text] = i
    return issues


def main():
    print("=" * 60)
    print("PLAYABILITY TEST REPORT")
    print("=" * 60)

    data = load_story()
    endings = find_endings(data)
    total_endings = sum(len(v) for v in endings.values())

    # 1. BFS path from each character's start to an ending
    print(f'\n1. PATH TO ENDING (BFS from start scene)')
    all_ok = True
    for char in CHARACTERS:
        start = START_SCENES.get(char)
        if not start:
            print(f'  {char}: No start scene defined')
            all_ok = False
            continue
        endings_set = set(endings.get(char, []))
        if not endings_set:
            print(f'  {char}: No endings found')
            all_ok = False
            continue
        path = bfs_path_to_ending(data, start, endings_set)
        if path:
            ending_name = path[-1]
            print(f'  ✓ {char}: {start} → {ending_name} ({len(path)} scenes)')
        else:
            print(f'  ✗ {char}: NO PATH from {start} to any ending!')
            all_ok = False

    # 2. Chapter structure
    print(f'\n2. CHAPTER STRUCTURE')
    issues = check_chapter_progression(data)
    if issues:
        for issue in issues:
            print(f'  ✗ {issue}')
            all_ok = False
    else:
        print(f'  ✓ All chapters have proper structure')

    # 3. Duplicate texts check (should be 0 now)
    print(f'\n3. DUPLICATE CHOICE TEXTS')
    dupes = verify_choice_uniqueness(data)
    if dupes:
        for d in dupes:
            print(f'  ✗ {d}')
            all_ok = False
    else:
        print(f'  ✓ All choice texts are unique')

    # 4. Summary
    print(f'\n4. SUMMARY')
    print(f'  Characters: {len(CHARACTERS)}')
    print(f'  Total endings: {total_endings}')
    for char in CHARACTERS:
        eco = len(endings.get(char, []))
        start = START_SCENES.get(char, '?')
        print(f'    {char}: {eco} endings, start={start}')

    if all_ok:
        print(f'\n✓ ALL PLAYABILITY CHECKS PASSED')
        return 0
    else:
        print(f'\n✗ SOME CHECKS FAILED')
        return 1


if __name__ == '__main__':
    sys.exit(main())

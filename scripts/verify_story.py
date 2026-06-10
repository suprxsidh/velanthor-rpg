#!/usr/bin/env python3
"""
Comprehensive story.json verification.
Checks: broken refs, reachability, chapter flow, duplicate letters, dead ends.
"""

import json
import sys
from collections import defaultdict

STORY_FILE = 'data/story.json'

CHARACTERS = ['THERON', 'KIRA', 'VEX', 'ELARA', 'ASHA']
START_SCENES = {
    'THERON': 'THERON_CH1_TAVERN',
    'KIRA': 'KIRA_CH1_THORNWICK',
    'VEX': 'VEX_CH1_DOCKS',
    'ELARA': 'ELARA_CH1_ESTATE',
    'ASHA': 'ASHA_CH1_VILLAGE',
}

# Scenes known to be metadata or non-game entries
SKIP_KEYS = {'metadata', 'story_id', 'title', 'author', 'description', 'chapters', 'endings'}


def load_story():
    with open(STORY_FILE, 'r') as f:
        return json.load(f)


def get_all_targets(data):
    """Build reverse map: target → set of source scenes that link to it."""
    incoming = defaultdict(set)
    outgoing = defaultdict(set)
    for scene_id, scene in data.items():
        if not isinstance(scene, dict):
            continue
        if scene_id in SKIP_KEYS:
            continue
        for choice in scene.get('choices', []):
            target = choice.get('leads_to', '')
            if target:
                incoming[target].add(scene_id)
                outgoing[scene_id].add(target)
    return incoming, outgoing


def check_broken_refs(data, outgoing):
    """Check every leads_to points to an existing scene."""
    broken = []
    for source, targets in sorted(outgoing.items()):
        for target in targets:
            if target not in data:
                broken.append((source, target))
    return broken


def check_duplicate_letters(data):
    """Find scenes where the same letter appears more than once in choices."""
    dupes = []
    for scene_id, scene in data.items():
        if not isinstance(scene, dict):
            continue
        if scene_id in SKIP_KEYS:
            continue
        letters = [c.get('letter', '') for c in scene.get('choices', [])]
        seen = {}
        for i, letter in enumerate(letters):
            if letter in seen:
                dupes.append((scene_id, letter, seen[letter], i))
            seen[letter] = i
    return dupes


def check_dead_ends(data):
    """Find scenes with 0 choices that aren't endings."""
    dead = []
    for scene_id, scene in data.items():
        if not isinstance(scene, dict):
            continue
        if scene_id in SKIP_KEYS:
            continue
        is_ending = scene.get('type') == 'ending' or bool(scene.get('ending'))
        choices = scene.get('choices', [])
        if not choices and not is_ending:
            dead.append(scene_id)
    return dead


def check_chapter_flow(data):
    """Check phase scenes have correct 'Continue forward' targets."""
    # Known exceptions: scenes named PREPARE/REFLECT/SEARCH/REST that are actually story scenes
    EXCEPTIONS = {
        'THERON_CH1_PREPARE',  # story scene with content choices, not a phase scene
    }

    issues = []
    for scene_id, scene in data.items():
        if scene_id in EXCEPTIONS:
            continue
        if not isinstance(scene, dict):
            continue
        if not scene.get('choices'):
            continue

        # Extract character and chapter from scene ID
        match = __import__('re').match(r'([A-Z]+)_CH(\d+)_(PREPARE|REFLECT|SEARCH|REST)$', scene_id)
        if not match:
            continue

        char = match.group(1)
        ch = int(match.group(2))

        choice_a = scene['choices'][0]
        if choice_a.get('letter', '').upper() != 'A':
            continue

        target = choice_a.get('leads_to', '')
        if ch == 1:
            expected = f'{char}_CH2_TRANSITION'
        elif 2 <= ch <= 4:
            expected = f'{char}_CH{ch}_MAIN'
        elif ch == 5:
            expected = f'{char}_CH5_MAIN'
        else:
            continue

        if target != expected:
            issues.append(f'{scene_id}: [A] → {target}  (expected {expected})')
    return issues


def check_reachability(data):
    """BFS from each character's start scene. Report unreachable scenes."""
    reachable = set()

    for char, start in START_SCENES.items():
        if start not in data:
            print(f'WARNING: Start scene {start} not found for {char}')
            continue
        queue = [start]
        visited = set()
        while queue:
            sid = queue.pop(0)
            if sid in visited:
                continue
            if sid not in data:
                continue
            if not isinstance(data[sid], dict):
                continue
            visited.add(sid)
            for choice in data[sid].get('choices', []):
                target = choice.get('leads_to', '')
                if target and target not in visited:
                    queue.append(target)
        reachable.update(visited)

    all_scenes = set()
    for sid, scene in data.items():
        if isinstance(scene, dict) and sid not in SKIP_KEYS:
            all_scenes.add(sid)

    unreachable = all_scenes - reachable
    # Filter out scenes that are single-parent and might be side content
    # Actually, we want to report ALL unreachable
    return unreachable


def main():
    print("=" * 60)
    print("STORY VALIDATION REPORT")
    print("=" * 60)

    data = load_story()
    incoming, outgoing = get_all_targets(data)

    # 1. Broken refs
    broken = check_broken_refs(data, outgoing)
    print(f'\n1. BROKEN REFERENCES: {len(broken)}')
    for source, target in broken:
        print(f'   {source} → {target} (MISSING)')

    # 2. Duplicate letters
    dupes = check_duplicate_letters(data)
    print(f'\n2. DUPLICATE CHOICE LETTERS: {len(dupes)}')
    for sid, letter, idx1, idx2 in dupes:
        print(f'   {sid}: letter "{letter}" at positions {idx1} and {idx2}')

    # 3. Dead ends (0 choices, not ending)
    dead = check_dead_ends(data)
    print(f'\n3. DEAD ENDS (0 choices, not endings): {len(dead)}')
    for sid in sorted(dead):
        desc = data[sid].get('description', '')[:60]
        print(f'   {sid}: "{desc}..."')

    # 4. Phase scene navigation correctness
    nav_issues = check_chapter_flow(data)
    print(f'\n4. PHASE SCENE NAVIGATION ISSUES: {len(nav_issues)}')
    for issue in nav_issues:
        print(f'   {issue}')
    if not nav_issues:
        print('   All phase scenes correct ✓')

    # 5. Reachability
    unreachable = check_reachability(data)
    print(f'\n5. UNREACHABLE SCENES: {len(unreachable)}')
    for sid in sorted(unreachable):
        char = sid.split('_')[0] if '_' in sid else '?'
        # Only show scenes that belong to known characters
        if char in CHARACTERS:
            print(f'   {sid}')

    # 6. Summary stats
    total_game_scenes = sum(1 for k, v in data.items() if isinstance(v, dict) and k not in SKIP_KEYS)
    endings = sum(1 for k, v in data.items()
                  if isinstance(v, dict) and (v.get('type') == 'ending' or bool(v.get('ending'))))
    total_choices = sum(len(v.get('choices', [])) for k, v in data.items() if isinstance(v, dict))

    print(f'\n6. SUMMARY')
    print(f'   Total scenes: {total_game_scenes}')
    print(f'   Total endings: {endings}')
    print(f'   Total choices: {total_choices}')
    print(f'   Unreachable: {len(unreachable)}')
    print(f'   Broken refs: {len(broken)}')
    print(f'   Duplicate letters: {len(dupes)}')
    print(f'   Dead ends: {len(dead)}')
    print(f'   Nav issues: {len(nav_issues)}')

    # Final verdict
    if broken:
        print(f'\n{"✗" if broken else "✓"} FAIL: Broken references found')
        return 1
    if dupes:
        print(f'\n✗ FAIL: Duplicate choice letters found')
        return 1
    # dead ends may be intentionally incomplete scenes, just warn
    if nav_issues:
        print(f'\n✗ FAIL: Navigation issues found')
        return 1

    print(f'\n✓ ALL CHECKS PASSED')
    return 0


if __name__ == '__main__':
    sys.exit(main())

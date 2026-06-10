#!/usr/bin/env python3
"""
Fix 1: Correct "Continue forward" targets in prepare/reflect/search/rest phase scenes.

Rule:
  CH1 phases  → {CHAR}_CH2_TRANSITION  (forward to next chapter)
  CH2-4 phases → {CHAR}_CH{N}_MAIN      (stay in current chapter)
  CH5 phases  → {CHAR}_CH5_MAIN         (stay in Ch5, not ending)

Plus individual exception overrides for wildly wrong targets.
"""

import json
import sys
import re

STORY_FILE = 'data/story.json'
BACKUP_FILE = 'data/story.json.bak'

CHARACTERS = ['THERON', 'KIRA', 'VEX', 'ELARA', 'ASHA']
PHASES = ['PREPARE', 'REFLECT', 'SEARCH', 'REST']

# Override for individual scenes that don't follow the pattern
# (scene_id, current_looking_for_value) -> new_target
# If current matches, replace with new_target. If current is None, always replace.
EXCEPTIONS = {
    # Theron CH1_PREPARE goes to CH1_TEMPLE instead of CH2_TRANSITION
    'THERON_CH1_PREPARE': ('THERON_CH1_TEMPLE', 'THERON_CH2_TRANSITION'),
    # Kira CH2_PREPARE goes to KIRA_CH2_CROWNHAVEN instead of KIRA_CH2_MAIN
    'KIRA_CH2_PREPARE': ('KIRA_CH2_CROWNHAVEN', 'KIRA_CH2_MAIN'),
    # Vex CH4_PREPARE goes to VEX_CH4_DUEL instead of VEX_CH4_MAIN
    'VEX_CH4_PREPARE': ('VEX_CH4_DUEL', 'VEX_CH4_MAIN'),
    # Vex CH4_SEARCH goes to VEX_CH5_REVENGE_FINAL instead of VEX_CH4_MAIN
    'VEX_CH4_SEARCH': ('VEX_CH5_REVENGE_FINAL', 'VEX_CH4_MAIN'),
    # Vex CH5_PREPARE goes to VEX_CH5_FINALE instead of VEX_CH5_MAIN
    'VEX_CH5_PREPARE': ('VEX_CH5_FINALE', 'VEX_CH5_MAIN'),
    # Vex CH5_SEARCH goes to VEX_CH5_ESCAPE instead of VEX_CH5_MAIN
    'VEX_CH5_SEARCH': ('VEX_CH5_ESCAPE', 'VEX_CH5_MAIN'),
}


def get_expected_target(scene_id):
    """Determine the correct target for a phase scene's choice A."""
    for char in CHARACTERS:
        for ch in range(1, 6):
            for phase in PHASES:
                expected = f'{char}_CH{ch}_{phase}'
                if scene_id == expected:
                    if ch == 1:
                        return f'{char}_CH2_TRANSITION'
                    elif 2 <= ch <= 4:
                        return f'{char}_CH{ch}_MAIN'
                    elif ch == 5:
                        return f'{char}_CH5_MAIN'
    return None


def fix_navigation():
    print("Loading story.json...")
    with open(STORY_FILE, 'r') as f:
        data = json.load(f)

    changes = []
    skipped_not_found = []
    skipped_not_needed = []

    for scene_id in sorted(data.keys()):
        scene = data[scene_id]
        if not isinstance(scene, dict):
            continue
        if 'choices' not in scene or not scene['choices']:
            continue

        choices = scene['choices']
        if not choices:
            continue

        choice_a = choices[0]
        if choice_a.get('letter', '').upper() != 'A':
            continue

        current_target = choice_a.get('leads_to', '')

        # Check exceptions first
        if scene_id in EXCEPTIONS:
            expected_current, new_target = EXCEPTIONS[scene_id]
            if current_target == expected_current:
                if current_target != new_target:
                    choice_a['leads_to'] = new_target
                    changes.append(f'{scene_id}: [A] {current_target} → {new_target} (exception)')
                else:
                    skipped_not_needed.append(f'{scene_id}: already {current_target}')
            else:
                skipped_not_found.append(f'{scene_id}: expected current={expected_current}, found {current_target}')
            continue

        # Apply general rule
        expected_target = get_expected_target(scene_id)
        if expected_target is None:
            continue

        if current_target == expected_target:
            skipped_not_needed.append(f'{scene_id}: already {current_target}')
            continue

        # Check if current target is already the same-chapter MAIN
        # (some are already correct, like Elara/Asha CH5 phases)
        choice_a['leads_to'] = expected_target
        changes.append(f'{scene_id}: [A] {current_target} → {expected_target}')

    print(f'\nChanges applied ({len(changes)}):')
    for c in changes:
        print(f'  {c}')

    if skipped_not_needed:
        print(f'\nAlready correct ({len(skipped_not_needed)}):')
        for s in skipped_not_needed:
            print(f'  {s}')

    if skipped_not_found:
        print(f'\nWARNING - Unexpected current target ({len(skipped_not_found)}):')
        for s in skipped_not_found:
            print(f'  {s}')

    if changes:
        with open(STORY_FILE, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f'\nSaved {STORY_FILE}')
    else:
        print('\nNo changes needed.')


if __name__ == '__main__':
    fix_navigation()

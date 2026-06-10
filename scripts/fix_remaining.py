#!/usr/bin/env python3
"""
Fix remaining issues after nav fix:
1. Revert THERON_CH1_PREPARE (story scene, not phase scene)
2. Fix Asha CH4 duplicate letter D entries
3. Fix Asha CH1_CH2_TRANSITION (skips to CH4)
4. Rename all duplicate "Explore alternative path" texts to unique labels
"""

import json

STORY_FILE = 'data/story.json'

def fix_revert_theron_ch1_prepare(data):
    """Revert THERON_CH1_PREPARE choice A: it's a story scene, not a phase scene."""
    sid = 'THERON_CH1_PREPARE'
    scene = data.get(sid)
    if not scene:
        return 0
    choices = scene.get('choices', [])
    if not choices:
        return 0
    choice_a = choices[0]
    if choice_a.get('letter', '').upper() == 'A' and choice_a.get('leads_to') == 'THERON_CH2_TRANSITION':
        choice_a['leads_to'] = 'THERON_CH1_TEMPLE'
        choice_a['text'] = 'Go to the temple—confront her there'
        print(f'{sid}: reverted A → THERON_CH1_TEMPLE')
        return 1
    return 0


def fix_asha_duplicate_letters(data):
    """Fix duplicate letter D in ASHA_CH4_SEARCH and ASHA_CH4_REST."""
    fixes = 0

    # ASHA_CH4_SEARCH: second D → E
    sid = 'ASHA_CH4_SEARCH'
    scene = data.get(sid)
    if scene:
        choices = scene.get('choices', [])
        d_count = 0
        for c in choices:
            if c.get('letter', '').upper() == 'D':
                d_count += 1
                if d_count == 2:
                    c['letter'] = 'E'
                    print(f'{sid}: second D → E ({c["text"]})')
                    fixes += 1

    # ASHA_CH4_REST: second D → E
    sid = 'ASHA_CH4_REST'
    scene = data.get(sid)
    if scene:
        choices = scene.get('choices', [])
        d_count = 0
        for c in choices:
            if c.get('letter', '').upper() == 'D':
                d_count += 1
                if d_count == 2:
                    c['letter'] = 'E'
                    print(f'{sid}: second D → E ({c["text"]})')
                    fixes += 1

    return fixes


def fix_asha_ch1_transition(data):
    """Fix ASHA_CH1_CH2_TRANSITION pointing to CH4 instead of CH2."""
    sid = 'ASHA_CH1_CH2_TRANSITION'
    scene = data.get(sid)
    if not scene:
        return 0

    fixes = 0
    expected = [
        ('A', 'ASHA_CH4_ALT', 'ASHA_CH2_TRANSITION', 'Continue forward'),
        ('B', 'ASHA_CH4_SEARCH', 'ASHA_CH2_SEARCH', 'Search for answers'),
        ('C', 'ASHA_CH4_REST', 'ASHA_CH2_REST', 'Rest and prepare'),
    ]

    choices = scene.get('choices', [])
    for i, (letter, old_target, new_target, new_text) in enumerate(expected):
        if i < len(choices):
            c = choices[i]
            if c.get('leads_to') == old_target:
                c['leads_to'] = new_target
                c['text'] = new_text
                print(f'{sid}: [{letter}] {old_target} → {new_target}')
                fixes += 1

    return fixes


def fix_duplicate_texts(data):
    """
    Rename all duplicate explore/alternative/etc. texts to unique labels.
    No choices are removed - only text changes.
    """
    changes = 0

    # Mapping of scene_id to list of (letter, new_text) for duplicate choices
    rename_map = {
        'THERON_CH1_MAIN': [
            ('D', 'Investigate a Cult ritual in the hills'),
            ('E', 'Navigate a street ambush'),
            ('F', 'Cross the contested border'),
            ('G', 'Evade the Watch patrol'),
            ('H', 'Survive a night assault'),
            ('I', 'Handle a tavern fight'),
            ('J', 'Outwit the Cult hunters'),
        ],
        'THERON_CH4_MAIN': [
            ('G', 'Move toward the temple'),
            ('H', 'Reflect on your journey'),
            ('L', 'Rest and recover'),
            ('M', 'Search for more information'),
            # I,J,K go to same targets as D,E,F - keep but rename uniquely
            ('I', 'Help the farmer again'),
            ('J', 'Track more corrupted wolves'),
            ('K', 'Investigate the mage further'),
        ],
        'THERON_CH5_MAIN': [
            ('D', 'Search for more answers'),
            ('E', 'Take time to rest'),
        ],
        'KIRA_CH1_MAIN': [
            ('D', 'Shadow the Watch patrol'),
            ('E', 'Ambush the Cult bandits'),
            ('F', 'Face the Circle trial'),
            ('G', 'Explore the deep wasteland'),
            ('H', 'Sense a void-touched child'),
            ('I', 'Search for answers'),
            ('J', 'Question a secret Cultist'),
            ('K', 'Confront the border guard'),
            ('L', 'Stand firm in the wasteland'),
            ('M', 'Face the Watch trial'),
        ],
        'KIRA_CH4_MAIN': [
            ('D', 'Help a merchant with a side quest'),
            ('E', 'Clear out the bandit camp'),
            ('F', 'Journey toward the capital'),
            ('G', 'Reflect on your path'),
            ('H', 'Prepare for what lies ahead'),
            ('I', 'Side quest: merchant again'),
            ('J', 'Clear more bandits'),
            ('K', 'Continue toward the capital'),
        ],
        'VEX_CH4_MAIN': [
            ('N', 'Reform the Guild from within'),
            ('O', 'Fight through the guards'),
            ('P', 'Accept the escape offer'),
            ('Q', 'Counter the Shadowmaster plans'),
            ('R', 'Train a young thief'),
            ('S', 'Investigate the betrayal'),
        ],
        'VEX_CH5_MAIN': [
            ('D', 'Test your allies loyalty'),
            ('E', 'Seek information on the streets'),
            ('F', 'Consider the final offer'),
            ('G', 'Take on an extra job'),
            ('H', 'Ambush the smugglers'),
            ('I', 'Raid the Founder Vault'),
        ],
        'ELARA_CH1_MAIN': [
            ('D', 'Gather information from street kids'),
            ('E', 'Refuse to deal with a shady fence'),
            ('F', 'Accept an old contact job'),
            ('G', 'Investigate a hidden treasure map'),
            ('H', 'Infiltrate the Cult ceremony'),
            ('I', 'Evade a bounty hunter'),
            ('J', 'Witness a noble assault'),
            ('K', 'Complete a pickpocket job'),
        ],
        'ELARA_CH5_MAIN': [
            ('D', 'Pass the Guild initiation test'),
            ('E', 'Quiet interlude before the end'),
            ('F', 'Find a third option'),
            ('G', 'Evade a guard pursuit'),
            ('H', 'Survive an assassin encounter'),
            ('I', 'Settle the merchant war'),
        ],
        'ASHA_CH1_MAIN': [
            ('D', 'Discover a hidden spring'),
            ('E', 'Track and hunt a corrupted beast'),
            ('F', 'Complete the Guardian test'),
            ('G', 'Protect a villager in need'),
            ('H', 'Save a wounded wolf'),
            ('I', 'Follow a forest vision'),
            ('J', 'Learn the spirits language'),
        ],
        'ASHA_CH3_MAIN': [
            ('I', 'Rally the forest spirits'),
            ('J', 'Scout the Cult army'),
            ('K', 'Meditate for guidance'),
            ('L', 'Train with the Wardens'),
            ('M', 'Search ancient ruins'),
        ],
        'ASHA_CH4_MAIN': [
            ('D', 'Make camp and plan your approach'),
            ('E', 'Help a friend in dire need'),
            ('F', 'Consult the stargazer'),
            ('G', 'Pause time to study'),
            ('H', 'Summon spirit helpers'),
            ('I', 'Climb the mountain pass'),
            ('J', 'Walk through memory lane'),
            ('K', 'Scout the Hollow forces'),
            ('L', 'Prepare for aerial battle'),
            ('M', 'Prepare defenses for siege'),
            ('N', 'Walk the void edge'),
            ('O', 'Honor old traditions'),
        ],
        'ASHA_CH5_MAIN': [
            ('E', 'Cross the river crossing'),
            ('F', 'Face the final moment'),
            ('G', 'Learn from the elder'),
            ('H', 'Drive back void creatures'),
            ('I', 'Listen to the forest spirits'),
            ('J', 'Prepare for the pre-battle'),
            ('K', 'Search for final answers'),
            ('L', 'Rally the team together'),
        ],
    }

    for scene_id, renames in rename_map.items():
        scene = data.get(scene_id)
        if not scene:
            print(f'WARNING: {scene_id} not found')
            continue
        choices = scene.get('choices', [])
        for letter, new_text in renames:
            for c in choices:
                if c.get('letter', '').upper() == letter.upper():
                    old_text = c.get('text', '')
                    if old_text != new_text:
                        c['text'] = new_text
                        print(f'{scene_id}: [{letter}] "{old_text}" → "{new_text}"')
                        changes += 1
                    break

    return changes


def main():
    print("Loading story.json...")
    with open(STORY_FILE, 'r') as f:
        data = json.load(f)

    total = 0

    print("\n--- Fix 1: Revert THERON_CH1_PREPARE ---")
    total += fix_revert_theron_ch1_prepare(data)

    print("\n--- Fix 2: Asha duplicate letters ---")
    total += fix_asha_duplicate_letters(data)

    print("\n--- Fix 3: Asha CH1_CH2_TRANSITION ---")
    total += fix_asha_ch1_transition(data)

    print("\n--- Fix 4: Duplicate text labels ---")
    total += fix_duplicate_texts(data)

    if total:
        with open(STORY_FILE, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f'\nTotal fixes applied: {total}')
    else:
        print('\nNo fixes needed.')


if __name__ == '__main__':
    main()

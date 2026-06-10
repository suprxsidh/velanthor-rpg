#!/usr/bin/env python3
"""
Comprehensive per-character story analysis.
Usage: python3 scripts/analyze_character.py <CHARACTER_NAME>
Outputs structured JSON report to stdout.
"""

import json
import re
import sys
from collections import defaultdict, deque

STORY_FILE = 'data/story.json'
SKIP = {'metadata', 'story_id', 'title', 'author', 'description', 'chapters', 'endings'}

START_SCENES = {
    'THERON': 'THERON_CH1_TAVERN',
    'KIRA': 'KIRA_CH1_THORNWICK',
    'VEX': 'VEX_CH1_DOCKS',
    'ELARA': 'ELARA_CH1_ESTATE',
    'ASHA': 'ASHA_CH1_VILLAGE',
}

def load():
    with open(STORY_FILE) as f:
        return json.load(f)

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

def reachable_from_start(scenes, start):
    visited = set()
    q = [start]
    while q:
        sid = q.pop(0)
        if sid in visited or sid not in scenes:
            continue
        visited.add(sid)
        for c in scenes[sid].get('choices', []):
            t = c.get('leads_to', '')
            if t and t not in visited:
                q.append(t)
    return visited

def can_reach_ending(scenes, endings):
    reverse = defaultdict(set)
    for sid, s in scenes.items():
        for c in s.get('choices', []):
            t = c.get('leads_to', '')
            if t:
                reverse[t].add(sid)
    can_reach = set(endings)
    q = list(endings)
    while q:
        sid = q.pop(0)
        for parent in reverse.get(sid, set()):
            if parent not in can_reach:
                can_reach.add(parent)
                q.append(parent)
    return can_reach

def find_graph_components(scenes, start):
    components = []
    all_sids = set(scenes.keys())
    visited_global = set()
    for sid in sorted(all_sids):
        if sid in visited_global:
            continue
        component = set()
        q = [sid]
        while q:
            cur = q.pop(0)
            if cur in visited_global or cur not in scenes:
                continue
            visited_global.add(cur)
            component.add(cur)
            for c in scenes[cur].get('choices', []):
                t = c.get('leads_to', '')
                if t and t not in visited_global and t in scenes:
                    q.append(t)
            for parent in get_parents(scenes, sid):
                if parent not in visited_global and parent in scenes:
                    q.append(parent)
        components.append(component)
    return components

def get_parents(scenes, target):
    parents = set()
    for sid, s in scenes.items():
        for c in s.get('choices', []):
            if c.get('leads_to', '') == target:
                parents.add(sid)
    return parents

def check_illusion_of_choice(scenes):
    issues = []
    for sid, s in sorted(scenes.items()):
        choices = s.get('choices', [])
        target_to_letters = defaultdict(list)
        for c in choices:
            t = c.get('leads_to', '')
            target_to_letters[t].append(c.get('letter', ''))
        for target, letters in target_to_letters.items():
            if len(letters) > 1 and target:
                texts = [c.get('text','') for c in choices if c.get('leads_to','') == target]
                issues.append({
                    'scene': sid,
                    'letters': letters,
                    'same_target': target,
                    'texts': texts
                })
    return issues

def check_spelling_grammar(text, scene_id):
    common_typos = {
        r'\bteh\b': 'the',
        r'\byoure\b': "you're",
        r'\bit\'s\b(?=\s+its)': "its",  # contextual
        r'\bi\b(?=[\'\w])': 'I',
        r'\bi\'m\b': "I'm",
        r'\bdont\b': "don't",
        r'\bdoesnt\b': "doesn't",
        r'\bwont\b': "won't",
        r'\bcant\b': "can't",
        r'\bcouldnt\b': "couldn't",
        r'\bwouldnt\b': "wouldn't",
        r'\bshoudl\b': 'should',
        r'\brecieve\b': 'receive',
        r'\bacheive\b': 'achieve',
        r'\bbeleive\b': 'believe',
        r'\bseperate\b': 'separate',
        r'\bdefinately\b': 'definitely',
        r'\boccured\b': 'occurred',
        r'\boccuring\b': 'occurring',
        r'\baccomodate\b': 'accommodate',
        r'\bembarass\b': 'embarrass',
        r'\bneccessary\b': 'necessary',
        r'\btommorow\b': 'tomorrow',
        r'\bcalender\b': 'calendar',
        r'\bconcious\b': 'conscious',
        r'\bdesparate\b': 'desperate',
        r'\benviroment\b': 'environment',
        r'\bgovernment\b': 'government',
        r'\bindependant\b': 'independent',
        r'\blieing\b': 'lying',
        r'\bminiscule\b': 'minuscule',
        r'\bpriviledge\b': 'privilege',
        r'\bpronounciation\b': 'pronunciation',
        r'\bwierd\b': 'weird',
        r'\bthier\b': 'their',
        r'\btruely\b': 'truly',
        r'\buntill\b': 'until',
        r'\bupper most\b': 'uppermost',
        r'\bwich\b': 'which',
        r'\byou\'r\b': 'your',
    }
    findings = []
    for pattern, correction in common_typos.items():
        for m in re.finditer(pattern, text, re.IGNORECASE):
            findings.append({
                'scene': scene_id,
                'original': m.group(),
                'correction': correction,
                'position': m.start()
            })
    return findings

def analyze_char(char):
    data = load()
    scenes = char_scenes(data, char)
    start = START_SCENES.get(char)
    endings = find_endings(scenes)

    # Basic counts
    total_scenes = len(scenes)
    total_choices = sum(len(s.get('choices', [])) for s in scenes.values())
    total_endings = len(endings)
    death_endings = [e for e in endings if any(w in e.upper() for w in ['DIE','DEATH','DEAD','KILL','FALL','SACRIFICE','BETRAY','BLOOD','MARTYR','PERISH'])]

    # Reachability
    reachable = reachable_from_start(scenes, start) if start else set()
    unreachable = set(scenes.keys()) - reachable

    # Can reach ending
    reaching_ending = can_reach_ending(scenes, endings)
    cant_reach_ending = set(scenes.keys()) - reaching_ending

    # Dead ends
    dead_ends = [sid for sid, s in scenes.items()
                 if not s.get('choices') and sid not in endings]

    # Broken refs
    broken = []
    for sid, s in scenes.items():
        for c in s.get('choices', []):
            t = c.get('leads_to', '')
            if t and t not in data:
                broken.append({'source': sid, 'target': t, 'text': c.get('text','')})

    # Duplicate letters
    dup_letters = []
    for sid, s in scenes.items():
        letters = [c.get('letter','') for c in s.get('choices',[])]
        seen = {}
        for i, l in enumerate(letters):
            if l in seen:
                dup_letters.append({'scene': sid, 'letter': l, 'pos1': seen[l], 'pos2': i})
            seen[l] = i

    # Duplicate texts
    dup_texts = []
    for sid, s in scenes.items():
        texts = [c.get('text','') for c in s.get('choices',[])]
        seen = {}
        for i, t in enumerate(texts):
            if t in seen:
                dup_texts.append({'scene': sid, 'text': t, 'pos1': seen[t], 'pos2': i})
            seen[t] = i

    # Illusion of choice
    illusion = check_illusion_of_choice(scenes)

    # Spelling
    spelling = []
    for sid, s in scenes.items():
        spelling.extend(check_spelling_grammar(s.get('description',''), sid))
        for c in s.get('choices',[]):
            spelling.extend(check_spelling_grammar(c.get('text',''), sid))

    # Chapter flow
    chapter_issues = []
    for ch in range(1, 6):
        main = f'{char}_CH{ch}_MAIN'
        if ch > 1 and main not in scenes and main in data:
            pass
        for phase in ['PREPARE','REFLECT','SEARCH','REST']:
            ps = f'{char}_CH{ch}_{phase}'
            if ps not in scenes:
                continue
            choices = scenes[ps].get('choices',[])
            if choices and choices[0].get('letter','').upper() == 'A':
                target = choices[0].get('leads_to','')
                expected = f'{char}_CH{ch}_MAIN' if ch >= 2 else f'{char}_CH2_TRANSITION'
                if ch == 5:
                    expected = f'{char}_CH5_MAIN'
                if target and target != expected:
                    chapter_issues.append(f'{ps}: [A] -> {target} (expected {expected})')

    # Orphan components (graph parts with no ending)
    all_sids = set(scenes.keys())
    visited_global = set()
    orphan_components = []
    for sid in sorted(all_sids):
        if sid in visited_global:
            continue
        component = set()
        q = [sid]
        while q:
            cur = q.pop(0)
            if cur in visited_global or cur not in scenes:
                continue
            visited_global.add(cur)
            component.add(cur)
            for c in scenes[cur].get('choices', []):
                t = c.get('leads_to', '')
                if t and t not in visited_global and t in scenes:
                    q.append(t)
        has_ending = bool(component & endings)
        if not has_ending and component:
            orphan_components.append(sorted(component))

    # Count branching choices ratio
    branch_ratio = round(total_choices / total_scenes, 2) if total_scenes else 0

    report = {
        'character': char,
        'start_scene': start,
        'total_scenes': total_scenes,
        'total_choices': total_choices,
        'total_endings': total_endings,
        'death_endings': sorted(death_endings),
        'non_death_endings': sorted(endings - set(death_endings)),
        'reachable_from_start': len(reachable),
        'unreachable_scenes': sorted(unreachable),
        'scenes_cant_reach_ending': sorted(cant_reach_ending),
        'dead_ends': sorted(dead_ends),
        'broken_refs': broken,
        'duplicate_letters': dup_letters,
        'duplicate_texts': dup_texts,
        'illusion_of_choice': illusion,
        'chapter_flow_issues': chapter_issues,
        'orphan_components': [{'size': len(c), 'scenes': c} for c in orphan_components],
        'spelling_issues': spelling,
        'branching_ratio': branch_ratio,
        'quality_score_base': 10,
    }

    # Deductions
    deductions = 0
    if broken:
        deductions += 2
    if dup_letters:
        deductions += 1
    if dup_texts:
        deductions += 1
    if dead_ends:
        deductions += 1
    if chapter_issues:
        deductions += 1
    if illusion:
        deductions += 0.5
    if len(unreachable) > 2:
        deductions += 1
    report['quality_score_base'] = max(1, 10 - deductions)

    return report

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_character.py <CHARACTER>", file=sys.stderr)
        sys.exit(1)
    char = sys.argv[1].upper()
    if char not in START_SCENES:
        print(f"Unknown character: {char}", file=sys.stderr)
        sys.exit(1)
    report = analyze_char(char)
    print(json.dumps(report, indent=2))

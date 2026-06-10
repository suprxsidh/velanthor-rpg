#!/usr/bin/env python3
"""
Comprehensive replay tracer: simulates playthroughs for all characters.
Verifies: all scenes reachable, can reach endings, no dead ends, no broken loops.
"""

import json
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

def bfs_all_paths(scenes, start, endings, max_depth=500):
    """BFS to find SHORTEST path from start to each ending."""
    paths_to_ending = {}
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue and len(paths_to_ending) < len(endings):
        sid, path = queue.popleft()
        if sid in endings and sid not in paths_to_ending:
            paths_to_ending[sid] = path
        if len(path) >= max_depth:
            continue
        scene = scenes.get(sid)
        if not isinstance(scene, dict):
            continue
        for choice in scene.get('choices', []):
            target = choice.get('leads_to', '')
            if target and target not in visited and target in scenes:
                visited.add(target)
                queue.append((target, path + [target]))
    return paths_to_ending

def verify_every_choice_reachable(data, char, scenes):
    """Check every choice target is reachable from the start scene."""
    start = START_SCENES[char]
    reachable = set()
    q = [start]
    while q:
        sid = q.pop(0)
        if sid in reachable or sid not in scenes:
            continue
        reachable.add(sid)
        for c in scenes[sid].get('choices', []):
            t = c.get('leads_to', '')
            if t and t not in reachable:
                q.append(t)
    
    unreachable_choices = []
    for sid in scenes:
        if sid not in reachable:
            continue
        for c in scenes[sid].get('choices', []):
            t = c.get('leads_to', '')
            if t and t not in reachable:
                unreachable_choices.append((sid, c.get('letter', '?'), t))
    return unreachable_choices

def dfs_representative_paths(scenes, start, endings, max_paths=5):
    """DFS to find diverse paths exploring different branches."""
    paths = []
    visited_edges = set()
    
    def dfs(sid, path, depth=0):
        if depth > 200:
            return
        if sid in endings:
            paths.append((sid, path))
            return
        
        choices = scenes.get(sid, {}).get('choices', [])
        if not choices:
            return
        
        # Try each choice to explore diversity
        for c in choices:
            t = c.get('leads_to', '')
            edge = (sid, t)
            if t and t in scenes and edge not in visited_edges:
                visited_edges.add(edge)
                dfs(t, path + [t], depth + 1)
                if len(paths) >= max_paths:
                    return
    
    dfs(start, [start])
    return paths

def simulate_playthrough(scenes, start, path):
    """Print a human-readable playthrough trace."""
    print(f'\n--- PLAYTHROUGH: {start} → {path[-1]} ({len(path)} scenes) ---')
    for i, sid in enumerate(path):
        scene = scenes.get(sid, {})
        desc = scene.get('description', '')[:80].replace('\n', ' ')
        choices = scene.get('choices', [])
        print(f'  [{i:3d}] {sid}')
        print(f'        {desc}...')
        if choices and i + 1 < len(path):
            next_sid = path[i + 1]
            for c in choices:
                if c.get('leads_to', '') == next_sid:
                    print(f'        → ({c.get("letter")}) {c.get("text","")[:60]}')
                    break
    print()

def main():
    data = load()
    
    print('=' * 70)
    print('COMPREHENSIVE REPLAY TRACER')
    print('=' * 70)
    
    all_ok = True
    
    for char in ['THERON', 'KIRA', 'VEX', 'ELARA', 'ASHA']:
        print(f'\n{"=" * 70}')
        print(f'CHARACTER: {char}')
        print(f'{"=" * 70}')
        
        scenes = char_scenes(data, char)
        start = START_SCENES[char]
        endings = find_endings(scenes)
        
        print(f'  Total scenes: {len(scenes)}')
        print(f'  Total choices: {sum(len(s.get("choices", [])) for s in scenes.values())}')
        print(f'  Total endings: {len(endings)}')
        
        # 1. Reachability from start
        reachable = set()
        q = [start]
        while q:
            sid = q.pop(0)
            if sid in reachable or sid not in scenes:
                continue
            reachable.add(sid)
            for c in scenes[sid].get('choices', []):
                t = c.get('leads_to', '')
                if t and t not in reachable:
                    q.append(t)
        
        unreachable = set(scenes.keys()) - reachable
        if unreachable:
            print(f'  ✗ UNREACHABLE: {len(unreachable)} scenes')
            for u in sorted(unreachable):
                print(f'      {u}')
            all_ok = False
        else:
            print(f'  ✓ All {len(scenes)} scenes reachable from start')
        
        # 2. Every scene can reach an ending (reverse BFS)
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
        
        cant_reach = set(scenes.keys()) - can_reach
        if cant_reach:
            print(f'  ✗ CANNOT REACH ENDING: {len(cant_reach)} scenes')
            for u in sorted(cant_reach):
                print(f'      {u}')
            all_ok = False
        else:
            print(f'  ✓ All scenes can reach an ending')
        
        # 3. Find paths to each ending
        print(f'  Finding paths to {len(endings)} endings...')
        paths_to = bfs_all_paths(scenes, start, endings)
        unreachable_endings = endings - set(paths_to.keys())
        if unreachable_endings:
            print(f'  ✗ UNREACHABLE ENDINGS: {len(unreachable_endings)}')
            for e in sorted(unreachable_endings):
                print(f'      {e}')
            all_ok = False
        else:
            print(f'  ✓ All {len(endings)} endings reachable')
            # Show shortest path lengths
            path_lens = [(eid, len(p)) for eid, p in paths_to.items()]
            path_lens.sort(key=lambda x: x[1])
            print(f'  Shortest paths: min={path_lens[0][1]}, max={path_lens[-1][1]} scenes')
            for eid, plen in path_lens[:5]:
                print(f'      {eid}: {plen} scenes')
            if len(path_lens) > 5:
                print(f'      ... and {len(path_lens)-5} more')
        
        # 4. DFS representative paths (shows branching works)
        print(f'  Exploring diverse branches...')
        repr_paths = dfs_representative_paths(scenes, start, endings, max_paths=3)
        print(f'  Found {len(repr_paths)} diverse paths')
        for eid, path in repr_paths:
            print(f'      → {eid} ({len(path)} scenes)')
        
        # 5. Verify every choice reaches a reachable target
        bad_choices = verify_every_choice_reachable(data, char, scenes)
        if bad_choices:
            print(f'  ✗ {len(bad_choices)} choices lead to unreachable targets')
            for sid, letter, target in bad_choices[:5]:
                print(f'      {sid} [{letter}] → {target}')
            all_ok = False
        else:
            print(f'  ✓ All choices lead to reachable targets')
        
        # 6. Check for dead ends that aren't endings
        dead = [sid for sid, s in scenes.items()
                if not s.get('choices') and sid not in endings]
        if dead:
            print(f'  ✗ DEAD ENDS: {len(dead)}')
            for d in dead:
                print(f'      {d}')
            all_ok = False
        else:
            print(f'  ✓ No dead ends')
        
        # 7. Play through a representative path
        if repr_paths:
            simulate_playthrough(scenes, start, repr_paths[0][1])
    
    print(f'\n{"=" * 70}')
    if all_ok:
        print('✓ ALL CHARACTERS VERIFIED - GAME IS FULLY PLAYABLE')
    else:
        print('✗ ISSUES FOUND')
    print(f'{"=" * 70}')
    
    return 0 if all_ok else 1

if __name__ == '__main__':
    sys.exit(main())

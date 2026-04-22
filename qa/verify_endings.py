#!/usr/bin/env python3
"""
BFS analysis to verify which endings are reachable from each character's starting scene.
"""

import json
from collections import deque
from typing import Set, Dict, List

def load_story_data():
    """Load story data from JSON files."""
    story = {}
    
    # Load main story file
    with open('data/story.json', 'r') as f:
        story.update(json.load(f))
    
    # Load character-specific files if they exist
    character_files = [
        'data/story_kira.json',
        'data/story_theron.json', 
        'data/story_vex_converted.json',
        'data/story_elara.json'
    ]
    
    for filepath in character_files:
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                story.update(data)
                print(f"Loaded {filepath}: {len(data)} scenes")
        except FileNotFoundError:
            pass
    
    print(f"Total scenes loaded: {len(story)}")
    return story

def get_character_endings(story: Dict, character_prefix: str) -> Set[str]:
    """Get all defined endings for a character (scenes without choices or with 'ending' field)."""
    endings = set()
    for scene_id, scene_data in story.items():
        if not scene_id.startswith(character_prefix + '_'):
            continue
        # Check if it's an ending scene
        if is_ending_scene(scene_id, scene_data):
            endings.add(scene_id)
    return endings

def is_ending_scene(scene_id: str, scene_data: Dict) -> bool:
    """Check if a scene is an ending (terminal node with no choices or with 'ending' field)."""
    # Explicit ending marker
    if scene_data.get('ending'):
        return True
    # Terminal node - no choices
    if not scene_data.get('choices'):
        return True
    return False

def bfs_reachable_endings(story: Dict, start_scene: str) -> Set[str]:
    """BFS from start scene to find all reachable endings."""
    reachable = set()
    visited = set()
    all_reachable_scenes = set()
    queue = deque([start_scene])
    visited.add(start_scene)
    all_reachable_scenes.add(start_scene)
    
    while queue:
        current = queue.popleft()
        
        # Get the scene data
        scene = story.get(current)
        if not scene:
            # This scene is referenced but doesn't exist in data
            print(f"  WARNING: Scene '{current}' referenced but not found in data!")
            continue
        
        # Check if current scene is an ending
        if is_ending_scene(current, scene):
            reachable.add(current)
            continue
        
        # Follow all choices
        choices = scene.get('choices', [])
        for choice in choices:
            next_scene = choice.get('leads_to')
            if next_scene:
                if next_scene not in visited:
                    visited.add(next_scene)
                    all_reachable_scenes.add(next_scene)
                    queue.append(next_scene)
                # Also add to reachable endings if it's a terminal node
                elif next_scene in story:
                    next_data = story[next_scene]
                    if is_ending_scene(next_scene, next_data):
                        reachable.add(next_scene)
    
    print(f"  Total scenes visited: {len(visited)}")
    print(f"  Sample reachable scenes: {sorted(list(all_reachable_scenes)[:10])}")
    
    return reachable

def main():
    story = load_story_data()
    
    # Define starting scenes for each character
    characters = {
        'KIRA': 'KIRA_CH1_THORNWICK',
        'THERON': 'THERON_CH1_TAVERN',
        'VEX': 'VEX_CH1_DOCKS',
        'ELARA': 'ELARA_CH1_ESTATE'
    }
    
    results = {}
    
    for char_name, start_scene in characters.items():
        print(f"\n{'='*60}")
        print(f"Analyzing {char_name} starting from: {start_scene}")
        print(f"{'='*60}")
        
        # Get all defined endings for this character
        all_endings = get_character_endings(story, char_name)
        print(f"Defined endings ({len(all_endings)}): {sorted(all_endings)}")
        
        # BFS to find reachable endings
        reachable = bfs_reachable_endings(story, start_scene)
        
        # Filter to only this character's endings
        char_reachable = {e for e in reachable if e.startswith(char_name + '_ENDING') or e.startswith(char_name + '_CH4_')}
        char_unreachable = all_endings - char_reachable
        
        print(f"\nReachable endings ({len(char_reachable)}):")
        for ending in sorted(char_reachable):
            print(f"  ✓ {ending}")
        
        print(f"\nUnreachable endings ({len(char_unreachable)}):")
        for ending in sorted(char_unreachable):
            print(f"  ✗ {ending}")
        
        results[char_name] = {
            'start': start_scene,
            'all_endings': sorted(all_endings),
            'reachable': sorted(char_reachable),
            'unreachable': sorted(char_unreachable)
        }
    
    # Print summary table
    print(f"\n{'='*80}")
    print("SUMMARY TABLE")
    print(f"{'='*80}")
    print(f"{'Character':<12} {'Reachable':<12} {'Unreachable':<12}")
    print(f"{'-'*12} {'-'*12} {'-'*12}")
    for char_name, data in results.items():
        print(f"{char_name:<12} {len(data['reachable']):<12} {len(data['unreachable']):<12}")
    
    return results

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
DFS analysis of story paths for each character.
Analyzes: max_depth, loops, dead_ends, path_completeness
"""

import json
from typing import Dict, Set, List, Tuple, Optional
from collections import defaultdict

def load_story(filename: str) -> Dict:
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_characters_from_scenes(story_data: Dict) -> Set[str]:
    """Extract unique character prefixes from scene IDs"""
    characters = set()
    for scene_id in story_data.keys():
        # ID format: CHARACTER_CHAPTER_SCENE (e.g., KIRA_CH1_THORNWICK)
        parts = scene_id.split('_')
        if len(parts) >= 1:
            characters.add(parts[0])
    return characters

def get_scenes_for_character(story_data: Dict, character: str) -> Dict[str, dict]:
    """Get all scenes belonging to a specific character"""
    character_scenes = {}
    for scene_id, scene_data in story_data.items():
        if scene_id.startswith(f"{character}_"):
            character_scenes[scene_id] = scene_data
    return character_scenes

def get_next_scenes(scene_id: str, story_data: Dict) -> Tuple[List[str], str]:
    """
    Extract all possible next scene IDs from choices.
    Returns (list of next scene IDs, any error message)
    """
    next_scenes = []
    error_msg = ""
    
    # Get scene data
    scene_data = story_data.get(scene_id)
    if not scene_data:
        return [], f"Scene {scene_id} not in story_data"
    
    if not isinstance(scene_data, dict):
        return [], f"Scene {scene_id} is not a dict: {type(scene_data)}"
    
    choices = scene_data.get('choices', [])
    
    if choices is None:
        return [], f"Scene {scene_id} has null choices"
    
    if not isinstance(choices, list):
        return [], f"Scene {scene_id} choices is not a list: {type(choices)}"
    
    for choice in choices:
        if not isinstance(choice, dict):
            continue
        leads_to = choice.get('leads_to')
        if leads_to:
            next_scenes.append(leads_to)
    
    return next_scenes, error_msg

def dfs_analyze(
    story_data: Dict,
    start_scene: str,
    character_scenes: Set[str]
) -> Tuple[int, int, int, bool, List[str]]:
    """
    Perform DFS from start_scene to analyze all paths.
    
    Returns:
        - max_depth_reached: Maximum depth in the tree
        - loops_found: Number of times we visited a scene we've already visited in current path
        - dead_ends: Number of scenes with no forward paths
        - path_complete: Whether all paths lead to terminal nodes (no broken links)
        - visited_scenes: List of all visited scene IDs
    """
    
    all_visited = set()
    max_depth = 0
    loops_found = 0
    dead_ends = 0
    broken_links = 0
    
    def dfsRecursive(scene_id: str, depth: int, current_path: Set[str]) -> None:
        nonlocal max_depth, loops_found, dead_ends, broken_links
        
        max_depth = max(max_depth, depth)
        
        # Check if scene exists
        if scene_id not in story_data:
            broken_links += 1
            return
        
        # Check for loop (backedge - visiting a node already in current DFS stack)
        if scene_id in current_path:
            loops_found += 1
            return  # Don't continue from a loop node
        
        # Mark as visited
        if scene_id in all_visited:
            # Already fully explored this node
            return
            
        all_visited.add(scene_id)
        
        # Add to current path
        current_path.add(scene_id)
        
        # Get next possible scenes
        next_scenes, error = get_next_scenes(scene_id, story_data)
        
        if error:
            print(f"  Warning: {error}")
        
        # Filter to only valid next scenes
        valid_next = [s for s in next_scenes if s in story_data]
        
        if not valid_next and next_scenes:
            # Some links are broken
            broken_links += len([s for s in next_scenes if s not in story_data])
        
        if not valid_next:
            # Dead end - no valid forward paths
            dead_ends += 1
        else:
            for next_scene in valid_next:
                dfsRecursive(next_scene, depth + 1, current_path.copy())
        
        # Remove from current path (backtracking happens via .copy() above)
    
    # Start DFS
    if start_scene in story_data:
        dfsRecursive(start_scene, 0, set())
    else:
        broken_links += 1
        print(f"  ERROR: Starting scene {start_scene} not found in story data")
    
    path_complete = broken_links == 0
    
    return max_depth, loops_found, dead_ends, path_complete, list(all_visited)

def main():
    # Load story data
    story_data = load_story('data/story.json')
    
    print("=" * 60)
    print("STORY PATH ANALYSIS - DFS WALK")
    print("=" * 60)
    
    # Character starting points as specified
    characters = {
        'KIRA': 'KIRA_CH1_THORNWICK',
        'THERON': 'THERON_CH1_TAVERN',
        'VEX': 'VEX_CH1_DOCKS',
        'ELARA': 'ELARA_CH1_ESTATE'
    }
    
    results = {}
    
    for character, start_scene in characters.items():
        print(f"\n{'=' * 60}")
        print(f"CHARACTER: {character}")
        print(f"Starting Scene: {start_scene}")
        print("=" * 60)
        
        # Get all scenes for this character
        character_scenes = {sid for sid in story_data.keys() if sid.startswith(f"{character}_")}
        
        if not character_scenes:
            print(f"  WARNING: No scenes found for character {character}")
            continue
            
        if start_scene not in story_data:
            print(f"  ERROR: Starting scene {start_scene} not found in story data")
            continue
        
        # Run DFS analysis
        max_depth, loops, dead_ends, path_complete, visited = dfs_analyze(
            story_data, 
            start_scene, 
            character_scenes
        )
        
        results[character] = {
            'max_depth': max_depth,
            'loops_found': loops,
            'dead_ends': dead_ends,
            'path_complete': path_complete,
            'scenes_visited': len(visited),
            'total_character_scenes': len(character_scenes)
        }
        
        print(f"  Total character scenes: {len(character_scenes)}")
        print(f"  Scenes visited: {len(visited)}")
        print(f"  Max depth reached: {max_depth}")
        print(f"  Loops found: {loops}")
        print(f"  Dead ends: {dead_ends}")
        print(f"  Path complete: {'YES' if path_complete else 'NO'}")
    
    # Print summary table
    print("\n" + "=" * 60)
    print("SUMMARY TABLE")
    print("=" * 60)
    print(f"{'Character':<12} {'Max Depth':<12} {'Loops':<8} {'Dead Ends':<12} {'Complete':<10}")
    print("-" * 60)
    
    for char, data in results.items():
        complete_str = "YES" if data['path_complete'] else "NO"
        print(f"{char:<12} {data['max_depth']:<12} {data['loops_found']:<8} {data['dead_ends']:<12} {complete_str:<10}")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
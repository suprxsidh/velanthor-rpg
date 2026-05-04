#!/usr/bin/env python3
"""
Story Graph - Directed graph representation of the RPG story.
Provides path analysis, validation, and expansion helpers.
"""

import json
import hashlib
from collections import deque, defaultdict
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path


@dataclass
class Choice:
    letter: str
    text: str
    leads_to: str
    effects: dict
    is_valid: bool = False


@dataclass
class SceneNode:
    id: str
    character: str
    description: str
    type: str = "story"
    chapter: int = 1
    choices: list = field(default_factory=list)
    is_leaf: bool = False
    is_ending: bool = False
    depth: int = -1
    path_count: int = 0
    parent_count: int = 0


class StoryGraph:
    def __init__(self, story_path: str = "data/story.json"):
        self.story_path = story_path
        self.story_data = {}
        self.nodes: dict[str, SceneNode] = {}
        self.characters: list[str] = []
        self._story_hash: str = ""
        
    def load(self) -> bool:
        """Load story.json and build graph. Returns True if changed."""
        path = Path(self.story_path)
        if not path.exists():
            print(f"Error: {self.story_path} not found")
            return False
            
        with open(path, 'r') as f:
            content = f.read()
            new_hash = hashlib.md5(content.encode()).hexdigest()
            
        if new_hash == self._story_hash:
            print("Graph unchanged, using cached version")
            return False
            
        self.story_data = json.loads(content)
        self._story_hash = new_hash
        self._build_graph()
        return True
    
    def _build_graph(self):
        """Parse story.json into graph structure."""
        self.nodes = {}
        self.characters = []
        
        # First pass: create all nodes
        for scene_id, scene_data in self.story_data.items():
            if not isinstance(scene_data, dict):
                continue
                
            char = scene_data.get('character', '')
            if char and char not in self.characters:
                self.characters.append(char)
            
            chapter = 1
            if '_CH' in scene_id:
                try:
                    chapter = int(scene_id.split('_CH')[1].split('_')[0])
                except:
                    pass
            
            # Check if it's an ending (type='ending' OR has 'ending' field)
            is_ending = scene_data.get('type') == 'ending' or bool(scene_data.get('ending'))
            
            node = SceneNode(
                id=scene_id,
                character=char,
                description= scene_data.get('description', '')[:100],
                type=scene_data.get('type', 'story'),
                chapter=chapter,
                is_ending=is_ending,
                choices=[]
            )
            
            # Parse choices
            for c in scene_data.get('choices', []):
                choice = Choice(
                    letter=c.get('letter', ''),
                    text=c.get('text', ''),
                    leads_to=c.get('leads_to', ''),
                    effects=c.get('effects', {})
                )
                node.choices.append(choice)
            
            self.nodes[scene_id] = node
        
        # Second pass: validate edges
        for node_id, node in self.nodes.items():
            valid_choices = []
            for choice in node.choices:
                choice.is_valid = choice.leads_to in self.nodes
                if choice.is_valid:
                    valid_choices.append(choice)
                else:
                    # Track broken reference
                    pass
            
            node.choices = valid_choices if valid_choices else node.choices
            node.is_leaf = len(node.choices) == 0 or all(not c.is_valid for c in node.choices)
    
    def find_start_nodes(self, character: str = None) -> list[str]:
        """Find starting nodes - prefer Chapter 1 scenes as primary starts."""
        # Get all valid targets
        valid_targets = set()
        for node in self.nodes.values():
            for c in node.choices:
                if c.is_valid:
                    valid_targets.add(c.leads_to)
        
        # Find nodes that are never targeted = potential starts
        untargeted = []
        for node_id, node in self.nodes.items():
            if character and node.character != character:
                continue
            if node_id not in valid_targets:
                untargeted.append((node_id, node))
        
        # Sort by chapter, prefer Ch1 scenes
        untargeted.sort(key=lambda x: (x[1].chapter, x[0]))
        
        # Also include commonly referenced Ch1 nodes as fallbacks
        results = [n[0] for n in untargeted[:5]]
        
        # If we don't have enough, add some Ch1 nodes that might have parents
        if len(results) < 3:
            ch1_nodes = [n for n in self.nodes.keys() 
                        if (not character or self.nodes[n].character == character)
                        and '_CH1_' in n][:5]
            results.extend([n for n in ch1_nodes if n not in results])
        
        return results[:5]
    
    def count_paths_bfs(self, start_node: str, max_depth: int = 30, max_paths: int = 100000) -> int:
        """Count all paths from start to any ending using DFS with cycle detection."""
        if start_node not in self.nodes:
            return 0
        
        total_paths = [0]  # Use list to allow mutation in nested function
        
        def dfs(node_id: str, depth: int, visited: set):
            if total_paths[0] >= max_paths:
                return
            if depth > max_depth:
                return
            if node_id not in self.nodes:
                return
            if node_id in visited:
                return  # Cycle detected
            
            node = self.nodes[node_id]
            if node.is_ending:
                total_paths[0] += 1
                return
            
            visited.add(node_id)
            for choice in node.choices:
                if choice.is_valid:
                    dfs(choice.leads_to, depth + 1, visited.copy())
            visited.discard(node_id)
        
        dfs(start_node, 0, set())
        return min(total_paths[0], max_paths)
    
    def find_all_paths(self, start_node: str, end_node: str = None, max_paths: int = 1000) -> list[list[str]]:
        """Find all paths from start to end (or any ending)."""
        if start_node not in self.nodes:
            return []
        
        paths = []
        
        def dfs(node_id: str, path: list[str]):
            if len(paths) >= max_paths:
                return
            if node_id in path:
                return  # Avoid cycles
                
            path = path + [node_id]
            node = self.nodes.get(node_id)
            
            if not node:
                return
                
            if node.is_ending:
                if end_node is None or end_node == node_id:
                    paths.append(path)
                return
            
            for choice in node.choices:
                if choice.is_valid:
                    dfs(choice.leads_to, path)
        
        dfs(start_node, [])
        return paths
    
    def get_character_stats(self, character: str = None) -> dict:
        """Get detailed statistics for a character or all."""
        stats = {}
        chars = [character] if character else self.characters
        
        for char in chars:
            char_nodes = {k: v for k, v in self.nodes.items() if v.character == char}
            
            # Count by type
            by_type = defaultdict(int)
            by_chapter = defaultdict(int)
            leaf_nodes = []
            ending_nodes = []
            broken_refs = 0
            total_choices = 0
            
            for node in char_nodes.values():
                by_type[node.type] += 1
                by_chapter[node.chapter] += 1
                if node.is_leaf:
                    leaf_nodes.append(node.id)
                if node.is_ending:
                    ending_nodes.append(node.id)
                
                total_choices += len(node.choices)
                for c in node.choices:
                    if not c.is_valid:
                        broken_refs += 1
            
            # Count paths from each potential start
            start_nodes = self.find_start_nodes(char)
            path_counts = {}
            for start in start_nodes[:3]:
                path_counts[start] = self.count_paths_bfs(start)
            
            stats[char] = {
                'total_scenes': len(char_nodes),
                'by_type': dict(by_type),
                'by_chapter': dict(by_chapter),
                'leaf_nodes': len(leaf_nodes),
                'endings': len(ending_nodes),
                'total_choices': total_choices,
                'broken_refs': broken_refs,
                'start_nodes': start_nodes[:3],
                'path_counts': path_counts,
                'sample_leaf_nodes': leaf_nodes[:10],
                'ending_ids': ending_nodes
            }
        
        return stats
    
    def validate(self) -> dict:
        """Validate entire graph and return issues."""
        issues = {
            'broken_refs': [],
            'leaf_nodes_ needing_expansion': [],
            'characters_with_few_endings': [],
            'unbalanced_path_counts': []
        }
        
        for node in self.nodes.values():
            for c in node.choices:
                if not c.is_valid:
                    issues['broken_refs'].append({
                        'from': node.id,
                        'to': c.leads_to,
                        'character': node.character
                    })
        
        # Find leaf nodes that aren't endings
        for node in self.nodes.values():
            if node.is_leaf and not node.is_ending:
                issues['leaf_nodes_ needing_expansion'].append(node.id)
        
        # Check ending counts
        stats = self.get_character_stats()
        for char, s in stats.items():
            if s['endings'] < 10:
                issues['characters_with_few_endings'].append(
                    f"{char}: {s['endings']} endings"
                )
        
        # Check path count balance
        path_counts = []
        for char, s in stats.items():
            total = sum(s['path_counts'].values())
            if total > 0:
                path_counts.append((char, total))
        
        if path_counts:
            max_paths = max(p[1] for p in path_counts)
            min_paths = min(p[1] for p in path_counts)
            if max_paths > min_paths * 10:
                issues['unbalanced_path_counts'].append(
                    f"Max: {max_paths}, Min: {min_paths} (ratio > 10x)"
                )
        
        return issues
    
    def get_expansion_candidates(self, character: str = None) -> list[dict]:
        """Get leaf nodes that should be expanded."""
        candidates = []
        
        for node in self.nodes.values():
            if character and node.character != character:
                continue
            if node.is_leaf and not node.is_ending:
                candidates.append({
                    'id': node.id,
                    'character': node.character,
                    'chapter': node.chapter,
                    'description': node.description[:50],
                    'choices_needed': 3 - len(node.choices)
                })
        
        return sorted(candidates, key=lambda x: (x['character'], x['chapter']))
    
    def export_mermaid(self, character: str = None, max_depth: int = 3) -> str:
        """Export graph as Mermaid diagram."""
        lines = ["graph TD"]
        
        for node_id, node in self.nodes.items():
            if character and node.character != character:
                continue
            if node.chapter > max_depth:
                continue
            
            label = f"{node_id[:20]}.."
            if node.is_ending:
                lines.append(f'    {node_id}["{label}"]:::ending')
            elif node.is_leaf:
                lines.append(f'    {node_id}["{label}"]:::leaf')
            else:
                lines.append(f'    {node_id}["{label}"]')
            
            for c in node.choices:
                if c.is_valid:
                    target_node = self.nodes.get(c.leads_to)
                    if target_node and target_node.chapter <= max_depth:
                        lines.append(f'    {node_id} -->|{c.letter}| {c.leads_to}')
        
        lines.append("    classDef ending fill:#f96,stroke:#333")
        lines.append("    classDef leaf fill:#f99,stroke:#333")
        
        return "\n".join(lines)
    
    def save_cache(self, cache_path: str = "data/story_graph.json"):
        """Save graph to cache file."""
        data = {
            'hash': self._story_hash,
            'characters': self.characters,
            'nodes': {
                k: {
                    'id': v.id,
                    'character': v.character,
                    'type': v.type,
                    'chapter': v.chapter,
                    'is_leaf': v.is_leaf,
                    'is_ending': v.is_ending,
                    'choice_count': len(v.choices),
                    'valid_choice_count': sum(1 for c in v.choices if c.is_valid)
                }
                for k, v in self.nodes.items()
            }
        }
        
        with open(cache_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Graph cached to {cache_path}")


def main():
    """Test and demonstrate the graph."""
    graph = StoryGraph()
    graph.load()
    
    print("=" * 60)
    print("STORY GRAPH ANALYSIS")
    print("=" * 60)
    
    # Get stats for each character
    stats = graph.get_character_stats()
    
    for char in graph.characters:
        s = stats[char]
        print(f"\n{char}:")
        print(f"  Scenes: {s['total_scenes']}")
        print(f"  Endings: {s['endings']}")
        print(f"  Leaf nodes: {s['leaf_nodes']}")
        print(f"  Broken refs: {s['broken_refs']}")
        print(f"  Path counts: {s['path_counts']}")
        print(f"  By chapter: {s['by_chapter']}")
    
    # Validation
    print("\n" + "=" * 60)
    print("VALIDATION ISSUES")
    print("=" * 60)
    
    issues = graph.validate()
    for issue_type, items in issues.items():
        if items:
            print(f"\n{issue_type}: {len(items)}")
            for item in items[:5]:
                print(f"  - {item}")
    
    # Save cache
    graph.save_cache()


if __name__ == "__main__":
    main()
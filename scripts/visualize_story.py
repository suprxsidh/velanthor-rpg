#!/usr/bin/env python3
"""
Story Visualization Tool - ASCII tree rendering and Mermaid export.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.story_graph import StoryGraph


def print_tree(graph: StoryGraph, start_node: str, max_depth: int = 3, prefix: str = "", is_last: bool = True):
    """Print ASCII tree of story paths."""
    node = graph.nodes.get(start_node)
    if not node:
        return
    
    connector = "└── " if is_last else "├── "
    ending_mark = " [ENDING]" if node.is_ending else (" [LEAF]" if node.is_leaf else "")
    type_mark = f" [{node.type}]"
    
    print(f"{prefix}{connector}{node.id}{type_mark}{ending_mark}")
    
    if max_depth <= 0:
        return
    
    new_prefix = prefix + ("    " if is_last else "│   ")
    
    choices = node.choices[:3]  # Limit children display
    
    for i, choice in enumerate(choices):
        is_last_child = (i == len(choices) - 1)
        if choice.is_valid:
            print_tree(graph, choice.leads_to, max_depth - 1, new_prefix, is_last_child)
        else:
            print(f"{new_prefix}{'└── ' if is_last_child else '├── '}{choice.leads_to} [BROKEN]")


def show_character_summary(graph: StoryGraph, character: str):
    """Show summary for a single character."""
    stats = graph.get_character_stats()[character]
    s = stats
    
    print(f"\n{'='*60}")
    print(f"CHARACTER: {character}")
    print(f"{'='*60}")
    
    print(f"\n  Total Scenes: {s['total_scenes']}")
    print(f"  Endings: {s['endings']}")
    print(f"  Leaf Nodes: {s['leaf_nodes']}")
    print(f"  Broken Refs: {s['broken_refs']}")
    
    print(f"\n  By Chapter:")
    for ch in range(1, 6):
        count = s['by_chapter'].get(ch, 0)
        bar = "█" * (count // 3) + "░" * (10 - count // 3)
        print(f"    Ch{ch}: {bar} ({count})")
    
    print(f"\n  Path Counts from Start Nodes:")
    for start, count in s['path_counts'].items():
        print(f"    {start}: {count:,} paths")
    
    if s['sample_leaf_nodes']:
        print(f"\n  Leaf Nodes (need expansion):")
        for leaf in s['sample_leaf_nodes'][:5]:
            print(f"    - {leaf}")
    
    print(f"\n  Endings:")
    for ending in s['ending_ids'][:12]:
        print(f"    - {ending}")


def show_validation_issues(graph: StoryGraph):
    """Show validation issues."""
    issues = graph.validate()
    
    print(f"\n{'='*60}")
    print("VALIDATION ISSUES")
    print(f"{'='*60}")
    
    # Broken refs
    broken = issues['broken_refs']
    if broken:
        print(f"\n  Broken References ({len(broken)}):")
        by_char = {}
        for b in broken:
            by_char[b['character']] = by_char.get(b['character'], 0) + 1
        for char, count in by_char.items():
            print(f"    {char}: {count} broken refs")
    
    # Leaf nodes
    leaves = issues['leaf_nodes_ needing_expansion']
    if leaves:
        print(f"\n  Leaf Nodes Needing Expansion ({len(leaves)}):")
        by_char = {}
        for leaf in leaves:
            char = graph.nodes.get(leaf, {}).character
            by_char[char] = by_char.get(char, 0) + 1
        for char, count in by_char.items():
            print(f"    {char}: {count} leaves")
    
    # Ending counts
    ending_issues = issues['characters_with_few_endings']
    if ending_issues:
        print(f"\n  Characters with Few Endings:")
        for e in ending_issues:
            print(f"    {e}")
    
    # Path imbalance
    path_issues = issues['unbalanced_path_counts']
    if path_issues:
        print(f"\n  Path Count Imbalance:")
        for p in path_issues:
            print(f"    {p}")


def export_mermaid_file(graph: StoryGraph, output_path: str = "story_diagram.mmd"):
    """Export Mermaid diagram for all characters."""
    with open(output_path, 'w') as f:
        f.write("# Story Graph - Mermaid Diagram\n\n")
        
        for char in graph.characters:
            f.write(f"## {char}\n\n")
            f.write("```mermaid\n")
            f.write(graph.export_mermaid(character=char, max_depth=2))
            f.write("\n```\n\n")
    
    print(f"\nExported to {output_path}")


def main():
    """Main visualization entry point."""
    graph = StoryGraph()
    graph.load()
    
    # Parse args
    args = sys.argv[1:]
    
    if not args or '--help' in args or '-h' in args:
        print("""
Story Visualization Tool
Usage: python visualize_story.py [options]

Options:
  --all              Show all characters (default)
  --summary          Show per-character summary
  --validate         Show validation issues
  --tree <char>      Show tree for character
  --mermaid          Export to Mermaid format
  --expand           Show expansion candidates

Examples:
  python scripts/visualize_story.py --summary
  python scripts/visualize_story.py --tree KIRA
  python scripts/visualize_story.py --validate --mermaid
""")
        return
    
    if '--summary' in args or '--all' in args:
        for char in graph.characters:
            show_character_summary(graph, char)
    
    if '--validate' in args:
        show_validation_issues(graph)
    
    if '--tree' in args:
        try:
            idx = args.index('--tree')
            char = args[idx + 1] if idx + 1 < len(args) else 'KIRA'
            stats = graph.get_character_stats()[char]
            for start in stats['start_nodes'][:2]:
                print(f"\n--- Tree from {start} ---")
                print_tree(graph, start, max_depth=2)
        except Exception as e:
            print(f"Error: {e}")
    
    if '--mermaid' in args:
        export_mermaid_file(graph)
    
    if '--expand' in args:
        print("\n" + "="*60)
        print("EXPANSION CANDIDATES (Leaf Nodes)")
        print("="*60)
        
        candidates = graph.get_expansion_candidates()
        by_char = {}
        for c in candidates:
            by_char[c['character']] = by_char.get(c['character'], 0) + 1
        
        for char in graph.characters:
            count = by_char.get(char, 0)
            print(f"\n  {char}: {count} leaf nodes to expand")
            char_cands = [c for c in candidates if c['character'] == char][:5]
            for c in char_cands:
                print(f"    - {c['id']} (Ch{c['chapter']}, needs {c['choices_needed']} choices)")


if __name__ == "__main__":
    main()
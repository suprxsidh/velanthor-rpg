#!/usr/bin/env python3
"""
Agentic Combat System Tests
Writer Agent: Validates move descriptions
Critique Agent: Validates balance
Game Dev Agent: Validates code structure
Verifier Agent: Validates functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.moves import (
    get_moves_for_class, get_combo_bonus, get_available_combos,
    STATUS_EFFECTS, COMBO_CHAINS, Move, ComboChain
)
from src.bestiary import get_enemy_by_name, Enemy

# ANSI colors
GREEN = "\033[1;32m"
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
RESET = "\033[0m"

def pass_test(name):
    print(f"{GREEN}✓{RESET} {name}")

def fail_test(name, reason):
    print(f"{RED}✗{RESET} {name}: {reason}")

def warn_test(name, reason):
    print(f"{YELLOW}⚠{RESET} {name}: {reason}")


class WriterAgent:
    """Validates move descriptions are meaningful and complete."""
    
    def run(self):
        print(f"\n{CYAN}━━━ Writer Agent: Validating Descriptions ━━━{RESET}")
        issues = []
        
        for char_class in ['void_mage', 'knight', 'shadow', 'merchant', 'warden']:
            moves = get_moves_for_class(char_class)
            for key, move in moves.items():
                if not move.description or len(move.description) < 5:
                    issues.append(f"{char_class}.{key}: Description too short")
        
        if issues:
            for issue in issues:
                fail_test("Move descriptions", issue)
            return False
        else:
            pass_test(f"All {sum(len(get_moves_for_class(c)) for c in ['void_mage', 'knight', 'shadow', 'merchant', 'warden'])} moves have valid descriptions")
            return True


class CritiqueAgent:
    """Validates combat balance (mana costs, damage, DC)."""
    
    def run(self):
        print(f"\n{CYAN}━━━ Critique Agent: Validating Balance ━━━{RESET}")
        warnings = []
        
        # Check damage vs mana cost ratio
        for char_class in ['void_mage', 'knight', 'shadow', 'merchant', 'warden']:
            moves = get_moves_for_class(char_class)
            for key, move in moves.items():
                if move.mana_cost > 0 and move.damage > 0:
                    dmg_per_mana = move.damage / move.mana_cost
                    if dmg_per_mana > 4:
                        warnings.append(f"{char_class}.{key}: High efficiency ({dmg_per_mana:.1f} dmg/mana)")
                    elif dmg_per_mana < 1:
                        warnings.append(f"{char_class}.{key}: Low efficiency ({dmg_per_mana:.1f} dmg/mana)")
                
                # DC vs damage check
                if move.damage > 0:
                    if move.accuracy_dc < 10:
                        warnings.append(f"{char_class}.{key}: Low DC ({move.accuracy_dc}) with high damage ({move.damage})")
        
        # Check status effects are reasonable
        for effect, data in STATUS_EFFECTS.items():
            if data.get('damage', 0) > 5:
                warnings.append(f"Status {effect}: High damage ({data['damage']}) per turn")
        
        if warnings:
            for w in warnings[:5]:
                warn_test("Balance check", w)
            print(f"  ... {len(warnings)} total warnings")
        else:
            pass_test("All moves within balance parameters")
        
        return True


class GameDevAgent:
    """Validates code structure (all required fields)."""
    
    def run(self):
        print(f"\n{CYAN}━━━ Game Dev Agent: Validating Structure ━━━{RESET}")
        
        # Check all moves have required fields
        required_fields = ['name', 'mana_cost', 'damage', 'accuracy_dc', 'stat_used', 'description']
        missing = []
        
        for char_class in ['void_mage', 'knight', 'shadow', 'merchant', 'warden']:
            moves = get_moves_for_class(char_class)
            for key, move in moves.items():
                for field in required_fields:
                    if not hasattr(move, field) or getattr(move, field) is None:
                        missing.append(f"{char_class}.{key}.{field}")
        
        if missing:
            fail_test("Move structure", f"Missing fields: {missing[:3]}")
            return False
        
        pass_test("All moves have required fields")
        
        # Check combo chains are valid
        for char_class, combos in COMBO_CHAINS.items():
            moves = get_moves_for_class(char_class)
            for combo in combos:
                if combo.first_move not in moves:
                    fail_test("Combo chain", f"{char_class}.{combo.first_move} not found")
                    return False
                if combo.second_move not in moves:
                    fail_test("Combo chain", f"{char_class}.{combo.second_move} not found")
                    return False
        
        pass_test("All combo chains reference valid moves")
        
        # Check STATUS_EFFECTS has all used status effects
        used_statuses = set()
        for char_class in ['void_mage', 'knight', 'shadow', 'merchant', 'warden']:
            for move in get_moves_for_class(char_class).values():
                if move.status_effect:
                    used_statuses.add(move.status_effect)
        
        missing_effects = used_statuses - set(STATUS_EFFECTS.keys())
        if missing_effects:
            fail_test("Status effects", f"Missing definitions: {missing_effects}")
            return False
        
        pass_test("All used status effects have definitions")
        
        return True


class VerifierAgent:
    """Validates functionality and integration."""
    
    def run(self):
        print(f"\n{CYAN}━━━ Verifier Agent: Validating Functionality ━━━{RESET}")
        
        # Test combo detection
        bonus, effect, desc = get_combo_bonus('void_mage', 'void_burst', 'shadow_bolt')
        if bonus != 5 or effect != 'mark':
            fail_test("Combo detection", f"Expected (5, 'mark'), got ({bonus}, '{effect}')")
            return False
        pass_test("Combo detection works")
        
        # Test available combos
        available = get_available_combos('void_mage', 'void_burst')
        if len(available) != 2:
            fail_test("Available combos", f"Expected 2, got {len(available)}")
            return False
        pass_test("Available combos calculation works")
        
        # Test enemy weaknesses
        enemy = get_enemy_by_name('bandit')
        if not enemy:
            fail_test("Enemy loading", "Could not load bandit")
            return False
        pass_test("Enemy system works")
        
        # Test element weakness calculation
        from src.moves import apply_elemental_weakness
        # Enemy weak_against=stealth, strong_against=charisma
        # attack_element=stealth should hit weakness -> 1.5x
        dmg = apply_elemental_weakness(10, 'stealth', 'stealth', 'charisma')
        if dmg != 15:  # 1.5x for weakness
            fail_test("Elemental weakness", f"Expected 15, got {dmg}")
            return False
        
        # attack_element=charisma should hit strength -> 0.5x
        dmg = apply_elemental_weakness(10, 'charisma', 'stealth', 'charisma')
        if dmg != 5:  # 0.5x for strength
            fail_test("Elemental strength", f"Expected 5, got {dmg}")
            return False
        
        pass_test("Elemental system calculations work")
        
        # Test status effect application (mock)
        test_move = Move("Test", 5, 10, 10, "strength", "Test desc", "void", "poison", 3)
        if test_move.status_effect != "poison" or test_move.status_turns != 3:
            fail_test("Move status fields", "Status fields not properly set")
            return False
        pass_test("Move status fields work")
        
        return True


def main():
    print("=" * 60)
    print("AGENTIC COMBAT SYSTEM TESTS")
    print("=" * 60)
    
    results = []
    
    # Phase 1: Writer Agent
    writer = WriterAgent()
    results.append(("Writer Agent", writer.run()))
    
    # Phase 2: Critique Agent
    critique = CritiqueAgent()
    results.append(("Critique Agent", critique.run()))
    
    # Phase 3: Game Dev Agent
    gamedev = GameDevAgent()
    results.append(("Game Dev Agent", gamedev.run()))
    
    # Phase 4: Verifier Agent
    verifier = VerifierAgent()
    results.append(("Verifier Agent", verifier.run()))
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"  {name}: {status}")
    
    print(f"\nTotal: {passed}/{total} agents passed")
    
    if passed == total:
        print(f"\n{GREEN}✓ ALL AGENTS APPROVED - COMBAT SYSTEM READY{RESET}")
        return 0
    else:
        print(f"\n{RED}✗ SOME AGENTS FAILED - REVIEW NEEDED{RESET}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
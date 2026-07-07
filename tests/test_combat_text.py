import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.combat_text import hp_bar, damage_line, enemy_tell, low_hp_warning


class TestHpBar(unittest.TestCase):
    def test_full(self):
        self.assertEqual(hp_bar(10, 10, width=10), "▓" * 10)

    def test_half(self):
        self.assertEqual(hp_bar(5, 10, width=10), "▓" * 5 + "░" * 5)

    def test_zero_floor(self):
        self.assertEqual(hp_bar(-3, 10, width=10), "░" * 10)


class TestDamageLine(unittest.TestCase):
    def test_contains_number_and_target(self):
        line = damage_line("Bandit", "Dirty Strike", 12, 60, 100)
        self.assertIn("12", line)
        self.assertIn("Bandit", line)

    def test_kill_band_wording_differs(self):
        healthy = damage_line("Bandit", "Dirty Strike", 12, 80, 100)
        kill = damage_line("Bandit", "Dirty Strike", 12, 0, 100)
        self.assertNotEqual(healthy, kill)


class TestEnemyTell(unittest.TestCase):
    def test_contains_name_and_tell(self):
        line = enemy_tell("Hollow Priest", "begins the same syllable twice")
        self.assertIn("Hollow Priest", line)
        self.assertIn("syllable", line)


class TestLowHpWarning(unittest.TestCase):
    def test_warns_once_per_band(self):
        warned = set()
        self.assertIsNotNone(low_hp_warning(49, 100, warned))
        self.assertIsNone(low_hp_warning(45, 100, warned))
        self.assertIsNotNone(low_hp_warning(20, 100, warned))
        self.assertIsNone(low_hp_warning(10, 100, warned))

    def test_no_warning_above_half(self):
        self.assertIsNone(low_hp_warning(80, 100, set()))


if __name__ == "__main__":
    unittest.main()

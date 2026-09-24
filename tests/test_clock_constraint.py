import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "checker"))

from check_clock_constraint import parse_clock, validate


class ClockConstraintTest(unittest.TestCase):
    def test_good_clock_defines_default_same_clock_relationships(self):
        clock = parse_clock(ROOT / "sdc" / "002_clock_good.sdc")
        self.assertEqual(validate(clock), [])
        self.assertEqual(clock.period, 10.0)
        self.assertEqual(clock.setup_edge_separation, 10.0)
        self.assertEqual(clock.hold_edge_separation, 0.0)

    def test_missing_target_is_rejected(self):
        clock = parse_clock(ROOT / "sdc" / "002_clock_bad_target.sdc")
        errors = validate(clock)
        self.assertTrue(any("expected top-level port 'clk'" in e for e in errors))


if __name__ == "__main__":
    unittest.main()

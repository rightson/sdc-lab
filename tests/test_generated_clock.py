import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "checker"))

from check_generated_clock import parse, validate


class GeneratedClockTest(unittest.TestCase):
    def test_generated_clock_keeps_source_lineage(self):
        e = parse(ROOT / "sdc" / "003_generated_clock_good.sdc")
        self.assertEqual(validate(e), [])
        self.assertTrue(e.lineage_preserved)
        self.assertEqual(e.root_period, 10.0)
        self.assertEqual(e.generated_period, 20.0)
        self.assertEqual(e.source_edge_indices, (1, 3, 5))

    def test_same_period_as_independent_clock_is_rejected(self):
        e = parse(ROOT / "sdc" / "003_generated_clock_independent.sdc")
        self.assertEqual(e.generated_period, 20.0)
        self.assertFalse(e.lineage_preserved)
        errors = validate(e)
        self.assertTrue(any("lineage is missing" in err for err in errors))


if __name__ == "__main__":
    unittest.main()

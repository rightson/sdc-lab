import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from timing_model import analyze


class TimingModelTest(unittest.TestCase):
    def test_same_path_passes_with_relaxed_clock(self):
        result = analyze(period=10.0, delay=7.0)
        self.assertEqual(result.slack, 3.0)
        self.assertTrue(result.meets_timing)

    def test_same_path_fails_with_tighter_clock(self):
        result = analyze(period=5.0, delay=7.0)
        self.assertEqual(result.slack, -2.0)
        self.assertFalse(result.meets_timing)

    def test_invalid_clock_is_rejected(self):
        with self.assertRaises(ValueError):
            analyze(period=0.0, delay=7.0)


if __name__ == "__main__":
    unittest.main()

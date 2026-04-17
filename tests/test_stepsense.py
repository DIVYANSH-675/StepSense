import unittest
from stepsense import align, review, segments


class SequenceTests(unittest.TestCase):
    def test_missing_step(self):
        result = review([1, 1, 3, 3], [1, 2, 3])
        self.assertEqual(result["issues"], [{"kind": "missing", "step": 1, "expected": 2}])

    def test_extra_step_has_original_frames(self):
        result = review([1, 1, 7, 7, 2, 2], [1, 2])
        self.assertEqual(result["issues"][0]["frame_range"], [2, 4])
        self.assertEqual(result["issues"][0]["kind"], "extra")

    def test_repeat_and_substitution(self):
        self.assertEqual(align([1, 2, 1], [1, 2, 1])["edit_distance"], 0)
        self.assertEqual(align([1, 2], [1, 3])["issues"][0]["kind"], "substitution")

    def test_debounce_and_empty(self):
        self.assertEqual(segments([9, 1, 1], 2), [{"action": 1, "start": 1, "end": 3}])
        self.assertEqual(review([], [1])["edit_distance"], 1)

    def test_invalid_predictions(self):
        for pred in ([-1], [1.5], [True]):
            with self.assertRaises(ValueError):
                segments(pred)

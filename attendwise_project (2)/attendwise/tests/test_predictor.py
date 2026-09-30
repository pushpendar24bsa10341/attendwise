import unittest

from attendwise import predictor as p


class TestPredictor(unittest.TestCase):
    def test_skip_known_values(self):
        self.assertEqual(p.classes_can_skip(9, 10, 75), 2)    # 9/12 = 75%
        self.assertEqual(p.classes_can_skip(6, 10, 75), 0)    # already short

    def test_needed_known_values(self):
        self.assertEqual(p.classes_needed(6, 10, 75), 6)      # 12/16 = 75%
        self.assertEqual(p.classes_needed(9, 10, 75), 0)

    def test_impossible_at_100_percent(self):
        self.assertIsNone(p.classes_needed(9, 10, 100))
        self.assertEqual(p.classes_needed(10, 10, 100), 0)

    def test_formulas_match_brute_force(self):
        """Check the closed-form answers against simple loops for many inputs."""
        for T in (50, 65, 75, 80, 90):
            for t in range(0, 31):
                for a in range(0, t + 1):
                    x = 0
                    while a * 100 >= T * (t + x + 1):
                        x += 1
                    if p.meets(a, t, T):
                        self.assertEqual(p.classes_can_skip(a, t, T), x, (a, t, T))
                    y = 0
                    while not p.meets(a + y, t + y, T):
                        y += 1
                    self.assertEqual(p.classes_needed(a, t, T), y, (a, t, T))

    def test_status_levels(self):
        self.assertEqual(p.status(0, 0, 75), "NO DATA")
        self.assertEqual(p.status(6, 10, 75), "SHORTAGE")
        self.assertEqual(p.status(8, 10, 75), "SAFE")      # 80% >= 80
        self.assertEqual(p.status(15, 20, 75), "WARNING")  # exactly 75%

    def test_forecast(self):
        self.assertAlmostEqual(p.forecast(15, 20, 10, 2), 23 / 30 * 100)
        with self.assertRaises(ValueError):
            p.forecast(15, 20, 10, 11)

    def test_semester_outlook(self):
        out = p.semester_outlook(15, 20, 10, 75)           # need 23 of 30
        self.assertEqual((out["must_attend"], out["can_miss"]), (8, 2))
        bad = p.semester_outlook(2, 20, 5, 75)
        self.assertFalse(bad["achievable"])

    def test_advice_text(self):
        self.assertIn("skip 2", p.advice(9, 10, 75))
        self.assertIn("next 6", p.advice(6, 10, 75))
        self.assertIn("Do not skip", p.advice(8, 10, 75))   # 80% but 8/11 < 75%


if __name__ == "__main__":
    unittest.main()

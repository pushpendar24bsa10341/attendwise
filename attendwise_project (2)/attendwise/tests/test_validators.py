import unittest
from datetime import date, timedelta

from attendwise import validators as v
from attendwise.exceptions import ValidationError


class TestValidators(unittest.TestCase):
    def test_name(self):
        self.assertEqual(v.validate_name("  Maths "), "Maths")
        for bad in ("", "   ", "x" * 41):
            with self.assertRaises(ValidationError):
                v.validate_name(bad)

    def test_counts(self):
        self.assertEqual(v.validate_counts_pair("8", "10"), (8, 10))
        for a, t in (("11", "10"), ("-1", "5"), ("x", "5"), ("2.5", "5")):
            with self.assertRaises(ValidationError):
                v.validate_counts_pair(a, t)

    def test_threshold(self):
        self.assertEqual(v.validate_threshold("75"), 75)
        for bad in ("0", "101", "abc", ""):
            with self.assertRaises(ValidationError):
                v.validate_threshold(bad)

    def test_present(self):
        self.assertTrue(v.validate_present("P"))
        self.assertFalse(v.validate_present("absent"))
        with self.assertRaises(ValidationError):
            v.validate_present("maybe")

    def test_date(self):
        self.assertEqual(v.validate_date(""), date.today())
        self.assertEqual(v.validate_date("2024-01-15"), date(2024, 1, 15))
        with self.assertRaises(ValidationError):
            v.validate_date("15/01/2024")
        with self.assertRaises(ValidationError):
            v.validate_date((date.today() + timedelta(days=3)).isoformat())


if __name__ == "__main__":
    unittest.main()

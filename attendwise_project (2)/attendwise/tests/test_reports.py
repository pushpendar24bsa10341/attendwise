import csv
import os
import tempfile
import unittest

from attendwise.exceptions import ValidationError
from attendwise.models import Subject
from attendwise.reports import bunk_calculator, build_report, export_csv, whatif_report


class TestReports(unittest.TestCase):
    def setUp(self):
        self.good = Subject("Python", 9, 10, 10)
        self.bad = Subject("Maths", 6, 10, 0)

    def test_report_flags_shortage(self):
        text = build_report([self.good, self.bad], 75)
        self.assertIn("SHORTAGE", text)
        self.assertIn("ATTENTION - shortage in: Maths", text)
        self.assertIn("Overall: 15/20", text)

    def test_empty_report(self):
        self.assertEqual(build_report([], 75), "No subjects yet.")

    def test_bunk_calculator(self):
        text = bunk_calculator(self.good, 75)
        self.assertIn("Can still skip : 2", text)
        self.assertIn("no classes recorded", bunk_calculator(Subject("New"), 75))

    def test_whatif(self):
        self.assertIn("PASS", whatif_report(self.good, 75, 2))
        with self.assertRaises(ValidationError):
            whatif_report(self.good, 75, 99)
        with self.assertRaises(ValidationError):
            whatif_report(self.bad, 75, 1)      # no remaining classes set

    def test_export_csv(self):
        with tempfile.TemporaryDirectory() as d:
            path = export_csv([self.good, self.bad], 75, os.path.join(d, "r.csv"))
            with open(path, newline="") as f:
                rows = list(csv.reader(f))
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[2][4], "SHORTAGE")


if __name__ == "__main__":
    unittest.main()

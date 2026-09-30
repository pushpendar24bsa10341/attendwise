import os
import tempfile
import unittest

from attendwise.exceptions import DuplicateError, NotFoundError, ValidationError
from attendwise.manager import AttendanceManager


class TestManager(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.dir.name, "a.json")
        self.m = AttendanceManager(self.path)

    def tearDown(self):
        self.dir.cleanup()

    def test_add_and_find_case_insensitive(self):
        self.m.add_subject("Python", 8, 10, 20)
        self.assertEqual(self.m.get_subject("python").total, 10)

    def test_duplicate_and_invalid(self):
        self.m.add_subject("Python")
        with self.assertRaises(DuplicateError):
            self.m.add_subject("PYTHON")
        with self.assertRaises(ValidationError):
            self.m.add_subject("Maths", 9, 5)

    def test_log_class_updates_counts_and_remaining(self):
        self.m.add_subject("Python", 8, 10, 5)
        self.m.log_class("Python", "P")
        self.m.log_class("Python", "A")
        s = self.m.get_subject("Python")
        self.assertEqual((s.attended, s.total, s.remaining), (9, 12, 3))

    def test_undo(self):
        self.m.add_subject("Python", 8, 10)
        self.m.log_class("Python", "P")
        self.m.undo_last("Python")
        s = self.m.get_subject("Python")
        self.assertEqual((s.attended, s.total), (8, 10))
        with self.assertRaises(NotFoundError):
            self.m.undo_last("Python")

    def test_update_and_remove(self):
        self.m.add_subject("Python", 8, 10)
        self.m.update_subject("Python", attended="9")
        self.assertEqual(self.m.get_subject("Python").attended, 9)
        with self.assertRaises(ValidationError):
            self.m.update_subject("Python", attended="50")
        self.m.remove_subject("Python")
        with self.assertRaises(NotFoundError):
            self.m.get_subject("Python")

    def test_persistence_and_threshold(self):
        self.m.add_subject("Python", 8, 10, 4)
        self.m.log_class("Python", "A")
        self.m.set_threshold("80")
        again = AttendanceManager(self.path)
        self.assertEqual(again.threshold, 80)
        s = again.get_subject("Python")
        self.assertEqual((s.attended, s.total, len(s.history)), (8, 11, 1))

    def test_bad_log_inputs(self):
        self.m.add_subject("Python")
        with self.assertRaises(ValidationError):
            self.m.log_class("Python", "maybe")
        with self.assertRaises(NotFoundError):
            self.m.log_class("Ghost", "P")


if __name__ == "__main__":
    unittest.main()

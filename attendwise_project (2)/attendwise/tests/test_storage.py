import os
import tempfile
import unittest

from attendwise.storage import DEFAULT_THRESHOLD, load_data


class TestStorage(unittest.TestCase):
    def test_missing_file_gives_defaults(self):
        self.assertEqual(load_data("no/such/file.json"), (DEFAULT_THRESHOLD, []))

    def test_corrupt_file_is_backed_up(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "bad.json")
            with open(path, "w") as f:
                f.write("{ not valid json")
            self.assertEqual(load_data(path), (DEFAULT_THRESHOLD, []))
            self.assertTrue(os.path.exists(path + ".corrupt"))


if __name__ == "__main__":
    unittest.main()

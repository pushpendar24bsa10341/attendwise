"""JSON file storage with safe writes and corrupt-file recovery."""
import json
import os
import shutil

from .exceptions import StorageError
from .logger import get_logger
from .models import Subject

log = get_logger()
DEFAULT_PATH = os.path.join("data", "attendance.json")
DEFAULT_THRESHOLD = 75


def load_data(path=DEFAULT_PATH):
    """Return (threshold, subjects). Missing file -> defaults."""
    if not os.path.exists(path):
        return DEFAULT_THRESHOLD, []
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        subjects = [Subject.from_dict(item) for item in raw["subjects"]]
        return int(raw.get("threshold", DEFAULT_THRESHOLD)), subjects
    except (json.JSONDecodeError, KeyError, ValueError, TypeError):
        backup = path + ".corrupt"
        shutil.copyfile(path, backup)  # keep the bad file for inspection
        log.error("Corrupt data file; backed up to %s", backup)
        return DEFAULT_THRESHOLD, []
    except OSError as err:
        raise StorageError(f"Cannot read {path}: {err}")


def save_data(threshold, subjects, path=DEFAULT_PATH):
    """Write via a temp file so a crash cannot corrupt existing data."""
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        temp = path + ".tmp"
        with open(temp, "w", encoding="utf-8") as f:
            json.dump({"threshold": threshold, "subjects": [s.to_dict() for s in subjects]},
                      f, indent=2)
        os.replace(temp, path)
    except OSError as err:
        log.error("Save failed: %s", err)
        raise StorageError(f"Cannot save data: {err}")

"""Module 1 - Subject & attendance management (CRUD operations)."""
from .exceptions import DuplicateError, NotFoundError
from .logger import get_logger
from .models import Subject
from .storage import DEFAULT_PATH, load_data, save_data
from .validators import (validate_count, validate_counts_pair, validate_date,
                         validate_name, validate_present, validate_threshold)

log = get_logger()


class AttendanceManager:
    """Create, read, update and delete subjects; log classes; hold the threshold."""

    def __init__(self, path=DEFAULT_PATH):
        self.path = path
        self.threshold, self.subjects = load_data(path)

    def _save(self):
        save_data(self.threshold, self.subjects, self.path)

    def get_subject(self, name):
        for subject in self.subjects:
            if subject.name.lower() == (name or "").strip().lower():
                return subject
        raise NotFoundError(f"Subject '{name}' not found.")

    def add_subject(self, name, attended=0, total=0, remaining=0):
        name = validate_name(name, "Subject name")
        attended, total = validate_counts_pair(attended, total)
        remaining = validate_count(remaining, "Remaining classes")
        if any(s.name.lower() == name.lower() for s in self.subjects):
            raise DuplicateError(f"Subject '{name}' already exists.")
        subject = Subject(name, attended, total, remaining)
        self.subjects.append(subject)
        self._save()
        log.info("Added subject %s (%d/%d)", name, attended, total)
        return subject

    def update_subject(self, name, attended=None, total=None, remaining=None):
        subject = self.get_subject(name)
        new_att = subject.attended if attended in (None, "") else attended
        new_tot = subject.total if total in (None, "") else total
        subject.attended, subject.total = validate_counts_pair(new_att, new_tot)
        if remaining not in (None, ""):
            subject.remaining = validate_count(remaining, "Remaining classes")
        self._save()
        log.info("Updated subject %s", subject.name)
        return subject

    def remove_subject(self, name):
        subject = self.get_subject(name)
        self.subjects.remove(subject)
        self._save()
        log.info("Removed subject %s", subject.name)

    def log_class(self, name, present, day=None):
        subject = self.get_subject(name)
        subject.log_class(validate_present(present), validate_date(day))
        self._save()
        log.info("Logged class for %s (present=%s)", subject.name, subject.history[-1].present)
        return subject

    def undo_last(self, name):
        subject = self.get_subject(name)
        record = subject.undo_last()
        self._save()
        log.info("Undid last entry for %s", subject.name)
        return record

    def set_threshold(self, value):
        self.threshold = validate_threshold(value)
        self._save()
        log.info("Threshold set to %d", self.threshold)

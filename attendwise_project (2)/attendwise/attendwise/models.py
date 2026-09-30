"""Data models: Record (one logged class) and Subject."""
from datetime import date, datetime

from .exceptions import NotFoundError


class Record:
    """One class that was logged as present or absent."""

    def __init__(self, day, present):
        self.day = day            # datetime.date
        self.present = present    # bool

    def to_dict(self):
        return {"date": self.day.isoformat(), "present": self.present}

    @classmethod
    def from_dict(cls, data):
        return cls(datetime.strptime(data["date"], "%Y-%m-%d").date(), bool(data["present"]))


class Subject:
    """Attendance counters for one subject plus the log of individual classes."""

    def __init__(self, name, attended=0, total=0, remaining=0, history=None):
        self.name = name
        self.attended = attended      # classes attended so far
        self.total = total            # classes held so far
        self.remaining = remaining    # classes still to be held this semester
        self.history = history or []  # list of Record

    def percentage(self):
        return 0.0 if self.total == 0 else self.attended / self.total * 100

    def log_class(self, present, day=None):
        """Record one class; also uses up one 'remaining' class if any are left."""
        self.total += 1
        if present:
            self.attended += 1
        if self.remaining > 0:
            self.remaining -= 1
        self.history.append(Record(day or date.today(), present))

    def undo_last(self):
        """Reverse the most recently logged class."""
        if not self.history:
            raise NotFoundError(f"No logged classes to undo for {self.name}.")
        last = self.history.pop()
        self.total -= 1
        if last.present:
            self.attended -= 1
        return last

    def to_dict(self):
        return {"name": self.name, "attended": self.attended, "total": self.total,
                "remaining": self.remaining, "history": [r.to_dict() for r in self.history]}

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], int(data["attended"]), int(data["total"]),
                   int(data.get("remaining", 0)),
                   [Record.from_dict(r) for r in data.get("history", [])])

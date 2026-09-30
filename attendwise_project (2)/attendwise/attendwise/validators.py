"""Input validation helpers. Each returns a clean value or raises ValidationError."""
from datetime import date, datetime

from .exceptions import ValidationError


def validate_name(value, label="Name", max_len=40):
    value = (value or "").strip()
    if not value:
        raise ValidationError(f"{label} cannot be empty.")
    if len(value) > max_len:
        raise ValidationError(f"{label} must be at most {max_len} characters.")
    return value


def validate_count(value, label="Value"):
    """Whole number >= 0 (used for class counts)."""
    try:
        number = int(str(value).strip())
    except (TypeError, ValueError):
        raise ValidationError(f"{label} must be a whole number.")
    if number < 0:
        raise ValidationError(f"{label} cannot be negative.")
    return number


def validate_counts_pair(attended, total):
    """Attended classes can never exceed total classes."""
    attended = validate_count(attended, "Classes attended")
    total = validate_count(total, "Total classes held")
    if attended > total:
        raise ValidationError("Classes attended cannot be more than total classes held.")
    return attended, total


def validate_threshold(value):
    """Required attendance percentage, a whole number from 1 to 100."""
    try:
        number = int(str(value).strip())
    except (TypeError, ValueError):
        raise ValidationError("Required percentage must be a whole number (e.g. 75).")
    if not 1 <= number <= 100:
        raise ValidationError("Required percentage must be between 1 and 100.")
    return number


def validate_present(value):
    """Accepts p/present/y/yes or a/absent/n/no (case-insensitive)."""
    text = str(value).strip().lower()
    if text in ("p", "present", "y", "yes"):
        return True
    if text in ("a", "absent", "n", "no"):
        return False
    raise ValidationError("Enter P for present or A for absent.")


def validate_date(value=None):
    """Parse YYYY-MM-DD. Blank means today. Future dates are not allowed."""
    if value is None or (isinstance(value, str) and not value.strip()):
        return date.today()
    if isinstance(value, date):
        parsed = value
    else:
        try:
            parsed = datetime.strptime(value.strip(), "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError("Date must be in YYYY-MM-DD format.")
    if parsed > date.today():
        raise ValidationError("You cannot log a class for a future date.")
    return parsed

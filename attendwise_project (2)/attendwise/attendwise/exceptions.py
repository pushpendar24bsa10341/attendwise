"""Custom exceptions used across AttendWise (error handling strategy)."""


class AttendWiseError(Exception):
    """Base class for all application errors."""


class ValidationError(AttendWiseError):
    """Raised when user input is invalid."""


class NotFoundError(AttendWiseError):
    """Raised when a subject or log entry does not exist."""


class DuplicateError(AttendWiseError):
    """Raised when a subject already exists."""


class StorageError(AttendWiseError):
    """Raised when data cannot be read from or written to disk."""

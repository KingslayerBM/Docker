class DomainError(Exception):
    """Base class for domain-level errors."""


class ValidationError(DomainError):
    """Raised when an entity/value object fails validation."""


class DiffValidationError(Exception):
    pass


class FileScopeViolation(DiffValidationError):
    pass


class ActionTypeViolation(DiffValidationError):
    pass


class EmptyDiffNotAllowed(DiffValidationError):
    pass


class ContextMismatchViolation(DiffValidationError):
    pass

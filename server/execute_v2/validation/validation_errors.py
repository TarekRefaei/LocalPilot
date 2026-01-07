from server.execute_v2.errors.classified_error import ClassifiedExecutionError
from server.execute_v2.errors.codes import ErrorCode


class DiffValidationError(ClassifiedExecutionError):
    def __init__(self, message: str = "Diff validation error", code: str = "DIFF_VALIDATION_ERROR", retryable: bool = False):
        super().__init__(code, message, retryable)


class FileScopeViolation(DiffValidationError):
    def __init__(self, message: str = "File scope violation"):
        super().__init__(message, ErrorCode.FILE_SCOPE_VIOLATION, retryable=False)


class ActionTypeViolation(DiffValidationError):
    def __init__(self, message: str = "Action type violation"):
        super().__init__(message, ErrorCode.ACTION_TYPE_VIOLATION, retryable=False)


class EmptyDiffNotAllowed(DiffValidationError):
    def __init__(self, message: str = "Empty diff not allowed"):
        super().__init__(message, ErrorCode.EMPTY_DIFF_NOT_ALLOWED, retryable=True)


class ContextMismatchViolation(DiffValidationError):
    def __init__(self, message: str = (
        "Top-level return detected in script file. Script files must use print(...) instead of return."
    )):
        super().__init__(message, ErrorCode.CONTEXT_MISMATCH, retryable=True)

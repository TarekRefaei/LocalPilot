class ClassifiedExecutionError(Exception):
    def __init__(self, code: str, message: str, retryable: bool):
        self.code = code
        self.retryable = retryable
        super().__init__(message)

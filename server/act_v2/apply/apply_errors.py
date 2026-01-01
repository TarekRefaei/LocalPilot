class ApplyError(Exception):
    pass


class PatchApplyFailed(ApplyError):
    pass


class WorkspaceWriteViolation(ApplyError):
    pass

from __future__ import annotations
from pathlib import Path
import re


def is_absolute_path(fp: str) -> bool:
    try:
        if Path(fp).is_absolute():
            return True
    except Exception:
        pass
    # Windows drive pattern e.g. C:\ or D:/
    try:
        if bool(re.match(r"^[A-Za-z]:\\", fp)):
            return True
    except Exception:
        pass
    return False


def has_windows_separators(fp: str) -> bool:
    try:
        return "\\" in fp
    except Exception:
        return False


def is_directory_path(fp: str) -> bool:
    try:
        return fp.endswith("/")
    except Exception:
        return False


def is_multi_file_reference(fp: str) -> bool:
    try:
        return "," in fp
    except Exception:
        return False

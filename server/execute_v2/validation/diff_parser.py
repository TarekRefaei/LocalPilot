import re


DIFF_HEADER = re.compile(r"^---\s+.+\n\+\+\+\s+.+", re.MULTILINE)


def extract_diff(diff_text: str) -> str:
    # normalize EOLs and trim outer whitespace
    text = (diff_text or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    if not text:
        return ""

    if not DIFF_HEADER.search(text):
        raise ValueError("Output is not a valid unified diff")

    lines = text.splitlines()
    # find the first header line to start from
    start = 0
    for i, line in enumerate(lines):
        if line.startswith("diff --git") or line.startswith("--- "):
            start = i
            break

    allowed_starts = (
        "diff --git",
        "index ",
        "--- ",
        "+++ ",
        "@@",
        " ",
        "+",
        "-",
    )

    cleaned: list[str] = []
    for line in lines[start:]:
        if line.startswith(allowed_starts) or line.startswith("\\ No newline"):
            cleaned.append(line)
        else:
            # stop at first invalid line (e.g., trailing '...', code fences, prose)
            break

    result = "\n".join(cleaned).strip()
    if not DIFF_HEADER.search(result):
        raise ValueError("Output is not a valid unified diff")

    return result

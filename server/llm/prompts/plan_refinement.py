from pathlib import Path


def _load_prompt() -> str:
    here = Path(__file__).resolve().parent
    return (here / "plan_refinement.md").read_text(encoding="utf-8")


PROMPT = _load_prompt()

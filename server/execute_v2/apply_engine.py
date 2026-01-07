import subprocess
import tempfile
import shutil
from pathlib import Path
import logging
import hashlib
from server.execute_v2.validation.python_ast_validator import (
    validate_python_structure,
    PythonStructureError,
)


logger = logging.getLogger(__name__)


class ApplyError(Exception):
    pass


class ApplyEngine:
    def __init__(self, workspace: Path):
        self.workspace = workspace

    def apply(self, diff: str, *, is_script: bool = False) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            shutil.copytree(self.workspace, tmp_path / "repo", dirs_exist_ok=True)

            # Normalize line endings for files involved in the patch to avoid CRLF/BOM mismatches
            for rel in self._files_in_diff(diff):
                p = (tmp_path / "repo" / rel).resolve()
                if p.exists() and p.is_file():
                    try:
                        data = p.read_text(encoding="utf-8-sig", errors="ignore")
                        # force LF endings
                        data = data.replace("\r\n", "\n").replace("\r", "\n")
                        p.write_text(data, encoding="utf-8")
                    except Exception:
                        # best effort; continue even if normalization fails
                        pass

            # Make git more tolerant of line ending differences in this temp repo
            try:
                subprocess.run(["git", "init"], cwd=tmp_path / "repo", capture_output=True, text=True)
                subprocess.run(["git", "config", "core.autocrlf", "false"], cwd=tmp_path / "repo", capture_output=True, text=True)
                subprocess.run(["git", "config", "core.safecrlf", "false"], cwd=tmp_path / "repo", capture_output=True, text=True)
            except Exception:
                pass

            # Normalize diff line endings and ensure trailing newline to avoid EOF matching issues
            normalized = diff.replace("\r\n", "\n").replace("\r", "\n")
            diff_to_apply = normalized if normalized.endswith("\n") else normalized + "\n"

            proc = subprocess.run(
                [
                    "git",
                    "apply",
                    "--whitespace=nowarn",
                    "--ignore-space-change",
                    "--ignore-whitespace",
                    "--inaccurate-eof",
                ],
                input=diff_to_apply,
                text=True,
                cwd=tmp_path / "repo",
                capture_output=True,
            )

            if proc.returncode != 0:
                logger.error("GIT APPLY ERROR (strict):\n%s", proc.stderr)
                # Retry with --reject to attempt best-effort application
                retry = subprocess.run(
                    [
                        "git",
                        "apply",
                        "--reject",
                        "--whitespace=nowarn",
                        "--ignore-space-change",
                        "--ignore-whitespace",
                        "--inaccurate-eof",
                    ],
                    input=diff_to_apply,
                    text=True,
                    cwd=tmp_path / "repo",
                    capture_output=True,
                )
                if retry.returncode != 0:
                    logger.error("GIT APPLY ERROR (reject):\n%s", retry.stderr)
                    # Final fallback: attempt Python-side unified diff apply for single-file patch
                    try:
                        self._apply_unified_diff_python(tmp_path / "repo", diff_to_apply)
                    except Exception as e:
                        raise ApplyError(
                            "Patch could not be applied cleanly.\n"
                            "Reason:\n" + proc.stderr + ("\n" + retry.stderr if retry.stderr else "")
                        ) from e

            # AST validation for Python files before writing back
            try:
                changed = self._files_in_diff(diff)
                for rel in changed:
                    if rel.endswith('.py'):
                        py_path = (tmp_path / "repo" / rel).resolve()
                        if py_path.exists():
                            new_source = py_path.read_text(encoding="utf-8-sig", errors="ignore")
                            validate_python_structure(new_source, is_script=is_script)
            except PythonStructureError as e:
                raise ApplyError(str(e))

            shutil.copytree(
                tmp_path / "repo",
                self.workspace,
                dirs_exist_ok=True,
            )

        return self._changed_files(diff)

    def _changed_files(self, diff: str) -> list[str]:
        return [
            line[6:]
            for line in diff.splitlines()
            if line.startswith("+++ b/")
        ]

    def _files_in_diff(self, diff: str) -> list[str]:
        files = []
        for line in diff.splitlines():
            if line.startswith("+++ b/"):
                files.append(line[6:])
            elif line.startswith("--- a/"):
                files.append(line[6:])
        # keep unique order
        seen = set()
        ordered = []
        for f in files:
            if f not in seen:
                seen.add(f)
                ordered.append(f)
        return ordered

    def _apply_unified_diff_python(self, repo: Path, diff_text: str) -> None:
        lines = diff_text.splitlines()
        # locate file headers
        old_file = None
        new_file = None
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith('--- '):
                old_file = line.split('\t')[0][4:].strip()
            if line.startswith('+++ '):
                new_file = line.split('\t')[0][4:].strip()
                break
            i += 1
        if not new_file:
            raise RuntimeError('No file headers found in diff')
        def strip_prefix(p: str) -> str:
            return p[2:] if p.startswith('a/') or p.startswith('b/') else p
        target_rel = strip_prefix(new_file)
        target_path = (repo / target_rel).resolve()

        orig = ''
        if target_path.exists():
            orig = target_path.read_text(encoding='utf-8-sig', errors='ignore')
        orig_lines = orig.replace('\r\n', '\n').replace('\r', '\n').split('\n')

        patched = orig_lines[:]
        while i < len(lines) and not lines[i].startswith('@@'):
            i += 1
        offset = 0
        while i < len(lines) and lines[i].startswith('@@'):
            header = lines[i]
            i += 1
            try:
                h = header.split('@@')[1].strip()
                left, right = h.split(' ')
                old_start = int(left.split(',')[0][1:])
                old_len = int(left.split(',')[1]) if ',' in left else 1
            except Exception:
                raise RuntimeError('Invalid hunk header: ' + header)
            hunk_ops = []
            while i < len(lines) and not lines[i].startswith('@@') and not lines[i].startswith('diff --git'):
                l = lines[i]
                if l.startswith(' ') or l.startswith('-') or l.startswith('+'):
                    hunk_ops.append((l[0], l[1:]))
                i += 1

            idx = max(0, old_start - 1 + offset)
            left_cursor = idx
            new_chunk: list[str] = []
            for op, text in hunk_ops:
                if op == ' ':
                    if left_cursor < len(patched):
                        new_chunk.append(patched[left_cursor])
                        left_cursor += 1
                    else:
                        new_chunk.append(text)
                elif op == '-':
                    if left_cursor < len(patched):
                        left_cursor += 1
                elif op == '+':
                    new_chunk.append(text)

            patched = patched[:idx] + new_chunk + patched[left_cursor:]
            offset = len(patched) - len(orig_lines)
            orig_lines = patched[:]

        result = '\n'.join(patched)
        if not result.endswith('\n'):
            result += '\n'
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(result, encoding='utf-8')

    @staticmethod
    def compute_hash(workspace: Path) -> str:
        hasher = hashlib.sha256()
        parts = []
        for p in sorted([p for p in Path(workspace).rglob("*") if p.is_file()]):
            try:
                parts.append(p.read_text(encoding="utf-8", errors="ignore"))
            except Exception:
                parts.append("")
        hasher.update("".join(parts).encode())
        return hasher.hexdigest()

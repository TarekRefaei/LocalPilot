from __future__ import annotations

import fnmatch
import math
import os
from dataclasses import dataclass
from pathlib import Path

from pathspec import PathSpec


@dataclass
class DiscoveryResult:
    total_files: int
    files_by_type: dict[str, int]
    project_type: str
    root_files: list[str]
    estimated_duration_seconds: int
    total_size_mb: float
    files: list[Path]


class DiscoveryExecutor:
    LANGUAGE_EXTENSIONS = {
        "typescript": [".ts", ".tsx"],
        "javascript": [".js", ".jsx", ".mjs", ".cjs"],
        "python": [".py"],
        "markdown": [".md", ".markdown", ".rst"],
        "json": [".json"],
        "yaml": [".yml", ".yaml"],
    }

    PROJECT_MARKERS = {
        "react": ["package.json", "src/App.tsx"],
        "react-native": ["package.json", "app.json"],
        "vue": ["package.json", "vue.config.js"],
        "angular": ["package.json", "angular.json"],
        "python": ["setup.py", "pyproject.toml", "requirements.txt"],
        "fastapi": ["main.py", "app/main.py"],
        "generic": [],
    }

    DEFAULT_EXCLUDES = [
        "node_modules/",
        ".git/",
        "dist/",
        "build/",
        ".next/",
        "__pycache__/",
        "venv/",
        ".venv/",
        "env/",
        "target/",
        "out/",
        "coverage/",
        ".pytest_cache/",
    ]

    BINARY_EXTS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".ico",
        ".svg",
        ".pdf",
        ".zip",
        ".tar",
        ".gz",
        ".rar",
        ".exe",
        ".dll",
        ".so",
        ".dylib",
        ".woff",
        ".woff2",
        ".ttf",
        ".eot",
        ".mp4",
        ".mp3",
        ".wav",
        ".avi",
    }

    def __init__(self, exclude_patterns: list[str] | None = None) -> None:
        self.exclude_patterns = exclude_patterns or self.DEFAULT_EXCLUDES

    async def execute(self, workspace_path: str) -> DiscoveryResult:
        ws = Path(workspace_path)
        if not ws.exists():
            raise ValueError(f"Workspace path does not exist: {workspace_path}")

        spec = self._build_pathspec(ws)
        files = self._scan_files(ws, spec)
        files_by_type = self._categorize_files(files)
        project_type = self._detect_project_type(ws)
        root_files = self._get_root_files(ws)

        total_size_mb = sum(f.stat().st_size for f in files) / (1024 * 1024)
        eta = self._estimate_duration(len(files), total_size_mb)

        return DiscoveryResult(
            total_files=len(files),
            files_by_type=files_by_type,
            project_type=project_type,
            root_files=root_files,
            estimated_duration_seconds=eta,
            total_size_mb=round(total_size_mb, 2),
            files=files,
        )

    def _build_pathspec(self, workspace: Path) -> PathSpec:
        patterns: list[str] = []
        gitignore = workspace / ".gitignore"
        if gitignore.exists():
            patterns.extend(gitignore.read_text(encoding="utf-8").splitlines())
        # ensure defaults included
        patterns.extend(self.exclude_patterns)
        # Normalize trailing slashes
        normalized = []
        for p in patterns:
            if p and not p.startswith("#"):
                normalized.append(p.strip())
        return PathSpec.from_lines("gitwildmatch", normalized)

    def _is_excluded(self, spec: PathSpec, workspace: Path, path: Path) -> bool:
        try:
            rel = path.resolve().relative_to(workspace)
        except Exception:
            rel = path
        rel_str = str(rel).replace(os.sep, "/")
        # Exclude hidden entries
        if any(part.startswith(".") for part in rel.parts if part):
            return True
        return spec.match_file(rel_str)

    def _is_binary(self, path: Path) -> bool:
        if path.suffix.lower() in self.BINARY_EXTS:
            return True
        try:
            with open(path, "rb") as f:
                chunk = f.read(1024)
                return b"\x00" in chunk
        except Exception:
            return True

    def _scan_files(self, workspace: Path, spec: PathSpec) -> list[Path]:
        out: list[Path] = []
        for root, dirs, files in os.walk(workspace):
            root_path = Path(root)
            # Filter directories in-place
            dirs[:] = [d for d in dirs if not self._is_excluded(spec, workspace, root_path / d)]
            for name in files:
                p = root_path / name
                if self._is_excluded(spec, workspace, p):
                    continue
                if self._is_binary(p):
                    continue
                out.append(p)
        return out

    def _categorize_files(self, files: list[Path]) -> dict[str, int]:
        counts: dict[str, int] = {}
        for f in files:
            lang = "other"
            ext = f.suffix.lower()
            for k, exts in self.LANGUAGE_EXTENSIONS.items():
                if ext in exts:
                    lang = k
                    break
            counts[lang] = counts.get(lang, 0) + 1
        return counts

    def _detect_project_type(self, workspace: Path) -> str:
        names = {p.name for p in workspace.iterdir() if p.is_file()}
        for t, markers in self.PROJECT_MARKERS.items():
            if all(any(fnmatch.fnmatch(n, m) for n in names) for m in markers):
                return t
        return "generic"

    def _get_root_files(self, workspace: Path) -> list[str]:
        important = [
            "README.md",
            "package.json",
            "pyproject.toml",
            "requirements.txt",
            "setup.py",
            "Cargo.toml",
            "go.mod",
            "build.gradle",
            "pom.xml",
            "pubspec.yaml",
            "Package.swift",
        ]
        found: list[str] = []
        for p in workspace.iterdir():
            if p.name in important:
                found.append(p.name)
        return found

    def _estimate_duration(self, file_count: int, size_mb: float) -> int:
        base = file_count * 0.3
        size = size_mb * 0.1
        emb = file_count * 0.2
        total = (base + size + emb) * 1.2
        return int(math.ceil(total))

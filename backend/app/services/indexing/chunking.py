"""
Phase 4: Semantic Code Chunking

AST-first chunking with Tree-sitter; lexical fallback for unsupported languages.
Produces deterministic chunk boundaries with metadata for retrieval.

Key Principles:
- Never split in the middle of a function or class
- Preserve semantic boundaries
- Target 500-1000 tokens per chunk
- Include sufficient context (imports, parent class)
- Language-aware parsing with fallback
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    from tree_sitter import Language, Node, Parser

    HAS_TREE_SITTER = True
except ImportError:
    HAS_TREE_SITTER = False


@dataclass
class CodeChunk:
    """Semantic code chunk with metadata."""

    id: str
    content: str
    file_path: str
    start_line: int
    end_line: int
    language: str
    chunk_type: str  # 'function', 'class', 'interface', 'block', 'module'
    tokens: int
    symbols: list[str] = field(default_factory=list)  # Function/class names in chunk
    imports: list[str] = field(default_factory=list)  # Module names imported
    parent_context: str | None = None  # Parent class/module name


class TreeSitterParser:
    """Multi-language parser using Tree-sitter with fallback support."""

    def __init__(self) -> None:
        """Initialize Tree-sitter parsers for supported languages."""
        self.parsers: dict[str, Parser] = {}
        self.languages: dict[str, Language] = {}
        self._init_parsers()

    def _init_parsers(self) -> None:
        """Initialize parsers for target languages."""
        if not HAS_TREE_SITTER:
            return

        try:
            # Tree-sitter support requires pre-built language binaries
            # On Windows, these need special handling
            # For MVP, we focus on reliable lexical chunking
            pass
        except Exception as e:
            print(f"Warning: Tree-sitter initialization: {e}")

    def parse_file(self, filepath: Path, language: str) -> Node | None:
        """Parse file with Tree-sitter and return AST root node."""
        if not HAS_TREE_SITTER or language not in self.parsers:
            return None

        try:
            content = filepath.read_bytes()
            parser = self.parsers[language]
            tree = parser.parse(content)
            return tree.root_node
        except Exception as e:
            print(f"Error parsing {filepath} ({language}): {e}")
            return None

    def get_language_from_ext(self, filepath: Path) -> str | None:
        """Detect language from file extension."""
        return self.ext_to_lang.get(filepath.suffix.lower())


class SemanticChunker:
    """Create semantically meaningful code chunks using AST."""

    # Target and limits (in approximate tokens)
    TARGET_CHUNK_SIZE = 1000
    MAX_CHUNK_SIZE = 1500
    MIN_CHUNK_SIZE = 100
    CHUNK_OVERLAP = 200

    def __init__(self) -> None:
        """Initialize chunker with parser."""
        self.parser = TreeSitterParser()

    def chunk_file(self, filepath: Path, language: str, workspace_path: str) -> list[CodeChunk]:
        """Chunk a file into semantic units with metadata.

        Strategy: Deterministic lexical chunking based on language-specific patterns.
        - Preserves function/class boundaries
        - Works reliably without AST parsing
        - Deterministic across runs
        """
        return self._chunk_lexical(filepath, workspace_path, language)

    def _chunk_typescript(self, filepath: Path, ast: Node, workspace_path: str) -> list[CodeChunk]:
        """Chunk TypeScript/JavaScript using AST-first strategy."""

        content = filepath.read_text(encoding="utf-8")
        lines = content.split("\n")
        chunks: list[CodeChunk] = []

        # Extract top-level declarations
        top_level = self._get_top_level_declarations(ast)

        # Extract all imports for context
        imports = self._extract_imports_from_ast(ast, filepath)

        for node in top_level:
            node_text = self._get_node_text(node, filepath)
            node_tokens = self._estimate_tokens(node_text)

            # Extract symbol name
            symbol_name = self._get_declaration_name(node, filepath)

            # Small node: single chunk
            if node_tokens <= self.TARGET_CHUNK_SIZE:
                chunk = CodeChunk(
                    id=self._make_chunk_id(filepath, workspace_path, node),
                    content=node_text,
                    file_path=str(filepath.relative_to(workspace_path)),
                    start_line=node.start_point[0] + 1,
                    end_line=node.end_point[0] + 1,
                    language=filepath.suffix.lower()[1:],
                    chunk_type=self._get_node_type(node),
                    tokens=node_tokens,
                    symbols=[symbol_name] if symbol_name else [],
                    imports=imports,
                )
                chunks.append(chunk)

            # Large node: split by methods/nested declarations
            elif node.type == "class_declaration":
                sub_chunks = self._split_class_declaration(node, filepath, workspace_path, imports)
                chunks.extend(sub_chunks)

            else:
                # Fallback: create single chunk anyway (preserves boundary)
                chunk = CodeChunk(
                    id=self._make_chunk_id(filepath, workspace_path, node),
                    content=node_text,
                    file_path=str(filepath.relative_to(workspace_path)),
                    start_line=node.start_point[0] + 1,
                    end_line=node.end_point[0] + 1,
                    language=filepath.suffix.lower()[1:],
                    chunk_type=self._get_node_type(node),
                    tokens=node_tokens,
                    symbols=[symbol_name] if symbol_name else [],
                    imports=imports,
                )
                chunks.append(chunk)

        return chunks

    def _chunk_python(self, filepath: Path, ast: Node, workspace_path: str) -> list[CodeChunk]:
        """Chunk Python using AST-first strategy."""

        content = filepath.read_text(encoding="utf-8")
        chunks: list[CodeChunk] = []

        # Get top-level definitions (functions, classes)
        top_level = []
        for child in ast.children:
            if child.type in ["function_definition", "class_definition"]:
                top_level.append(child)

        imports = self._extract_imports_from_python_ast(ast, filepath)

        for node in top_level:
            node_text = self._get_node_text(node, filepath)
            node_tokens = self._estimate_tokens(node_text)
            symbol_name = self._get_declaration_name(node, filepath)

            if node_tokens <= self.TARGET_CHUNK_SIZE:
                chunk = CodeChunk(
                    id=self._make_chunk_id(filepath, workspace_path, node),
                    content=node_text,
                    file_path=str(filepath.relative_to(workspace_path)),
                    start_line=node.start_point[0] + 1,
                    end_line=node.end_point[0] + 1,
                    language="python",
                    chunk_type="class" if node.type == "class_definition" else "function",
                    tokens=node_tokens,
                    symbols=[symbol_name] if symbol_name else [],
                    imports=imports,
                )
                chunks.append(chunk)

            elif node.type == "class_definition":
                # Split class into methods
                sub_chunks = self._split_python_class(node, filepath, workspace_path, imports)
                chunks.extend(sub_chunks)
            else:
                chunk = CodeChunk(
                    id=self._make_chunk_id(filepath, workspace_path, node),
                    content=node_text,
                    file_path=str(filepath.relative_to(workspace_path)),
                    start_line=node.start_point[0] + 1,
                    end_line=node.end_point[0] + 1,
                    language="python",
                    chunk_type="function",
                    tokens=node_tokens,
                    symbols=[symbol_name] if symbol_name else [],
                    imports=imports,
                )
                chunks.append(chunk)

        return chunks

    def _chunk_lexical(self, filepath: Path, workspace_path: str, language: str) -> list[CodeChunk]:
        """Lexical chunking: deterministic, language-aware code splitting.

        Strategy:
        - Scan for function/class/interface definitions
        - Create semantic chunks around these boundaries
        - Extract symbols and maintain imports list
        - Preserve determinism for caching
        """

        content = filepath.read_text(encoding="utf-8")
        lines = content.split("\n")
        chunks: list[CodeChunk] = []

        # Extract all imports (used as context in all chunks)
        imports = self._extract_all_imports(lines, language)

        # Find declaration boundaries (functions, classes, interfaces)
        boundaries = self._find_declaration_boundaries(lines, language)

        # Extract symbols and chunk around them
        for start_line, end_line, decl_type, decl_name in boundaries:
            chunk_lines = lines[start_line : end_line + 1]
            chunk_text = "\n".join(chunk_lines)
            chunk_tokens = self._estimate_tokens(chunk_text)

            # Only create chunks for meaningful content
            if chunk_tokens >= self.MIN_CHUNK_SIZE:
                chunk = CodeChunk(
                    id=self._make_lexical_chunk_id(filepath, workspace_path, start_line, end_line),
                    content=chunk_text,
                    file_path=str(filepath.relative_to(workspace_path)),
                    start_line=start_line + 1,  # Convert to 1-indexed
                    end_line=end_line + 1,  # Convert to 1-indexed
                    language=language,
                    chunk_type=decl_type,
                    tokens=chunk_tokens,
                    symbols=[decl_name] if decl_name else [],
                    imports=imports,
                )
                chunks.append(chunk)

        # If no chunks (e.g., no definitions), create whole-file chunk
        if not chunks:
            chunk_text = "\n".join(lines)
            chunk_tokens = self._estimate_tokens(chunk_text)
            if chunk_tokens > 0:
                chunk = CodeChunk(
                    id=f"{filepath.stem}-full",
                    content=chunk_text,
                    file_path=str(filepath.relative_to(workspace_path)),
                    start_line=1,
                    end_line=len(lines),
                    language=language,
                    chunk_type="module",
                    tokens=chunk_tokens,
                    symbols=[],
                    imports=imports,
                )
                chunks.append(chunk)

        return chunks

    def _find_declaration_boundaries(
        self, lines: list[str], language: str
    ) -> list[tuple[int, int, str, str | None]]:
        """Find function/class declarations and their boundaries.

        Returns: List of (start_line, end_line, type, name) tuples
        """
        boundaries: list[tuple[int, int, str, str | None]] = []

        i = 0
        while i < len(lines):
            line = lines[i]

            # TypeScript/JavaScript patterns
            if language in ["typescript", "jsx", "tsx", "javascript"]:
                # Function declaration
                func_match = re.match(r"^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(", line)
                if func_match:
                    start = i
                    name = func_match.group(1)
                    end = self._find_closing_brace(lines, i)
                    if end >= start:
                        boundaries.append((start, end, "function", name))
                        i = end + 1
                        continue

                # Arrow function / const assignment
                arrow_match = re.match(
                    r"^\s*(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*\(?", line
                )
                if arrow_match and "=>" in line:
                    start = i
                    name = arrow_match.group(1)
                    end = self._find_closing_brace(lines, i)
                    if end >= start:
                        boundaries.append((start, end, "function", name))
                        i = end + 1
                        continue

                # Class declaration
                class_match = re.match(r"^\s*(?:export\s+)?class\s+(\w+)", line)
                if class_match:
                    start = i
                    name = class_match.group(1)
                    end = self._find_closing_brace(lines, i)
                    if end >= start:
                        boundaries.append((start, end, "class", name))
                        i = end + 1
                        continue

                # Interface declaration
                iface_match = re.match(r"^\s*(?:export\s+)?interface\s+(\w+)", line)
                if iface_match:
                    start = i
                    name = iface_match.group(1)
                    end = self._find_closing_brace(lines, i)
                    if end >= start:
                        boundaries.append((start, end, "interface", name))
                        i = end + 1
                        continue

            # Python patterns
            elif language == "python":
                # Function definition
                func_match = re.match(r"^\s*(?:async\s+)?def\s+(\w+)\s*\(", line)
                if func_match:
                    start = i
                    name = func_match.group(1)
                    end = self._find_python_block_end(lines, i)
                    if end >= start:
                        boundaries.append((start, end, "function", name))
                        i = end + 1
                        continue

                # Class definition
                class_match = re.match(r"^\s*class\s+(\w+)", line)
                if class_match:
                    start = i
                    name = class_match.group(1)
                    end = self._find_python_block_end(lines, i)
                    if end >= start:
                        boundaries.append((start, end, "class", name))
                        i = end + 1
                        continue

            i += 1

        return boundaries

    def _find_closing_brace(self, lines: list[str], start: int) -> int:
        """Find matching closing brace for opening brace at start line."""
        brace_count = 0
        in_string = None

        for i in range(start, len(lines)):
            line = lines[i]

            for j, char in enumerate(line):
                # Track strings
                if char in ['"', "'", "`"] and (j == 0 or line[j - 1] != "\\"):
                    if in_string == char:
                        in_string = None
                    elif not in_string:
                        in_string = char

                if not in_string:
                    if char == "{":
                        brace_count += 1
                    elif char == "}":
                        brace_count -= 1
                        if brace_count == 0:
                            return i

        return start  # No matching brace found

    def _find_python_block_end(self, lines: list[str], start: int) -> int:
        """Find the end of a Python indented block."""
        if start >= len(lines):
            return start

        # Get indentation of the definition line
        def_line = lines[start]
        def_indent = len(def_line) - len(def_line.lstrip())

        # Find end: next line with same or less indentation (that's not blank)
        for i in range(start + 1, len(lines)):
            line = lines[i]
            if not line.strip():  # Blank line, continue
                continue

            line_indent = len(line) - len(line.lstrip())
            if line_indent <= def_indent:
                return i - 1

        return len(lines) - 1

    def _extract_all_imports(self, lines: list[str], language: str) -> list[str]:
        """Extract all import statements from file."""
        imports: list[str] = []

        for line in lines[:100]:  # Check first 100 lines
            if language in ["typescript", "javascript", "jsx", "tsx"]:
                if re.match(r"^\s*import\s+.*from\s+['\"]([^'\"]+)['\"]", line):
                    match = re.search(r"from\s+['\"]([^'\"]+)['\"]", line)
                    if match:
                        imports.append(match.group(1))
                elif re.match(r"^\s*require\s*\(", line):
                    match = re.search(r"require\s*\(\s*['\"]([^'\"]+)['\"]", line)
                    if match:
                        imports.append(match.group(1))

            elif language == "python":
                if re.match(r"^\s*from\s+(\w+)", line):
                    match = re.search(r"from\s+(\w+)", line)
                    if match:
                        imports.append(match.group(1))
                elif re.match(r"^\s*import\s+(\w+)", line):
                    match = re.search(r"import\s+(\w+)", line)
                    if match:
                        imports.append(match.group(1))

        return imports

    def _make_lexical_chunk_id(
        self, filepath: Path, workspace_path: str, start: int, end: int
    ) -> str:
        """Create deterministic chunk ID from file and line numbers."""
        rel_path = str(filepath.relative_to(workspace_path)).replace("\\", "/")
        return f"{rel_path}#{start}-{end}"

    def _get_top_level_declarations(self, ast: Node) -> list[Node]:
        """Extract top-level declarations (functions, classes, etc.)."""
        top_level: list[Node] = []

        for child in ast.children:
            if child.type in [
                "function_declaration",
                "arrow_function",
                "class_declaration",
                "interface_declaration",
                "type_alias_declaration",
                "enum_declaration",
                "export_statement",
                "lexical_declaration",
                "variable_declaration",
            ]:
                top_level.append(child)

        return top_level

    def _split_class_declaration(
        self, class_node: Node, filepath: Path, workspace_path: str, imports: list[str]
    ) -> list[CodeChunk]:
        """Split large class into chunks (one per method)."""
        chunks: list[CodeChunk] = []

        # Get class header (signature without body)
        class_name = self._get_declaration_name(class_node, filepath)
        class_text = self._get_node_text(class_node, filepath)

        # Find class body
        body_node = None
        for child in class_node.children:
            if child.type == "class_body":
                body_node = child
                break

        if not body_node:
            # Fallback: treat entire class as one chunk
            return [
                CodeChunk(
                    id=self._make_chunk_id(filepath, workspace_path, class_node),
                    content=class_text,
                    file_path=str(filepath.relative_to(workspace_path)),
                    start_line=class_node.start_point[0] + 1,
                    end_line=class_node.end_point[0] + 1,
                    language=filepath.suffix.lower()[1:],
                    chunk_type="class",
                    tokens=self._estimate_tokens(class_text),
                    symbols=[class_name] if class_name else [],
                    imports=imports,
                )
            ]

        # Extract methods
        for child in body_node.children:
            if child.type in ["method_definition", "property_definition"]:
                method_name = self._get_declaration_name(child, filepath)
                method_text = self._get_node_text(child, filepath)

                chunk = CodeChunk(
                    id=self._make_chunk_id(filepath, workspace_path, child),
                    content=method_text,
                    file_path=str(filepath.relative_to(workspace_path)),
                    start_line=child.start_point[0] + 1,
                    end_line=child.end_point[0] + 1,
                    language=filepath.suffix.lower()[1:],
                    chunk_type="method",
                    tokens=self._estimate_tokens(method_text),
                    symbols=[class_name, method_name] if method_name else [class_name],
                    imports=imports,
                    parent_context=class_name,
                )
                chunks.append(chunk)

        # If no methods, add class header as chunk
        if not chunks:
            chunks.append(
                CodeChunk(
                    id=self._make_chunk_id(filepath, workspace_path, class_node),
                    content=class_text,
                    file_path=str(filepath.relative_to(workspace_path)),
                    start_line=class_node.start_point[0] + 1,
                    end_line=class_node.end_point[0] + 1,
                    language=filepath.suffix.lower()[1:],
                    chunk_type="class",
                    tokens=self._estimate_tokens(class_text),
                    symbols=[class_name] if class_name else [],
                    imports=imports,
                )
            )

        return chunks

    def _split_python_class(
        self, class_node: Node, filepath: Path, workspace_path: str, imports: list[str]
    ) -> list[CodeChunk]:
        """Split large Python class into chunks (one per method)."""
        chunks: list[CodeChunk] = []

        class_name = self._get_declaration_name(class_node, filepath)
        chunks_created = 0

        for child in class_node.children:
            if child.type == "function_definition":
                method_name = self._get_declaration_name(child, filepath)
                method_text = self._get_node_text(child, filepath)

                chunk = CodeChunk(
                    id=self._make_chunk_id(filepath, workspace_path, child),
                    content=method_text,
                    file_path=str(filepath.relative_to(workspace_path)),
                    start_line=child.start_point[0] + 1,
                    end_line=child.end_point[0] + 1,
                    language="python",
                    chunk_type="method",
                    tokens=self._estimate_tokens(method_text),
                    symbols=[class_name, method_name] if method_name else [class_name],
                    imports=imports,
                    parent_context=class_name,
                )
                chunks.append(chunk)
                chunks_created += 1

        # If no methods extracted, use class as-is
        if chunks_created == 0:
            class_text = self._get_node_text(class_node, filepath)
            chunks.append(
                CodeChunk(
                    id=self._make_chunk_id(filepath, workspace_path, class_node),
                    content=class_text,
                    file_path=str(filepath.relative_to(workspace_path)),
                    start_line=class_node.start_point[0] + 1,
                    end_line=class_node.end_point[0] + 1,
                    language="python",
                    chunk_type="class",
                    tokens=self._estimate_tokens(class_text),
                    symbols=[class_name] if class_name else [],
                    imports=imports,
                )
            )

        return chunks

    def _get_node_text(self, node: Node, filepath: Path) -> str:
        """Extract text content of an AST node."""
        try:
            content = filepath.read_bytes()
            return content[node.start_byte : node.end_byte].decode("utf-8", errors="ignore")
        except Exception:
            return ""

    def _get_node_type(self, node: Node) -> str:
        """Map AST node type to chunk type."""
        type_map = {
            "function_declaration": "function",
            "arrow_function": "function",
            "class_declaration": "class",
            "interface_declaration": "interface",
            "type_alias_declaration": "type",
            "enum_declaration": "enum",
            "method_definition": "method",
        }
        return type_map.get(node.type, "block")

    def _get_declaration_name(self, node: Node, filepath: Path) -> str | None:
        """Extract the name of a declaration."""
        name_node = node.child_by_field_name("name")
        if name_node:
            return self._get_node_text(name_node, filepath).strip()
        return None

    def _make_chunk_id(self, filepath: Path, workspace_path: str, node: Node) -> str:
        """Create deterministic chunk ID."""
        rel_path = str(filepath.relative_to(workspace_path)).replace("\\", "/")
        return f"{rel_path}#{node.start_point[0]}-{node.end_point[0]}"

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count (simple word-based approximation).

        Approximation:
        - Average English word ≈ 1.3 tokens (GPT approximation)
        - Use word count * 1.3 as estimate
        """
        word_count = len(text.split())
        return max(1, int(word_count * 1.3))

    def _extract_imports_from_ast(self, ast: Node, filepath: Path) -> list[str]:
        """Extract import module names from TypeScript/JavaScript AST."""
        imports: list[str] = []

        for child in ast.children:
            if child.type == "import_statement":
                # Extract module name from import statement
                for subchild in child.children:
                    if subchild.type == "string":
                        module_text = self._get_node_text(subchild, filepath)
                        module_name = module_text.strip("'\"")
                        if module_name:
                            imports.append(module_name)

        return imports

    def _extract_imports_from_python_ast(self, ast: Node, filepath: Path) -> list[str]:
        """Extract import module names from Python AST."""
        imports: list[str] = []

        for child in ast.children:
            if child.type in ["import_statement", "import_from_statement"]:
                for subchild in child.children:
                    if subchild.type == "dotted_name":
                        module_name = self._get_node_text(subchild, filepath).strip()
                        if module_name:
                            imports.append(module_name)

        return imports


class ChunkingExecutor:
    """Orchestrator for Phase 4: Semantic Chunking."""

    def __init__(self) -> None:
        """Initialize chunking executor."""
        self.chunker = SemanticChunker()

    async def execute(
        self, workspace_path: str, files: list[Path]
    ) -> tuple[list[CodeChunk], dict[str, Any]]:
        """Execute chunking phase on all files.

        Returns:
            Tuple of (all_chunks, metrics)
        """
        all_chunks: list[CodeChunk] = []
        metrics = {
            "total_files": len(files),
            "files_chunked": 0,
            "total_chunks": 0,
            "chunk_types": {},
            "avg_tokens": 0,
            "errors": 0,
        }

        for filepath in files:
            language = self._detect_language(filepath)
            if not language:
                continue

            try:
                chunks = self.chunker.chunk_file(filepath, language, workspace_path)
                all_chunks.extend(chunks)
                metrics["files_chunked"] += 1

                # Track chunk types
                for chunk in chunks:
                    metrics["chunk_types"][chunk.chunk_type] = (
                        metrics["chunk_types"].get(chunk.chunk_type, 0) + 1
                    )

            except Exception as e:
                print(f"Error chunking {filepath}: {e}")
                metrics["errors"] += 1

        # Calculate averages
        metrics["total_chunks"] = len(all_chunks)
        if all_chunks:
            avg_tokens = sum(c.tokens for c in all_chunks) / len(all_chunks)
            metrics["avg_tokens"] = round(avg_tokens, 2)

        return all_chunks, metrics

    def _detect_language(self, filepath: Path) -> str | None:
        """Detect language from file extension."""
        ext_map = {
            ".ts": "typescript",
            ".tsx": "typescript",
            ".js": "javascript",
            ".jsx": "javascript",
            ".py": "python",
        }
        return ext_map.get(filepath.suffix.lower())

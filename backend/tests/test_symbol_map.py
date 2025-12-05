from app.services.indexing.chunking import CodeChunk
from app.services.indexing.symbol_map import (
    ImportMap,
    Symbol,
    SymbolImportMapBuilder,
    SymbolMap,
)


def make_chunk(
    id: str,
    file_path: str,
    start: int,
    end: int,
    language: str,
    chunk_type: str,
    symbols: list[str],
    imports: list[str] | None = None,
) -> CodeChunk:
    return CodeChunk(
        id=id,
        content="",  # not used by SymbolMap/ImportMap
        file_path=file_path,
        start_line=start,
        end_line=end,
        language=language,
        chunk_type=chunk_type,
        tokens=150,  # arbitrary > MIN_CHUNK_SIZE threshold in chunker, not used here
        symbols=symbols,
        imports=imports or [],
        parent_context=None,
    )


def test_symbol_map_add_get_and_chunks():
    sm = SymbolMap()

    chunk_a = make_chunk(
        id="a#1-10",
        file_path="src/a.py",
        start=1,
        end=10,
        language="python",
        chunk_type="function",
        symbols=["foo"],
    )
    chunk_b = make_chunk(
        id="b#1-20",
        file_path="src/b.py",
        start=1,
        end=20,
        language="python",
        chunk_type="class",
        symbols=["Bar"],
    )
    chunk_c = make_chunk(
        id="a#11-30",
        file_path="src/a.py",
        start=11,
        end=30,
        language="python",
        chunk_type="function",
        symbols=["foo"],
    )

    # Build via add_symbol to exercise paths
    for ch in [chunk_a, chunk_b, chunk_c]:
        for sym in ch.symbols:
            sm.add_symbol(
                Symbol(
                    name=sym,
                    kind=ch.chunk_type,
                    file_path=ch.file_path,
                    start_line=ch.start_line,
                    end_line=ch.end_line,
                    chunk_id=ch.id,
                    parent=ch.parent_context,
                    is_exported=False,
                )
            )

    # get_symbol scoped and unscoped
    s1 = sm.get_symbol("foo", file_path="src/a.py")
    assert s1 is not None and s1.name == "foo" and s1.file_path == "src/a.py"
    s2 = sm.get_symbol("Bar")
    assert s2 is not None and s2.name == "Bar"

    # get_symbols_in_file
    file_syms = sm.get_symbols_in_file("src/a.py")
    assert len(file_syms) == 2

    # chunk ids for symbol aggregation
    chunk_ids = sm.get_chunk_ids_for_symbol("foo")
    assert chunk_ids == {"a#1-10", "a#11-30"}

    # serialization
    data = sm.to_dict()
    # Duplicate symbol name in same file_path collapses to one entry in global index
    assert data["total_symbols"] == 2
    assert "src/a.py" in data["symbols"]


def test_import_map_build_and_queries():
    im = ImportMap()

    # Add via build_from_chunks using synthetic chunks with imports
    chunks = [
        make_chunk(
            "a#1-10",
            "src/a.ts",
            1,
            10,
            "typescript",
            "function",
            ["f"],
            ["lodash", "./b"],
        ),
        make_chunk(
            "b#1-10", "src/b.ts", 1, 10, "typescript", "function", ["g"], ["lodash"]
        ),
    ]
    im.build_from_chunks(chunks)

    # get_imports_in_file
    a_imports = im.get_imports_in_file("src/a.ts")
    assert any(link.to_module == "lodash" for link in a_imports)

    # get_files_importing
    files = im.get_files_importing("lodash")
    assert set(files) == {"src/a.ts", "src/b.ts"}


def test_builder_and_determinism():
    chunks1 = [
        make_chunk("p#1-5", "pkg/x.py", 1, 5, "python", "function", ["x"], []),
        make_chunk("p#6-10", "pkg/y.py", 6, 10, "python", "class", ["Y"], []),
    ]
    chunks2 = [
        make_chunk("p#1-5", "pkg/x.py", 1, 5, "python", "function", ["x"], []),
        make_chunk("p#6-10", "pkg/y.py", 6, 10, "python", "class", ["Y"], []),
    ]

    sm, im = SymbolImportMapBuilder.build(chunks1)
    assert sm.get_symbol("x", file_path="pkg/x.py") is not None
    assert len(im.get_imports_in_file("pkg/x.py")) == 0

    # Determinism true for identical chunks
    assert SymbolImportMapBuilder.validate_determinism(chunks1, chunks2) is True

    # Determinism false for changed chunk lines
    changed = [
        make_chunk("p#1-6", "pkg/x.py", 1, 6, "python", "function", ["x"], [])
    ] + chunks1[1:]
    assert SymbolImportMapBuilder.validate_determinism(changed, chunks1) is False

from app.services.act.diff_engine import unified_diff, summarize_diff


def test_unified_diff_and_summary_simple():
    before = "hello\nworld\n"
    after = "hello\nWORLD\nnew\n"
    d = unified_diff("README.md", before, after)
    assert "--- a/README.md" in d and "+++ b/README.md" in d
    s = summarize_diff("README.md", d)
    # WORLD line starts with '+'; one deletion for 'world'
    assert s.additions >= 1
    assert s.deletions >= 1

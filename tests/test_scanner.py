from password_tool.scanner import scan_file
from password_tool.context import tokenize_context


def test_scan_file(tmp_path):
    sample = tmp_path / "pw.txt"
    sample.write_text("password\nUniqueSTR0ng!\npassword\nabcde\n", encoding="utf-8")
    ctx = tokenize_context("Alice 1999 alice@example.com")
    records = scan_file(str(sample), ctx, redact=True)
    assert len(records) == 4
    # Ensure duplicate flagged
    dupes = [r for r in records if r['duplicate']]
    assert dupes, "Expected duplicate detection"
    # Ensure suggestions for weak ones
    weak_or_mod = [r for r in records if r['strength'] in {"Weak", "Moderate"}]
    assert any(r['suggestion'] for r in weak_or_mod)

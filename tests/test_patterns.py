from password_tool.patterns import find_patterns

def test_repeated_sequence():
    assert any("Repeated" in p for p in find_patterns("aaaa"))

def test_keyboard_walk():
    pats = find_patterns("xxqwerxx")
    assert any("Keyboard" in p for p in pats)

def test_common_term_leet():
    pats = find_patterns("P@ssword123")
    assert any("Common term" in p for p in pats)

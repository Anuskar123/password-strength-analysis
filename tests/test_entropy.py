from password_tool.entropy import calculate_entropy, classify_entropy


def test_entropy_basic():
    assert calculate_entropy("") == 0
    assert calculate_entropy("aaaa") > 0


def test_classification():
    r = classify_entropy(calculate_entropy("Short1!"), "Short1!")
    assert r.score >= 0
    assert r.strength in {"Weak", "Moderate", "Strong", "Robust"}

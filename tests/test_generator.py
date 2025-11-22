from password_tool.generator import generate_password, DEFAULT_POLICY, get_policy


def test_generate_password_length():
    pw = generate_password(16)
    assert len(pw) >= 16


def test_generate_password_classes():
    pw = generate_password(20)
    # Ensure each required class is represented
    classes = {
        'lower': any(c.islower() for c in pw),
        'upper': any(c.isupper() for c in pw),
        'digit': any(c.isdigit() for c in pw),
        'special': any(c in '!@#$%^&*' for c in pw),
    }
    for req in DEFAULT_POLICY['require_classes']:
        assert classes[req]


def test_policy_exposed():
    p = get_policy()
    assert p['min_length'] == DEFAULT_POLICY['min_length']
    assert set(p['required_classes']) == set(DEFAULT_POLICY['require_classes'])

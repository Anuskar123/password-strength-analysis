import secrets
import string
from typing import Iterable

SPECIALS = "!@#$%^&*"

DEFAULT_POLICY = {
    "min_length": 14,
    "require_classes": ["lower", "upper", "digit", "special"],
}

CLASS_MAP = {
    "lower": string.ascii_lowercase,
    "upper": string.ascii_uppercase,
    "digit": string.digits,
    "special": SPECIALS,
}


def get_policy() -> dict:
    """Expose the current password generation policy."""
    return {
        "min_length": DEFAULT_POLICY["min_length"],
        "required_classes": DEFAULT_POLICY["require_classes"],
        "class_sizes": {c: len(CLASS_MAP[c]) for c in DEFAULT_POLICY["require_classes"]},
    }


def generate_password(length: int = 14, policy: dict | None = None) -> str:
    policy = policy or DEFAULT_POLICY
    length = max(length, policy.get("min_length", 12))
    pools = [CLASS_MAP[c] for c in policy.get("require_classes", []) if c in CLASS_MAP]
    if not pools:
        pools = [string.ascii_letters + string.digits + SPECIALS]
    # Ensure at least one from each required
    password_chars: list[str] = [secrets.choice(pool) for pool in pools]
    all_chars = "".join(pools)
    while len(password_chars) < length:
        password_chars.append(secrets.choice(all_chars))
    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)

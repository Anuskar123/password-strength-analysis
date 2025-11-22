import math
from dataclasses import dataclass
from typing import Tuple

SPECIALS = "!@#$%^&*"  # policy-defined specials

@dataclass
class EntropyResult:
    entropy_bits: float
    score: int
    strength: str


def calculate_entropy(password: str) -> float:
    """Estimate entropy bits via length * log2(charset_size)."""
    if not password:
        return 0.0
    charset = 0
    if any(c.islower() for c in password):
        charset += 26
    if any(c.isupper() for c in password):
        charset += 26
    if any(c.isdigit() for c in password):
        charset += 10
    if any(c in SPECIALS for c in password):
        charset += len(SPECIALS)
    if charset == 0:
        return 0.0
    return round(len(password) * math.log2(charset), 2)


def classify_entropy(entropy: float, password: str) -> EntropyResult:
    """Map entropy to a score and qualitative strength with handcrafted thresholds."""
    # Score capped 0-100, mild curvature for shorter passwords.
    raw_score = int(entropy)
    score = min(100, raw_score)
    if score < 40:
        strength = "Weak"
    elif score < 65:
        strength = "Moderate"
    elif score < 80:
        strength = "Strong"
    else:
        strength = "Robust"
    return EntropyResult(entropy_bits=entropy, score=score, strength=strength)


def crack_time_estimate(entropy: float, guesses_per_second: float = 1e10) -> Tuple[int, str]:
    """Return seconds and a coarse human readable duration string.
    Assumes brute force space ~2**entropy.
    """
    if entropy <= 0:
        return 0, "instant"
    seconds = int((2 ** entropy) / guesses_per_second)
    if seconds < 1:
        return seconds, "<1s"
    # Convert to human scale
    units = [
        (60, "s"),
        (60, "m"),
        (24, "h"),
        (365, "d"),
    ]
    value = seconds
    parts = []
    labels = ["s", "m", "h", "d", "y"]
    idx = 0
    while value and idx < len(units):
        base, label = units[idx]
        parts.append(f"{value % base}{labels[idx]}")
        value //= base
        idx += 1
    if value:
        parts.append(f"{value}y")
    return seconds, " ".join(reversed(parts))


def improvement_hints(password: str) -> list[str]:
    hints = []
    if len(password) < 12:
        hints.append("Consider length >= 12 for baseline resilience.")
    if password.isalpha():
        hints.append("Add digits and symbols for diversity.")
    if password.isdigit():
        hints.append("Add letters and symbols; pure numbers are weak.")
    if password.islower():
        hints.append("Mix uppercase to raise combinations.")
    if not any(c in SPECIALS for c in password):
        hints.append(f"Introduce specials like {SPECIALS}.")
    return hints

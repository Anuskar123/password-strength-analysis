import re
from typing import Iterable, List

DATE_PATTERNS = [r"\\b(19|20)\\d{2}\\b", r"\\b\\d{4}\\b"]  # Years / obvious 4-digit blocks


def tokenize_context(raw: str) -> List[str]:
    return [t.lower() for t in re.split(r"\W+", raw) if t]


def detect_personal_leak(password: str, context_tokens: Iterable[str]) -> List[str]:
    pw_low = password.lower()
    leaks = []
    for token in context_tokens:
        if token and len(token) >= 3 and token in pw_low:
            leaks.append(token)
    # Year patterns
    for pat in DATE_PATTERNS:
        if re.search(pat, password):
            leaks.append("year-like")
            break
    return leaks

import re
from typing import List

KEYBOARD_ROWS = ["1234567890", "qwertyuiop", "asdfghjkl", "zxcvbnm"]
COMMON_SUBSTRINGS = {"password", "admin", "welcome", "qwerty", "letmein"}
LEET_MAP = {"@": "a", "4": "a", "0": "o", "1": "l", "$": "s", "3": "e"}


def _normalize_leet(s: str) -> str:
    return "".join(LEET_MAP.get(c.lower(), c.lower()) for c in s)


def find_patterns(pw: str) -> List[str]:
    findings: List[str] = []
    low = pw.lower()
    # Backreference for repeated characters (3+). Raw string must use single backslash.
    if re.search(r"(.)\1{2,}", pw):
        findings.append("Repeated character run (>=3).")
    # Sequential digits / alpha (length >=4)
    for i in range(len(low) - 3):
        slice_ = low[i : i + 4]
        if slice_.isalnum():
            # Check ascending sequence
            if all(ord(slice_[j + 1]) - ord(slice_[j]) == 1 for j in range(3)):
                findings.append(f"Ascending sequence '{slice_}'.")
                break
    # Keyboard row walks
    for row in KEYBOARD_ROWS:
        for i in range(len(row) - 3):
            seq = row[i : i + 4]
            if seq in low:
                findings.append(f"Keyboard walk '{seq}'.")
                break
    # Common words / substrings inc. leet
    norm = _normalize_leet(low)
    for w in COMMON_SUBSTRINGS:
        if w in low or w in norm:
            findings.append(f"Common term '{w}'.")
    return findings

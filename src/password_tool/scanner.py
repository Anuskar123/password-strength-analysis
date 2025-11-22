from __future__ import annotations
import hashlib
import json
from pathlib import Path
from typing import Iterable, Dict, List

from .entropy import calculate_entropy, classify_entropy, improvement_hints, crack_time_estimate
from .patterns import find_patterns
from .context import detect_personal_leak
from .generator import generate_password


def scan_file(path: str, context_tokens: Iterable[str], redact: bool = False, hash_only: bool = False) -> List[Dict]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    seen_hashes = set()
    records = []
    for line in p.read_text(encoding="utf-8").splitlines():
        pw = line.strip()
        if not pw:
            continue
        h = hashlib.sha256(pw.encode()).hexdigest()
        duplicate = h in seen_hashes
        seen_hashes.add(h)
        entropy = calculate_entropy(pw)
        entropy_result = classify_entropy(entropy, pw)
        secs, human_time = crack_time_estimate(entropy)
        patterns = find_patterns(pw)
        leaks = detect_personal_leak(pw, context_tokens)
        hints = improvement_hints(pw) if entropy_result.strength in {"Weak", "Moderate"} else []
        display_pw = ("*" * len(pw)) if redact else (h if hash_only else pw)
        suggestion = generate_password(len(pw) + 2) if entropy_result.strength in {"Weak", "Moderate"} else None
        records.append({
            "password": display_pw,
            "sha256": h,
            "duplicate": duplicate,
            "entropy_bits": entropy_result.entropy_bits,
            "score": entropy_result.score,
            "strength": entropy_result.strength,
            "crack_seconds": secs,
            "crack_display": human_time,
            "patterns": patterns,
            "personal_leaks": leaks,
            "hints": hints,
            "suggestion": suggestion,
        })
    return records


def write_text_report(records: List[Dict], outfile: str) -> None:
    lines = ["--- Password Scan Report ---", f"Total: {len(records)}", ""]
    for r in records:
        lines.append(f"Password: {r['password']}")
        lines.append(f"Strength: {r['strength']} ({r['score']}/100)  Entropy: {r['entropy_bits']} bits")
        lines.append(f"Crack Time: {r['crack_display']}")
        if r["duplicate"]:
            lines.append("[!] Duplicate detected")
        if r["patterns"]:
            lines.append("[!] Patterns: " + ", ".join(r["patterns"]))
        if r["personal_leaks"]:
            lines.append("[!] Personal context leak: " + ", ".join(r["personal_leaks"]))
        if r["hints"]:
            lines.append("Hints: " + " | ".join(r["hints"]))
        if r["suggestion"]:
            lines.append("Suggestion: " + r["suggestion"])
        lines.append("-" * 50)
    Path(outfile).write_text("\n".join(lines), encoding="utf-8")


def write_json(records: List[Dict], outfile: str) -> None:
    Path(outfile).write_text(json.dumps(records, indent=2), encoding="utf-8")

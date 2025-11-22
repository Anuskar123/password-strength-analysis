# Password Tool Setup & Implementation Guide

This guide summarizes environment setup, key modules, how analysis works, and how to generate the accompanying PDF.

## 1. Environment Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev,docs]
```

## 2. Commands Cheatsheet

| Action            | Command                                                                   |
| ----------------- | ------------------------------------------------------------------------- |
| Help              | `pwtool --help`                                                           |
| Analyze single    | `pwtool analyze "MyP@ss!2025" --context "alice 1999" --json-out one.json` |
| Scan file         | `pwtool scan sample_passwords.txt --redact --json-out scan.json`          |
| Generate password | `pwtool generate --length 18`                                             |
| Show policy       | `pwtool policy`                                                           |
| Tips              | `pwtool tips`                                                             |

## 3. Module Responsibilities

| Module       | Purpose                                                              |
| ------------ | -------------------------------------------------------------------- |
| entropy.py   | Entropy bits, strength tier, hints, crack estimate                   |
| patterns.py  | Detect repeats, sequences, keyboard walks, common terms (leet aware) |
| context.py   | Tokenize user context & find leaks (names, years)                    |
| generator.py | Secure password generation w/ policy; exposes `get_policy()`         |
| scanner.py   | Batch file processing, duplicate detection, JSON + text reports      |
| cli.py       | Typer CLI wiring all features                                        |

## 4. Entropy & Strength

Entropy ~ `length * log2(charset_size)`. Charset size increments for lowercase, uppercase, digits, specials (`!@#$%^&*`). Strength thresholds: <40 Weak, 40-64 Moderate, 65-79 Strong, 80+ Robust.

## 5. Pattern Detection

- Regex for repeated character runs `(.)\1{2,}`
- 4-char ascending slices (abcd, 1234)
- Keyboard row walks (e.g. qwer, asdf)
- Common words list + leet normalization (P@ssw0rd → password)

## 6. Personal Context Leakage

User input (e.g. `alice 1999 alice@example.com`) tokenized; tokens length ≥3 matched in password. Year-like patterns flagged separately.

## 7. File Scan Flow

1. Read lines.
2. SHA-256 each password; track duplicates.
3. Compute entropy + strength; detect patterns and leaks.
4. Provide hints & suggestions if weak/moderate.
5. Write human text + optional JSON.

## 8. Generator Policy

```
min_length: 14
required_classes: [lower, upper, digit, special]
```

Guarantees one from each required class; fills remainder from combined pool. Shuffled using `secrets` for unpredictability.

## 9. Crack Time Estimate

Educational formula: `(2 ** entropy_bits) / 1e10` guesses/sec baseline. Not a guarantee—real attackers prune guesses.

## 10. Extending

- Add breach check API.
- More patterns (reverse sequences, shifted keyboard walks).
- Markov / PCFG estimation.
- CSV / HTML exporters.
- FastAPI wrapper for web usage.

## 11. Testing

Run all tests:

```bash
pytest -q
```

Focus on deterministic modules; randomness tested by required class presence.

## 12. Generating PDF

After installing docs extras:

```bash
python scripts/build_pdf.py
```

Produces `docs/password_tool_guide.pdf`.

## 13. Resume Bullet Example

"Developed a Python CLI for password analysis combining entropy scoring, pattern & personal data detection, secure generation, and batch auditing. Delivered JSON/Text reports, policy introspection, and a 10-test suite to ensure reliability."

## 14. Interview Sound Bite

"I went beyond simple length rules by modeling entropy, human pattern biases, and personal info leakage. The tool audits passwords, suggests improvements, and is cleanly modular so each piece is easy to extend."

## 15. Philosophy

Readable > Clever. Explainable > Flashy. Real attacker heuristics > superficial rules.

## 16. License

Currently UNLICENSED placeholder. Choose MIT/Apache 2.0 before publishing.

---

End of setup guide.

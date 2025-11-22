# Password Strength & Hygiene Toolkit

I built this to learn how attackers think about guessing passwords and to give myself (and others) feedback that is actually actionable. Instead of a generic "must include a number" rule set, this project looks at the patterns people really use and explains why they’re risky.

## What It Does (Short Version)

Analyze a single password or a whole file. Score it (entropy estimate), flag human patterns (repeats, keyboard walks, sequences, common words, leet variants like `P@ssw0rd`), warn if personal context (name, year) appears, suggest stronger alternatives, and optionally output JSON for automation.

## Why This Matters

Attackers start with patterns and leaked datasets, not random brute force. When you see _why_ a password is weak you learn how to build better ones next time.

## Layout

```
src/password_tool/
  entropy.py    # entropy & strength classification
  patterns.py   # pattern/common term detection
  context.py    # personal info leak detection
  generator.py  # secure password generator + policy
  scanner.py    # batch file processing & reports
  cli.py        # Typer-based CLI entry points
data/common_passwords.txt
tests/ (pytest unit tests)
```

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pwtool --help
```

## Example Usage

```bash
pwtool analyze "P@ssw0rd2025!" --context "alice 2000 alice@example.com" --json-out one.json
pwtool scan passwords.txt --redact --json-out scan.json
pwtool generate --length 18
pwtool policy
```

## Feature Highlights

- Entropy estimate + strength tiers (Weak / Moderate / Strong / Robust)
- Pattern detection (repeats, sequences, keyboard walks, common words, leet forms)
- Personal context leak check (names, emails, years)
- File scan: duplicate detection via SHA-256, suggestions for weak entries
- Secure generator using `secrets` with clear policy
- Policy inspection (`pwtool policy`)
- JSON + text reports
- 10 test cases covering core logic & CLI output

## Entropy (Approximate)

Formula: `bits = length * log2(charset_size)` where charset grows with detected classes (lower, upper, digits, specials). It’s a rough upper bound, not a guarantee.

## Patterns Detected

Repeated character runs, ascending sequences (`abcd`, `1234`), keyboard row walks (`qwer`, `asdf`), common terms (including leet normalization like `P@ssw0rd` → `password`).

## Personal Context

Tokens (length ≥3) from a user-supplied string plus year-like patterns (19xx/20xx) are matched inside the password.

## File Scan Flow

Read lines → hash for duplicate tracking → analyze (entropy, patterns, leaks) → collect hints/suggestion → write text and optional JSON.

## Crack Time Estimate

Educational only: `(2 ** entropy_bits) / 1e10` guesses/second. Real attacks prune the space; treat this as a rough scale.

## Generator Policy

Minimum length 14, requires lower, upper, digit, special. Ensures one of each then fills with randomized characters from combined pool and shuffles.

## Limitations

No breach API checks yet, simplified entropy model, small pattern corpus, CLI only, assumes local usage.

## Modules Overview

| Module       | Purpose                              |
| ------------ | ------------------------------------ |
| entropy.py   | Entropy math + strength tier + hints |
| patterns.py  | Pattern/common term detection        |
| context.py   | Personal info leak detection         |
| generator.py | Secure generation + policy exposure  |
| scanner.py   | Batch file scan + reporting          |
| cli.py       | Typer CLI glue                       |

## Testing

Run `pytest -q`. Tests cover entropy calc, patterns, generator policy, scanner logic, CLI JSON output.

## Add A New Pattern

Edit `patterns.py`, add logic or term, add a test, run pytest. Keep each addition simple and focused.

## Future Ideas

Breach API checks, reversed/shifted keyboard sequences, probabilistic strength models, CSV/HTML exporters, TUI, web wrapper.

## Automation Ideas

Use JSON output in CI to enforce minimum entropy; scan internal dumps without exposing raw passwords; auto-generate onboarding secrets.


## Philosophy

Readable > clever. Explain _why_, not just “weak”. Security learning > strict rule enforcement.




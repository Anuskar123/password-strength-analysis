import typer
from rich import print
from rich.table import Table
from typing import Optional

from .entropy import calculate_entropy, classify_entropy, improvement_hints, crack_time_estimate
from .patterns import find_patterns
from .context import tokenize_context, detect_personal_leak
from .generator import generate_password, get_policy
from .scanner import scan_file, write_text_report, write_json

app = typer.Typer(help="Advanced password strength & hygiene toolkit")


@app.command()
def analyze(password: str, context: Optional[str] = typer.Option(None, help="Space / punctuation separated personal context tokens"), json_out: Optional[str] = typer.Option(None, help="Write JSON record to file")):
    """Analyze a single password. Optionally emit JSON."""
    tokens = tokenize_context(context) if context else []
    entropy = calculate_entropy(password)
    result = classify_entropy(entropy, password)
    secs, human_time = crack_time_estimate(entropy)
    patterns = find_patterns(password)
    leaks = detect_personal_leak(password, tokens)
    hints = improvement_hints(password) if result.strength in {"Weak", "Moderate"} else []

    table = Table(title="Password Analysis", show_lines=True)
    table.add_column("Field")
    table.add_column("Value")
    table.add_row("Strength", f"{result.strength} ({result.score}/100)")
    table.add_row("Entropy", f"{result.entropy_bits} bits")
    table.add_row("Crack Time", human_time)
    table.add_row("Patterns", ", ".join(patterns) if patterns else "None")
    table.add_row("Personal Leaks", ", ".join(leaks) if leaks else "None")
    if hints:
        table.add_row("Hints", " | ".join(hints))
    if result.strength in {"Weak", "Moderate"}:
        table.add_row("Suggestion", generate_password(len(password) + 2))
    print(table)
    record = {
        "password_length": len(password),
        "entropy_bits": result.entropy_bits,
        "score": result.score,
        "strength": result.strength,
        "crack_display": human_time,
        "patterns": patterns,
        "personal_leaks": leaks,
        "hints": hints,
    }
    if json_out:
        import json
        with open(json_out, "w", encoding="utf-8") as fh:
            json.dump(record, fh, indent=2)
        print(f"[green]JSON written to {json_out}")


@app.command()
def scan(path: str, context: Optional[str] = typer.Option(None), redact: bool = typer.Option(False), hash_only: bool = typer.Option(False), json_out: Optional[str] = typer.Option(None), text_out: Optional[str] = typer.Option("scan_report.txt")):
    """Scan a file containing one password per line."""
    tokens = tokenize_context(context) if context else []
    records = scan_file(path, tokens, redact=redact, hash_only=hash_only)
    if text_out:
        write_text_report(records, text_out)
        print(f"[green]Text report written to {text_out}")
    if json_out:
        write_json(records, json_out)
        print(f"[green]JSON data written to {json_out}")
    print(f"Processed {len(records)} passwords.")


@app.command()
def generate(length: int = typer.Option(16, min=8, help="Desired length >=8")):
    """Generate a strong password respecting policy."""
    print(generate_password(length))


@app.command()
def tips():
    """Show general strengthening guidance."""
    print("[bold cyan]General Password Tips")
    for t in [
        "Length matters: favor >=12 characters.",
        "Avoid keyboard walks and obvious sequences.",
        "Don’t embed personal data (names, years).",
        "Mix character classes; unpredictability is the goal.",
        "Unique per service; reuse amplifies breach impact.",
    ]:
        print(f"• {t}")


@app.command()
def policy():
    """Show current password generation policy."""
    p = get_policy()
    tbl = Table(title="Password Policy")
    tbl.add_column("Key")
    tbl.add_column("Value")
    tbl.add_row("Min Length", str(p["min_length"]))
    tbl.add_row("Required Classes", ", ".join(p["required_classes"]))
    for cls, size in p["class_sizes"].items():
        tbl.add_row(f"Class '{cls}' size", str(size))
    print(tbl)


if __name__ == "__main__":  # pragma: no cover
    app()

import json
import subprocess
import sys
from pathlib import Path


def test_cli_analyze_json(tmp_path):
    out = tmp_path / "pw.json"
    cmd = [sys.executable, "-m", "password_tool.cli", "analyze", "Passw0rd!!", "--json-out", str(out)]
    subprocess.run(cmd, check=True)
    data = json.loads(out.read_text())
    assert data["entropy_bits"] > 0
    assert "strength" in data
    assert isinstance(data["patterns"], list)

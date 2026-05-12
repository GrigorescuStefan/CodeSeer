import json
import os
from scanner.normalize import normalize_bandit, normalize_semgrep, normalize_ruff

def load_findings(output_path="/output"):
    findings = []

    bandit_path = f"{output_path}/bandit-report.json"
    semgrep_path = f"{output_path}/semgrep-report.json"
    ruff_path = f"{output_path}/ruff-report.json"

    if os.path.exists(bandit_path):
        with open(bandit_path) as f:
            data = json.load(f)
        for item in data.get("results", []):
            findings.append(normalize_bandit(item))

    if os.path.exists(semgrep_path):
        with open(semgrep_path) as f:
            data = json.load(f)
        for item in data.get("results", []):
            findings.append(normalize_semgrep(item))

    if os.path.exists(ruff_path):
        with open(ruff_path) as f:
            data = json.load(f)
    print("RUFF RAW SAMPLE:", data[:1])

    if os.path.exists(ruff_path):
        with open(ruff_path) as f:
            data = json.load(f)
        for item in data.get("results", []):
            findings.append(normalize_ruff(item))

    return findings
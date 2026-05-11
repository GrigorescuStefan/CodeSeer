import json
import os
from scanner.normalize import normalize_bandit, normalize_semgrep

def load_findings(output_path="/output"):
    findings = []

    bandit_path = f"{output_path}/bandit-report.json"
    semgrep_path = f"{output_path}/semgrep-report.json"

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

    return findings
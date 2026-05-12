import os
import subprocess
import sys

INPUT_PATH = os.getenv("INPUT_PATH", "/input")
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "/output")

print(f"Scanning input: {INPUT_PATH}")
print(f"Writing output to: {OUTPUT_PATH}")

# Run Bandit
result = subprocess.run([
    "bandit",
    "-r",
    INPUT_PATH,
    "-x",
    f"{INPUT_PATH}/tests,{INPUT_PATH}/venv",
    "-f",
    "json",
    "-o",
    f"{OUTPUT_PATH}/bandit-report.json"
])

# Run Semgrep
semgrep_result = subprocess.run([
    "semgrep",
    "--config=auto",
    INPUT_PATH,
    "--json",
    "--output",
    f"{OUTPUT_PATH}/semgrep-report.json"
])

# Run Ruff
subprocess.run([
    "ruff",
    "check",
    INPUT_PATH,
    "--format",
    "json",
    "--output-file",
    f"{OUTPUT_PATH}/ruff-report.json"
])

# Generate HTML report
subprocess.run([
    "python",
    "-m",
    "scanner.report_generator"
])

# Evaluate results
policy = subprocess.run([
    "python",
    "-m",
    "scanner.evaluate"
])

sys.exit(policy.returncode)
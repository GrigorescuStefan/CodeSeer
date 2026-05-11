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
    "-f",
    "json",
    "-o",
    f"{OUTPUT_PATH}/report.json"
])

# Generate HTML report
subprocess.run([
    "python",
    "scanner/report_generator.py"
])

# Evaluate results
policy = subprocess.run([
    "python",
    "scanner/evaluate.py"
])

sys.exit(policy.returncode)
import os
import subprocess
import sys

TARGET = os.getenv("SCAN_PATH", "/scan")

print(f"Scanning: {TARGET}")

# Run Bandit (exclude venv + noise folders)
result = subprocess.run([
    "bandit",
    "-r",
    TARGET,
    "-x",
    f"{TARGET}/venv,{TARGET}/__pycache__,{TARGET}/site-packages",
    "-f",
    "json",
    "-o",
    f"{TARGET}/report.json"
])

# Generate HTML report
subprocess.run([
    "python",
    "scanner/report_generator.py"
])

# Run policy engine LAST
policy = subprocess.run([
    "python",
    "scanner/evaluate.py"
])

# Exit with policy result (CI gate)
sys.exit(policy.returncode)
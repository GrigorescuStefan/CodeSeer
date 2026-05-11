import os
import json
import sys

OUTPUT_PATH = os.getenv("OUTPUT_PATH", "/output")

BANDIT_REPORT = os.path.join(OUTPUT_PATH, "bandit-report.json")
SEMGREP_REPORT = os.path.join(OUTPUT_PATH, "semgrep-report.json")

total_high = 0
total_medium = 0
total_low = 0

print("\n=== Security Scan Summary ===")

# BANDIT
if os.path.exists(BANDIT_REPORT):

    with open(BANDIT_REPORT, "r") as f:
        bandit = json.load(f)

    bandit_results = bandit.get("results", [])

    high = [
        r for r in bandit_results
        if r.get("issue_severity") == "HIGH"
    ]

    medium = [
        r for r in bandit_results
        if r.get("issue_severity") == "MEDIUM"
    ]

    low = [
        r for r in bandit_results
        if r.get("issue_severity") == "LOW"
    ]

    total_high += len(high)
    total_medium += len(medium)
    total_low += len(low)

    print(f"\nBandit findings: {len(bandit_results)}")

# SEMGREP
if os.path.exists(SEMGREP_REPORT):

    with open(SEMGREP_REPORT, "r") as f:
        semgrep = json.load(f)

    semgrep_results = semgrep.get("results", [])

    for r in semgrep_results:

        severity = (
            r.get("extra", {})
             .get("severity", "LOW")
             .upper()
        )

        if severity == "ERROR":
            total_high += 1

        elif severity == "WARNING":
            total_medium += 1

        else:
            total_low += 1

    print(f"Semgrep findings: {len(semgrep_results)}")

# -------------------------
# FINAL SUMMARY
# -------------------------

total = total_high + total_medium + total_low

print("\n=== Combined Results ===")
print(f"Total Issues: {total}")
print(f"HIGH: {total_high}")
print(f"MEDIUM: {total_medium}")
print(f"LOW: {total_low}")

# Policy Gate
if total_high > 0:
    print("\nPipeline failed (HIGH severity vulnerabilities detected)")
    sys.exit(1)

print("\nPipeline passed!")
sys.exit(0)
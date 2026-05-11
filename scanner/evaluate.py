import json
import sys

with open("report.json", "r") as f:
    data = json.load(f)

results = data.get("results", [])

high = [r for r in results if r.get("issue_severity") == "HIGH"]
medium = [r for r in results if r.get("issue_severity") == "MEDIUM"]
low = [r for r in results if r.get("issue_severity") == "LOW"]

print("\n=== Security Scan Summary ===")
print(f"Total issues: {len(results)}")
print(f"HIGH: {len(high)}")
print(f"MEDIUM: {len(medium)}")
print(f"LOW: {len(low)}")

print("\n=== Findings ===")
for r in results:
    print("-" * 40)
    print(f"File: {r.get('filename')}")
    print(f"Line: {r.get('line_number')}")
    print(f"Severity: {r.get('issue_severity')}")
    print(f"Issue: {r.get('issue_text')}")

# Policy decision (your security gate)
if high:
    print("\nPipeline failed (HIGH severity vulnerabilities detected)")
    sys.exit(1)

print("\nPipeline passed!")
sys.exit(0)
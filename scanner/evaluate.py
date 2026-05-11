import sys
from scanner.aggregate import load_findings

findings = load_findings()

high = [f for f in findings if f.severity == "HIGH"]
medium = [f for f in findings if f.severity == "MEDIUM"]
low = [f for f in findings if f.severity == "LOW"]

print("\n=== Security Summary ===")
print(f"Total: {len(findings)}")
print(f"HIGH: {len(high)}")
print(f"MEDIUM: {len(medium)}")
print(f"LOW: {len(low)}")

print("\n=== Findings ===")

for f in findings:
    print("-" * 40)
    print(f"Tool: {f.tool}")
    print(f"File: {f.file}")
    print(f"Line: {f.line}")
    print(f"Severity: {f.severity}")
    print(f"Issue: {f.message}")

if high:
    print("\nFAILED: HIGH severity vulnerabilities detected")
    sys.exit(1)

print("\nPASSED")
sys.exit(0)
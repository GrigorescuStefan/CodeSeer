import json
import sys

with open("report.json", "r") as f:
    data = json.load(f)

high_severity = [
    issue for issue in data["results"]
    if issue["issue_severity"] == "HIGH"
]

print(f"Total issues: {len(data['results'])}")
print(f"High severity issues: {len(high_severity)}")

if high_severity:
    print("Pipeline failed due to 'High' severity vulnerabilities")
    sys.exit(1)
else:
    print("Pipeline passed!")
    sys.exit(0)
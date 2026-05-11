import json

with open("report.json", "r") as f:
    data = json.load(f)

for issue in data["results"]:
    print("Issue:", issue["issue_text"])
    print("Severity:", issue["issue_severity"])
    print("File:", issue["filename"])
    print("---")
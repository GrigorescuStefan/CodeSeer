import json
import os

OUTPUT_PATH = os.getenv("OUTPUT_PATH", "/output")

BANDIT_REPORT = f"{OUTPUT_PATH}/bandit-report.json"
SEMGREP_REPORT = f"{OUTPUT_PATH}/semgrep-report.json"

HTML_PATH = f"{OUTPUT_PATH}/report.html"

html = """
<html>
<head>
    <title>CodeSeer Security Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
        }

        h1 {
            color: #333;
        }

        h2 {
            margin-top: 40px;
            color: #444;
        }

        .finding {
            margin-bottom: 20px;
            padding: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }

        .HIGH {
            border-left: 8px solid red;
        }

        .MEDIUM {
            border-left: 8px solid orange;
        }

        .LOW {
            border-left: 8px solid green;
        }
    </style>
</head>
<body>

<h1>CodeSeer Security Report</h1>
"""

# BANDIT

html += "<h2>Bandit Findings</h2>"

if os.path.exists(BANDIT_REPORT):
    with open(BANDIT_REPORT) as f:
        bandit_data = json.load(f)
    for r in bandit_data.get("results", []):
        severity = r.get("issue_severity", "LOW")
        html += f"""
        <div class="finding {severity}">
            <h3>{severity}</h3>
            <p><b>Tool:</b> Bandit</p>
            <p><b>File:</b> {r.get('filename')}</p>
            <p><b>Line:</b> {r.get('line_number')}</p>
            <p><b>Issue:</b> {r.get('issue_text')}</p>
        </div>
        """
else:
    html += "<p>No Bandit report found.</p>"

# SEMGREP

html += "<h2>Semgrep Findings</h2>"

if os.path.exists(SEMGREP_REPORT):
    with open(SEMGREP_REPORT) as f:
        semgrep_data = json.load(f)
    for r in semgrep_data.get("results", []):
        severity = (
            r.get("extra", {})
             .get("severity", "LOW")
             .upper()
        )
        html += f"""
        <div class="finding {severity}">
            <h3>{severity}</h3>
            <p><b>Tool:</b> Semgrep</p>
            <p><b>File:</b> {r.get('path')}</p>
            <p><b>Rule:</b> {r.get('check_id')}</p>
            <p><b>Issue:</b> {r.get('extra', {}).get('message')}</p>
        </div>
        """
else:
    html += "<p>No Semgrep report found.</p>"

html += """
</body>
</html>
"""

with open(HTML_PATH, "w") as f:
    f.write(html)

print(f"Report generated at {HTML_PATH}")
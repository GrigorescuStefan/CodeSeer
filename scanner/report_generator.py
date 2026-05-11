import json
import os

OUTPUT_PATH = os.getenv("OUTPUT_PATH", "/output")

BANDIT_REPORT = f"{OUTPUT_PATH}/bandit-report.json"
SEMGREP_REPORT = f"{OUTPUT_PATH}/semgrep-report.json"

HTML_PATH = f"{OUTPUT_PATH}/report.html"

bandit_results = []
semgrep_results = []

if os.path.exists(BANDIT_REPORT):
    with open(BANDIT_REPORT) as f:
        bandit_data = json.load(f)
        bandit_results = bandit_data.get("results", [])

if os.path.exists(SEMGREP_REPORT):
    with open(SEMGREP_REPORT) as f:
        semgrep_data = json.load(f)
        semgrep_results = semgrep_data.get("results", [])

total_findings = len(bandit_results) + len(semgrep_results)

html = f"""
<html>
<head>
    <title>CodeSeer Security Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f5f5f5;
            color: #222;
        }}

        h1 {{
            color: #222;
        }}

        h2 {{
            margin-top: 40px;
            color: #333;
            border-bottom: 2px solid #ddd;
            padding-bottom: 10px;
        }}

        .summary {{
            display: flex;
            gap: 20px;
            margin-bottom: 40px;
        }}

        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            border-left: 8px solid #444;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            min-width: 180px;
        }}

        .finding {{
            background: white;
            margin-bottom: 20px;
            padding: 20px;
            border-radius: 8px;
            border-left: 8px solid gray;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}

        .HIGH {{
            border-left-color: #d9534f;
        }}

        .MEDIUM {{
            border-left-color: #f0ad4e;
        }}

        .LOW {{
            border-left-color: #5cb85c;
        }}

        .severity-title {{
            margin-top: 0;
        }}

        .tool-badge {{
            display: inline-block;
            background: #eee;
            padding: 4px 10px;
            border-radius: 5px;
            font-size: 14px;
            margin-bottom: 10px;
        }}

        code {{
            background: #eee;
            padding: 2px 6px;
            border-radius: 4px;
        }}

    </style>
</head>
<body>

<h1>CodeSeer Security Report</h1>

<div class="summary">
    <div class="summary-card">
        <h3>Total Findings</h3>
        <p>{total_findings}</p>
    </div>
    <div class="summary-card">
        <h3>Bandit Findings</h3>
        <p>{len(bandit_results)}</p>
    </div>
    <div class="summary-card">
        <h3>Semgrep Findings</h3>
        <p>{len(semgrep_results)}</p>
    </div>
</div>
"""

# BANDIT FINDINGS
html += "<h2>Bandit Findings</h2>"
if bandit_results:
    for r in bandit_results:
        severity = r.get("issue_severity", "LOW")
        html += f"""
        <div class="finding {severity}">
            <h3 class="severity-title">
                {severity} Severity Finding
            </h3>

            <div class="tool-badge">
                Bandit
            </div>

            <p>
                <b>File:</b>
                <code>{r.get('filename')}</code>
            </p>

            <p>
                <b>Line:</b>
                {r.get('line_number')}
            </p>

            <p>
                <b>Issue:</b>
                {r.get('issue_text')}
            </p>

        </div>
        """
else:
    html += "<p>No Bandit findings detected.</p>"

# SEMGREP FINDINGS
html += "<h2>Semgrep Findings</h2>"
if semgrep_results:
    for r in semgrep_results:
        raw_severity = (
            r.get("extra", {})
             .get("severity", "INFO")
             .upper()
        )
        severity_map = {
            "ERROR": "HIGH",
            "WARNING": "MEDIUM",
            "INFO": "LOW"
        }
        severity = severity_map.get(raw_severity, "LOW")
        html += f"""
        <div class="finding {severity}">

            <h3 class="severity-title">
                {severity} Severity Finding
            </h3>

            <div class="tool-badge">
                Semgrep
            </div>

            <p>
                <b>File:</b>
                <code>{r.get('path')}</code>
            </p>

            <p>
                <b>Rule:</b>
                <code>{r.get('check_id')}</code>
            </p>

            <p>
                <b>Issue:</b>
                {r.get('extra', {}).get('message')}
            </p>

        </div>
        """
else:
    html += "<p>No Semgrep findings detected.</p>"

html += """
</body>
</html>
"""

with open(HTML_PATH, "w") as f:
    f.write(html)

print(f"Report generated at {HTML_PATH}")
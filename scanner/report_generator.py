import json

with open("report.json") as f:
    data = json.load(f)

html = """
<html>
<head>
    <title>Security Report</title>
</head>
<body>
<h1>Security Scan Report</h1>
"""

for r in data.get("results", []):
    html += f"""
    <div style="margin-bottom:20px;padding:10px;border:1px solid #ccc;">
        <h3>{r.get('issue_severity')}</h3>
        <p><b>File:</b> {r.get('filename')}</p>
        <p><b>Line:</b> {r.get('line_number')}</p>
        <p><b>Issue:</b> {r.get('issue_text')}</p>
    </div>
    """

html += "</body></html>"

with open("report.html", "w") as f:
    f.write(html)
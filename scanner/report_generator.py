import os
from scanner.aggregate import load_findings

OUTPUT_PATH = os.getenv("OUTPUT_PATH", "/output")
HTML_PATH = f"{OUTPUT_PATH}/report.html"

findings = load_findings(OUTPUT_PATH)

total_findings = len(findings)

high = len([f for f in findings if f.severity == "HIGH"])
medium = len([f for f in findings if f.severity == "MEDIUM"])
low = len([f for f in findings if f.severity == "LOW"])

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

        .HIGH {{ border-left-color: #d9534f; }}
        .MEDIUM {{ border-left-color: #f0ad4e; }}
        .LOW {{ border-left-color: #5cb85c; }}

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
        <h3>HIGH</h3>
        <p>{high}</p>
    </div>

    <div class="summary-card">
        <h3>MEDIUM</h3>
        <p>{medium}</p>
    </div>

    <div class="summary-card">
        <h3>LOW</h3>
        <p>{low}</p>
    </div>
</div>

<h2>Findings</h2>
"""

for f in findings:

    html += f"""
    <div class="finding {f.severity}">

        <h3>{f.severity} Severity Finding</h3>

        <div class="tool-badge">
            {f.tool}
        </div>

        <p><b>File:</b> <code>{f.file}</code></p>
        <p><b>Line:</b> {f.line}</p>
        <p><b>Rule:</b> <code>{f.rule}</code></p>
        <p><b>Issue:</b> {f.message}</p>

    </div>
    """

html += """
</body>
</html>
"""

with open(HTML_PATH, "w") as f:
    f.write(html)

print(f"Report generated at {HTML_PATH}")
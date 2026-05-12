from scanner.model import Finding

SEVERITY_MAP = {
    "ERROR": "HIGH",
    "WARNING": "MEDIUM",
    "INFO": "LOW",
}

def normalize_bandit(item):
    return Finding(
        tool="bandit",
        severity=item.get("issue_severity", "LOW"),
        file=item.get("filename"),
        line=item.get("line_number"),
        rule=item.get("test_id"),
        message=item.get("issue_text"),
    )

def normalize_semgrep(item):
    extra = item.get("extra", {})

    raw = extra.get("severity", "INFO").upper()
    severity = SEVERITY_MAP.get(raw, "LOW")

    return Finding(
        tool="semgrep",
        severity=severity,
        file=item.get("path"),
        line=item.get("start", {}).get("line"),
        rule=item.get("check_id"),
        message=extra.get("message"),
    )

def normalize_ruff(item):
    location = item.get("location", {})

    return Finding(
        tool="ruff",
        severity="LOW",  # Ruff is for best-practices or linting, so it's non-blocking by default
        file=item.get("filename") or item.get("path"),
        line=location.get("row"),
        rule=item.get("code"),
        message=item.get("message"),
    )
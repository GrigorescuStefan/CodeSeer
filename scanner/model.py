from dataclasses import dataclass

@dataclass
class Finding:
    tool: str
    severity: str   # HIGH / MEDIUM / LOW
    file: str
    line: int | None
    rule: str | None
    message: str
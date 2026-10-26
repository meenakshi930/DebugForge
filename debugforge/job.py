from dataclasses import dataclass, field
from typing import Any


@dataclass
class Job:
    repo_path: str
    command: str
    bug_report: str = ""

    status: str = "CREATED"
    attempts: list[dict[str, Any]] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)

    def add_attempt(self, attempt: dict[str, Any]):
        self.attempts.append(attempt)

    def add_evidence(self, item: dict[str, Any]):
        self.evidence.append(item)
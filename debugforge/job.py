from dataclasses import dataclass, field
from typing import Any

from .attempt import AttemptHistory


@dataclass
class Job:
    repo_path: str
    command: str
    bug_report: str = ""

    status: str = "CREATED"
    attempts: AttemptHistory = field(
        default_factory=AttemptHistory
    )
    evidence: list[dict[str, Any]] = field(default_factory=list)

    def add_attempt(self, attempt):
        self.attempts.add_attempt(attempt)

    def add_evidence(self, item: dict[str, Any]):
        self.evidence.append(item)

    def last_attempt(self):
        return self.attempts.last_attempt()

    def is_verified(self):
        return self.attempts.successful()
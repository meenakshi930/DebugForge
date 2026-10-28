from dataclasses import dataclass, field


@dataclass
class RepairAttempt:
    attempt_number: int
    diagnosis: str
    file_path: str
    old_code: str
    new_code: str

    test_status: str = "NOT_RUN"
    verified: bool = False
    error: str | None = None


@dataclass
class AttemptHistory:
    attempts: list[RepairAttempt] = field(default_factory=list)

    def add_attempt(self, attempt: RepairAttempt):
        self.attempts.append(attempt)

    def last_attempt(self):
        if not self.attempts:
            return None

        return self.attempts[-1]

    def successful(self):
        if not self.attempts:
            return False

        return self.attempts[-1].verified
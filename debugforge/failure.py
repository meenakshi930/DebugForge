from dataclasses import dataclass


@dataclass
class TestFailure:
    command: str
    exit_code: int | None
    stdout: str
    stderr: str
    timed_out: bool = False

    @property
    def failed(self) -> bool:
        return self.exit_code != 0 or self.timed_out

    def summary(self) -> str:
        if self.timed_out:
            return "Test execution timed out."

        if self.exit_code == 0:
            return "Tests passed."

        return "Tests failed."
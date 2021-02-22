from enum import Enum

class SessionStatus(Enum):
    PASSED = "passed"
    FAILED = "failed"
    BROKEN = "broken"
    IN_PROGRESS = "in progress"
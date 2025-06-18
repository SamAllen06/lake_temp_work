from enum import auto, Enum


class CheckStatus(Enum):
    PASSED = auto()
    FAILED = auto()
    ERROR = auto()

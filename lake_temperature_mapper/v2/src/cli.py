from pathlib import Path

from output import console
from root import CONFIG_ROOT
from testing import Tester


DEFAULT_CONFIG_PATH = CONFIG_ROOT / "main.ini"


def _user_wants_to_continue_testing() -> bool:
    if input().strip().casefold() in ["yes", "y"]:
        return True
    return False


def main():
    console.enable()
    tester = Tester(DEFAULT_CONFIG_PATH)
    tester.prepare_for_testing()
    if _user_wants_to_continue_testing():
        tester.test_model()


if __name__ == "__main__":
    main()

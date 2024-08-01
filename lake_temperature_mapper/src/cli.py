from pathlib import Path

from output import view_manager
from output.views import View
import tester


def _enable_requested_views() -> None:
    requested_views = [View.CONSOLE, View.FILE, View.LOGS]
    # requested views is a list of View, not Module.
    view_manager.enable_views(requested_views) #type: ignore


def _user_wants_to_continue_testing() -> bool:
    if input().strip().casefold() in ["yes", "y"]:
        return True
    return False


def main():
    _enable_requested_views()
    tester.prepare_for_testing()
    if _user_wants_to_continue_testing():
        tester.test_model()


if __name__ == "__main__":
    main()

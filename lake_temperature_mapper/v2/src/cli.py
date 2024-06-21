from pathlib import Path

from output import console
from root import CONFIG_ROOT
from testing import Tester


DEFAULT_CONFIG_PATH = CONFIG_ROOT / "main.ini"


def main():
    console.enable()
    tester = Tester(DEFAULT_CONFIG_PATH)
    tester.begin()


if __name__ == "__main__":
    main()

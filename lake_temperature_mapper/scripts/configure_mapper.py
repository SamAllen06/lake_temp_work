import argparse
import importlib
import importlib.util
from pathlib import Path
from typing import Mapping

from config import ConfigWriter


def _parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-m", "--module",
        help="The module to configure. Must have a config submodule. Default: testing",
        default="testing"
    )

    return parser.parse_args()


def main():
    module_name = _parse_arguments().module

    if not importlib.util.find_spec(module_name):
        raise ModuleNotFoundError(f"Could not find module {module_name}")

    module = importlib.import_module(module_name)

    try:
        config_module = module.config
    except AttributeError:
        raise AttributeError(f"Could not find config module for {module_name}")

    config_writer = ConfigWriter(config_module)
    config_writer.configure_interactively()


if __name__ == "__main__":
    main()

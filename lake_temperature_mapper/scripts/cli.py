import argparse
from pathlib import Path

from mapping.mapper import Mapper

PARENT_DIRECTORY = Path(__file__).resolve().parent
DEFAULT_CONFIG_PATH = PARENT_DIRECTORY / "config" / "mapper.conf"


def _initialize_cli_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config_path", help="The path to the config file. Default: scripts/config/mapper.conf",
                        type=str, default="")

    return parser.parse_args()


def _resolve_config_path(config_path_arg: str) -> Path:
    if not config_path_arg:
        config_path = DEFAULT_CONFIG_PATH
    else:
        config_path = Path.cwd() / args.config_path

    if not config_path.exists() or not config_path.is_file():
        raise FileNotFoundError(
            f"Could not find config file {str(self._config_path)}"
        )

    return config_path


def main():
    args = _initialize_cli_arguments()

    config_path = _resolve_config_path(args.config_path)

    mapper = Mapper(config_path)
    mapper.map()


if __name__ == "__main__":
    main()

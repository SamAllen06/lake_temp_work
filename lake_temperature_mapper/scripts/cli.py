import argparse
from pathlib import Path

from mapping.mapper import Mapper


PARENT_DIRECTORY = Path(__file__).resolve().parent
DEFAULT_CONFIG_PATH = PARENT_DIRECTORY / "config" / "mapper.conf"


def initialize_cli_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config_path", help="The path to the config file. Default: scripts/config/mapper.conf",
                        type=str, default="")

    return parser.parse_args()


def main():
    args = initialize_cli_arguments()

    if not args.config_path:
        absolute_config_path = DEFAULT_CONFIG_PATH
    else:
        absolute_config_path = Path.cwd() / args.config_path

    mapper = Mapper(absolute_config_path)
    mapper.map()

    

if __name__ == "__main__":
    main()

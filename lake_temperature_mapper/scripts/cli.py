import argparse
from pathlib import Path

from config.config_reader import ConfigReader
from mapping.mapper import Mapper
from output.console_output_writer import ConsoleOutputWriter
from output.csv_output_writer import CSVOutputWriter
from output.group_output_writer import GroupOutputWriter
from output.output_writer import OutputWriter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "mapper.conf"


def _initialize_cli_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config_path",
                        help="The path to the config file. Default: scripts/config/mapper.conf",
                        type=str, default="")
    parser.add_argument("-s", "--store",
                        help="Store mapping data in csv files.",
                        action="store_true")
    parser.add_argument("-q", "--quiet",
                        help="Prevent printing of mapping data to stdout.",
                        action="store_true")

    return parser.parse_args()


def _resolve_config_path(config_path_arg: str) -> Path:
    if not config_path_arg:
        config_path = DEFAULT_CONFIG_PATH
    else:
        config_path = Path.cwd() / config_path_arg

    if not config_path.exists() or not config_path.is_file():
        raise FileNotFoundError(
            f"Could not find config file {str(self._config_path)}"
        )

    return config_path


def _generate_output_writer(
        args: argparse.Namespace,
        config_reader: ConfigReader
) -> GroupOutputWriter:
    group_writer = GroupOutputWriter()

    if not args.quiet:
        group_writer.add_writer(ConsoleOutputWriter())

    if args.store:
        group_writer.add_writer(
            CSVOutputWriter(config_reader.get_path("output_directory"))
        )

    return group_writer


def main():
    args = _initialize_cli_arguments()

    config_path = _resolve_config_path(args.config_path)
    config_reader = ConfigReader(config_path)

    output_writer = _generate_output_writer(args, config_reader)

    mapper = Mapper(config_reader, output_writer)
    mapper.map()


if __name__ == "__main__":
    main()

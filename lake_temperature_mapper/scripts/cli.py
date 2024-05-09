import argparse
from pathlib import Path

from mapping.binary_runner import BinaryRunner
from mapping.config_reader import ConfigReader
from mapping.difference_analyzer import DifferenceAnalyzer
from mapping.param_editor import ParamEditor
from mapping.range_reader import RangeReader

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

    config_reader = ConfigReader(absolute_config_path)

    if not config_reader.config_exists():
        raise FileNotFoundError(f"Could not find config file {absolute_config_path}.")

    runner = BinaryRunner(PARENT_DIRECTORY / config_reader.get_path_of("binary_path"))
    runner.run()

    range_reader = RangeReader(PARENT_DIRECTORY / config_reader.get_path_of("range_path"))
    print(range_reader.read_ranges())

    param_editor = ParamEditor(PARENT_DIRECTORY / config_reader.get_path_of("params_path"))
    param_editor.modify_parameter("betavis", 0.5)

    difference_analyzer = DifferenceAnalyzer(
        PARENT_DIRECTORY / config_reader.get_path_of("ref_output"),
        PARENT_DIRECTORY / config_reader.get_path_of("test_output")
    )

    print(difference_analyzer.compare_outputs())


if __name__ == "__main__":
    main()

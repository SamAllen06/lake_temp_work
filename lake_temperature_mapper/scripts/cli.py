import argparse

from binary_runner import BinaryRunner
from param_editor import ParamEditor
from range_reader import RangeReader


def initialize_cli_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("elmtest_path", help="The path to elmtest.exe.", type=str)
    parser.add_argument("range_path", help="The path to FUT_lake_range.txt.", type=str)
    parser.add_argument("params_path", help="The path to lakeparams.txt.", type=str)

    return parser.parse_args()


def main():
    args = initialize_cli_arguments()

    runner = BinaryRunner(args.elmtest_path)
    runner.run()

    range_reader = RangeReader(args.range_path)
    print(range_reader.read_ranges())

    param_editor = ParamEditor(args.params_path)
    param_editor.modify_parameter("betavis", 0.5)
    param_editor.modify_parameter("bleh", 0.0034)


if __name__ == "__main__":
    main()

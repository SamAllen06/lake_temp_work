import argparse
import os

from binary_runner import BinaryRunner
from difference_analyzer import DifferenceAnalyzer
from param_editor import ParamEditor
from range_reader import RangeReader


def initialize_cli_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("elmtest_path", help="The path to elmtest.exe.",
                        type=str)
    parser.add_argument("range_path", help="The path to FUT_lake_range.txt.",
                        type=str)
    parser.add_argument("params_path", help="The path to lakeparams.txt.",
                        type=str)
    parser.add_argument("-r", "--reference_path", help="The path to the reference output file.",
                        type=str, default="cpu_LakeTemperatureRef.txt")
    parser.add_argument("-t", "--test_path", help="The path to the test output file.",
                        type=str, default="cpu_LakeTemperatureTest.txt")

    return parser.parse_args()


def main():
    args = initialize_cli_arguments()

    script_directory = os.path.dirname(__file__)

    runner = BinaryRunner(os.path.join(script_directory, args.elmtest_path))
    runner.run()

    range_reader = RangeReader(os.path.join(script_directory, args.range_path))
    print(range_reader.read_ranges())

    param_editor = ParamEditor(os.path.join(script_directory, args.params_path))
    param_editor.modify_parameter("betavis", 0.5)

    difference_analyzer = DifferenceAnalyzer(
        os.path.join(script_directory, args.reference_path),
        os.path.join(script_directory, args.test_path)
    )

    print(difference_analyzer.compare_outputs())


if __name__ == "__main__":
    main()

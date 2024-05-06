import argparse

from binary_runner import BinaryRunner
from range_reader import RangeReader


def initialize_cli_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("elmtest_path", help="The path to elmtest.exe.", type=str)
    parser.add_argument("range_path", help="The path to FUT_lake_range.txt.", type=str)

    return parser.parse_args()


def main():
    args = initialize_cli_arguments()

    runner = BinaryRunner(args.elmtest_path)
    runner.run()

    range_reader = RangeReader(args.range_path)
    print(range_reader.read_ranges())


if __name__ == "__main__":
    main()

import argparse

from binary_runner import BinaryRunner


def initialize_cli_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("elmtest_path", help="The path to elmtest.exe.", type=str)
    return parser.parse_args()


def main():
    args = initialize_cli_arguments()
    runner = BinaryRunner(args.elmtest_path)
    runner.run()


if __name__ == "__main__":
    main()

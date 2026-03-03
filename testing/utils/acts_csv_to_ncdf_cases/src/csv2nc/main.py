from argparse import ArgumentParser
from collections import namedtuple
from pathlib import Path

from csv2nc.cases import Cases
from csv2nc.partition import Partition
from csv2nc.writer import Writer


Paths = namedtuple("Paths", ["acts_csv", "partition_file", "cases_output"])


def read_paths() -> Paths:
    parser = ArgumentParser(
        prog="csv2nc",
        description="Converts Acts CSV index files into NetCDF cases",
    )

    parser.add_argument("acts_csv")
    parser.add_argument("partition_file")
    parser.add_argument("cases_output")

    args = parser.parse_args()

    return Paths(
        Path(args.acts_csv),
        Path(args.partition_file),
        Path(args.cases_output),
    )


def main() -> None:
    paths = read_paths()

    cases = Cases(paths.acts_csv)
    partition = Partition(paths.partition_file)

    with Writer(paths.cases_output) as writer:
        for var in cases.get_variable_names():
            var_dimensions = partition.get_dimension(var)
            var_type = partition.get_value(var, 0).dtype
            writer.initialize_variable(var, var_dimensions, var_type)

        for case in cases:
            case_values = {
                name: partition.get_value(name, index) for name, index in case.items()
            }
            writer.write_case(case_values)
        


if __name__ == "__main__":
    main()

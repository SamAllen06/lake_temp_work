from argparse import ArgumentParser, Namespace
from pathlib import Path
import sys

from netCDF4 import Dataset
import numpy as np


def main() -> None:
    args = _parse_args()

    dataset_path = Path(args.dataset)
    if not dataset_path.is_file():
        print(f"Unable to find dataset {dataset_path}", file=sys.stderr)
        sys.exit(1)

    with Dataset(dataset_path, "r", format="NETCDF4") as dataset:
        input_data = _get_input_data(dataset, args.input)
        output_data = _get_output_data(dataset, args.output, args.output_index)

        print("In: " + str(input_data))
        print("Out: " + str(output_data))


def _parse_args() -> Namespace:
    parser = ArgumentParser(description="Creates graphs for data from NetCDF files")
    parser.add_argument("dataset")
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("output_index", type=int)

    return parser.parse_args()


def _get_input_data(dataset: Dataset, input: str) -> np.array:
    if input not in dataset.variables:
        print(f"Unable to find input {input} in dataset", file=sys.stderr)
        sys.exit(1)

    return dataset.variables[input]

def _get_output_data(dataset: Dataset, output: str, index: int) -> np.array:
    if output not in dataset.variables:
        print(f"Unable to find output {output} in dataset", file=sys.stderr)
        sys.exit(1)

    return dataset.variables[output][:, :, index]


if __name__ == "__main__":
    main()

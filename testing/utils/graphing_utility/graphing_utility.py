from argparse import ArgumentParser, Namespace
from pathlib import Path
import sys

from netCDF4 import Dataset
import numpy as np
from matplotlib import pyplot


def main() -> None:
    args = _parse_args()

    dataset_path = Path(args.dataset)
    if not dataset_path.is_file():
        print(f"Unable to find dataset {dataset_path}", file=sys.stderr)
        sys.exit(1)

    with Dataset(dataset_path, "r", format="NETCDF4") as dataset:
        input_data = _get_input_data(dataset, args.input)
        output_data = _get_output_data(dataset, args.input, args.output, args.output_index)

    _plot_data(input_data, output_data)


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

    return dataset.variables[input][:]

def _get_output_data(dataset: Dataset, input:str, output: str, index: int) -> np.array:
    if output not in dataset.variables:
        print(f"Unable to find output {output} in dataset", file=sys.stderr)
        sys.exit(1)

    input_index = dataset.variables[output].dimensions.index(input)
    output_slice_list = [0] * len(dataset.variables[output].dimensions)
    output_slice_list[input_index] = slice(None)
    output_slice_list[-1] = index
    output_slice = tuple(output_slice_list)

    return dataset.variables[output][output_slice]

def _plot_data(input_data: np.array, output_data: np.array) -> None:
    figure, axes = pyplot.subplots()
    axes.plot(input_data, output_data)
    axes.scatter(input_data, output_data)
    pyplot.show()

if __name__ == "__main__":
    main()

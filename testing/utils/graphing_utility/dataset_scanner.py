from argparse import ArgumentParser, Namespace
import math
from pathlib import Path
import sys

from netCDF4 import Dataset


def main() -> None:
    args = parse_args()
    results = find_indices(args.dataset, args.allow_constants)
    display_results(results)


def parse_args() -> Namespace:
    parser = ArgumentParser(
        description="Finds variable indices in a dataset that contains valid data"
    )
    parser.add_argument("dataset")
    parser.add_argument(
        "-c", "--allow-constants",
        action="store_true",
        help="allow finding indices that have constant values"
    )

    args = parser.parse_args()

    dataset_path = args.dataset
    if not Path(args.dataset).is_file():
        print(f"Dataset {dataset_path} does not exist", file=sys.stderr)
        sys.exit(1)

    return args


# Returns {var_name: list_of_indices, ...}
def find_indices(dataset: Path, allow_constants: bool) -> dict[str, list[int]]:
    results = {}

    with Dataset(dataset, "r", "NETCDF4") as dataset:
        for name, variable in dataset.variables.items():
            indices = []
            # Single dimension variables are inputs
            if not len(variable.shape) == 2:
                continue
            
            for index, val in enumerate(variable[0]):
                # In the old elmtest, 1e36 is a fill value representing a variable that
                # was not given a value, we can ignore them.
                if not math.isnan(val) and not val == 1e36:
                    if allow_constants or not variable[0][index] == variable[1][index]:
                        indices.append(index)

            if len(indices) > 0:
                results[name] = indices

    return results


def display_results(results: dict[str, list[int]]) -> None:
    for var_name, indices in results.items():
        print(f"{var_name}: {indices}")
        print("")


if __name__ == "__main__":
    main()


#with Dataset("test_datasets/star_samples/pudz.nc", "r", "NETCDF4") as dataset:
#    for name, var in dataset.variables.items():
#        print(name)
#        if name == "pudz":
#            continue
#        for index, val in enumerate(var[0]):
#            if not math.isnan(val) and not val == 1e36:
#                if not var[0][index] == var[1][index]:
#                    print(f"{index}: {val}")

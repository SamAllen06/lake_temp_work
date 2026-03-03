from pathlib import Path

from netCDF4 import Dataset
import numpy as np
import numpy.typing as npt


CASES_DIM = "cases"


class WriterSession:
    def __init__(self, dataset: Dataset):
        self._dataset = dataset
        self._case = 0
        self._initialize_dataset()

    def initialize_variable(
        self,
        name: str,
        dimensions: list[tuple[str, int]],
        type: np.dtype
    ) -> None:
        for dim_name, dim_size in dimensions:
            if dim_name in self._dataset.dimensions:
                continue

            self._dataset.createDimension(dim_name, dim_size)

        var_dimension_tuple = (name for name, _ in dimensions)
        self._dataset.createVariable(
            name,
            type,
            (CASES_DIM, *var_dimension_tuple),
            compression="zlib",
            complevel=2,
        )

    def write_case(self, values: dict[str, npt.NDArray]) -> None:
        for var_name, data in values.items():
            self._dataset.variables[var_name][self._case] = data

        self._case += 1

    def _initialize_dataset(self) -> None:
        self._dataset.createDimension(CASES_DIM, None)


class Writer:
    def __init__(self, path: Path):
        self._path = path
        self._dataset = None

    def __enter__(self) -> WriterSession:
        self._dataset = Dataset(self._path, "w", "NETCDF4")
        return WriterSession(self._dataset)

    def __exit__(self, *args) -> None:
        self._dataset.close()
        self._dataset = None

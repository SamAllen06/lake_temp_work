from pathlib import Path

from netCDF4 import Dataset
import numpy as np
import numpy.typing as npt


class Partition:
    def __init__(self, path: Path):
        self._read_file(path)

    def get_dimension(self, var_name: str) -> list[tuple[str, int]]:
        return list(zip(self._data[var_name][1], self._data[var_name][2]))

    def get_value(self, var_name: str, index: int) -> npt.NDArray:
        return np.array(self._data[var_name][0][index])

    def _read_file(self, path: Path) -> None:
        self._data = {}
        with Dataset(path, "r", "NETCDF4") as ds:
            for var_name, var in ds.variables.items():
                self._data[var_name] = (
                    np.copy(var[:]),
                    var.dimensions[1:],
                    var.shape[1:]
                )

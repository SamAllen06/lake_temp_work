from netCDF4 import Dataset


def get_plottable_variables(dataset_path: str) -> list[str]:
    plottable_vars = []

    with Dataset(dataset_path, "r", "NETCDF4") as dataset:
        for var, data in dataset.variables.items():
            if len(data.shape) >= 2:
                plottable_vars.append(var)

    return plottable_vars


def get_dimensions(dataset_path: str, variable: str) -> list[str]:
    with Dataset(dataset_path, "r", "NETCDF4") as dataset:
        return list(dataset.variables[variable].dimensions)


def get_dimension_size(dataset_path: str, dimension: str) -> int:
    with Dataset(dataset_path, "r", "NETCDF4") as dataset:
        return len(dataset.dimensions[dimension])

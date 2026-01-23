import matplotlib.pyplot as plt
from netCDF4 import Dataset
import numpy as np
import numpy.typing as npt

from graph_data import AxisInfo, GraphData


def show_graph(data: GraphData, dataset: Dataset) -> None:
    _verify_graph_data_usable(data, dataset)
    var_data = _get_var_data(data, dataset)

    x_axis_values, x_axis_name = _get_axis_values(data.x_axis, dataset)
    y_axis_values, y_axis_name = _get_axis_values(data.y_axis, dataset)

    x_data, y_data = np.meshgrid(x_axis_values, y_axis_values)

    x_line_int = data.x_axis.dim_range.step
    y_line_int = data.y_axis.dim_range.step

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.plot_wireframe(x_data, y_data, var_data, rstride=x_line_int, cstride=y_line_int)

    plt.show()


def _verify_graph_data_usable(data: GraphData, dataset: Dataset) -> None:
    if data.var_name not in dataset.variables:
        raise ValueError(f"Variable {data.var_name} not in dataset")
    if data.x_axis.dim_name not in dataset.variables[data.var_name].dimensions:
        raise ValueError(f"X Axis dimension {data.x_axis.dim_name} not in dataset")
    if data.y_axis.dim_name not in dataset.variables[data.var_name].dimensions:
        raise ValueError(f"Y Axis dimension {data.x_axis.dim_name} not in dataset")

    for fixed_dim in data.fixed_dims:
        if fixed_dim.name not in dataset.variables[data.var_name].dimensions:
            raise ValueError(f"Fixed dimension {fixed_dim.name} not in dataset")


def _get_var_data(data: GraphData, dataset: Dataset) -> npt.NDArray:
    variable = dataset.variables[data.var_name]

    slices = {}

    slices[data.x_axis.dim_name] = slice(
        data.x_axis.dim_range.start,
        data.x_axis.dim_range.stop
    )
    slices[data.y_axis.dim_name] = slice(
        data.y_axis.dim_range.start,
        data.y_axis.dim_range.stop
    )

    for fixed_dim in data.fixed_dims:
        slices[fixed_dim.name] = fixed_dim.value

    dimension_order = variable.dimensions

    full_slice = []
    transpose_flag = False
    for name in dimension_order:
        full_slice.append(slices[name])

        # Transpose if the x axis follows the y axis
        if name == data.x_axis.dim_name:
            transpose_flag = False
        elif name == data.y_axis.dim_name:
            transpose_flag = True

    array = variable[tuple(full_slice)]
    if transpose_flag:
        return array.T
    
    return array


# Returns (data, display_name)
def _get_axis_values(axis: AxisInfo, dataset: Dataset) -> tuple[npt.NDArray, str]:
    axis_slice = slice(axis.dim_range.start, axis.dim_range.stop)

    if axis.mapped_var_name:
        mapped_var = dataset.variables[axis.mapped_var_name]
        name = f"{axis.mapped_var_name}({axis.dim_name})"
        return mapped_var[axis_slice], name

    return np.arange(axis_slice.start, axis_slice.stop), axis.dim_name

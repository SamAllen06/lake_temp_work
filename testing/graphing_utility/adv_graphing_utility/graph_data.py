from dataclasses import dataclass

import numpy.typing as npt


@dataclass
class AxisInfo:
    dim_name: str
    dim_range: range
    mapped_var_name: str | None = None


@dataclass
class FixedDimension:
    name: str
    value: npt.NDArray


@dataclass
class GraphData:
    var_name: str
    x_axis: AxisInfo
    y_axis: AxisInfo
    fixed_dims: list[FixedDimension]

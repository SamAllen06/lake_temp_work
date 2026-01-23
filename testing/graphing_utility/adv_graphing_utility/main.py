from netCDF4 import Dataset
import numpy as np

import graphing
from graph_data import AxisInfo, FixedDimension, GraphData
from view import View


def main() -> None:
    #view = View()

    # Select the dimensions you want to use for the x and y axis, as well as their
    # ranges. (min, max (exclusive), step). step controls where the grid lines are
    # drawn.
    x = AxisInfo("sample_index", range(0, 11, 1), "betavis")
    y = AxisInfo("time", range(0, 36, 3))

    # Create a list of the dimensions that you aren't using for the axes. You will need
    # to set a value for each.
    fixed = [FixedDimension("column", np.array(336))]
    ds = Dataset(
        # Put your dataset path here.
        "something.nc",
        "r",
        "NETCDF4"
    )
   
    # Put the variable you want to plot here.
    dat = GraphData("lakestate_vars__betaprime_col", x, y, fixed)

    graphing.show_graph(dat, ds)


if __name__ == "__main__":
    main()

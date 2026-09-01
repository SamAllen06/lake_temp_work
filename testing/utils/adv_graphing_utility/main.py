from netCDF4 import Dataset
import numpy as np

from collections import namedtuple
import graphing as graphing
from graph_data import AxisInfo, FixedDimension, GraphData
import dataset_operations as ds_op
from pathlib import Path
import argparse

dim_index_dict = {
    'sample_index': 0,
    'time': 1,
    'layer': -2,
    'subgrid_level': -1
}


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def is_index_assignment_valid(
    arg,
    upper_bound,
) -> bool:
    if -1 not in arg:
        for index in arg:
            if index >= upper_bound or index < 0:
                return False
    return True


def is_dim_assignment_valid(
    length,
    dim,
    layer_str
) -> bool:
    if length == 4:
        return True
    else:
        return dim != layer_str


def read_path() -> list:
    axis_options = ['time', 'sample_index', 'subgrid_level', 'layer']

    Paths = namedtuple("Paths", ["netcdf4_output", "change_detection_outputs", "graphing_output_dir"])
    Dim_Args = namedtuple("Dim_Args", ["x_axis", "y_axis", "fixed_1", "fixed_2"])
    Indexing_Args = namedtuple("Indexing_Args", ["indices_1", "indices_2"])
    Perspective_Args = namedtuple("Perspective_Args", ["elevation", "azimuth", "roll"])
    Misc_Args = namedtuple("Misc_Args", ["output_vars", "preview", "confirm"])


    parser = argparse.ArgumentParser(prog="adv_graphing_utility", description="Visualizes the effects of model constants on model outputs using 3D graphs", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('netcdf4_output', help='the path to the NetCDF file produced by the NetCDF4 Output Analysis Plugin')
    parser.add_argument('change_detection_outputs', help='the path to the "outputs.txt" file produced by the Change Detection Analysis Plugin')
    parser.add_argument('graphing_output_dir', help='the directory in which to save all graphing output')

    dimensions = parser.add_argument_group(title='dimension arguments', description='optional arguments for assigning dimensions to the x- and y-axes and which to hold fixed')
    dimensions.add_argument('-x', '--x_axis', type=str, choices=axis_options, help='which dimension to map to the x-axis', default=axis_options[0])
    dimensions.add_argument('-y', '--y_axis', type=str, choices=axis_options, help='which dimension to map to the y-axis', default=axis_options[1])
    dimensions.add_argument('-f', '--fixed_1', type=str, choices=axis_options, help='which dimension to use as the first fixed dimension', default=axis_options[2])
    dimensions.add_argument('-F', '--fixed_2', type=str, choices=axis_options, help='which dimenion to use as the second fixed dimension', default=axis_options[3])

    dim_indices = parser.add_argument_group(title='dimension indexing arguments', description='optional arguments for graphing only certain indices of the fixed dimensions (-1 graphs all indices)')
    dim_indices.add_argument('-i', '--indices_1', type=int, nargs='+', help='which index/indices to graph the first fixed dimension at', default=[-1])
    dim_indices.add_argument('-I', '--indices_2', type=int, nargs='+', help='which index/indices to graph the second fixed dimension at', default=[-1])

    perspective = parser.add_argument_group(title='perspective arguments', description='optional arguments for graphing from specific perspectives')
    perspective.add_argument("-e", '--elevation', type=int, nargs='+', help='elevation angle(s) from which to view each graph', default=[20])
    perspective.add_argument("-a", '--azimuth', type=int, nargs='+', help='azimuth angle(s) from which to view each graph', default=[30, 120, 210, 300])
    perspective.add_argument("-r", '--roll', type=int, nargs='+', help='roll angle(s) from which to view each graph', default=[0])

    misc = parser.add_argument_group(title='miscellaneous arguments', description='other optional arguments')
    misc.add_argument('-o', '--output_vars', type=str, nargs='+', help='which output variable(s)s to graph', default=['all_changed'])
    misc.add_argument('-p', '--preview', type=str2bool, nargs='?', const=True, help='preview each graph before saving it', default=False)
    misc.add_argument('-c', '--confirm', type=str2bool, nargs='?', const=True, help='calculate the number of graphs that will be produced and ask for user confirmation before saving them', default=True)

    args = parser.parse_args()

    # validate axis arguments
    dims = [args.x_axis, args.y_axis, args.fixed_1, args.fixed_2]
    dim_names = ['x_axis', 'y_axis', 'fixed_1', 'fixed_2']
    i=0
    while i<4:
        j=i+1
        while j<4:
            if dims[i] == dims[j]:
                parser.error(f'{dim_names[i]} and {dim_names[j]} cannot be assigned the same dimension ({dims[i]})')
            j+=1
        i+=1

    with Dataset(Path(args.netcdf4_output), "r", "NETCDF4") as dataset:
        dim_string_dict = {args.x_axis: 'X axis', args.y_axis: 'Y axis', args.fixed_1: 'first fixed dimension'}
        # validate output var arguments
        for arg_var in args.output_vars:
            if arg_var != 'all_changed':
                valid = False
                for var in dataset.variables:
                    if arg_var == var and dataset[var].variable_type == 'output':
                        valid = True
                if not valid:
                    parser.error(f'{arg_var} is not a valid output variable')
                # validate axis assignments
                shape = dataset[arg_var].shape
                for key, value in dim_string_dict.items():
                    if not is_dim_assignment_valid(len(shape), key, axis_options[3]):
                        parser.error(f'layer assigned to {value} for output variable ({arg_var}) with no layer dimension')
                # validate index assignments
                upper_bound = dataset[arg_var].shape[dim_index_dict[args.fixed_1]]
                if not is_index_assignment_valid(args.indices_1, upper_bound):
                    parser.error(f'index assigned to fixed_1 ({args.fixed_1}) outside the boundaries for that dimension (0-{upper_bound})')
                if len(dataset[arg_var].shape) == 4:
                    if not is_index_assignment_valid(args.indices_2, upper_bound):
                        parser.error(f'index assigned to fixed_1 ({args.fixed_2}) outside the boundaries for that dimension (0-{upper_bound})')
        if 'all_changed' in args.output_vars:
            #validate axis assignments
            with open(Path(args.change_detection_outputs), "r") as file:
                changed_output_vars = file.read().splitlines()
            for changed_var in changed_output_vars:
                shape = dataset[changed_var].shape
                for key, value in dim_string_dict.items():
                    if not is_dim_assignment_valid(len(shape), key, axis_options[3]):
                        parser.error(f'layer assigned to {value} for output variable ({changed_var}) with no layer dimension')
            #validate index assignments
                upper_bound = dataset[changed_var].shape[dim_index_dict[args.fixed_1]]
                if not is_index_assignment_valid(args.indices_1, upper_bound):
                    parser.error(f'index assigned to fixed_1 ({args.fixed_1}) outside the boundaries for that dimension (0-{upper_bound})')
                if len(dataset[changed_var].shape) == 4:
                    if not is_index_assignment_valid(args.indices_2, upper_bound):
                        parser.error(f'index assigned to fixed_1 ({args.fixed_2}) outside the boundaries for that dimension (0-{upper_bound})')

    return [Paths(
        Path(args.netcdf4_output),
        Path(args.change_detection_outputs),
        Path(args.graphing_output_dir)
    ), Dim_Args(
        str(args.x_axis),
        str(args.y_axis),
        str(args.fixed_1),
        str(args.fixed_2)
    ), Indexing_Args(
        list(args.indices_1),
        list(args.indices_2)
    ), Perspective_Args(
        list(args.elevation),
        list(args.azimuth),
        list(args.roll)
    ), Misc_Args(
        list(args.output_vars),
        bool(args.preview),
        bool(args.confirm)
    )]


def convert_size(size) -> tuple[float, str]:
    if size >= 1:
        size_unit = "Gigabytes"
    elif size >= 1E-3:
        size *= 1E3
        size_unit = "Megabytes"
    elif size >= 1E-6:
        size *= 1E6
        size_unit = "Kilobytes"
    else:
        size *= 1E9
        size_unit = "Bytes"
    return size, size_unit


def convert_time(time) -> tuple[float, str]:
    if time >= 60:
        time /= 60
        time_unit = "minutes"
    else:
        time_unit = "seconds"
    return time, time_unit


def is_user_confirmed(
    path, 
    indexing_args, 
    perspective_args,
    output_vars,
    dim_args
):
    graph_num = 0
    with Dataset(path, 'r', 'NETCDF4') as ds:
        for output_var in output_vars:
            var_graph_num = len(perspective_args.elevation)*len(perspective_args.azimuth)*len(perspective_args.roll)
            if -1 in indexing_args.indices_1:
                var_graph_num *= ds[output_var].shape[dim_index_dict[dim_args.fixed_1]]
            else:
                var_graph_num *= len(indexing_args.indices_1)
            if len(ds[output_var].shape) == 4:
                if -1 in indexing_args.indices_2:
                    var_graph_num *= ds[output_var].shape[dim_index_dict[dim_args.fixed_2]]
                else:
                    var_graph_num *= len(indexing_args.indices_2)
            graph_num += var_graph_num
    size, size_unit = convert_size(81.2*graph_num*0.000001)
    time, time_unit = convert_time(0.08783483877*graph_num)
    confirmation = input("Your current presets will save %i graphs. This will be an estimated %.2f %s and take approximately %.2f %s. If you would like to continue, enter y or yes: " % (graph_num, size, size_unit, time, time_unit))
    if confirmation == 'y' or confirmation == 'yes':
        return True
    else:
        return False


def main() -> None:
    paths, dim_args, indexing_args, perspective_args, misc_args = read_path()

    if not paths.graphing_output_dir.exists():
        paths.graphing_output_dir.mkdir(parents=True)

    if 'all_changed' in misc_args.output_vars:
        with open(Path(paths.change_detection_outputs), "r") as file:
            output_vars = file.read().splitlines()
        output_vars = set(output_vars + misc_args.output_vars)
        output_vars.remove('all_changed')
    else:
        output_vars = misc_args.output_vars

    changed_model_consts = ds_op.get_changed_model_consts(paths.netcdf4_output)

    if misc_args.confirm:
        # import pdb; pdb.set_trace()
        do_graphing_loop = False
        if misc_args.confirm:
            do_graphing_loop = is_user_confirmed(paths.netcdf4_output, indexing_args, perspective_args, output_vars, dim_args)
    else:
        do_graphing_loop = True

    if do_graphing_loop:
        with Dataset(paths.netcdf4_output, 'r', 'NETCDF4') as ds:
            for output_var in output_vars:
                dim_name_dict = {
                    'sample_index': changed_model_consts,
                    'time': f"{ds['dtime_mod'][0]} s/timestep" if 'dtime_mod' not in changed_model_consts.keys() else "{value of dtime_mod} s/timestep",
                    'layer': ds[output_var].dimensions[-2] if len(ds[output_var].dimensions)==4 else None,
                    'subgrid_level': ds[output_var].dimensions[-1]
                }
                x_name = dim_name_dict[dim_args.x_axis]
                y_name = dim_name_dict[dim_args.y_axis]
                fixed_1_name = dim_name_dict[dim_args.fixed_1]
                fixed_2_name = dim_name_dict[dim_args.fixed_2]

                x_dat = AxisInfo(dim_args.x_axis, range(0, ds[output_var].shape[dim_index_dict[dim_args.x_axis]]), x_name)
                y_dat = AxisInfo(dim_args.y_axis, range(0, ds[output_var].shape[dim_index_dict[dim_args.y_axis]]), y_name)

                # create lists of indices to use for fixed dims. If shape != 4, there's no layer dim so use None for indices_2
                if -1 in indexing_args.indices_1:
                    indices_1 = range(0, ds[output_var].shape[dim_index_dict[dim_args.fixed_1]])
                else:
                    indices_1 = indexing_args.indices_1
                if len(ds[output_var].shape) == 4:
                    if -1 in indexing_args.indices_2:
                        indices_2 = range(0, ds[output_var].shape[dim_index_dict[dim_args.fixed_2]])
                    else:
                        indices_2 = indexing_args.indices_2
                else:
                    indices_2 = None

                for index_1 in indices_1:
                    fixed_dat1 = FixedDimension(dim_args.fixed_1, np.array(index_1), fixed_1_name)
                    for elevation in perspective_args.elevation:
                        for azimuth in perspective_args.azimuth:
                            for roll in perspective_args.roll:
                                
                                # graph all the model constants and fixed dims for each output var
                                if indices_2 is None:
                                    dat = GraphData(output_var, x_dat, y_dat, [fixed_dat1])
                                    dir_path = paths.graphing_output_dir.joinpath(dat.var_name, fixed_dat1.mapped_dim_name+' '+str(fixed_dat1.value))
                                    graphing.graph(dir_path, ds, dat, elevation, azimuth, roll, misc_args.preview)
                                else:
                                    for index_2 in indices_2:
                                        fixed_dat2 = FixedDimension(dim_args.fixed_2, np.array(index_2), fixed_2_name)
                                        dat = GraphData(output_var, x_dat, y_dat, [fixed_dat1, fixed_dat2])
                                        dir_path = paths.graphing_output_dir.joinpath(dat.var_name, fixed_dat1.mapped_dim_name+' '+str(fixed_dat1.value), fixed_dat2.mapped_dim_name+' '+str(fixed_dat2.value))
                                        graphing.graph(dir_path, ds, dat, elevation, azimuth, roll, misc_args.preview)    


if __name__ == "__main__":
    main()

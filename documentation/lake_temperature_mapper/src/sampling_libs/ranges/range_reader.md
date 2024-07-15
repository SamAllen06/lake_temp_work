# Range Reader (APP/src/sampling_libs/range_interpolation/range_reader.py)

## Purpose
Range Reader accepts a path to a range input file and parses it.

## Functionality
Range Reader reads a file in this format:
```
parameter
min - max
```

After reading the file, the minimum and maximum of a specified input parameter
can be obtained using the get_min and get_max methods.

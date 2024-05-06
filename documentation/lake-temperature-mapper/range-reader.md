# Range Reader (range_reader.py)

## Purpose
Range Reader accepts a path to a range input file and parses it.

## Functionality
Range Reader reads a file in this format:
```
parameter
min - max
```

It returns a dictionary linking the parameter to its minimum and maximum, paired
in a tuple.

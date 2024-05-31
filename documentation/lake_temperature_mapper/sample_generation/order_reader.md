# Order Reader (order_reader.py)

## Purpose
Reads in orders from a specified order directory. Orders provide instructions
for how to sample an input parameter.

## Functionality
Reads order files (JSON) in the specified directory. Order files use one of the
following formats:

Line Order:
```
{
  "samples": # of samples,
  "ranges": {
    "param1":["start_value", "end_value"]
    "param2":["start_value", "end_value"]
    ...
    "paramN":["start_value", "end_value"]
  }
}
```

Box Order:
```
{
  "ranges": {
    "param1":["start_value", "end_value", sample_count]
    "param2":["start_value", "end_value", sample_count]
    ...
    "paramN":["start_value", "end_value", sample_count]
  }
}
```

This data is then given to OrderFactory to create an Order. The resulting order
is stored in a dictionary, with the filename (minus the .json extension) as its
key.

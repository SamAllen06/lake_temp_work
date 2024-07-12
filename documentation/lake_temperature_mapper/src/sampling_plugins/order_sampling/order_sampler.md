# Order Sampler (order_sampler.py)

## Purpose
Reads order files from the directories specified in the order_sampler config
file to create orders. These order files specify instructions for their samples
should be generated. These orders are named using the names of the files that
generated them, and returned in the get_sample_groups method.

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
key. Order is a subclass of SampleGroup, and can therefore be iterated across to
access its samples.

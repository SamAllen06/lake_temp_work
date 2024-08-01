# Order Sampler
APP/src/sampling_plugins/order_sampling/order_sampler.py

## Purpose
Subclass of [Sampler](../../sampling/sampler.md) that reads order files from
the directories specified in [its config file](../../../config/sampling_plugins/order_sampling.md)
to create orders. These order files specify instructions for linearly
interpolating over an upper and lower bound for each parameter. Each
[Order](order.md) is named after the file that it was created from.

## Functionality
Reads order files (JSON) in the specified directory. Order files use one of the
following formats:

Line Order:
```
{
  "samples": total_sample_count,
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
    "param1":["start_value", "end_value", axis_sample_count]
    "param2":["start_value", "end_value", axis_sample_count]
    ...
    "paramN":["start_value", "end_value", axis_sample_count]
  }
}
```

This data is then given to [OrderFactory](order_factory.md) to create an Order.
The resulting [Order](order.md) is stored in a dictionary, with the filename
(minus the .json extension) as its key.
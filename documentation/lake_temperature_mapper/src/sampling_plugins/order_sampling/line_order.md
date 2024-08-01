# Line Order
APP/src/sampling_plugins/order_sampling/line_order.py

## Purpose
A subclass of [Order](order.md) representing a sequence of samples evenly
spaced along a line in the input space.

## Functionality
Contains the starting sample, ending sample, and the total number of samples.
Linearly interpolates between the starting an ending sample, generating the 
total number of samples specified. Ex:

JSON:
```
{
  "samples": 5,
  "ranges":{
    "param1": ["0.0", "2.0"]
    "param2": ["1.0", "5.0"]
  }
}
```

Samples:
| sample_index | param1 | param2 |
|--------------|--------|--------|
| 0            | 0.0    | 1.0    |
| 1            | 0.5    | 2.0    |
| 2            | 1.0    | 3.0    |
| 3            | 1.5    | 4.0    |
| 4            | 2.0    | 5.0    |
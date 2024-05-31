# Box Order (box_order.py)

## Purpose
Represents a sequence of samples in the form of a box, evenly spaced along each
individual axis, but not necessarily from each other.

## Functionality
Contains the starting vertex, the ending vertex, and the number of samples to 
take for each input parameter (axis). The total number of samples in this order
is not stored, but can be calculated by multiplying each axis' sample count
together. The exponential relationship between number of parameters being
changed and the number of samples should be considered when writing box samples.
As an example, 5 samples across 5 axes each results in 3125 samples. Ex:

JSON:
```
{
  "ranges":{
    "param1": ["0.0", "2.0", 3]
    "param2": ["1.0", "4.0", 4]
  }
}
```

Samples:
| sample_index | param1 | param2 |
|--------------|--------|--------|
| 0            | 0.0    | 1.0    |
| 1            | 1.0    | 1.0    |
| 2            | 2.0    | 1.0    |
| 3            | 0.0    | 2.0    |
| 4            | 1.0    | 2.0    |
| 5            | 2.0    | 2.0    |
| 6            | 0.0    | 3.0    |
| 7            | 1.0    | 3.0    |
| 8            | 2.0    | 3.0    |
| 9            | 0.0    | 4.0    |
| 10           | 1.0    | 4.0    |
| 11           | 2.0    | 4.0    |

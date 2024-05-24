# Sampler (sampler.py)

## Purpose
Is an iterable class that generates sample values for each parameter in the 
order.

## Functionality
Takes in a list of ranges and a sample count. Generates a linear sequence of
values between the starting ranges and ending ranges. It is important to clarify
that this effectively represents a line segment in the multidimensional input
space, as opposed to a box. Samples generated take the form of a dictionary
mapping the input parameter name to its generated value.

While it currently only does linear interpolation, it will likely be extended
in the future to include other sampling methods.

Example:

```
param: "A"
from: 5.0
to: 7.0

param: "B"
from: 2.0
to: -2.0

samples: 5

[
  {"A": 5.0, "B": 2.0},
  {"A": 5.5, "B": 1.0},
  {"A": 6.0, "B": 0.0},
  {"A": 6.5, "B":-1.0},
  {"A": 7.0, "B":-2.0}
]
```

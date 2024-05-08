# Sampler (sampler.py)

## Purpose
Generates a list of values for an input parameter to pass to the binary being
tested.

## Functionality
Takes in a starting value (from), and an ending value (to), and a sample count.
Generates a list inclusively linear interpolating between the values. The size
of the list is equal to the sample count.

While it currently only does linear interpolation, it will likely be extended
in the future to include other sampling methods.

Example:

```
from: 5.0
to: 7.0
samples: 5

[5.0, 5.5, 6.0, 6.5, 7.0]
```

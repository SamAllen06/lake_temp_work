# Output Difference (output_difference.py)

## Purpose
Compares and stores a reference value and a test value for an output variable.

## Functionality
get_difference() returns the difference between the reference and test value.
The difference is calculated like so:

```
test_value - ref_value
```

It is possible for an OutputDifference object to store an identical reference
and test value, though typically these differences are not stored by the
program.

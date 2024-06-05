# Output Difference (output_difference.py)

## Purpose
Stores and compares a reference value and test value for an output variable.

## Functionality
get_difference() returns the difference between the reference and test value.
The difference is calculated like so:

```
test_value - ref_value
```

It is possible for an OutputDifference object to store an identical reference
and test value, though DifferenceAnalyzer will not store these. A reference
value of NaN and a test value of NaN are considered to have a difference of 0.

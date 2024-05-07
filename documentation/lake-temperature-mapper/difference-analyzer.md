# Difference Analyzer (difference_analyzer.py)

## Purpose
DifferenceAnalyzer compares a two output files and returns a map of differences
between the two.

## Functionality
Output files compared by DifferenceAnalyzer are in the format:

```
parameter1
    num1 num2 ... numN
parameter2
    num1 num2 ... numN
...
parameterN
    num1 num2 ... numN
```

Differences between a reference file (default: cpu_LakeTemperatureRef.txt) and
a test file (default: cpu_LakeTemperatureTest.txt). Differences are returned
as a map with parameter names as keys and a list of differences as values.
Differences are in this form:

```
(num_index, ref_num, test_num, test_num - ref_num)
```

For example, these files:

reference.txt
```
cool%var
    2.0 7.8
```

test.txt
```
cool%var
    3.0 7.8
```

Would result in this difference map:
```
{
    cool%var: [(0, 2.0, 3.0, 1.0)]
}
```

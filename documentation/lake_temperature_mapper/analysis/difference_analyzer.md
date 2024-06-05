# Difference Analyzer (difference_analyzer.py)

## Purpose
DifferenceAnalyzer compares two output files and returns a map of differences
between the two.

## Functionality
Output files are read using OutputFileData.

Differences between a reference file (default: cpu_LakeTemperatureRef.txt) and
a test file (default: cpu_LakeTemperatureDockerTest.txt) are computed and
stored using OutputDifference(s). Then, non-zero differences between output
variables are stored in a map like so:

```
{output_variable_name: [OutputDifference(index, ref, test), ...]}
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
    cool%var: [OutputDifference(0, 2.0, 3.0)]
}
```

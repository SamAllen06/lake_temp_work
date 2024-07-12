# Differences Plugin (APP/src/analysis_plugins/differences/)

The Differences analysis plugin subclasses [PerSampleAnalyzer](../analysis/per_sample_analyzer.md).
It is designed to find an identify any differences between the reference output
and the test output. For each output parameter with differences, it generates
a table with the following headers:

- reference
- - The value of the variable in the reference data
- test
- - The new value of the variable in the test data for this sample
- difference
- - The difference between the test and reference data (test - reference)
- index
- - The row-major index inside this output variable's data where this difference
occurred

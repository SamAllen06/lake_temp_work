# Differences Plugin (APP/src/analysis_plugins/differences/)

The Differences analysis plugin uses [PerSampleAnalyzer](../analysis/per_sample_analyzer.md)
and is designed to find and identify any differences between the reference output
and the test output. For each output parameter with differences, it generates
a table with the following headers:

| header     | value                                                                                     |
|------------|-------------------------------------------------------------------------------------------|
| reference  | The value of the variable in the reference data                                           |
| test       | The value of the variable in the test data (dependent on the sample)                      |
| difference | test - reference                                                                          |
| index      | The row-major index of where the differing value is found in the output variable's values |
# Fault Finding Plugin
APP/src/analysis_plugins/fault_finding/

The Fault Finding plugin is a [PerSampleAnalyzer](../analysis/per_sample_analyzer.md)
intended to be used to check for physically impossible values in the model
output. It will import python modules inside its `checks_directory` that have
file names starting or ending with "check", ignoring the .py extension. From
there, it will store all of the functions in each module that start with
"check". For each sample passed to it, it will automatically pass the sample
data to each of these checks, which can then make assertions about it to ensure
physical accuracy. It has a similar design to a unit test suite.

## Getting Sample Data in Checks
Check functions will request certain parts of the sample data using their 
argument names. The prefix "test_" will request the test data for an output and
the prefix "ref_" will request the reference data. "%" in variable names will
automatically be converted to "_" for checks. So, to request the test data
for a variable "testvar%sum", the argument name for the check would be
"test_testvar_sum".

Here is an example check:
```python
# utils is imported locally by the check in the same directory.
def check_passes(test_fakevar_sum: list[float]):
    assert utils.is_positive(test_fakevar_sum), (
        f"fakevar_sum expected to be positive, was {test_fakevar_sum}"
    )
```

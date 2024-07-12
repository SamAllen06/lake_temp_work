# Tester (APP/src/tester.py)

## Purpose
Tester ties together the entirety of the testing program. It is the only part of
the model that is directly called by the CLI.

## Functionality
Tester contains two public functions, prepare_for_testing and test_model.
A controller, currently just the CLI, is intended to call prepare_for_testing
immediately, allow the user to verify that the plugins they need have been
loaded and that the time estimated for testing is reasonable, and then call 
test_model.

### prepare_for_testing()
prepare_for_testing verifies that the binary can be found, loads both the
sampling and analysis plugins, gets all sampling groups from their respective
plugins, and makes an estimate for how long testing will take.

### test_model()
test_model runs through the testing loop:

- Iteratively tests each [SampleGroup](sampling/sample_group.md)
- - Resets the parameters file to its defaults
- - Iteratively tests each sample inside each group
- - - Sets the parameters file to the values specified by the sample
- - - Runs the binary
- - - Sends the resulting test data along with the reference data to the
[PerSampleAnalyzer(s)](sampling/per_sample_analyzer.md)
- - Sends the resulting test data for the entire group of samples to the
[SampleGroupAnalyzer(s)](sampling/sample_group_analyzer.md) as a 
[Table](util/table.md)

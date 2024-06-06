# Mapper (mapper.py)

## Purpose
Maps out how the outputs of a binary change as its inputs are changed.

## Functionality
Resets the parameters file to its defaults before each order using
DefaultsWriter.

Uses a Sampler to read in SampleGroup(s). Tests the samples in the SampleGroup,
following this cycle:

- Change the value of the specified parameters using ParamEditor to the values
returned by iterating through the SampleGroup.
- Run the binary using BinaryRunner.
- Compare the differences between the reference and test file using
DifferenceAnalyzer.

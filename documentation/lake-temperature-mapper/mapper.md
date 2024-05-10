# Mapper (mapper.py)

## Purpose
Maps out how the outputs of a binary change as its inputs are changed.

## Functionality
Uses OrderReader to read in orders stored in a directory specified by a config
file. Executes the order, following this cycle:

- Change the value of the specified parameter using ParamEditor to the value
returned by the Sampler.
- Run the binary using BinaryRunner.
- Compare the differences between the reference and test file using
DifferenceAnalyzer.

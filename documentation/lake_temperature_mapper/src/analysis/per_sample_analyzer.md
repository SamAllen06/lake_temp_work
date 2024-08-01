# Per Sample Analyzer 
APP/src/analysis/per_sample_analyzer.py

## Purpose
PerSampleAnalyzer is an abstract class that analysis plugins should extend if
they intend to analyze each sample individually. 

## Functionality
A subclass of PerSampleAnalyzer will receive the sample itself, the test data,
and the reference data.

The sample is passed as a dictionary mapping each input parameter's name to its
respective value. Similarly, the test and reference data are passed as a
dictionary mapping each output variable's name to its values. (Each variable
typically has a number of values, so these are passed as a list, in the order
they appear in the output file in row major order.)

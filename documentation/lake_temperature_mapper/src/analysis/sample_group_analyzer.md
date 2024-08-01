# Sample Group Analyzer 
APP/src/analysis/sample_group_analyzer.py

## Purpose
SampleGroupAnalyzer is an abstract class which should be extended by plugins
that intend to analyze the [SampleGroup](../sampling/sample_group.md) as a
whole.

## Functionality
A subclass of SampleGroupAnalyzer will receive the [SampleGroup](../sampling/sample_group.md)
itself as well as the test data, in the form of a [Table](../util/table.md).
The table uses the output variable names as keys and the fisrt layer of the
table is the reference data.

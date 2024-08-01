# Analyzer Loader 
APP/src/plugin_loading/analyzer_loader.py

## Purpose
AnalyzerLoader is a subclass of [PluginLoader](plugin_loader.md) which loads
analysis plugins. Each plugin must have an "analyzer_class" attribute, which
stores a class that extends either [PerSampleAnalyzer](../analysis/per_sample_analyzer.md)
or [SampleGroupAnalyzer](../analysis/sample_group_analyzer.md).

It also has functions to run both analysis on individual samples using the 
[PerSampleAnalyzer(s)](../analysis/per_sample_analyzer.md) and group analysis
on a full [SampleGroup](../sampling/sample_group.md) using 
[SampleGroupAnalyzer(s).](../analysis/sample_group_analyzer.md)

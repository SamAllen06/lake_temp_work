# Analysis
APP/src/analysis/

## Purpose
The analysis module serves as the interface between analysis plugins and the
testing program. It contains two abstract classes necessary to create an
analysis plugin. Each plugin must extend one of the two, depending on if the
plugin is intended to analyze each individual sample ([PerSampleAnalyzer](per_sample_analyzer.md))
or the group of samples as a whole ([SampleGroupAnalyzer](sample_group_analyzer.md)).

## Output
Each analysis plugin is responsible for its own output. Plugins should return
console output as well as file output, in the form of a [FileSystemTree.](../output/file_utils/file_system_tree.md)

# How to create an analysis plugin

## Plugin Root Module
Each analysis plugin is to be contained inside a single module in the
analysis_plugins directory (single as in, there are no other modules for that
plugin in the analysis_plugins directory, however the plugin's module can be
a package.) This module will be referred to as the "plugin root module"
throughout this document.

## Naming
The name of the plugin root module will be used to determine the display name
of the plugin. All underscores will be replaced with spaces, and all words will
be capitalized. Thus, a plugin inside a module "my_analysis_plugin" will have
the display name "My Analysis Plugin".

## analyzer_class Attribute
Each plugin must have a "analyzer_class" attribute containing a reference to
an Analyzer subclass in the plugin. An "Analyzer" subclass constitutes a
subclass of either the [PerSampleAnalyzer](../analysis/per_sample_analyzer.md)
abstract class or the [SampleGroupAnalyzer](../analysis/sample_group_analyzer.md)
abstract class inside of [analysis.](../analysis/analysis.md)

## Output
Each plugin will return a tuple containing both the console output and file output
of that plugin. Analysis plugins were given full control of these two views
because there isn't really a common format that analysis plugin output can be
forced into, as each plugin may want to display its results differently.
However, analysis plugins may import some modules from output to avoid writing
view logic if they have a common output format, such as a table.

# How to create an analysis plugin

## Plugin Root Module
Each analysis plugin is to be contained inside a single module in the
analysis_plugins directory (single as in, there are no other modules for that
plugin in the analysis_plugins directory, however the plugin's module can 
contain other modules.) This module will be referred to as the "plugin root
module" throughout this document.

## Naming
The name of the plugin root module will be used to determine the display name
of the plugin. All underscores will be replaced with spaces, and all words will
be capitalized. Thus, a plugin inside a module "my_analysis_plugin" will have
the display name "My Analysis Plugin".

## analyzer_class Attribute
Each plugin must have an "analyzer_class" attribute containing a reference to
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
view logic if they have a common output format, such as a table. (See 
[console_utils](../output/console_utils/console_utils.md) and
[file_utils](../output/file_utils/file_utils.md) for more details.)

## Example
Plugin Directory Structure (from APP/src/analysis_plugins/):
```
.
└── example_plugin
    ├── __init__.py
    └── example_analyzer.py
```

Contents of \_\_init__.py:
```python
from .example_analyzer import ExampleAnalyzer

analyzer_class = ExampleAnalyzer
```

Contents of example_analyzer.py:
```python
from io import StringIO

from analysis import SampleGroupAnalyzer
from output.file_utils import FileSystemTree
from sampling import SampleGroup
from util import Table


# Extending SampleGroupAnalyzer to analyze the entire sample group as a whole.
class ExampleAnalyzer(SampleGroupAnalyzer):
    _OUTPUT_LINE_FORMAT = "{parameter}: {value}"

    def analyze_sample_data(
        self, sample_group: SampleGroup, data: Table
    ) -> tuple[str, FileSystemTree]:
        # Define a variable to track the maximum values for each variable.
        max_values: dict[str, float] = {}

        # Use the mapping interface of Table.
        data_mapping = data.as_mapping()

        for input_parameter, group_values in data_mapping.items():
            # Initialize the maximum for an input parameter to its first value in the first sample.
            max_values[input_parameter] = group_values[0][0]
            for sample_values in group_values:
                for value in sample_values:
                    if value > max_values[input_parameter]:
                        # Update the maximum accordingly.
                        max_values[input_parameter] = value

        # Convert the output data into a console and file output.
        # Analysis plugins are responsible for this view code to enable greater flexibility in
        # how they present information.
        return (
            self._generate_text_output(max_values),
            self._generate_file_output(max_values),
        )

    def _generate_text_output(self, max_values: dict[str, float]) -> str:
        lines: list[str] = []

        for input_parameter, max_value in max_values.items():
            # Should format each line like so:
            # input_parameter: max_value
            lines.append(
                self._OUTPUT_LINE_FORMAT.format(
                    parameter=input_parameter, value=max_value
                )
            )

        # Insert new line characters between each line.
        return "\n".join(lines)

    def _generate_file_output(self, max_values: dict[str, float]) -> FileSystemTree:
        # Contents of the file will be the same as the console output, this is usually
        # not the case, but it makes this example simpler.
        file_contents = self._generate_text_output(max_values)

        # StringIO acts as a text file in memory, so it can be easily used by FileSystemTree
        # to generate an actual text file.
        file_io = StringIO()
        file_io.write(file_contents)

        return FileSystemTree.create_from_file(".txt", file_io)
```
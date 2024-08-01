# File 
APP/src/output/views/file.py

## Purpose
Produces file output for the testing program.

## Functionality
This view produces three different forms of file output: samples, errors, and
analysis. The location of these three types can be configured using 
[its config file.](../../../config/output/files.md)

### Samples Output
Sample output stores the values of the input parameters for all samples in each
[SampleGroup.](../../sampling/sample_group.md)

Each csv is named after the [SampleGroup](../../sampling/sample_group.md) that
generated the samples it stores. Example structure for the samples directory:

```
samples/
├── sample_group_1.csv
└── sample_group_2.csv
```

Here is an example file:

```
var1,var2,var3
0.0,1.0,2.0
1.0,2.0,3.0
2.0,3.0,4.0
3.0,4.0,5.0
4.0,5.0,6.0
```

### Errors Output
Error output records what samples caused the binary to crash.

Similarly to the samples output, each csv in this directory is named after the
[SampleGroup](../../sampling/sample_group.md) that contained one or more samples
resulting in a crash. (A crash is defined as any time the binary returns an
exit code other than 0.) If no samples in a group caused the binary to crash,
that group will not have a file in this directory. (By extension, if no samples
caused the binary to crash, this directory will be empty.)

Example directory structure:

```
errors/
├── sample_group_1.csv
└── sample_group_3.csv
```

Example file:

```
sample_index,exit_code
0,1
5,1
10,1
15,1
20,1
```

### Analysis Output
Analysis output records the output of analysis plugins. It is split into two 
directories: "group" and "sample". Output from plugins extending
[PerSampleAnalyzer](../../analysis/per_sample_analyzer.md) will go inside the
"sample" directory, and output from plugins extending
[SampleGroupAnalyzer](../../analysis/sample_group_analyzer.md) will go inside
the "group" directory.

Inside each directory, each [SampleGroup](../../sampling/sample_group.md) will
have a directory. In the "group" directory, each plugin's output will be stored
under that plugin's name. In the "sample" directory, each plugin's output is
stored in a directory named after that plugin, under the sample's index inside
the [SampleGroup.](../../sampling/sample_group.md)

Example directory structure (each plugin's output has a .txt extension for
visualization purposes - plugin output isn't limited to a single file or text
output):

```
analysis/
├── group
│   ├── sample_group_1
│   │   ├── plugin_3.txt
│   │   └── plugin_4.txt
│   └── sample_group_2
│       ├── plugin_3.txt
│       └── plugin_4.txt
└── sample
    ├── sample_group_1
    │   ├── plugin_1
    │   │   ├── 0.txt
    │   │   ├── 1.txt
    │   │   └── 2.txt
    │   └── plugin_2
    │       ├── 0.txt
    │       ├── 1.txt
    │       └── 2.txt
    └── sample_group_2
        ├── plugin_1
        │   ├── 0.txt
        │   ├── 1.txt
        │   └── 2.txt
        └── plugin_2
            ├── 0.txt
            ├── 1.txt
            └── 2.txt
```

Plugin output beyond this structure is determined by the analysis plugin
itself. Analysis plugins are required to generate a [FileSystemTree,](../file_utils/file_system_tree.md)
which is rooted at the location of the text files shown above.

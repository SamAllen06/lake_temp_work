# Command Line Interface (cli.py)

## Purpose
The CLI script acts as the interface between the user and our mapping scripts.
It is the sole entry point to the program, however, the mapping scripts are 
entirely independant of this script.
## Functionality
The CLI does not contain any functionality other than accepting command line 
input and executing mapping scripts accordingly.

Currently, it is responsible for creating a GroupOutputWriter, adding 
OutputWriter(s) depending on the flags.

## Flags

### Help (-h, --help)
Display information about the usage of the script and exit.

### Config Path (-c, --config_path)
Override the path to the testing module's configuration file.
(This functionality will be removed in a future update, since it is not useful
in context and the configuration system is being refactored to handle the more
modular structure of the mapping scripts.)

### Store (-s, --store)
Store the output of each SampleGroup in a csv file, inside the output
directory (typically mapping_output/).

### Quiet (-q, --quiet)
Prevents the script from printing any console output.

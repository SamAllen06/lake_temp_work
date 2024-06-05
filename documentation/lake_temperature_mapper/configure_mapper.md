# Configure Mapper (configure_mapper.py)

## Purpose
Generates a configuration file for a module. By default, it configures the
testing module. If the configuration specified for the user references another 
configurable module, it will temporarily switch to configuring that module if
it is not already configured. testing is the default, since it references the
other modules.

## Functionality
Creates a ConfigWriter for the module requested.

## Flags

### Help (-h, --help)
Displays information about the usage of the script, then exits.

### Module (-m, --module)
Accepts the name of a configurable module. Module name is relative to the
position of the script on the filesystem.

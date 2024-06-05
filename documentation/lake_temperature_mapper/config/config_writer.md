# Config Writer (config_writer.py)

## Purpose

Interactively and recursively configures a module.

## Functionality

Loads the config submodule from the module, and uses its FIELDS constant to 
determine the fields that should be written to the config file. The 
configuration file is stored at the file path specified by the config module's
FILE_PATH constant. Specifics of input validation and formatting are handled by
Field(s).

This class is initially instantiated by configure_mapper.py, but can be 
recursively instantiated on any unconfigured modules referenced in a class
field.

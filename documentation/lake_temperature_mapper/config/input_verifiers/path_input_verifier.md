# Path Input Verifier (path_input_verifier.py)

## Purpose
Serves as an InputVerifier for fields that accept a path.

## Functionality
Verifies input using rules set in the constructor. The programmer can specify
if the path must be to an existing object on the file system, and if that object
should be a file or a directory.

Formats input by converting it to a path relative to the project root
(lake_temperature_mapper/). By using relative paths like this, the configuration
file is independent of the computer it was created on (it is only dependent on
the structure of the project.)

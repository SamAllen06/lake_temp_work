# Root Paths (APP/src/root.py)

## Purpose
The root module stores a number of [pathlib.Path](https://docs.python.org/3.10/library/pathlib.html)
constants. Paths are used at multiple points in the program, however, letting
individual modules define the paths of the files they make use of would be 
unwise.

There are two types of paths: absolute and relative. Absolute paths are defined
in relation to the root directory of the system, which is "/" on Unix-like
systems. Relative paths, however, are defined in relation to some other path.
Commonly this path is the current working directory, but not always.

For this program, relative paths are the better option for a number of reasons.
The most important of which is that the program can run inside both a
developer's computer, as well as inside the docker image.
However, every relative path is defined relative to some absolute path, so the
question then becomes, which path are the various paths in this program
relative to?

A common answer would be either the current working directory or the file's
path. However, using the current working directory would cause the paths to
change dependent on where the program is run, which is certainly not ideal.
Using the file's location is a better option, but it would require that the
paths be changed every time a module is moved. Additionally, common directories
would have to be updated across many different modules, which is highly
inconvenient.

To prevent this issue, the root module is the only module to reference relative
paths in relation to its location on the filesystem. All other modules reference
relative paths in relation to root's constant paths.

## Constants

### APP_ROOT (APP/) (root.py/../..)
App root is the root of the project. All files accessed by the program are
descendants of this directory. As such, it is the only path defined relative to 
the location of the root.py file. The remaining constants in this module 
are all relative to this path, and it will be referred to as "APP" when defining
them in this document.

### CONFIG_ROOT (APP/config/)
Config root is the directory that contains all the configuration files used by
the testing program's modules. All .ini files are located in here.

### SOURCE_ROOT (APP/src/)
Source root contains the source code of the program. All .py files are located
here. This includes plugin code.

### SAMPLING_PLUGIN_CONFIG_DIRECTORY (APP/config/sampling_plugins/)
The sampling plugin config directory contains all configuration files used by
[sampling plugins.](sampling_plugins/sampling_plugins.md)

### ANALYSIS_PLUGIN_CONFIG_DIRECTORY (APP/config/analysis_plugins/)
The analysis plugin config directory, similarly to its sampling equivalent,
contains all configuration files used by [analysis plugins.](analysis_plugins/analysis_plugins.md)

### OUTPUT_CONFIG_DIRECTORY (APP/config/output/)
The output config directory contains all configuration files used by the
[views.](output/views/views.md)

OUTPUT_CONFIG_DIRECTORY = CONFIG_ROOT / "output"

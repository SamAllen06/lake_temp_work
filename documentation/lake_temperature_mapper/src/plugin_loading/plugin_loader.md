# Plugin Loader
APP/src/plugin_loading/plugin_loader.py

## Purpose
The PluginLoader abstract class includes functionality for loading in plugins.

## Functionality
PluginLoader searches for all submodules of a specified module, then checks for
a specific attribute on each module. If the attribute is present, it is assumed
to hold a class that extends a specified abstract class. From there, the class
is instantiated with a no-args constructor and sorted into a dictionary mapping
the class to a dictionary of plugin names, each mapped to their object.
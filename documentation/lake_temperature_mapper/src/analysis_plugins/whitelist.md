# Whitelist
APP/src/analysis_plugins/whitelist or APP/src/sampling_plugins/whitelist

## Purpose
Whitelist files are plain text files that list the names of plugins from the
current directory that should be loaded. They provide a way to allow 
researchers to store more plugins than they need at the current moment inside
the plugin directories.

## Functionality
Plugin names are listed as they appear in the file system. If a whitelist file
is not present in a plugins directory (sampling_plugins or analysis_plugins),
all plugins in that directory are assumed to be whitelisted and are loaded.

## Example
With this directory structure:
```
plugins/
├── plugin1
├── plugin2
├── plugin3
└── whitelist
```

And the whitelist contents:
```
plugin1
plugin3
```

Only plugin1 and plugin3 will be loaded by [PluginLoader.](../plugin_loading/plugin_loader.md)
With no whitelist file, plugin1, plugin2, and plugin3 will all be loaded.

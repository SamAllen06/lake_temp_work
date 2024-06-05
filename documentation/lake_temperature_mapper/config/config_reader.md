# Config Reader (config_reader.py)

## Purpose
Reads a module's config file.

## Functionality
Reads a config file in the following format:
```
key1: path1
key2: path2
...

```

Has a function, get_path_to(key), which will return the path to that key, as 
listed in the config file.

Also has get_class(key), which loads and returns the class specified by the 
configuration file.

In the future these methods may be moved to Field, allowing each type of Field 
to handle the interpretation of its value.

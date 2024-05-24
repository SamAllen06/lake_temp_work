# Config Reader (config_reader.py)

## Purpose
Reads a mapper config file.

## Functionality
Reads a config file in the following format:
```
key1: path1
key2: path2
...

```

Has a function, get_path_to(key), which will return the path to that key, as 
listed in the config file.

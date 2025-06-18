# ScopedImporter 
APP/src/util/scoped_importer.py

## Purpose
Can import modules relative to its `import_directory` without requiring a programmer to
handle the logic for adding and removing that path from `sys.path`.

## Functionality
ScopedImporter, when asked to import a module, will add its `import_directory` to
[sys.path](https://docs.python.org/3.10/library/sys.html?highlight=sys%20path#sys.path),
import the module, remove its `import_directory` from `sys.path`, then return the
module.

## Example

```
>>> from pathlib import Path
>>> from util.scoped_importer import ScopedImporter
>>> 
>>> # Cannot import, this module is in ../fault_checks/
>>> import sum_check
Traceback (most recent call last):
  File "<python-input-3>", line 1, in <module>
    import sum_check
ModuleNotFoundError: No module named 'sum_check'
>>> 
>>> module_path = Path("..") / "fault_checks"
>>> 
>>> importer = ScopedImporter(module_path)
>>> 
>>> module = importer.import_module("sum_check")
```

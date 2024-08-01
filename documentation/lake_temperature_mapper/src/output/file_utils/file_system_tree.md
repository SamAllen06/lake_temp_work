# File System Tree 
APP/src/output/file_utils/file_system_tree.py

## Purpose
A FileSystemTree object stores a tree of files and directories under an unnamed
root.

## Examples
The two common ways of creating a FileSystemTree are by using the class methods
create_from_file and create_from_files. For each example, "." will the parent
directory and "root" will be the name of the root node of the tree.

### Create a single file
```python
from io import StringIO
from pathlib import Path

from output.file_utils import FileSystemTree

empty_io = StringIO()
parent = Path.cwd()

tree = FileSystemTree.create_from_file(".txt", empty_io)


tree.write_to_filesystem(parent, "root")
```

Resulting tree:
```
.
└── root.txt
```

### Create multiple files
```python
from io import StringIO
from pathlib import Path

from output.file_utils import FileSystemTree

empty_io = StringIO()
parent = Path.cwd()

files = {
...     Path("a.csv"): empty_io,
...     Path("b") / "0.txt": empty_io,
...     Path("b") / "1.txt": empty_io,
... }
tree = FileSystemTree.create_from_files(files)

tree.write_to_filesystem(parent, "root")
```

Resulting tree:
```
.
└── root
    ├── a.csv
    └── b
        ├── 0.txt
        └── 1.txt
```

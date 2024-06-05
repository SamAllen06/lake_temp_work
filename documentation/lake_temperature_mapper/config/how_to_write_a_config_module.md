# How to write a config module

A config module must be a direct submodule of the module it configures, meaning
it can be loaded using `module.config`

It must contain two constants, FIELDS, and FILE_PATH.

FEILDS represents the fields stored in the config file, and is a list of
Field instances. FILE_PATH is a pathlib.Path to the configuration file. It is
recommended to make this relative to config.root.CONFIG_ROOT.

## Example

```
from config import Field
from config.input_verifiers import *
from config.root import CONFIG_ROOT

from some_module import SomeSuperClass


FILE_PATH = CONFIG_ROOT / "module_category" / "module_name.conf"

FIELDS = [
    Field(
        "some_string",
        "Enter some string (Ex: some string): ",
        NoCheckInputVerifier()
    ),
    Field(
        "some_file",
        "Enter the path to some file (Ex: some_file.txt): ",
        PathInputVerifier(True, True)
    ),
    Field(
        "some_class",
        "Enter the name of some class (Ex: some_module:SomeClass): ",
        ClassInputVerifier(SomeSuperClass)
    ),
]
```

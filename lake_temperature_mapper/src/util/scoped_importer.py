import importlib
from pathlib import Path
import sys
from types import ModuleType


class ScopedImporter:
    def __init__(self, import_directory: Path):
        self._import_directory = import_directory.resolve()

    def import_module(self, name: str) -> ModuleType:
        sys.path.insert(0, str(self._import_directory))
        module = importlib.import_module(name)
        sys.path.remove(str(self._import_directory))
        return module

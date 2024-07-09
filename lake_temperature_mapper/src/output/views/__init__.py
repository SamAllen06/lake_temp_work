from enum import Enum as _Enum

from output.views import console, file, logs


class View(_Enum):
    CONSOLE = console
    FILE = file
    LOGS = logs

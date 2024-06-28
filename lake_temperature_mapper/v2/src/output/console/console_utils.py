import re

from .ansi_code import AnsiCode

ERASE_CODE = "\033[2K\r"


def with_ansi(text: str, ansi_code: AnsiCode) -> str:
    return f"\033[{ansi_code.value}m{text}\033[0m"


def print_ansi(text: str, ansi_code: AnsiCode, **kwargs) -> None:
    print(with_ansi(text, ansi_code), **kwargs)


def clear_line() -> None:
    print(ERASE_CODE, end="")


def indented(text: str, indent_level: int) -> str:
    return re.sub(r"^", "\t" * indent_level, text, flags=re.M)


def print_indented(text: str, indent_level: int, **kwargs) -> None:
    print(indented(text, indent_level), **kwargs)

from enum import StrEnum

_CSI = "\033["

# See https://en.wikipedia.org/wiki/ANSI_escape_code


class AnsiCode(StrEnum):
    pass


class ParameterizedAnsiCode(StrEnum):
    def get_value(self, parameter: int) -> str:
        return self.value.format(parameter)


class AnsiColor(AnsiCode):
    BRIGHT_RED = _CSI + "91m"
    BRIGHT_GREEN = _CSI + "92m"
    BRIGHT_YELLOW = _CSI + "93m"
    BRIGHT_BLUE = _CSI + "94m"
    BRIGHT_MAGENTA = _CSI + "95m"
    BRIGHT_CYAN = _CSI + "96m"


class AnsiGraphic(AnsiCode):
    CLEAR = _CSI + "0m"
    UNDERLINE = _CSI + "4m"


class AnsiControl(ParameterizedAnsiCode):
    ERASE_IN_LINE = _CSI + "{0}K"


def with_ansi_graphic(text: str, code: AnsiGraphic | AnsiColor) -> str:
    return f"{code.value}{text}{AnsiGraphic.CLEAR.value}"


def print_ansi_graphic(text: str, code: AnsiGraphic | AnsiColor, **kwargs) -> None:
    print(with_ansi_graphic(text, code), **kwargs)


def with_ansi_color(text: str, code: AnsiColor) -> str:
    return with_ansi_graphic(text, code)


def print_ansi_color(text: str, code: AnsiColor, **kwargs) -> None:
    print_ansi_graphic(text, code, **kwargs)


def print_ansi_code(code: AnsiCode, **kwargs) -> None:
    print(code.value, **kwargs)


def print_parameterized_ansi_code(
        code: ParameterizedAnsiCode,
        parameter: int,
        **kwargs
) -> None:
    print(code.get_value(parameter), **kwargs)


def reset_line() -> None:
    print_parameterized_ansi_code(AnsiControl.ERASE_IN_LINE, 2, end="")
    print("\r", end="")

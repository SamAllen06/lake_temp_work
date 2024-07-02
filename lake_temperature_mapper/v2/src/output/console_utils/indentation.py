import re


def with_indentation(text: str, indent_level: int) -> str:
    return re.sub(r"^", "\t" * indent_level, text, flags=re.M)


def print_indented(text: str, indent_level: int, **kwargs) -> None:
    print(with_indentation(text, indent_level), **kwargs)

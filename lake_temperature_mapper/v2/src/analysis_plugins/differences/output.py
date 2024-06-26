from collections.abc import Mapping, Sequence
from io import StringIO
from pathlib import Path

from analysis.output.console import table_to_text
from analysis.output.file import table_to_csv, list_to_txt
from output import FileSystemTree
from output.console import AnsiCode, console_utils
from util import Table


OUTPUT_FILE_EXTENSION = ".csv"
NO_DIFFERENCES_LINE = console_utils.with_ansi("No differences", AnsiCode.BRIGHT_YELLOW)
NO_DIFFERENCES_FILEPATH = Path("unchanged_parameters.txt")


def generate_output(differences: Mapping[str, Table]) -> tuple[str, FileSystemTree]:
    console_output = _generate_console_output(differences)
    file_output = _generate_file_output(differences)

    return (
        console_output,
        file_output,
    )


def _generate_console_output(differences: Mapping[str, Table]) -> str:
    lines: list[str] = []
    no_differences_flag = True

    for parameter in differences:
        if differences[parameter].get_row_count() == 0:
            continue

        no_differences_flag = False
        parameter_header = console_utils.with_ansi(parameter, AnsiCode.BRIGHT_CYAN)
        lines.append(parameter_header)

        lines.append(table_to_text.convert_to_text(differences[parameter]))

    if no_differences_flag:
        lines.append(NO_DIFFERENCES_LINE)

    return "\n".join(lines)


def _generate_file_output(differences: Mapping[str, Table]) -> FileSystemTree:
    files: dict[Path, StringIO] = {}
    unchanged_parameters: list[str] = []

    for parameter in differences:
        if differences[parameter].get_row_count() == 0:
            unchanged_parameters.append(parameter)
            continue

        file_path = Path(parameter + OUTPUT_FILE_EXTENSION)
        files[file_path] = table_to_csv.convert_to_csv_data(differences[parameter])

    if unchanged_parameters:
            files[NO_DIFFERENCES_FILEPATH] = list_to_txt.convert_to_txt_data(
            unchanged_parameters
        )

    return FileSystemTree.create_from_files(files)






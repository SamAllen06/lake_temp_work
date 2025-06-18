from collections import namedtuple
from io import StringIO
from pathlib import Path
import traceback
from typing import cast

from output.console_utils import ansi
from output.file_utils import FileSystemTree, table_to_csv
from util import Table

from .check_status import CheckStatus

_STATUS_FILEPATH = Path("check_statuses.csv")
_FAILED_FILEPATH = Path("failed.csv")
_ERRORS_DIRECTORY = Path("errors")
_ERROR_FILENAME = "{check_name}.txt"


Summary = namedtuple("Summary", ["passed", "failed", "error"])


def generate_output(
    check_results: dict[str, tuple[CheckStatus, None | str | Exception]]
) -> tuple[str, FileSystemTree]:
    passed, failed, errored = _sort_by_status(check_results)

    console_output = _generate_console_output(passed, failed, errored)
    file_output = _generate_file_output(check_results, failed, errored)

    return (console_output, file_output)

def _sort_by_status(
        check_results: dict[str, tuple[CheckStatus, None | str | Exception]]
) -> tuple[
    set[str],
    dict[str, str],
    dict[str, Exception]
]:
    passed: set[str] = set()
    failed: dict[str, str] = {}
    errored: dict[str, Exception] = {}

    for check_name, (status, data) in check_results.items():
        match (status):
            case CheckStatus.PASSED:
                passed.add(check_name)
            case CheckStatus.FAILED:
                message = cast(str, data)
                failed[check_name] = message
            case CheckStatus.ERROR:
                error = cast(Exception, data)
                errored[check_name] = error

    return (passed, failed, errored)

def _generate_console_output(
        passed: set[str],
        failed: dict[str, str],
        errored: dict[str, Exception]
) -> str:
    if not failed and not errored:
        passed_count = len(passed)
        return ansi.with_ansi_color(
            f"All {passed_count} tests passed!",
            ansi.AnsiColor.BRIGHT_GREEN
        )

    lines: list[str] = []

    for check_name, message in failed.items():
        lines.append(ansi.with_ansi_color(
            f"[FAILED]: {check_name}",
            ansi.AnsiColor.BRIGHT_RED
        ))
        if message:
            lines.append(ansi.with_ansi_color(
                f"\t{message}",
                ansi.AnsiColor.BRIGHT_RED
            ))

    for check_name, error in errored.items():
        formatted_exception = "\t".join(traceback.format_exception(error))
        lines.append(ansi.with_ansi_color(
            f"[ERROR]: {check_name}\n"
            f"\t{formatted_exception}",
            ansi.AnsiColor.BRIGHT_RED
        ))

    lines.append(_generate_summary_line(passed, failed, errored))

    return "\n".join(lines)

def _generate_summary_line(
        passed: set[str],
        failed: dict[str, str],
        errored: dict[str, Exception]
) -> str:
    pass_count = len(passed)
    fail_count = len(failed)
    error_count = len(errored)

    line = (
        f"[Summary]: {pass_count} passed, {fail_count} failed, "
        f"and {error_count} errored"
    )

    return ansi.with_ansi_color(line, ansi.AnsiColor.BRIGHT_RED)

def _generate_file_output(
        check_results: dict[str, tuple[CheckStatus, None | str | Exception]],
        failed: dict[str, str],
        errored: dict[str, Exception]
) -> FileSystemTree:
    files: dict[Path, StringIO] = {}

    files |= _generate_status_file(check_results)
    if failed:
        files |= _generate_failed_file(failed)
    if errored:
        files |= _generate_error_files(errored)

    return FileSystemTree.create_from_files(files)

def _generate_status_file(
        check_results: dict[str, tuple[CheckStatus, None | str | Exception]]
) -> dict[Path, StringIO]:
    statuses_table: Table[dict[str, list[str]], list[str]] = Table({}, [])
    statuses_sequence = statuses_table.as_sequence()
    statuses_sequence.initialize_keys(["check", "status"])

    for check, result in check_results.items():
        status_name = result[0].name
        check_status_entry = {"check": check, "status": status_name}
        statuses_sequence.append(check_status_entry)

    status_file_contents = table_to_csv.convert_to_csv_data(statuses_table)
    return {_STATUS_FILEPATH: status_file_contents}

def _generate_failed_file(failed: dict[str, str]) -> dict[Path, StringIO]:
    failed_table: Table[dict[str, list[str]], list[str]] = Table({}, [])
    failed_sequence = failed_table.as_sequence()
    failed_sequence.initialize_keys(["check", "message"])

    for check, message in failed.items():
        failed_sequence.append({"check": check, "message": message})

    failed_file_contents = table_to_csv.convert_to_csv_data(failed_sequence)
    return {_FAILED_FILEPATH: failed_file_contents}

def _generate_error_files(errored: dict[str, Exception]) -> dict[Path, StringIO]:
    files: dict[Path, StringIO] = {}

    for check, error in errored.items():
        filepath = _ERRORS_DIRECTORY / _ERROR_FILENAME.format(check_name=check)
        file_contents = StringIO()

        formatted_exception = "".join(traceback.format_exception(error))
        file_contents.write(formatted_exception)

        files[filepath] = file_contents

    return files

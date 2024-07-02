from configparser import ConfigParser
import csv
from pathlib import Path
import shutil

from output.events import Event
from output.file_utils import FileSystemTree
from root import APP_ROOT, OUTPUT_CONFIG_DIRECTORY

CONFIG_FILE = OUTPUT_CONFIG_DIRECTORY / "files.ini"

CONFIG = ConfigParser()
CONFIG.read(CONFIG_FILE)

SAMPLES_DIRECTORY = APP_ROOT / CONFIG["Directories"]["samples"]
ERRORS_DIRECTORY = APP_ROOT / CONFIG["Directories"]["errors"]
SAMPLE_ANALYSIS_DIRECTORY = APP_ROOT / CONFIG["Directories"]["analysis"] / "sample"
GROUP_ANALYSIS_DIRECTORY = APP_ROOT / CONFIG["Directories"]["analysis"] / "group"

BINARY_EXIT_FILE_HEADERS = ("sample_index", "exit_code")

_parameter_order: list[str] = []

_current_group: str
_current_sample: int


def _prepare_directory(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    for child in directory.iterdir():
        if child.is_file():
            child.unlink()
        else:
            shutil.rmtree(child)


def _on_initialize() -> None:
    directories = [
        SAMPLES_DIRECTORY,
        ERRORS_DIRECTORY,
        SAMPLE_ANALYSIS_DIRECTORY,
        GROUP_ANALYSIS_DIRECTORY,
    ]

    for directory in directories:
        _prepare_directory(directory)


def _on_began_sampling_from_group(group_name: str) -> None:
    global _current_group
    _current_group = group_name


def _on_sample_generated(sample_index: int, values: dict[str, float]) -> None:
    global _current_sample
    _current_sample = sample_index

    global _current_group

    global _parameter_order
    if not _parameter_order:
        _parameter_order = list(values.keys())

    sample_group_file = SAMPLES_DIRECTORY / f"{_current_group}.csv"
    is_first_write = not sample_group_file.exists()

    with open(sample_group_file, "a", newline="") as file:
        writer = csv.writer(file)
        
        if is_first_write:
            writer.writerow(_parameter_order)

        sample_row = [values[parameter] for parameter in _parameter_order]
        writer.writerow(sample_row)


def _on_binary_exited(exit_code: int) -> None:
    if not exit_code:
        return

    global _current_group
    global _current_sample

    error_file = ERRORS_DIRECTORY / f"{_current_group}.csv"
    is_first_write = not error_file.exists()
    
    with open(error_file, "a", newline="") as file:
        writer = csv.writer(file)

        if is_first_write:
            writer.writerow(BINARY_EXIT_FILE_HEADERS)

        writer.writerow((_current_sample, exit_code))


def _on_sample_analysis_with_plugin_success(
        plugin_name: str,
        file_output: FileSystemTree
) -> None:
    global _current_group
    global _current_sample

    analysis_tree_parent = SAMPLE_ANALYSIS_DIRECTORY / _current_group / plugin_name

    analysis_tree_parent.mkdir(exist_ok=True, parents=True)

    file_output.write_to_filesystem(analysis_tree_parent, str(_current_sample))


def _on_group_analysis_with_plugin_success(
        plugin_name: str,
        file_output: FileSystemTree
) -> None:
    global _current_group

    analysis_tree_parent = GROUP_ANALYSIS_DIRECTORY / _current_group

    analysis_tree_parent.mkdir(exist_ok=True)

    file_output.write_to_filesystem(analysis_tree_parent, str(plugin_name))


SUBSCRIPTIONS = {
    Event.INITIALIZE: _on_initialize,
    Event.BEGAN_SAMPLING_FROM_GROUP: _on_began_sampling_from_group,
    Event.SAMPLE_GENERATED: _on_sample_generated,
    Event.BINARY_EXITED: _on_binary_exited,
    Event.SAMPLE_ANALYSIS_WITH_PLUGIN_SUCCESS: _on_sample_analysis_with_plugin_success,
    Event.GROUP_ANALYSIS_WITH_PLUGIN_SUCCESS: _on_group_analysis_with_plugin_success,
}

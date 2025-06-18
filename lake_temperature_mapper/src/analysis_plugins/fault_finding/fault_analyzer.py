from collections.abc import Iterable, Mapping, Sequence
from configparser import ConfigParser
import inspect
from pathlib import Path
import sys
from types import ModuleType
from typing import Callable

from analysis import PerSampleAnalyzer
from output.file_utils import FileSystemTree
from root import ANALYSIS_PLUGIN_CONFIG_DIRECTORY, APP_ROOT
from util import ScopedImporter

from . import output
from .check_status import CheckStatus

_CONFIG_PATH = ANALYSIS_PLUGIN_CONFIG_DIRECTORY / "fault_finding.ini"
_CONFIG = ConfigParser()
_CONFIG.read(_CONFIG_PATH)


class _CheckFunction:
    def __init__(self, name: str, function: Callable):
        self._name = name
        self._function = function
        self._args: Iterable[str] = inspect.signature(function).parameters.keys()

    def call(
            self,
            data: Mapping[str, float | Sequence[float]]
    ) -> tuple[CheckStatus, None | str | Exception]:
        try:
            relevant_args = self._get_relevant_args(data)

            self._function(**relevant_args)

            return (CheckStatus.PASSED, None)
        except AssertionError as assertion:
            message = ""
            if len(assertion.args) > 0:
                message = assertion.args[0]
            
            return (CheckStatus.FAILED, message)
        except Exception as error:
            return (CheckStatus.ERROR, error)

    def get_name(self) -> str:
        return self._name

    def _get_relevant_args(
            self,
            data: Mapping[str, float | Sequence[float]]
    ) -> Mapping[str, float | Sequence[float]]:
        relevant_args: dict[str, float | Sequence[float]] = {}

        for arg in self._args:
            if arg == "kwargs":
                continue
            if arg not in data:
                raise KeyError(
                    f"Requested argument {arg} not in avaliable arguments "
                    f"{list(data.keys())}"
                )
            relevant_args[arg] = data[arg]

        # Check is done after to avoid situation where check function specifies an
        # unavaliable argument AND kwargs.
        if "kwargs" in self._args:
            return data

        return relevant_args


class FaultAnalyzer(PerSampleAnalyzer):
    _CHECK_IDENTIFIER = "check"
    _CHECKS_PATH = APP_ROOT / _CONFIG["Paths"]["checks_directory"]
    _PYTHON_EXTENSION = ".py"

    _REFERENCE_PARAM_PREFIX = "ref_"
    _TEST_PARAM_PREFIX = "test_"

    def __init__(self):
        self._checks = self._find_check_functions()

        if not self._checks:
            raise RuntimeError(f"No check functions found in {self._CHECKS_PATH}!")

    def analyze_sample_data(
        self,
        sample: Mapping[str, float],
        reference_data: Mapping[str, Sequence[float]],
        test_data: Mapping[str, Sequence[float]]
    ) -> tuple[str, FileSystemTree]:
        data = self._combine_data(sample, reference_data, test_data)

        check_results: dict[str, tuple[CheckStatus, None | str | Exception]] = {}
        for check in self._checks:
            check_result = check.call(data)
            check_results[check.get_name()] = check_result

        return output.generate_output(check_results)

    def _find_check_functions(self) -> list[_CheckFunction]:
        check_modules = self._find_check_modules()
        check_functions: list[_CheckFunction] = []

        test_importer = ScopedImporter(self._CHECKS_PATH)

        for module_path in check_modules:
            module = test_importer.import_module(module_path.stem)
            module_functions = inspect.getmembers(module, inspect.isfunction)

            for function_name, function in module_functions:
                if function_name.startswith(self._CHECK_IDENTIFIER):
                    check_functions.append(
                        _CheckFunction(function_name, function)
                    )

        return check_functions

    def _find_check_modules(self) -> list[Path]:
        check_module_paths: list[Path] = []

        for file in self._CHECKS_PATH.iterdir():
            if not file.is_file() or not file.suffix == self._PYTHON_EXTENSION:
                continue

            stem = file.stem
            if (not stem.startswith(self._CHECK_IDENTIFIER)
                and not stem.endswith(self._CHECK_IDENTIFIER)
            ):
                continue

            check_module_paths.append(file)

        return check_module_paths

    def _combine_data(
        self,
        sample: Mapping[str, float],
        reference_data: Mapping[str, Sequence[float]],
        test_data: Mapping[str, Sequence[float]]
    ) -> dict[str, float | Sequence[float]]:
        data: dict[str, float | Sequence[float]] = dict(sample)

        for variable, values in reference_data.items():
            arg_name = self._REFERENCE_PARAM_PREFIX + variable.replace("%", "_")
            data[arg_name] = values

        for variable, values in test_data.items():
            arg_name = self._TEST_PARAM_PREFIX + variable.replace("%", "_")
            data[arg_name] = values

        return data

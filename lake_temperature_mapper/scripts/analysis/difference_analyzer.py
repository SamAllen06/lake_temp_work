from pathlib import Path
from typing import Mapping

from analysis.output_difference import OutputDifference
from testing.output_file_data import OutputFileData


class DifferenceAnalyzer:
    def __init__(self, ref_file_path: Path, test_file_path: Path):
        self._ref_file_path = ref_file_path
        self._test_file_path = test_file_path

    def compare_outputs(self) -> Mapping[str, list[OutputDifference]]:
        ref_data = OutputFileData(self._ref_file_path)
        test_data = OutputFileData(self._test_file_path)

        assert ref_data.is_same_format_as(test_data)

        return ref_data.compare_to(test_data)

from collections import namedtuple
from collections.abc import Mapping, Sequence
import math

from analysis import PerSampleAnalyzer
from output.file_utils import FileSystemTree
from util import Table

from . import output


DIFFERENCE_KEYS = ["reference", "test", "difference", "index"]


class DifferenceAnalyzer(PerSampleAnalyzer):
    def analyze_sample_data(
        self,
        sample: Mapping[str, float],
        reference_data: Mapping[str, Sequence[float]],
        test_data: Mapping[str, Sequence[float]]
    ) -> tuple[str, FileSystemTree]:
        differences: dict[str, Table] = {}

        for parameter in reference_data:
            differences[parameter] = self._compare_parameter_data(
                reference_data[parameter],
                test_data[parameter]
            )

        return output.generate_output(differences)

    def _compare_parameter_data(
            self,
            reference_values: Sequence[float],
            test_values: Sequence[float]
    ) -> Table:
        differences: Table = Table({}, [])
        difference_sequence = differences.as_sequence()
        difference_sequence.initialize_keys(DIFFERENCE_KEYS)

        for index, (reference_value, test_value) in enumerate(
            zip(reference_values, test_values)
        ):
            difference_value = self._get_difference(reference_value, test_value)

            if not difference_value == 0.0:
                difference_sequence.append(
                    {
                        "reference": reference_value,
                        "test": test_value,
                        "difference": difference_value,
                        "index": index,
                    }
                )

        return differences

    def _get_difference(self, reference_value: float, test_value: float) -> float:
        difference = test_value - reference_value

        if math.isnan(reference_value) and math.isnan(test_value):
            difference = 0.0

        return difference

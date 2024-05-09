import os
from typing import Mapping


class DifferenceAnalyzer:
    def __init__(self, ref_file_path: os.PathLike, test_file_path: os.PathLike):
        self._ref_file_path = ref_file_path
        self._test_file_path = test_file_path

    def _read_output_values(
            self, file_path: os.PathLike
    ) -> Mapping[str, list[float]]:
        with open(file_path, "r") as file:
            lines = file.readlines()

        outputs = {}

        for line in lines:
            stripped_line = line.strip()
            if "%" in stripped_line:
                parameter_name = stripped_line
                outputs[parameter_name] = []
                continue

            outputs[parameter_name] += [
                float(value) for value in stripped_line.split()
            ]

        return outputs

    def compare_outputs(self) -> Mapping[
        str, list[tuple[int, float, float, float]]
    ]:
        ref_outputs = self._read_output_values(self._ref_file_path)
        test_outputs = self._read_output_values(self._test_file_path)

        differences = {}

        for parameter in ref_outputs.keys():
            differences[parameter] = []
            for index, (ref_output, test_output) in enumerate(
                zip(ref_outputs[parameter], test_outputs[parameter])
            ):
                difference = (
                    index,
                    ref_output,
                    test_output,
                    test_output - ref_output
                )

                # Ignore values with no difference.
                if difference[3] == 0:
                    continue

                differences[parameter].append(difference)

        return differences



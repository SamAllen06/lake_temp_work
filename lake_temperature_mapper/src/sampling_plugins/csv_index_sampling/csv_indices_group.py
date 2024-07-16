from collections.abc import Sequence
import csv
from pathlib import Path
from typing import cast

from sampling import SampleGroup, SampleGroupIterator
from util import Table

from sampling_libs.ranges import RangeReader


class CsvIndicesGroupIterator(SampleGroupIterator):
    def __init__(
            self,
            index_samples: Table,
            translation_table: dict[str, list[float]]
    ):
        self._index_samples_sequence = index_samples.as_sequence()
        self._translation_table = translation_table
        self._index = 0

    def __next__(self) -> dict[str, float]:
        sample: dict[str, float] = {}

        if len(self._index_samples_sequence) == self._index:
            raise StopIteration

        index_sample = self._index_samples_sequence[self._index]
        
        for parameter, index in index_sample.items():
            translated_value = self._translation_table[parameter][index]
            sample[parameter] = translated_value

        self._index += 1

        return sample


class CsvIndicesGroup(SampleGroup):
    def __init__(self, csv_file: Path, range_reader: RangeReader):
        self._index_samples, max_indicies = self._read_index_samples(csv_file)
        self._translation_table = self._generate_translation_table(
            range_reader,
            max_indicies
        )

    def get_sample_count(self) -> int:
        return self._index_samples.get_row_count()

    def __iter__(self) -> SampleGroupIterator:
        return CsvIndicesGroupIterator(self._index_samples, self._translation_table)

    def _read_index_samples(self, csv_file: Path) -> tuple[
        Table, dict[str, int]
    ]:
        index_samples: Table = Table({}, [])
        index_samples_sequence = index_samples.as_sequence()
        max_indicies: dict[str, int] = {}

        with open(csv_file, "r", newline="") as file:
            reader = csv.DictReader(file)

            if reader.fieldnames == None:
                raise RuntimeError(f"{csv_file} is missing parameter headers")

            # reader.fieldnames cannot be None due to the guard if statement.
            index_samples_sequence.initialize_keys(reader.fieldnames) # type: ignore
            for parameter in reader.fieldnames: # type: ignore
                max_indicies[parameter] = 0

            for row in reader:
                int_row = {key: int(row[key]) for key in row}
                index_samples_sequence.append(int_row)
                for parameter in int_row:
                    max_indicies[parameter] = max(
                        max_indicies[parameter],
                        int_row[parameter]
                    )

        return (index_samples, max_indicies)

    def _generate_translation_table(
            self,
            range_reader: RangeReader,
            max_indicies: dict[str, int]
    ) -> dict[str, list[float]]:
        translation_table: dict[str, list[float]] = {key: [] for key in max_indicies}

        for parameter, max_index in max_indicies.items():
            min = range_reader.get_min(parameter)
            max = range_reader.get_max(parameter)

            for index in range(max_index + 1):
                time = index / max_index
                value = self._linear_interpolate(min, max, time)
                translation_table[parameter].append(value)

        return translation_table

    def _linear_interpolate(self, min: float, max: float, time: float) -> float:
        return min * (1 - time) + max * time

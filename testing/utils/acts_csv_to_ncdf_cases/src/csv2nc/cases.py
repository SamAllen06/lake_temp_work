from collections.abc import Iterable, Iterator
import csv
from pathlib import Path


class CasesIterator(Iterator):
    def __init__(self, path: Path):
        self._file = open(path, "r", newline="")
        self._file_iter = iter(csv.DictReader(self._file))

    def __iter__(self):
        return self

    def __next__(self) -> dict[str, int]:
        try:
            row = next(self._file_iter)
        except StopIteration:
            self._file.close()
            raise StopIteration()

        return {key: int(value) for key, value in row.items()}


class Cases(Iterable):
    def __init__(self, path: Path):
        self._path = path

    def __iter__(self) -> CasesIterator:
        return CasesIterator(self._path)

    def get_variable_names(self) -> list[str]:
        with open(self._path, "r", newline="") as file:
            reader = csv.reader(file)
            return list(next(reader))

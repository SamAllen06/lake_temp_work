from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence

from output import FileSystemTree
from util import Table


class PerSampleAnalyzer(ABC):
    @abstractmethod
    def analyze_sample_data(
        self,
        sample: Mapping[str, float],
        reference_data: Mapping[str, Sequence[float]],
        test_data: Mapping[str, Sequence[float]]
    ) -> tuple[str, FileSystemTree]:
        pass

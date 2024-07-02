from abc import ABC, abstractmethod

from output.file_utils import FileSystemTree
from sampling import SampleGroup
from util import Table


class SampleGroupAnalyzer(ABC):
    @abstractmethod
    def analyze_sample_data(
        self,
        sample_group: SampleGroup,
        data: Table
    ) -> tuple[str, FileSystemTree]:
        pass

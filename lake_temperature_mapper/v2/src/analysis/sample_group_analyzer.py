from abc import ABC, abstractmethod

from output import FileSystemTree
from sampling import SampleGroup
from util import Table, TransparentLayerList


class SampleGroupAnalyzer(ABC):
    @abstractmethod
    def analyze_sample_data(
        self,
        sample_group: SampleGroup,
        data: Table[dict, TransparentLayerList]
    ) -> tuple[str, FileSystemTree]:
        pass

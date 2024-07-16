from configparser import ConfigParser

from root import APP_ROOT, SAMPLING_PLUGIN_CONFIG_DIRECTORY
from sampling import Sampler

from sampling_libs.ranges import RangeReader
from .csv_indices_group import CsvIndicesGroup

CONFIG_FILE = SAMPLING_PLUGIN_CONFIG_DIRECTORY / "csv_index_sampling.ini"


class CsvIndexSampler(Sampler):
    def __init__(self):
        config = ConfigParser()
        config.read(CONFIG_FILE)

        self.range_reader = RangeReader(APP_ROOT / config["Paths"]["range_path"])
        self.csv_directory = APP_ROOT / config["Paths"]["csv_index_files_directory"]

    def get_sample_groups(self) -> dict[str, CsvIndicesGroup]:
        groups: dict[str, CsvIndicesGroup] = {}

        for csv_file in self.csv_directory.iterdir():
            if not csv_file.is_file():
                continue

            groups[csv_file.stem] = CsvIndicesGroup(csv_file, self.range_reader)

        return groups


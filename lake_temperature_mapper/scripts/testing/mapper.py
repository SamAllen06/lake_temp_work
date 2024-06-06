from pathlib import Path
from typing import Mapping

from analysis.difference_analyzer import DifferenceAnalyzer
from config.config_reader import ConfigReader
from output.output_writer import OutputWriter
from sample_generation import SampleGroup, Sampler
from testing.binary_runner import BinaryRunner
from testing.defaults_writer import DefaultsWriter
from testing.param_editor import ParamEditor


class Mapper:
    def __init__(
            self,
            config_reader: ConfigReader,
            output_writer: OutputWriter
    ):
        self._config_reader = config_reader
        self._output_writer = output_writer
        self._defaults_writer = DefaultsWriter(
            self._config_reader.get_path("defaults_path"),
            self._config_reader.get_path("params_path")
        )
        self._param_editor = ParamEditor(
            self._config_reader.get_path("params_path")
        )
        self._binary_runner = BinaryRunner(
            self._config_reader.get_path("binary_path"),
            self._config_reader.get("binary_args")
        )
        self._difference_analyzer = DifferenceAnalyzer(
            self._config_reader.get_path("ref_output"),
            self._config_reader.get_path("test_output")
        )

    def map(self):
        sample_groups = self._read_sample_groups()
        self._execute_sample_groups(sample_groups)

    def _read_sample_groups(self) -> Mapping[str, SampleGroup]:
        SamplerClass = self._config_reader.get_class("sampler_class")
        sampler: Sampler = SamplerClass()

        return sampler.get_sample_groups()

    def _execute_sample_groups(
            self, sample_groups: Mapping[str, SampleGroup]
    ) -> None:
        for sample_group_name in sample_groups.keys():
            sample_group = sample_groups[sample_group_name]
            self._output_writer.write_sample_group_header(
                sample_group_name, sample_group
            )
            self._execute_sample_group(sample_group)

        self._defaults_writer.write_defaults()
        self._output_writer.finish()

    def _execute_sample_group(self, sample_group: SampleGroup) -> None:
        self._defaults_writer.write_defaults()
        for sample in sample_group:
            self._output_writer.write_sample(
                sample
            )
            self._param_editor.modify_parameters(sample)

            exit_code = self._binary_runner.run_binary()
            if exit_code:
                self._output_writer.write_binary_exit(exit_code)
                continue

            difference_map = self._difference_analyzer.compare_outputs()
            self._output_writer.write_difference_map(difference_map)

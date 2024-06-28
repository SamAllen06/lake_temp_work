from collections.abc import Mapping
from configparser import ConfigParser
from pathlib import Path
import sys
import time

from analysis import AnalyzerLoader
from output.events import Event, event_bus
from root import APP_ROOT
from sampling import SampleGroup, SamplerLoader
from testing import BinaryRunner, DefaultsWriter, OutputFileReader, ParamEditor


class Tester:
    def __init__(self, config_path: Path):
        self._config = ConfigParser()
        self._config.read(config_path)

        self._binary_runner = BinaryRunner()
        self._sampler_loader = SamplerLoader()
        self._analyzer_loader = AnalyzerLoader()

        self._defaults_writer = DefaultsWriter(
            APP_ROOT / self._config["Model"]["parameter_defaults"],
            APP_ROOT / self._config["Model"]["parameters"]
        )
        self._param_editor = ParamEditor(APP_ROOT / self._config["Model"]["parameters"])
        self._output_file_reader = OutputFileReader(
            APP_ROOT / self._config["Model"]["reference_output"],
            APP_ROOT / self._config["Model"]["test_output"]
        )

        self._sample_groups: dict[str, SampleGroup] = {}

    def prepare_for_testing(self) -> None:
        self._load_binary()
        self._load_sampling_plugins()
        self._load_analysis_plugins()
        self._sample_groups, sample_count = self._sample_from_plugins()
        self._estimate_testing_time(sample_count)

    def test_model(self) -> None:
        group_count = len(self._sample_groups)

        for group_index, group_name in enumerate(self._sample_groups):
            sample_group = self._sample_groups[group_name]

            event_bus.fire_event(
                Event.BEGAN_SAMPLING_FROM_GROUP,
                group_name=group_name,
                group_index=group_index,
                group_count=group_count
            )
            self._test_with_group(sample_group)

        self._defaults_writer.write_defaults()
        event_bus.fire_event(Event.TESTING_COMPLETED)

    def _load_binary(self) -> None:
        binary_path = APP_ROOT / self._config["Model"]["binary"]
        binary_args = self._config["Model"]["args"]
        binary_name = binary_path.name

        event_bus.fire_event(Event.LOADING_BINARY, binary_name=binary_name)

        try:
            self._binary_runner.load_binary(binary_path, binary_args)
        except FileNotFoundError as error:
            event_bus.fire_event(Event.BINARY_LOAD_FAILURE, reason=error)
            sys.exit(1)

        event_bus.fire_event(Event.BINARY_LOAD_SUCCESS)

    def _load_sampling_plugins(self) -> None:
        event_bus.fire_event(Event.BEGAN_LOADING_SAMPLING_PLUGINS)

        self._sampler_loader.load_plugins()

        plugins_loaded = self._sampler_loader.get_total_plugins_loaded_count()

        if not plugins_loaded:
            event_bus.fire_event(Event.SAMPLING_PLUGINS_LOAD_FAILURE)
            sys.exit(1)

        event_bus.fire_event(Event.SAMPLING_PLUGINS_LOAD_SUCCESS, count=plugins_loaded)

    def _load_analysis_plugins(self) -> None:
        event_bus.fire_event(Event.BEGAN_LOADING_ANALYSIS_PLUGINS)

        self._analyzer_loader.load_plugins()

        plugins_loaded = self._analyzer_loader.get_total_plugins_loaded_count()

        if not plugins_loaded:
            event_bus.fire_event(Event.ANALYSIS_PLUGINS_LOAD_FAILURE)
            sys.exit(1)

        event_bus.fire_event(Event.ANALYSIS_PLUGINS_LOAD_SUCCESS, count=plugins_loaded)

    def _sample_from_plugins(self) -> tuple[dict[str, SampleGroup], int]:
        event_bus.fire_event(Event.BEGAN_SAMPLE_GENERATION)
        
        sample_groups = self._sampler_loader.sample_from_plugins()

        if not sample_groups:
            event_bus.fire_event(Event.SAMPLING_FROM_PLUGINS_FAILURE)
            sys.exit(1)

        group_count = len(sample_groups)
        sample_count = self._count_group_samples(sample_groups)

        event_bus.fire_event(
            Event.SAMPLING_FROM_PLUGINS_SUCCESS,
            group_count=group_count,
            sample_count=sample_count
        )

        return (sample_groups, sample_count)

    def _count_group_samples(self, sample_groups: dict[str, SampleGroup]) -> int:
        count = 0

        for group in sample_groups.values():
            count += group.get_sample_count()

        return count

    def _estimate_testing_time(self, sample_count: int) -> None:
        binary_name = self._binary_runner.get_binary_name()
        self._defaults_writer.write_defaults()
        
        event_bus.fire_event(Event.BEGAN_TIMING_BINARY, binary_name=binary_name)

        start = time.time()
        exit_code = self._binary_runner.run_binary()
        end = time.time()

        if exit_code:
            event_bus.fire_event(Event.TIMING_BINARY_FAILURE, exit_code=exit_code)
            return

        seconds_estimated = (end - start) * sample_count

        event_bus.fire_event(
            Event.TIMING_BINARY_SUCCESS,
            seconds_estimate=seconds_estimated
        )

    def _test_with_group(self, group: SampleGroup) -> None:
        sample_count = len(group)
        self._defaults_writer.write_defaults()
        full_sample_values = self._defaults_writer.get_defaults()

        for index, sample in enumerate(group):
            full_sample_values.update(sample)

            event_bus.fire_event(
                Event.SAMPLE_GENERATED,
                sample_index=index,
                sample_count=sample_count,
                values=full_sample_values
            )

            self._test_with_sample(sample)

        if (not self._analyzer_loader.any_group_plugins_loaded()
                or not self._output_file_reader.group_data_exists()
        ):
            return

        event_bus.fire_event(Event.BEGAN_GROUP_ANALYSIS)

        group_data = self._output_file_reader.read_group_data()
        self._analyzer_loader.run_group_analysis(group, group_data)

    def _test_with_sample(self, sample: Mapping[str, float]) -> None:
        binary_name = self._binary_runner.get_binary_name()

        self._param_editor.modify_parameters(sample)

        event_bus.fire_event(Event.RUNNING_BINARY, binary_name=binary_name)
        exit_code = self._binary_runner.run_binary()
        event_bus.fire_event(Event.BINARY_EXITED, exit_code=exit_code)

        if exit_code:
            return

        reference_data = self._output_file_reader.get_reference_data()
        test_data = self._output_file_reader.read_sample_data()

        if not self._analyzer_loader.any_sample_plugins_loaded():
            return

        event_bus.fire_event(Event.BEGAN_SAMPLE_ANALYSIS)

        self._analyzer_loader.run_sample_analysis(sample, reference_data, test_data)



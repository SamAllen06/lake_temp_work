from collections.abc import Mapping
from configparser import ConfigParser
from pathlib import Path
import sys
import time

from output.events import Event, event_bus
from plugin_loading import AnalyzerLoader, SamplerLoader
from root import APP_ROOT, CONFIG_ROOT
from sampling import SampleGroup
from testing import BinaryRunner, DefaultsWriter, OutputFileReader, ParamEditor

CONFIG_PATH = CONFIG_ROOT / "main.ini"

CONFIG = ConfigParser()
CONFIG.read(CONFIG_PATH)

BINARY_RUNNER = BinaryRunner()

SAMPLER_LOADER = SamplerLoader()
ANALYZER_LOADER = AnalyzerLoader()

DEFAULTS_WRITER = DefaultsWriter(
    APP_ROOT / CONFIG["Model"]["parameter_defaults"],
    APP_ROOT / CONFIG["Model"]["parameters"]
)
PARAM_EDITOR = ParamEditor(APP_ROOT / CONFIG["Model"]["parameters"])
OUTPUT_FILE_READER = OutputFileReader(
    APP_ROOT / CONFIG["Model"]["reference_output"],
    APP_ROOT / CONFIG["Model"]["test_output"]
)

_sample_groups: dict[str, SampleGroup] = {}

def prepare_for_testing() -> None:
    event_bus.fire_event(Event.INITIALIZE)

    _load_binary()

    _load_sampling_plugins()
    _load_analysis_plugins()

    global _sample_groups
    _sample_groups, sample_count = _sample_from_plugins()

    _estimate_testing_time(sample_count)

def test_model() -> None:
    global _sample_groups
    group_count = len(_sample_groups)

    for group_index, (group_name, sample_group) in enumerate(_sample_groups.items()):
        event_bus.fire_event(
            Event.BEGAN_SAMPLING_FROM_GROUP,
            group_name=group_name,
            group_index=group_index,
            group_count=group_count
        )
        _test_with_group(sample_group)

    DEFAULTS_WRITER.write_defaults()
    event_bus.fire_event(Event.TESTING_COMPLETED)

def _load_binary() -> None:
    binary_path = APP_ROOT / CONFIG["Model"]["binary"]
    binary_args = CONFIG["Model"]["args"]
    binary_name = binary_path.name

    event_bus.fire_event(Event.LOADING_BINARY, binary_name=binary_name)

    try:
        BINARY_RUNNER.load_binary(binary_path, binary_args)
    except FileNotFoundError as error:
        event_bus.fire_event(Event.BINARY_LOAD_FAILURE, reason=error)
        sys.exit(1)

    event_bus.fire_event(Event.BINARY_LOAD_SUCCESS)

def _load_sampling_plugins() -> None:
    event_bus.fire_event(Event.BEGAN_LOADING_SAMPLING_PLUGINS)

    SAMPLER_LOADER.load_plugins()

    plugins_loaded = SAMPLER_LOADER.get_total_plugins_loaded_count()

    if not plugins_loaded:
        event_bus.fire_event(Event.SAMPLING_PLUGINS_LOAD_FAILURE)
        sys.exit(1)

    event_bus.fire_event(Event.SAMPLING_PLUGINS_LOAD_SUCCESS, count=plugins_loaded)

def _load_analysis_plugins() -> None:
    event_bus.fire_event(Event.BEGAN_LOADING_ANALYSIS_PLUGINS)

    ANALYZER_LOADER.load_plugins()

    plugins_loaded = ANALYZER_LOADER.get_total_plugins_loaded_count()

    if not plugins_loaded:
        event_bus.fire_event(Event.ANALYSIS_PLUGINS_LOAD_FAILURE)
        sys.exit(1)

    event_bus.fire_event(Event.ANALYSIS_PLUGINS_LOAD_SUCCESS, count=plugins_loaded)

def _sample_from_plugins() -> tuple[dict[str, SampleGroup], int]:
    event_bus.fire_event(Event.BEGAN_SAMPLE_GENERATION)
    
    sample_groups = SAMPLER_LOADER.sample_from_plugins()

    if not sample_groups:
        event_bus.fire_event(Event.SAMPLING_FROM_PLUGINS_FAILURE)
        sys.exit(1)

    group_count = len(sample_groups)
    sample_count = _count_group_samples(sample_groups)

    event_bus.fire_event(
        Event.SAMPLING_FROM_PLUGINS_SUCCESS,
        group_count=group_count,
        sample_count=sample_count
    )

    return (sample_groups, sample_count)

def _count_group_samples(sample_groups: dict[str, SampleGroup]) -> int:
    count = 0

    for group in sample_groups.values():
        count += group.get_sample_count()

    return count

def _estimate_testing_time(sample_count: int) -> None:
    binary_name = BINARY_RUNNER.get_binary_name()
    DEFAULTS_WRITER.write_defaults()
    
    event_bus.fire_event(Event.BEGAN_TIMING_BINARY, binary_name=binary_name)

    start = time.time()
    exit_code = BINARY_RUNNER.run_binary()
    end = time.time()

    if exit_code:
        event_bus.fire_event(Event.TIMING_BINARY_FAILURE, exit_code=exit_code)
        return

    seconds_estimated = (end - start) * sample_count

    event_bus.fire_event(
        Event.TIMING_BINARY_SUCCESS,
        seconds_estimate=seconds_estimated
    )

def _test_with_group(group: SampleGroup) -> None:
    sample_count = len(group)
    DEFAULTS_WRITER.write_defaults()
    full_sample_values = DEFAULTS_WRITER.get_defaults()

    for index, sample in enumerate(group):
        full_sample_values.update(sample)

        event_bus.fire_event(
            Event.SAMPLE_GENERATED,
            sample_index=index,
            sample_count=sample_count,
            values=full_sample_values
        )

        _test_with_sample(sample)

    if (not ANALYZER_LOADER.any_group_plugins_loaded()
            or not OUTPUT_FILE_READER.group_data_exists()
    ):
        return

    event_bus.fire_event(Event.BEGAN_GROUP_ANALYSIS)

    group_data = OUTPUT_FILE_READER.read_group_data()
    ANALYZER_LOADER.run_group_analysis(group, group_data)

def _test_with_sample(sample: Mapping[str, float]) -> None:
    binary_name = BINARY_RUNNER.get_binary_name()

    PARAM_EDITOR.modify_parameters(sample)

    event_bus.fire_event(Event.RUNNING_BINARY, binary_name=binary_name)
    exit_code = BINARY_RUNNER.run_binary()
    event_bus.fire_event(Event.BINARY_EXITED, exit_code=exit_code)

    if exit_code:
        return

    reference_data = OUTPUT_FILE_READER.get_reference_data()
    test_data = OUTPUT_FILE_READER.read_sample_data()

    if not ANALYZER_LOADER.any_sample_plugins_loaded():
        return

    event_bus.fire_event(Event.BEGAN_SAMPLE_ANALYSIS)

    ANALYZER_LOADER.run_sample_analysis(sample, reference_data, test_data)



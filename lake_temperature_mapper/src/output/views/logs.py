import configparser
import datetime
import logging
from pathlib import Path
import traceback

from output.events import Event
from root import APP_ROOT, OUTPUT_CONFIG_DIRECTORY


LOGGER = logging.getLogger("event")


def _define_log_file():
    config_path = OUTPUT_CONFIG_DIRECTORY / "logs.ini"
    config = configparser.ConfigParser()
    config.read(config_path)

    log_directory = APP_ROOT / config["Directories"]["log_directory"]
    log_directory.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().replace(microsecond=0).isoformat()
    log_path = log_directory / f"{timestamp}.log"

    print("Logging at " + str(log_path))
    logging.basicConfig(filename=log_path, level=logging.INFO)


def _on_initialize():
    _define_log_file()

    LOGGER.info("Initialized")


def _on_loading_binary(binary_name: str):
    LOGGER.info(f'Attemping to find the binary "{binary_name}"...')


def _on_binary_load_success():
    LOGGER.info("Successfully found the binary")


def _on_binary_load_failure(reason: Exception):
    formatted_exception = traceback.format_exception(reason)
    LOGGER.critical(f"Failed to find the binary.\n{formatted_exception}")


def _on_began_loading_sampling_plugins():
    LOGGER.info("Started loading sampling plugins")


def _on_loading_sampling_plugin(plugin_name: str):
    LOGGER.info(f'Loading sampling plugin "{plugin_name}"')


def _on_sampling_plugin_load_success(plugin_name: str):
    LOGGER.info(f'Successfully loaded sampling plugin "{plugin_name}"')


def _on_sampling_plugin_load_failure(plugin_name: str, reason: Exception):
    formatted_exception = traceback.format_exception(reason)
    LOGGER.error(
        f'Failed to load sampling plugin "{plugin_name}"\n'
        f'{formatted_exception}'
    )


def _on_sampling_plugins_load_success(count: int) -> None:
    LOGGER.info(f"Successfully loaded {count} sampling plugins")


def _on_sampling_plugins_load_failure() -> None:
    LOGGER.critical(f"No sampling plugins were able to load.")


def _on_began_loading_analysis_plugins() -> None:
    LOGGER.info("Started loading analysis plugins")


def _on_loading_analysis_plugin(plugin_name: str) -> None:
    LOGGER.info(f'Loading analysis plugin "{plugin_name}"')


def _on_analysis_plugin_load_success(plugin_name: str) -> None:
    LOGGER.info(f'Successfully loaded analysis plugin "{plugin_name}"')


def _on_analysis_plugin_load_failure(plugin_name: str, reason: Exception) -> None:
    formatted_exception = traceback.format_exception(reason)
    LOGGER.error(
        f'Failed to load analysis plugin "{plugin_name}"\n'
        f'{formatted_exception}'
    )


def _on_analysis_plugins_load_success(count: int) -> None:
    LOGGER.info(f"Successfully loaded {count} analysis plugins")


def _on_analysis_plugins_load_failure() -> None:
    LOGGER.critical(f"No analysis plugins were able to load")


def _on_began_sample_generation() -> None:
    LOGGER.info("Began sample group generation")


def _on_began_sampling_from_plugin(plugin_name: str) -> None:
    LOGGER.info(f'Getting sample groups from plugin "{plugin_name}"')


def _on_sampling_from_plugin_success(plugin_name: str, group_sample_counts: dict[str, int]) -> None:
    group_count = len(group_sample_counts)
    sample_count = sum([group_sample_counts[group] for group in group_sample_counts])
    LOGGER.info(
        f'Got {group_count} groups with {sample_count} total samples from plugin '
        f'"{plugin_name}"'
    )


def _on_sampling_from_plugin_failure(plugin_name: str, reason: Exception) -> None:
    formatted_exception = traceback.format_exception(reason)
    LOGGER.error(
        f'Failed to get sample groups from plugin "{plugin_name}"\n'
        f'{formatted_exception}'
    )


def _on_sampling_from_plugins_success(group_count: int, sample_count: int) -> None:
    LOGGER.info(f"Got {group_count} total groups and {sample_count} from plugins")


def _on_sampling_from_plugins_failure() -> None:
    LOGGER.critical(f"Failed to get any sample groups from plugins")


def _on_began_timing_binary(binary_name: str) -> None:
    LOGGER.info(f"Timing {binary_name}")


def _on_timing_binary_success(seconds_estimate: float) -> None:
    LOGGER.info(f"Estimated testing to take {seconds_estimate} seconds")


def _on_timing_binary_failure(exit_code: int) -> None:
    LOGGER.warning(
        f"Binary exited with code {exit_code} when using its default inputs, "
        "this may indicate that the testing program is misconfigured"
    )


def _on_began_sampling_from_group(group_name: str, group_index: int, group_count: int) -> None:
    LOGGER.info(
        f'Started sampling from group "{group_name}" '
        f'({group_index + 1} / {group_count})'
    )


def _on_sample_generated(sample_index: int, sample_count: int) -> None:
    LOGGER.info(f"Generated sample {sample_index + 1} out of {sample_count}")


def _on_running_binary(binary_name: str) -> None:
    LOGGER.info(f"Running {binary_name}")


def _on_binary_exited(exit_code: int) -> None:
    if exit_code:
        LOGGER.info(f"Binary exited with error code {exit_code}")
    else:
        LOGGER.info("Binary exited ok")


def _on_began_sample_analysis() -> None:
    LOGGER.info("Began analysis on individual samples")


def _on_began_sample_analysis_with_plugin(plugin_name: str) -> None:
    LOGGER.info(f'Began analyzing sample with plugin "{plugin_name}"')


def _on_sample_analysis_with_plugin_success(plugin_name: str) -> None:
    LOGGER.info(f'Successfully analyzed sample with plugin "{plugin_name}"')


def _on_sample_analysis_with_plugin_failure(plugin_name: str, reason: Exception) -> None:
    formatted_exception = traceback.format_exception(reason)
    LOGGER.info(
        f'Failed to analyze sample with plugin "{plugin_name}"\n{formatted_exception}'
    )


def _on_began_group_analysis() -> None:
    LOGGER.info("Began analysis on the sample group as a whole")


def _on_began_group_analysis_with_plugin(plugin_name: str) -> None:
    LOGGER.info(f'Began analyzing group with plugin "{plugin_name}"')


def _on_group_analysis_with_plugin_success(plugin_name: str) -> None:
    LOGGER.info(f'Successfully analyzed group with plugin "{plugin_name}"')


def _on_group_analysis_with_plugin_failure(plugin_name: str, reason: Exception) -> None:
    formatted_exception = traceback.format_exception(reason)
    LOGGER.info(
        f'Failed to analyze group with plugin "{plugin_name}"\n{formatted_exception}'
    )


def _on_testing_completed() -> None:
    LOGGER.info("Finished testing")


SUBSCRIPTIONS = {
    Event.INITIALIZE: _on_initialize,

    Event.LOADING_BINARY: _on_loading_binary,
    Event.BINARY_LOAD_SUCCESS: _on_binary_load_success,
    Event.BINARY_LOAD_FAILURE: _on_binary_load_failure,

    Event.BEGAN_LOADING_SAMPLING_PLUGINS: _on_began_loading_sampling_plugins,
    Event.LOADING_SAMPLING_PLUGIN: _on_loading_sampling_plugin,
    Event.SAMPLING_PLUGIN_LOAD_SUCCESS: _on_sampling_plugin_load_success,
    Event.SAMPLING_PLUGIN_LOAD_FAILURE: _on_sampling_plugin_load_failure,
    Event.SAMPLING_PLUGINS_LOAD_SUCCESS: _on_sampling_plugins_load_success,
    Event.SAMPLING_PLUGINS_LOAD_FAILURE: _on_sampling_plugins_load_failure,

    Event.BEGAN_LOADING_ANALYSIS_PLUGINS: _on_began_loading_analysis_plugins,
    Event.LOADING_ANALYSIS_PLUGIN: _on_loading_analysis_plugin,
    Event.ANALYSIS_PLUGIN_LOAD_SUCCESS: _on_analysis_plugin_load_success,
    Event.ANALYSIS_PLUGIN_LOAD_FAILURE: _on_analysis_plugin_load_failure,
    Event.ANALYSIS_PLUGINS_LOAD_SUCCESS: _on_analysis_plugins_load_success,
    Event.ANALYSIS_PLUGINS_LOAD_FAILURE: _on_analysis_plugins_load_failure,

    Event.BEGAN_SAMPLE_GENERATION: _on_began_sample_generation,
    Event.BEGAN_SAMPLING_FROM_PLUGIN: _on_began_sampling_from_plugin,
    Event.SAMPLING_FROM_PLUGIN_SUCCESS: _on_sampling_from_plugin_success,
    Event.SAMPLING_FROM_PLUGIN_FAILURE: _on_sampling_from_plugin_failure,
    Event.SAMPLING_FROM_PLUGINS_SUCCESS: _on_sampling_from_plugins_success,
    Event.SAMPLING_FROM_PLUGINS_FAILURE: _on_sampling_from_plugins_failure,

    Event.BEGAN_TIMING_BINARY: _on_began_timing_binary,
    Event.TIMING_BINARY_SUCCESS: _on_timing_binary_success,
    Event.TIMING_BINARY_FAILURE: _on_timing_binary_failure,

    Event.BEGAN_SAMPLING_FROM_GROUP: _on_began_sampling_from_group,
    Event.SAMPLE_GENERATED: _on_sample_generated,
    Event.RUNNING_BINARY: _on_running_binary,
    Event.BINARY_EXITED: _on_binary_exited,
    Event.BEGAN_SAMPLE_ANALYSIS: _on_began_sample_analysis,
    Event.BEGAN_SAMPLE_ANALYSIS_WITH_PLUGIN: _on_began_sample_analysis_with_plugin,
    Event.SAMPLE_ANALYSIS_WITH_PLUGIN_SUCCESS: _on_sample_analysis_with_plugin_success,
    Event.SAMPLE_ANALYSIS_WITH_PLUGIN_FAILURE: _on_sample_analysis_with_plugin_failure,

    Event.BEGAN_GROUP_ANALYSIS: _on_began_group_analysis,
    Event.BEGAN_GROUP_ANALYSIS_WITH_PLUGIN: _on_began_group_analysis_with_plugin,
    Event.GROUP_ANALYSIS_WITH_PLUGIN_SUCCESS: _on_group_analysis_with_plugin_success,
    Event.GROUP_ANALYSIS_WITH_PLUGIN_FAILURE: _on_group_analysis_with_plugin_failure,

    Event.TESTING_COMPLETED: _on_testing_completed,
}

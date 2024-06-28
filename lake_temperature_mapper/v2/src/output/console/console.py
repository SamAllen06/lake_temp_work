from sys import stderr

from output import FileSystemTree #TODO: Refactor analysis events to avoid this.
from output.console import console_utils
from output.console.ansi_code import AnsiCode
from output.events import Event, event_bus


def _on_loading_binary(binary_name: str) -> None:
    print(f"Loading Binary: {binary_name}...", end="")


def _on_binary_load_success() -> None:
    console_utils.clear_line()
    console_utils.print_ansi("Successfully loaded binary.\n", AnsiCode.BRIGHT_GREEN)


def _on_binary_load_failure(reason: Exception) -> None:
    console_utils.clear_line()
    print(
        console_utils.with_ansi(
            f"Failed to load binary due to {type(reason).__name__}.",
            AnsiCode.BRIGHT_RED
        ),
        file=stderr
    )
    console_utils.print_ansi(str(reason) + "\n", AnsiCode.BRIGHT_RED, file=stderr)


def _on_began_loading_sampling_plugins() -> None:
    print("Loading sampling plugins:")


def _on_loading_plugin(plugin_name: str) -> None:
    print(f"\t[{plugin_name}]: Loading...", end="")


def _on_plugin_load_success(plugin_name: str) -> None:
    console_utils.clear_line()
    console_utils.print_ansi(f"\t[{plugin_name}]: Loaded", AnsiCode.BRIGHT_GREEN)


def _on_plugin_load_failure(plugin_name: str, reason: Exception) -> None:
    console_utils.clear_line()
    console_utils.print_ansi(
        f"\t[{plugin_name}]: Load Failed ({type(reason).__name__})",
        AnsiCode.BRIGHT_RED
    )


def _on_sampling_plugins_load_success(count: int) -> None:
    print(f"\nLoaded {count} sampling plugins successfully.\n")


def _on_sampling_plugins_load_failure() -> None:
    console_utils.print_ansi(
        "\nAll sampling plugins failed to load, exiting...\n",
        AnsiCode.BRIGHT_RED,
        file=stderr
    )


def _on_began_loading_analysis_plugins() -> None:
    print("Loading analysis plugins:")


def _on_analysis_plugins_load_success(count: int) -> None:
    print(f"\nLoaded {count} analysis plugins successfully.\n")


def _on_analysis_plugins_load_failure() -> None:
    console_utils.print_ansi(
        "\nAll analysis plugins failed to load, exiting...\n",
        AnsiCode.BRIGHT_RED,
        file=stderr
    )


def _on_began_sample_generation() -> None:
    print("Sampling from plugins:")


def _on_began_sampling_from_plugin(plugin_name: str) -> None:
    print(f"\t[{plugin_name}]: Sampling...", end="")


def _on_sampling_from_plugin_success(
        plugin_name: str,
        group_sample_counts: dict[str, int]
) -> None:
    console_utils.clear_line()
    console_utils.print_ansi(f"\t[{plugin_name}]:", AnsiCode.BRIGHT_GREEN)

    group_lines = [
        f"\t\t({name}): {group_sample_counts[name]} samples"
        for name in group_sample_counts
    ]

    print("\n".join(group_lines))

    group_count = len(group_sample_counts)
    sample_count = sum(group_sample_counts.values())

    print(f"\t\tTotal: {group_count} groups, {sample_count} samples\n")


def _on_sampling_from_plugin_failure(plugin_name: str, reason: Exception) -> None:
    console_utils.clear_line()
    console_utils.print_ansi(
        f"\t[{plugin_name}]: Sampling Failed ({type(reason).__name__})",
        AnsiCode.BRIGHT_RED
    )


def _on_sampling_from_plugins_success(group_count: int, sample_count: int) -> None:
    print(f"\tGrand Total: {group_count} groups, {sample_count} samples\n")


def _on_sampling_from_plugins_failure() -> None:
    console_utils.print_ansi("Sampling failed. Exiting...", AnsiCode.BRIGHT_RED)


def _on_began_timing_binary(binary_name: str) -> None:
    print(f"Timing {binary_name}...", end="")


def _on_timing_binary_success(seconds_estimate: float) -> None:
    formatted_estimate = _format_estimate(seconds_estimate)

    console_utils.clear_line()
    print(f"Time estimated: {formatted_estimate}")
    _prompt_to_continue_with_testing()


def _format_estimate(seconds_estimate: float) -> str:
    rounded_seconds = round(seconds_estimate)

    days = int(rounded_seconds / 86400)
    rounded_seconds -= days * 86400

    hours = int(rounded_seconds / 3600)
    rounded_seconds -= hours * 3600

    minutes = int(rounded_seconds / 60)
    rounded_seconds -= minutes * 60

    return f"{days}:{hours}:{minutes}:{rounded_seconds}"


def _on_timing_binary_failure(exit_code: int) -> None:
    console_utils.print_ansi(
        f"Timing estimate failed because binary exited with code {exit_code}",
        AnsiCode.BRIGHT_RED
    )
    _prompt_to_continue_with_testing()


def _prompt_to_continue_with_testing() -> None:
    print("Would you like to continue? (Yes/No)")


def _on_began_sampling_from_group(
        group_name: str,
        group_index: int,
        group_count: int
) -> None:
    print(f"\nGroup {group_index + 1} / {group_count}: {group_name}\n")


def _on_sample_generated(
        sample_index: int,
        sample_count: int,
        values: dict[str, float]
) -> None:
    print(f"Sample {sample_index + 1} / {sample_count}:")
    for variable, value in values.items():
        print(f"\t{variable}: {value}")

    print("")


def _on_running_binary(binary_name: str) -> None:
    print(f"Running {binary_name}...", end="")


def _on_binary_exited(exit_code: int) -> None:
    console_utils.clear_line()
    if exit_code:
        console_utils.print_ansi(
            f"Binary exited with code {exit_code}\n", AnsiCode.BRIGHT_RED
        )
    else:
        console_utils.print_ansi("Binary ran successfully.\n", AnsiCode.BRIGHT_GREEN)


def _on_began_sample_analysis() -> None:
    print("Sample Analysis:")


def _on_began_analysis_with_plugin(plugin_name: str) -> None:
    print(f"\t[{plugin_name}]: Analyzing...", end="")


def _on_analysis_with_plugin_success(
        plugin_name: str,
        console_output: str,
        file_output: FileSystemTree
) -> None:
    console_utils.clear_line()
    console_utils.print_ansi(f"\t[{plugin_name}]:", AnsiCode.BRIGHT_GREEN)
    console_utils.print_indented(console_output, 2)
    print("")


def _on_analysis_with_plugin_failure(
        plugin_name: str,
        reason: Exception
) -> None:
    console_utils.clear_line()
    console_utils.print_ansi(
        f"\t[{plugin_name}]: Analysis Failed ({type(reason).__name__})\n",
        AnsiCode.BRIGHT_RED
    )


def _on_began_group_analysis() -> None:
    print("Group Analysis:")


def _on_testing_completed() -> None:
    print("Testing completed.")


_EVENT_FUNCTIONS = {
    Event.LOADING_BINARY: _on_loading_binary,
    Event.BINARY_LOAD_SUCCESS: _on_binary_load_success,
    Event.BINARY_LOAD_FAILURE: _on_binary_load_failure,

    Event.BEGAN_LOADING_SAMPLING_PLUGINS: _on_began_loading_sampling_plugins,
    Event.LOADING_SAMPLING_PLUGIN: _on_loading_plugin,
    Event.SAMPLING_PLUGIN_LOAD_SUCCESS: _on_plugin_load_success,
    Event.SAMPLING_PLUGIN_LOAD_FAILURE: _on_plugin_load_failure,
    Event.SAMPLING_PLUGINS_LOAD_SUCCESS: _on_sampling_plugins_load_success,
    Event.SAMPLING_PLUGINS_LOAD_FAILURE: _on_sampling_plugins_load_failure,

    Event.BEGAN_LOADING_ANALYSIS_PLUGINS: _on_began_loading_analysis_plugins,
    Event.LOADING_ANALYSIS_PLUGIN: _on_loading_plugin,
    Event.ANALYSIS_PLUGIN_LOAD_SUCCESS: _on_plugin_load_success,
    Event.ANALYSIS_PLUGIN_LOAD_FAILURE: _on_plugin_load_failure,
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
    Event.BEGAN_SAMPLE_ANALYSIS_WITH_PLUGIN: _on_began_analysis_with_plugin,
    Event.SAMPLE_ANALYSIS_WITH_PLUGIN_SUCCESS: _on_analysis_with_plugin_success,
    Event.SAMPLE_ANALYSIS_WITH_PLUGIN_FAILURE: _on_analysis_with_plugin_failure,

    Event.BEGAN_GROUP_ANALYSIS: _on_began_group_analysis,
    Event.BEGAN_GROUP_ANALYSIS_WITH_PLUGIN: _on_began_analysis_with_plugin,
    Event.GROUP_ANALYSIS_WITH_PLUGIN_SUCCESS: _on_analysis_with_plugin_success,
    Event.GROUP_ANALYSIS_WITH_PLUGIN_FAILURE: _on_analysis_with_plugin_failure,

    Event.TESTING_COMPLETED: _on_testing_completed,
}


def enable():
    for event in _EVENT_FUNCTIONS:
        event_bus.subscribe(event, _EVENT_FUNCTIONS[event])

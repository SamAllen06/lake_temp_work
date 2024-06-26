from sys import stderr

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


def _on_loading_sampling_plugin(plugin_name: str) -> None:
    print(f"\t[{plugin_name}]: Loading...", end="")


def _on_sampling_plugin_load_success(plugin_name: str) -> None:
    console_utils.clear_line()
    console_utils.print_ansi(f"\t[{plugin_name}]: Loaded", AnsiCode.BRIGHT_GREEN)


def _on_sampling_plugin_load_failure(plugin_name: str, reason: Exception) -> None:
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


_EVENT_FUNCTIONS = {
    Event.LOADING_BINARY: _on_loading_binary,
    Event.BINARY_LOAD_SUCCESS: _on_binary_load_success,
    Event.BINARY_LOAD_FAILURE: _on_binary_load_failure,

    Event.BEGAN_LOADING_SAMPLING_PLUGINS: _on_began_loading_sampling_plugins,
    Event.LOADING_SAMPLING_PLUGIN: _on_loading_sampling_plugin,
    Event.SAMPLING_PLUGIN_LOAD_SUCCESS: _on_sampling_plugin_load_success,
    Event.SAMPLING_PLUGIN_LOAD_FAILURE: _on_sampling_plugin_load_failure,
    Event.SAMPLING_PLUGINS_LOAD_SUCCESS: _on_sampling_plugins_load_success,
    Event.SAMPLING_PLUGINS_LOAD_FAILURE: _on_sampling_plugins_load_failure,
}


def enable():
    for event in _EVENT_FUNCTIONS:
        event_bus.subscribe(event, _EVENT_FUNCTIONS[event])

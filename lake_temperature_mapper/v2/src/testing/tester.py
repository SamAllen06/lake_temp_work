from configparser import ConfigParser
from pathlib import Path
import sys

from output.events import Event, event_bus
from root import APP_ROOT
from sampling import SamplerLoader
from testing.binary_runner import BinaryRunner


class Tester:
    def __init__(self, config_path: Path):
        self._config = ConfigParser()
        self._config.read(config_path)

        self._binary_runner = BinaryRunner()
        self._sampler_loader = SamplerLoader()

    def begin(self) -> None:
        self._load_binary()
        self._load_sampling_plugins()

    def _load_binary(self) -> None:
        binary_path = APP_ROOT / self._config["Model"]["binary"]
        binary_name = binary_path.name

        event_bus.fire_event(Event.LOADING_BINARY, binary_name=binary_name)

        try:
            self._binary_runner.load_binary(binary_path)
        except FileNotFoundError as error:
            event_bus.fire_event(Event.BINARY_LOAD_FAILURE, reason=error)
            sys.exit(1)

        event_bus.fire_event(Event.BINARY_LOAD_SUCCESS)

    def _load_sampling_plugins(self) -> None:
        event_bus.fire_event(Event.BEGAN_LOADING_SAMPLING_PLUGINS)

        self._sampler_loader.load_sampling_plugins()

        plugins_loaded = self._sampler_loader.get_sampling_plugins_loaded_count()

        if not plugins_loaded:
            event_bus.fire_event(Event.SAMPLING_PLUGINS_LOAD_FAILURE)
            sys.exit(1)

        event_bus.fire_event(Event.SAMPLING_PLUGINS_LOAD_SUCCESS, count=plugins_loaded)

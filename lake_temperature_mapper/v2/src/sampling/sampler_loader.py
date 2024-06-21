import importlib
from output.events import Event, event_bus
import pkgutil
from sampling import Sampler
import sampling_plugins
import sys


class SamplerLoader:
    def __init__(self):
        self._samplers = []
        self._plugin_names = []

    def load_sampling_plugins(self) -> None:
        plugin_module_names = self._discover_sampling_plugins()

        for plugin_module_name in plugin_module_names:
            plugin_display_name = self._generate_plugin_display_name(plugin_module_name)

            event_bus.fire_event(
                Event.LOADING_SAMPLING_PLUGIN, plugin_name=plugin_display_name
            )

            try:
                sampler = self._load_sampling_plugin(plugin_module_name)
            except Exception as error:
                event_bus.fire_event(
                    Event.SAMPLING_PLUGIN_LOAD_FAILURE,
                    plugin_name=plugin_display_name,
                    reason=error,
                )
                continue

            self._samplers.append(sampler)
            self._plugin_names.append(plugin_display_name)

            event_bus.fire_event(
                Event.SAMPLING_PLUGIN_LOAD_SUCCESS, plugin_name=plugin_display_name
            )

    def get_sampling_plugins_loaded_count(self) -> int:
        return len(self._samplers)

    def _discover_sampling_plugins(self) -> list[str]:
        return [
            plugin.name for plugin in pkgutil.iter_modules(sampling_plugins.__path__)
        ]

    def _load_sampling_plugin(self, plugin_module_name: str) -> Sampler:
        plugin_module = importlib.import_module(
            f"{sampling_plugins.__name__}.{plugin_module_name}"
        )

        PluginSampler = getattr(plugin_module, "sampler_class")
        return PluginSampler()

    def _generate_plugin_display_name(self, plugin_module_name: str) -> str:
        words = plugin_module_name.split("_")
        words = [word.capitalize() for word in words]
        return " ".join(words)

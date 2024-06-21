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

    def load_sampler_plugins(self) -> None:
        event_bus.fire_event(Event.BEGAN_LOADING_SAMPLING_PLUGINS)

        plugin_module_names = [
            plugin.name for plugin in pkgutil.iter_modules(sampling_plugins.__path__)
        ]

        for plugin_module_name in plugin_module_names:
            plugin_display_name = self._generate_plugin_display_name(plugin_module_name)

            event_bus.fire_event(
                Event.LOADING_SAMPLING_PLUGIN, plugin_name=plugin_display_name
            )

            plugin_module = importlib.import_module(
                f"{sampling_plugins.__name__}.{plugin_module_name}"
            )

            try:
                PluginSampler = getattr(plugin_module, "sampler_class")
                sampler = PluginSampler()
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

        if not self._samplers:
            event_bus.fire_event(Event.SAMPLING_PLUGINS_LOAD_FAILURE)
            sys.exit(1)

        event_bus.fire_event(
            Event.SAMPLING_PLUGINS_LOAD_SUCCESS, count=len(self._samplers)
        )

    def _generate_plugin_display_name(self, plugin_module_name: str) -> str:
        words = plugin_module_name.split("_")
        words = [word.capitalize() for word in words]
        return " ".join(words)

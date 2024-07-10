import importlib
from output.events import Event, event_bus
import pkgutil
from root import SOURCE_ROOT
from sampling import Sampler, SampleGroup
import sys

from plugin_loading.plugin_loader import PluginLoader
import sampling_plugins

PLUGINS_MODULE_NAME = "sampling_plugins"
PLUGIN_CLASS_ATTRIBUTE = "sampler_class"

UNIQUE_GROUP_NAME_FORMAT = "{sampler}:{name}"


class SamplerLoader(PluginLoader):
    def __init__(self):
        super().__init__([Sampler])

    def load_plugins(self) -> None:
        self._load_plugins_in_module(PLUGINS_MODULE_NAME, PLUGIN_CLASS_ATTRIBUTE)

    def sample_from_plugins(self) -> dict[str, SampleGroup]:
        sample_groups: dict[str, SampleGroup] = {}
        samplers = self._plugin_objects[Sampler]

        for plugin_name in samplers:
            sampler = samplers[plugin_name]
            event_bus.fire_event(
                Event.BEGAN_SAMPLING_FROM_PLUGIN,
                plugin_name=plugin_name
            )

            try:
                sampler_sample_groups = sampler.get_sample_groups()
            except Exception as error:
                event_bus.fire_event(
                    Event.SAMPLING_FROM_PLUGIN_FAILURE,
                    plugin_name=plugin_name,
                    reason=error
                )

            self._add_new_sample_groups(
                sample_groups,
                sampler_sample_groups,
                plugin_name
            )

            group_sample_counts = {
                group_name: sampler_sample_groups[group_name].get_sample_count()
                for group_name in sampler_sample_groups
            }

            event_bus.fire_event(
                Event.SAMPLING_FROM_PLUGIN_SUCCESS,
                plugin_name=plugin_name,
                group_sample_counts=group_sample_counts
            )

        return sample_groups

    def _add_new_sample_groups(
            self,
            current_sample_groups: dict[str, SampleGroup],
            new_sample_groups: dict[str, SampleGroup],
            plugin_name: str
    ) -> None:
        for group_name in new_sample_groups:
            if group_name not in current_sample_groups:
                current_sample_groups[group_name] = new_sample_groups[group_name]
                continue

            unique_name = UNIQUE_GROUP_NAME_FORMAT.format(
                sampler=plugin_name,
                name=group_name
            )

            current_sample_groups[unique_name] = new_sample_groups[group_name]

    def _fire_loading_plugin_event(self, plugin_name: str) -> None:
        event_bus.fire_event(Event.LOADING_SAMPLING_PLUGIN, plugin_name=plugin_name)

    def _fire_plugin_load_failed_event(self, plugin_name: str, error: Exception) -> None:
        event_bus.fire_event(
            Event.SAMPLING_PLUGIN_LOAD_FAILURE,
            plugin_name=plugin_name,
            reason=error
        )

    def _fire_plugin_load_success_event(self, plugin_name: str) -> None:
        event_bus.fire_event(
            Event.SAMPLING_PLUGIN_LOAD_SUCCESS,
            plugin_name=plugin_name
        )


#class SamplerLoader:
#    def __init__(self):
#        self._samplers = []
#        self._plugin_names = []
#
#    def load_sampling_plugins(self) -> None:
#        plugin_module_names = plugin_loading.discover_plugins_in(PLUGIN_DIRECTORY)
#
#        for plugin_module_name in plugin_module_names:
#            plugin_display_name = self._generate_plugin_display_name(plugin_module_name)
#
#            event_bus.fire_event(
#                Event.LOADING_SAMPLING_PLUGIN, plugin_name=plugin_display_name
#            )
#
#            try:
#                sampler = self._load_sampling_plugin(plugin_module_name)
#            except Exception as error:
#                event_bus.fire_event(
#                    Event.SAMPLING_PLUGIN_LOAD_FAILURE,
#                    plugin_name=plugin_display_name,
#                    reason=error,
#                )
#                continue
#
#            self._samplers.append(sampler)
#            self._plugin_names.append(plugin_display_name)
#
#            event_bus.fire_event(
#                Event.SAMPLING_PLUGIN_LOAD_SUCCESS, plugin_name=plugin_display_name
#            )
#
#    def get_sampling_plugins_loaded_count(self) -> int:
#        return len(self._samplers)
#
#    def _load_sampling_plugin(self, plugin_module_name: str) -> Sampler:
#        plugin_module = importlib.import_module(
#            f"{sampling_plugins.__name__}.{plugin_module_name}"
#        )
#
#        PluginSampler = getattr(plugin_module, "sampler_class")
#        return PluginSampler()


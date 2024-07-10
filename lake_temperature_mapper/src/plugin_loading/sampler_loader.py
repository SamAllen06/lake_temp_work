import importlib
from output.events import Event, event_bus
import pkgutil
from root import SOURCE_ROOT
from sampling import Sampler, SampleGroup
import sys

from plugin_loading.plugin_loader import PluginLoader
import sampling_plugins

UNIQUE_GROUP_NAME_FORMAT = "{sampler}:{name}"


class SamplerLoader(PluginLoader):
    def __init__(self):
        super().__init__([Sampler], "sampling_plugins", "sampler_class")

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

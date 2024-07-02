from collections.abc import Mapping, Sequence
import importlib
from output.events import Event, event_bus
import pkgutil
import sys

from analysis import PerSampleAnalyzer, SampleGroupAnalyzer
from plugin_loader import PluginLoader
from sampling import SampleGroup
from util import Table

PLUGINS_MODULE_NAME = "analysis_plugins"
PLUGIN_CLASS_ATTRIBUTE = "analyzer_class"


class AnalyzerLoader(PluginLoader):
    def __init__(self):
        super().__init__([PerSampleAnalyzer, SampleGroupAnalyzer])

    def load_plugins(self) -> None:
        self._load_plugins_in_module(PLUGINS_MODULE_NAME, PLUGIN_CLASS_ATTRIBUTE)

    def any_sample_plugins_loaded(self) -> bool:
        return len(self._plugin_objects[PerSampleAnalyzer]) > 0

    def any_group_plugins_loaded(self) -> bool:
        return len(self._plugin_objects[SampleGroupAnalyzer]) > 0

    def run_sample_analysis(
            self,
            sample: Mapping[str, float],
            reference_data: Mapping[str, Sequence[float]],
            test_data: Mapping[str, Sequence[float]]
    ) -> None:
        for plugin_name, analyzer in self._plugin_objects[PerSampleAnalyzer].items():
            event_bus.fire_event(
                Event.BEGAN_SAMPLE_ANALYSIS_WITH_PLUGIN,
                plugin_name=plugin_name
            )

            try:
                console_out, file_out = analyzer.analyze_sample_data(
                    sample, reference_data, test_data
                )
                event_bus.fire_event(
                    Event.SAMPLE_ANALYSIS_WITH_PLUGIN_SUCCESS,
                    plugin_name=plugin_name,
                    console_output=console_out,
                    file_output=file_out
                )
            except Exception as error:
                event_bus.fire_event(
                    Event.SAMPLE_ANALYSIS_WITH_PLUGIN_FAILURE,
                    plugin_name=plugin_name,
                    reason=error
                )

    def run_group_analysis(
            self,
            sample_group: SampleGroup,
            data: Table
    ) -> None:
        for plugin_name, analyzer in self._plugin_objects[SampleGroupAnalyzer].items():
            event_bus.fire_event(
                Event.BEGAN_GROUP_ANALYSIS_WITH_PLUGIN,
                plugin_name=plugin_name
            )

            try:
                console_out, file_out = analyzer.analyze_sample_data(
                    sample_group, data
                )
                event_bus.fire_event(
                    Event.GROUP_ANALYSIS_WITH_PLUGIN_SUCCESS,
                    plugin_name=plugin_name,
                    console_output=console_out,
                    file_output=file_out
                )
            except Exception as error:
                event_bus.fire_event(
                    Event.GROUP_ANALYSIS_WITH_PLUGIN_FAILURE,
                    plugin_name=plugin_name,
                    reason=error
                )

    def _fire_loading_plugin_event(self, plugin_name: str) -> None:
        event_bus.fire_event(Event.LOADING_ANALYSIS_PLUGIN, plugin_name=plugin_name)

    def _fire_plugin_load_failed_event(self, plugin_name: str, error: Exception) -> None:
        event_bus.fire_event(
            Event.ANALYSIS_PLUGIN_LOAD_FAILURE,
            plugin_name=plugin_name,
            reason=error
        )

    def _fire_plugin_load_success_event(self, plugin_name: str) -> None:
        event_bus.fire_event(
            Event.ANALYSIS_PLUGIN_LOAD_SUCCESS,
            plugin_name=plugin_name
        )

import importlib
from output.events import Event, event_bus
import pkgutil
import sys

from analysis import PerSampleAnalyzer, SampleGroupAnalyzer
from plugin_loader import PluginLoader

PLUGINS_MODULE_NAME = "analysis_plugins"
PLUGIN_CLASS_ATTRIBUTE = "analyzer_class"


class AnalyzerLoader(PluginLoader):
    def __init__(self):
        super().__init__([PerSampleAnalyzer, SampleGroupAnalyzer])

    def load_plugins(self) -> None:
        self._load_plugins_in_module(PLUGINS_MODULE_NAME, PLUGIN_CLASS_ATTRIBUTE)

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

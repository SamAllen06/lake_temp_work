from abc import ABC, abstractmethod
from collections.abc import Sequence
import importlib
from pathlib import Path
from typing import Any

from root import SOURCE_ROOT


class PluginLoader(ABC):
    def __init__(
            self,
            acceptable_plugin_classes: Sequence[type],
            plugins_module_name: str,
            plugin_class_attribute: str
    ):
        self._plugin_objects: dict[type, dict[str, Any]] = {
            plugin_class: {} for plugin_class in acceptable_plugin_classes
        }
        self._plugins_module_name = plugins_module_name
        self._plugin_class_attribute = plugin_class_attribute

    def load_plugins(self) -> None:
        discovered_plugin_names = self._discover_plugins_in(
            SOURCE_ROOT / self._plugins_module_name
        )

        for plugin_name in discovered_plugin_names:
            plugin_display_name = self._generate_plugin_display_name(plugin_name)

            self._fire_loading_plugin_event(plugin_display_name)

            try:
                plugin_object, plugin_superclass = self._load_plugin(
                    plugin_name,
                    self._plugins_module_name,
                    self._plugin_class_attribute
                )
            except Exception as error:
                self._fire_plugin_load_failed_event(plugin_display_name, error)
                continue

            self._plugin_objects[plugin_superclass][plugin_display_name] = plugin_object
            self._fire_plugin_load_success_event(plugin_display_name)

    def get_total_plugins_loaded_count(self) -> int:
        count = 0;

        for plugin_class in self._plugin_objects:
            count += len(self._plugin_objects[plugin_class])

        return count

    @abstractmethod
    def _fire_loading_plugin_event(self, plugin_name: str) -> None:
        pass

    @abstractmethod
    def _fire_plugin_load_failed_event(self, plugin_name: str, error: Exception) -> None:
        pass

    @abstractmethod
    def _fire_plugin_load_success_event(self, plugin_name: str) -> None:
        pass

    def _discover_plugins_in(self, path: Path) -> list[str]:
        plugin_module_names: list[str] = []

        for plugin_path in path.iterdir():
            plugin_module_names.append(plugin_path.stem)

        return plugin_module_names

    def _generate_plugin_display_name(self, plugin_module_name: str) -> str:
        words = plugin_module_name.split("_")
        words = [word.capitalize() for word in words]
        return " ".join(words)

    def _load_plugin(
            self,
            plugin_name: str,
            plugins_module_name: str,
            plugin_class_attribute: str
    ) -> tuple[Any, type]:
        acceptable_classes = [plugin_class for plugin_class in self._plugin_objects]

        plugin_module = importlib.import_module(f"{plugins_module_name}.{plugin_name}")

        PluginClass = getattr(plugin_module, plugin_class_attribute)

        for acceptable_class in acceptable_classes:
            if issubclass(PluginClass, acceptable_class):
                plugin_superclass = acceptable_class
                break
        else:
            raise TypeError(
                f"{plugin_name}.{plugin_class_attribute} was expected to have a type "
                f"in {acceptable_classes}, but its type was {PluginClass.__name__}"
            )

        return (PluginClass(), plugin_superclass)




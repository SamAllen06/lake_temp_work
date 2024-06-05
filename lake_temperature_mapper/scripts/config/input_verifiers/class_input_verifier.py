import importlib
import importlib.util
from types import ModuleType

from config.input_verifiers.input_verifier import InputVerifier
from config.config_writer import ConfigWriter


class ClassInputVerifier(InputVerifier):
    def __init__(self, extends: type = object):
        self._extends = extends

    def verify_input(self, input: str) -> str | None:
        split_input = input.split(":")
        module_name = split_input[0]
        class_name = split_input[1]

        if not module_name or not class_name:
            return f"Format: [module]:[class]"

        if not importlib.util.find_spec(module_name):
            return f"Could not find module: {module_name}"

        module: ModuleType = importlib.import_module(module_name)

        try:
            loaded_class = getattr(module, class_name)
        except AttributeError:
            return f"Could not find class {class_name} in {module_name}"

        if not issubclass(loaded_class, self._extends):
            return f"{class_name} is not a subclass of {self._extends.__name__}"
    
        try:
            config_module: ModuleType = module.config
        except AttributeError:
            # Assume modules without a config don't need to be configured.
            return None
    
        config_writer = ConfigWriter(config_module)

        if config_writer.is_already_configured():
            return None

        print(f"\nNow configuring {module_name}")
        config_writer.configure_interactively()
        print(f"Done configuring {module_name}\n")

        return None


    def format_input(self, input: str) -> str:
        return input

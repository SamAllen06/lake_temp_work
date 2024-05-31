from pathlib import Path
from types import ModuleType
from typing import Mapping


class ConfigWriter:
    def __init__(self, config_module: ModuleType):
        self._file_path = config_module.FILE_PATH
        self._fields = config_module.FIELDS

    def is_already_configured(self) -> bool:
        return self._file_path.exists()

    def configure_interactively(self) -> None:
        selections = self._prompt_for_selections()
        self._write_config_file(selections)

    def _prompt_for_selections(self) -> Mapping[str, str]:
        selections = {}

        for field in self._fields:
            while True:
                field_input = input(field.prompt)

                error_message = field.verifier.verify_input(field_input)

                if error_message:
                    print(error_message)
                    continue

                selections[field.key] = field.verifier.format_input(field_input)
                break

        return selections

    def _write_config_file(self, selections: Mapping[str, str]) -> None:
        lines = []

        for key in selections.keys():
            lines.append(f"{key}: {str(selections[key])}\n")

        with open(self._file_path, "w") as config_file:
            config_file.writelines(lines)

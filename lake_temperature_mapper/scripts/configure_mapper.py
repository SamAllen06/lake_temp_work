from pathlib import Path
from typing import Mapping

from config.fields import FIELDS
from config.project_root import PROJECT_ROOT

CONFIG_FILE = PROJECT_ROOT / "config" / "mapper.conf"


def _prompt_for_selections() -> Mapping[str, str]:
    selections = {}

    for field in FIELDS:
        while True:
            field_input = input(field.prompt)

            error_message = field.verifier.verify_input(field_input)

            if error_message:
                print(error_message)
                continue

            selections[field.key] = field.verifier.format_input(field_input)
            break

    return selections


def _write_config_file(selections: Mapping[str, str]) -> None:
    lines = []

    for key in selections.keys():
        lines.append(f"{key}: {str(selections[key])}\n")

    with open(CONFIG_FILE, "w") as config_file:
        config_file.writelines(lines)



def main():
    selections = _prompt_for_selections()
    _write_config_file(selections)


if __name__ == "__main__":
    main()

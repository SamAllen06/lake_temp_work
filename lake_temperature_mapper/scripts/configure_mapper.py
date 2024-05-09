from pathlib import Path
from typing import Mapping

PARENT = Path(__file__).resolve().parent
CONFIG_FILE = PARENT / "config" / "mapper.conf"
KEYS = [
    "binary_path",
    "range_path",
    "params_path",
    "ref_output",
    "test_output"
]
KEY_PROMPTS = [
    "binary to test",
    "range file",
    "parameters file",
    "reference output file",
    "test output file"
]


def _prompt_for_selections() -> Mapping[str, Path]:
    selections = {}

    for key, key_file_name in zip(KEYS, KEY_PROMPTS):
        while True:
            input_path = input(f"Please enter the path to the {key_file_name}: ")

            path = Path.cwd() / input_path

            if path.exists() and path.is_file():
                selections[key] = path.relative_to(PARENT, walk_up=True)
                break

            print(f"Could not find file at {str(path)}")

    return selections


def _write_config_file(selections: Mapping[str, Path]) -> None:
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

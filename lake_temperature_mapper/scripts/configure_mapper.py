from pathlib import Path
from typing import Mapping

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "mapper.conf"
KEY_INFO = [
    ("binary_path", "binary to test", True, True),
    ("range_path", "range file", True, True),
    ("params_path", "parameters file", True, True),
    ("defaults_path", "parameter defaults file", True, True),
    ("ref_output", "reference output file", True, True),
    ("test_output", "test output file", False, True),
    ("order_directory", "order directory", True, False),
]


def _prompt_for_selections() -> Mapping[str, Path]:
    selections = {}

    for key, key_prompt, must_exist, is_file in KEY_INFO:
        while True:
            input_path = input(f"Please enter the path to the {key_prompt}: ")

            path = Path.cwd() / input_path

            if must_exist and not path.exists():
                print(f"Could not find {str(path)}")
                continue

            if path.exists() and not path.is_file() == is_file:
                print(f"{str(path)} is not a "
                    f"{'file' if is_file else 'directory'}.")
                continue

            selections[key] = path.relative_to(PROJECT_ROOT)
            break

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

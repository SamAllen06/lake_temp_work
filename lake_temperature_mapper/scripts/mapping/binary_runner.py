from pathlib import Path
import subprocess
import sys


class BinaryRunner:
    def __init__(self, binary_path: Path):
        self._binary_path = Path(binary_path)

    def run_binary(self) -> None:
        text_files_directory = self._binary_path.parent
        output = subprocess.run(
            self._binary_path,
            capture_output=True,
            text=True,
            cwd=text_files_directory
        )

        # "output" can later be used to access stdout and stderr output from
        # the binary.

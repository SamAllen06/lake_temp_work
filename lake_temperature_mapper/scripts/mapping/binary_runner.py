from pathlib import Path
import shlex
import subprocess
import sys


class BinaryRunner:
    def __init__(self, binary_path: Path, binary_args: str):
        self._binary_path = Path(binary_path)
        self._binary_args = shlex.split(binary_args)

    def run_binary(self) -> None:
        text_files_directory = self._binary_path.parent
        output = subprocess.run(
            [self._binary_path] + self._binary_args,
            capture_output=True,
            text=True,
            cwd=text_files_directory
        )

        # "output" can later be used to access stdout and stderr output from
        # the binary.

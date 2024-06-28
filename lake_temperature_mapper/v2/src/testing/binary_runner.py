from pathlib import Path
import shlex
import subprocess
import sys


class BinaryRunner:
    def __init__(self):
        self._binary_path = None
        self._binary_args = []

    def get_binary_name(self) -> str:
        return self._binary_path.name

    def load_binary(self, binary_path: Path, binary_args: str = "") -> None:
        if not binary_path.exists():
            raise FileNotFoundError(f"Unable to find binary: {binary_path}")
        self._binary_path = binary_path
        self._binary_args = shlex.split(binary_args)

    def run_binary(self) -> int:
        if self._binary_path == None:
            raise FileNotFoundError("No binary loaded, call load_binary first")

        binary_directory = self._binary_path.parent
        output = subprocess.run(
            [str(self._binary_path)] + self._binary_args,
            capture_output=True,
            text=True,
            cwd=binary_directory,
        )

        return output.returncode

from pathlib import Path
import subprocess
import sys


class BinaryRunner:
    def __init__(self, binary_path: Path):
        self.binary_path = Path(binary_path)
        self._validate_path()

    def _validate_path(self):
        if not self.binary_path.exists():
            raise FileNotFoundError(
                "Could not find file " + str(self.binary_path)
            )

    def run(self):
        output = subprocess.run(
            self.binary_path,
            capture_output=True,
            text=True,
            cwd=self.binary_path.parent)

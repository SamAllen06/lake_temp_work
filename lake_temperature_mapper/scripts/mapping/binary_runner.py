from pathlib import Path
import subprocess


class BinaryRunner:
    def __init__(self, binary_path: str):
        self.binary_path = Path(binary_path)
        self._validate_path()

    def _validate_path(self):
        if not self.binary_path.exists():
            raise FileNotFoundError(
                "Could not find file " + str(self.binary_path)
            )

    def run(self):
        subprocess.Popen(str(self.binary_path))

from pathlib import Path

from config.input_verifier import InputVerifier

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class PathInputVerifier(InputVerifier):
    DOES_NOT_EXIST_MESSAGE = "Could not find {path}"
    WRONG_TYPE_MESSAGE = "{path} is not a {expected_type}."
    

    def __init__(self, must_exist: bool, is_file: bool):
        self._must_exist = must_exist
        self._is_file = is_file

    def verify_input(self, input: str) -> str | None:
        path = Path.cwd() / input

        if self._must_exist and not path.exists():
            return self.DOES_NOT_EXIST_MESSAGE.format(path=path)
        
        if path.exists() and not self._is_file == path.is_file():
            return self.WRONG_TYPE_MESSAGE.format(
                path=path,
                expected_type="file" if self._is_file else "directory"
            )

    def format_input(self, input: str) -> str:
        path = Path.cwd() / input
        return str(path.resolve().relative_to(PROJECT_ROOT))



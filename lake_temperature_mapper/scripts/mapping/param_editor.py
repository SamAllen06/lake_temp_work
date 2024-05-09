import os

class ParamEditor:
    def __init__(self, file_path: os.PathLike):
        self.file_path = file_path

    def modify_parameter(self, parameter: str, value: float):
        with open(self.file_path, "r") as file:
            lines = file.readlines()

        for index, line in enumerate(lines):
            if line.strip() == parameter:
                lines[index + 1] = str(value) + "\n"
                break
        else:
            raise KeyError(
                f"Could not find parameter \"{parameter}\" in {self.file_path}."
            )

        with open(self.file_path, "w") as file:
            file.writelines(lines)

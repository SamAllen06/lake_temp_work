from collections.abc import Sequence
from io import StringIO


def convert_to_txt_data(data: Sequence[str]) -> StringIO:
    file_data = StringIO()
    file_data.writelines([f"{line}\n" for line in data])
    return file_data

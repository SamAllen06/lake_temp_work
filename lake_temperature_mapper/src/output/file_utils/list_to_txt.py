from collections.abc import Sequence
from io import StringIO


def convert_to_txt_data(data: Sequence[str]) -> StringIO:
    file_data = StringIO()
    file_data.write("\n".join(data))
    return file_data

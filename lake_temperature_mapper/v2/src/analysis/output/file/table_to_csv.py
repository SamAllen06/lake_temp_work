import csv
from io import StringIO

from util import Table


def convert_to_csv_data(data: Table) -> StringIO:
    data_mapping = data.as_mapping()
    data_sequence = data.as_sequence()
    key_order = [key for key in data_mapping]

    csv_file = StringIO(newline="")
    csv_writer = csv.writer(csv_file)

    key_strings = [str(key) for key in key_order]
    csv_writer.writerow(key_strings)

    for row_mapping in data_sequence:
        row_sequence = [row_mapping[key] for key in key_order]
        csv_writer.writerow(row_sequence)

    return csv_file



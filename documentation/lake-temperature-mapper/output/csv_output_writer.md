# CSV Output Writer (csv_output_writer.py)

## Purpose
Writes mapping data to a CSV file in a specified directory.

## Functionality
Csv files are named after the order they represent the data for. Each file is 
written to after its respective order completes, meaning, if the program were
interupted in the middle of an order, all previous orders would be stored, but
the current one would not.

Rows are created in this format:
```
[input_parameter_name] [input_parameter_value1]
[output_variable_name1]
[reference_value1] [test_value1] [difference1] [index1]
[reference_value2] [test_value2] [difference2] [index2]
...
[reference_valueN] [test_valueN] [differenceN] [indexN]
[output_variable_name2]
[reference_value1] [test_value1] [difference1] [index1]
[reference_value2] [test_value2] [difference2] [index2]
...
[reference_valueN] [test_valueN] [differenceN] [indexN]
...
[output_variable_nameN]
[reference_value1] [test_value1] [difference1] [index1]
[reference_value2] [test_value2] [difference2] [index2]
...
[reference_valueN] [test_valueN] [differenceN] [indexN]
...
```

If the binary crashes, the differences are replaced with this row:
```
EXIT [exit_code]
```

These rows are passed to Python's csv module to write to the file, so specific
details about the csv have been left out of the above format.

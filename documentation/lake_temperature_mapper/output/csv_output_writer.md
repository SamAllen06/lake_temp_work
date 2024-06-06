# CSV Output Writer (csv_output_writer.py)

## Purpose
Writes mapping data to a CSV file in a specified directory.

## Functionality
Csv files are named after the sample group that they represent the data for. 
Each file is written to after its respective sample group has been fully tested,
meaning, if the program were interrupted in the middle of testing the samples of
a group, all previous groups' output would be stored, but the current group
would not store any output.

Rows are created in this format:
```
[input_parameter1_name] [input_parameter1_value1]
[input_parameter2_name] [input_parameter2_value1]
...
[input_parameterN_name] [input_parameterN_value1]
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
details about the csv have been left out of this documentation.

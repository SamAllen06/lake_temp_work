# Output File Data (output_file_data.py)

## Purpose
Stores and compares data from a unit test output file.

## Functionality
Reads an output file in the following format:

```
parameter1
    num1 num2 ... numN
parameter2
    num1 num2 ... numN
...
parameterN
    num1 num2 ... numN
```

Compares the current OutputFileData to another OutputFileData, returning a list
of OutputDifference(s) for each output variable.

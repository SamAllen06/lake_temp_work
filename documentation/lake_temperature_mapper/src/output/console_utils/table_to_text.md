# Table to Text 
APP/src/output/console_utils/table_to_text.py

## Purpose
Table to text is a module that converts a [Table](../../util/table.md) into
text that can be printed to a console.

## Example
```
>>> from util import Table
>>> from output.console_utils import table_to_text
>>> 
>>> table = Table({}, [])
>>> table_mapping = table.as_mapping()
>>> table_mapping["a"] = [1, 2, 3]
>>> table_mapping["b"] = [2, 3, 4]
>>> table_mapping["c"] = [3, 4, 5]
>>> 
>>> table_text = table_to_text.convert_to_text(table)
>>> print(table_text)
a   b   c   
1   2   3   
2   3   4   
3   4   5   
```

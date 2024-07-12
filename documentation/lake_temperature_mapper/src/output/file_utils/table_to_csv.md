# Table to CSV (APP/src/output/file_utils/table_to_csv.py)

## Purpose
Converts a [Table](../../util/table.md) to csv data using
[Python's csv module.](https://docs.python.org/3.10/library/csv.html)

## Example
```
>>> from output.file_utils import table_to_csv
>>> from util import Table
>>> 
>>> table = Table({}, [])
>>> table_mapping = table.as_mapping()
>>> 
>>> table_mapping["a"] = [1, 2, 3]
>>> table_mapping["b"] = [2, 3, 4]
>>> table_mapping["c"] = [3, 4, 5]
>>> 
>>> data = table_to_csv.convert_to_csv_data(table)
>>> 
>>> print(data.getvalue())
a,b,c
1,2,3
2,3,4
3,4,5

```

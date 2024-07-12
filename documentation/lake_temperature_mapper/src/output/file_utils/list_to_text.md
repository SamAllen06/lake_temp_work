# List to Text (APP/src/output/file_utils/list_to_text.py)

## Purpose
Converts a list of strings into a StringIO with each of strings on a new line.

## Example
```
>>> from output.file_utils import list_to_txt
>>> 
>>> lines = ["Hello", "World!"]
>>> data = list_to_txt.convert_to_txt_data(lines)
>>> 
>>> print(data.getvalue())
Hello
World!
```

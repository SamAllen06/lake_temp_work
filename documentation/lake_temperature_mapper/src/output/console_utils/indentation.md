# Indentation 
APP/src/output/console_utils/indentation.py

## Purpose
The indentation module includes functions to add indentation to text.

## Example
```
>>> from output.console_utils import indentation
>>> 
>>> text = "This is some text.\nIsn't it cool?"
>>> print(text)
This is some text.
Isn't it cool?
>>> indentation.print_indented(text, 1)
	This is some text.
	Isn't it cool?
```

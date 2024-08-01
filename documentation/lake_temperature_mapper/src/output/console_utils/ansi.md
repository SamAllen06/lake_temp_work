# Ansi 
APP/src/output/console_utils/ansi.py

## Purpose
The Ansi module includes functions to print and generate strings using ansi
escape sequences. This includes effects such as colors and
underlining, as well as clearing the current line. 

See [this Wikipedia article](https://en.wikipedia.org/wiki/ANSI_escape_code)
for more specific details.

## Examples
```
>>> from output.console_utils import ansi
>>>
>>> # These effects work in a console, but are not shown in the documentation. 
>>> # Print with color
>>> ansi.print_ansi_color("Hello!", ansi.AnsiColor.BRIGHT_YELLOW)
Hello!
>>> # Print with underline
>>> ansi.print_ansi_graphic("Hello again!", ansi.AnsiGraphic.UNDERLINE)
Hello again!
>>> # Clear and replace line, useful for "loading..." messages.
>>> print("Clear me!", end=""); ansi.reset_line(); print("Replacement text!")
Replacement text!
```

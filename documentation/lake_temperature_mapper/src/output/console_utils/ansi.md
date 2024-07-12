# Ansi (APP/src/output/console_utils/ansi.py)

## Purpose
The Ansi module includes functions to print and generate strings using ansi
escape sequences. This includes effects such as colors and
underlining, as well as clearing the current line. 

See [this Wikipedia article](https://en.wikipedia.org/wiki/ANSI_escape_code)
for more details.

## Examples
```
>>> from output.console_utils import ansi
>>> 
>>> # Print with color
>>> ansi.print_ansi_color("Hello!", ansi.AnsiColor.BRIGHT_YELLOW)
Hello! (Note: This text is yellow in a console, but not the documentation.)
>>> # Print with underline
>>> ansi.print_ansi_graphic("Hello again!", ansi.AnsiGraphic.UNDERLINE)
Hello again!
>>> # Clear and replace line
>>> print("Clear me!", end=""); ansi.reset_line(); print("Replacement text!")
Replacement text!
```

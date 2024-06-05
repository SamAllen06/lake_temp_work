# Class Input Verifier (class_input_verifier.py)

## Purpose

Accepts a module and a class contained by that module as input, and optionally
verifies that it is a subclass of a class specified in the constructor.

## Functionality

Takes input in the form `module:class`. This is then split into the module and 
class names using the colon as the delimiter. For the input to be accepted,
the script must be able to load the module, load the class from the module, and
the class must be a subclass of the class optionally specified in the
constructor. Additionally, if the module has a config submodule, the script will
create a ConfigWriter to configure it if it is not already configured.

Since the module is relative to the script directory, any valid input is already
formatted, and is stored as it was entered.

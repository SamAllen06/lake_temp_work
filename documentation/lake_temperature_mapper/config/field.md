# Field {field.py}

## Purpose
Stores information about a field in the mapper's configuration file.

## Functionality
Stores a key, prompt, and verifier. The key is the string that will be saved in
front of the user's input in the configuration file, the prompt is the text that
the user sees when they are asked to enter input for this field, and the
verifier is an InputVerifier, which is used to reject the user's input if it is
invalid, as well as to convert the user's input into the value that is stored in
the configuration file.

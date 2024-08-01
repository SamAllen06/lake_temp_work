# Command Line Interface
APP/src/cli.py

## Purpose
The CLI script acts as the interface between the user and the testing program.
It is also the sole entry point to the program.

## Functionality
The CLI is responsible for interpreting the arguments it receives to enable 
the program's views accordingly. Currently, it does not have any arguments, and
automatically enables all three views.

Additionally, the CLI prompts the user to confirm that, after seeing what
plugins were able to load and how long the testing process should take, they
still wish to continue with testing. If the user confirms, the CLI will tell
the [tester](tester.md) to begin testing.

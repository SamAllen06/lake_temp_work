# Command Line Interface (cli.py)

## Purpose
The CLI script acts as the interface between the user and our mapping scripts.
It is the sole entry point to the program, however, if another interface was
needed to replace it, it could.

## Functionality
CLI does not contain any functionality other than accepting user input and
executing mapping scripts accordingly. It should not be opening files, running
a binary, etc.

It can optionally accept an alternative configuration file, but defaults to
using scripts/config/mapper.conf

It also constructs a GroupOutputWriter, providing console and/or file output.

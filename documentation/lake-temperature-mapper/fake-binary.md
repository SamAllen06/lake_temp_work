# Fake Binary (fake_binary.exe)

## Purpose
Acts like elmtext.exe, but does not depend on anything in the docker image and
generates output using a simple, known function. This allows us to test our
mapping scripts, which will eventually be run on elmtext.exe, outside of the
docker image and with a known function.

fake_binary.exe is a C binary, *not* a Windows executable. elmtest.exe is a 
Fortran binary, but since both are compiled, our scripts can treat them the
same way.

## Functionality
fake_binary.exe currently outputs a line to stdout and stderr, allowing us to
to test output stream filtering. (For example, we may decide to disregard
output to stdout, as we don't want our mapping process to spam the console with
output, but perhapts we want to print or parse the output to stderr, because it
can contain important information about the program's response to certain
inputs.)

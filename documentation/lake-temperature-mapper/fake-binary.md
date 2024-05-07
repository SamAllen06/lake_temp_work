# Fake Binary (fake_binary.exe)

## Purpose
Acts like elmtext.exe, but does not depend on anything in the docker image and
generates output using a simple, known function. This allows us to test our
mapping scripts, which will eventually be run on elmtext.exe, outside of the
docker image and with a known function.

fake_binary.exe is a C binary, *not* a Windows executable. elmtest.exe is a 
Fortran binary, but since both are compiled languages, our scripts can treat
them the same way.

## Functionality
fake_binary.exe outputs a line to stdout and stderr, allowing us to
to test output stream filtering. (For example, we may decide to disregard
output to stdout, as we don't want our mapping process to spam the console with
output, but perhapts we want to print or parse the output to stderr, because it
can contain important information about the program's response to certain
inputs.)

Additionally, fake_binary reads in the values from lakeparams.txt and uses them
to compute outputs, which are stored in fake_LakeTemperatureTest.txt. The
outputs are computed as follows:

| Parameter     | First                 | Second                                  |
|---------------|-----------------------|-----------------------------------------|
|fakevar%sum    | sum of all inputs     | double the sum of all inputs            |
|favevar%product| product of all inputs | the square of the product of all inputs |

fake_LakeTemperatureRef.txt is the output file (fake_LakeTemperatureTest.txt)
from fake_binary when it is run on the default values in lakeparams.txt. It can
be used to note differences in outputs when it is compared to an output file
from a run with modified parameters. This is similar to how 
cpu_LakeTemperatureRef.txt and cpu_LakeTemperatureTest.txt will be compared by
our mapping scripts in the docker image.

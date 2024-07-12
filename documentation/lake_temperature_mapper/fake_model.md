# Fake Model (fake_model.exe)

## Purpose
Acts like elmtext.exe, but does not depend on the docker image environment and
generates output using a simple, known function. This allows us to test our
testing program, which will eventually be run on elmtext.exe, outside of the
docker image and with a known function.

fake_model.exe is a C binary, *not* a Windows executable. elmtest.exe is a 
Fortran binary, but since both are compiled languages, our program can treat
them the same way.

## Functionality
fake_model.exe outputs a line to stdout and stderr, allowing us to
to test output stream filtering. (For example, we may decide to disregard
output to stdout, as we don't want our testing process to spam the console with
output, but perhaps we want to print or parse the output to stderr, because it
can contain important information about the program's response to certain
inputs.)

Additionally, fake_model reads in the values from lakeparams.txt and uses them
to compute outputs, which are stored in fake_LakeTemperatureTest.txt. The
outputs are computed as follows:

```
key:
s = sum of all inputs
p = product of all inputs
```

| Parameter       | First Column | Second Column |
|-----------------|--------------|---------------|
| fakevar%sum     | s            | s * 2         |
| (Second Row)    | s * 0.1      | s * 0.5       |
| fakevar%product | p            | p * p         |
| (Second Row)    | p * s        | p * p * s     |

If any of the inputs is a zero, the model will exit with exit code 1. 
(Ensuring the testing program can handle the model crashing.)

fake_LakeTemperatureRef.txt is the output file (fake_LakeTemperatureTest.txt)
from fake_model when it is run on the default values in lakeparams.txt. It can
be used to note differences in outputs when it is compared to an output file
from a run with modified parameters. This is similar to how 
cpu_LakeTemperatureRef.txt and cpu_LakeTemperatureTest.txt will be compared by
our testing programs in the docker image.

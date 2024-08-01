# Fake Model
APP/fake_model/fake_model.exe

## Purpose
Has the same interface as elmtext.exe, but does not depend on the docker image
environment and generates output using known functions. This allows developers
to test Lake Temperature Mapper quickly without needing to enter the Docker
image.

It is important to note that fake_model.exe is a C executable, *not* a Windows
executable. elmtest.exe is a Fortran executable, but since both are compiled
languages, our program can treat them the same way.

## Functionality
fake_model.exe outputs lines to stdout and stderr, allowing us to test output
stream filtering. Currently, Lake Temperature Mapper ignores output from the
executable.

Additionally, fake_model reads in the values from lakeparams.txt and uses them
to compute outputs, which are then stored in fake_LakeTemperatureTest.txt. The
outputs are computed as follows:

```
key:
s = sum of all inputs
p = product of all inputs
```

| Parameter       | First Column | Second Column |
|-----------------|--------------|---------------|
| fakevar%sum     | s            | s * 2         |
|                 | s * 0.1      | s * 0.5       |
| fakevar%product | p            | p * p         |
|                 | p * s        | p * p * s     |

If any of the inputs is a zero, the model will exit with exit code 1. (This is
intentional.)

fake_LakeTemperatureRef.txt is the output file (fake_LakeTemperatureTest.txt)
from fake_model when it is run on the default values in lakeparams.txt. It can
be used to note differences in outputs when it is compared to an output file
from a run with modified parameters. This is equivilent to how
cpu_LakeTemperatureRef.txt and cpu_LakeTemperatureTest.txt are compared by
Lake Temperature Mapper in the docker image.

## Running Fake Model
1. Change directory to the fake_model directory
```
cd lake_temperature_mapper/fake_model/
```
2. Run the model
```
./fake_model.exe
```

## Compiling Fake Model
1. Change directory to the fake_model directory
```
cd lake_temperature_mapper/fake_model/
```
2. Run make
```
make
```
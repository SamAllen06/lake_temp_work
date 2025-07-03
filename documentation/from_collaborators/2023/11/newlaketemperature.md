# newlaketemperature.tar
Provided modifications to the elmtest executable that enable us to change constants used
by LakeTemperature. It is meant to be extracted inside the docker image provided at
[Docker4SPEL](https://github.com/daliwang/Docker4SPEL) (wangdl1108/docker4spel_demo).
Instructions for compiling elmtest for both the CPU version and GPU version are located
there. 

## Contents
newlaketemperature.tar contains the following files:

### LakeCon.F90
Update for LakeCon.F90 in the docker image (I believe it is responsible for setting the
constants we are changing.)

### Makefile
Update to the Makefile in the docker image

### ReadInputParamsMod.F90
Module that enables elmtest to read model constants from lakeparams.txt

### lakeparams.txt
The file containing values for constants that will be read by elmtest.

### main.F90
Update for main.F90 in the docker image.

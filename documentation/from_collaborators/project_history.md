# Project History
The purpose of this file is to document the history of our work on this project so that
people working on/reviewing our work in the future can have an understanding of the
current state of the project.


## Aidan takes over from Spencer - 03/27/2024
Prior to this point, Spencer Smith, Jayden Gillam, and Melody Hammel appear to have been
working on this project. To my (Aidan) knowledge, not much if anything was done before
this point, other than some files being provided. (See commit f25a7f7.) Additionally,
Spencer started work on a script to change the values in lakeparams.txt using user
input. This script was last updated on commit b8c788b and is not in use currently,
because the Model Testing Framework changes these automatically.

## elmtest compiled successfully for the first time - 04/03/2024
I was able to compile elmtest.exe for the first time, thanks to a new version of
[LakeTemperatureMod.F90](2024/04/LakeTemperatureMod.md) I was provided and a manual
modification to the Makefile. (It is also possible some additional modifications
were necessary. According to past me, I added "the if else that sets gpuflag", 
"commented out the stop", and added "the call to
update_vars_LakeTemperature(gpuflag, "Test") to main.F90". Keep in mind it must be run
with an argument (usually "1"). (This LakeTemperatureMod was updated again at the first
meeting because it didn't produce output. This older version isn't stored.)

## First meeting - 04/12/2024
This is when we first met with Dali and Peter to discuss this project. Specifically, the
current version of LakeTemperature I had compiled, but did not produce outputs, and so
the main goal of the meeting was to get output from elmtest. This is when I was given
the updated [LakeTemperatureMod.F90](2024/04/LakeTemperatureMod.md). (This one is
stored in our repository.)

## Dataset updated - 05/22/2024
The previous dataset, when run with the default constants, had differences from the
reference. We were originally told these were initialization values, but the values
didn't match what we'd expect to see for that (1.0E36 for floating points,
2147483647 for integers). In response, we were provided an updated LakeTemperature
without these differences
([update-LakeTemp-UnitTest.tar.gz](2024/05/update-LakeTemp-UnitTest.md)). All that is
required to compile this one is to extract it inside the docker image, enter the
LakeTemp directory, and run `make`.

## Second meeting - 05/30/2024
In this meeting, we demonstrated an earlier version of the Model Testing Framework
(originally named Lake Temperature Mapper). It was able to read "orders" that described
"line" and "box" samples to take, automatically set the constants in lakeparams.txt, and
compare the resulting output to the reference output. (The "orders" have since been
moved to the Order Sampling plugin, and the difference analysis was moved to the
Differences (analysis) plugin.)

## Output constraints provided - 06/27/2024
In a meeting with Dali and Peter, we discussed the idea of using combinatorial testing
to find and identify physically impossible values produced by elmtest. In order to do
so, we requested a list of constraints on the values of the outputs. We were given
[output-description.md](2024/06/output-description.md) for this purpose.

## Last commit before project paused - 08/01/2024
The commit 23571c8 was the last commit I (Aidan) made to the LakeTemperature project
before fully switching over to work on completing our work for the CyberWater project.

## First commit since project resumed - 06/18/2025
The commit cbec08a was the first commit since I (still Aidan) resumed work on the
project.

## model-testing-framework split off from lake_temp_work - 06/19/2025
The commit bd7e000 split the lake_temp_work into two. The model-testing-framework is for
work on the software we are using to test LakeTemperature, that, in the future, could be
used to test more modules of ELM. Everything that remains in lake_temp_work is specific
to our work on testing LakeTemperature. model-testing-framework has been added as a
submodule.

# Testing Process

This is a quick overview of how we partitioned the input space for combinatorial
testing, and how we validate the model output.

## Key Values

We've been provided the boundaries for the extremes of each constant. For boolean flags,
we just use true and false, since those are the only two possibilities anyways. For
integer and floating point constants, we linearly interpolate between the extremes in
order to generate 11 values. If we want, we can modify the values beyond the extremes
and see if we encounter limitations in the model on how far we can push those values.

## Test Oracle

We were provided two files from our collaborators, LakeTemperatureOutput and 
LakeTemperatureTestPlan. LakeTemperatureOutput provides physical boundaries for the
outputs, as well as simple aggreggation calculations, and overall things that can be
checked for every sample.

LakeTemperatureTestPlan provides test scenarios and ways we should expect the outputs
to change because of those inputs. For instance, if the lake is freezing, it should 
release latent heat and raise the sensible heat of the surrounding water/ice. We write
this as conditional checks that run only when at least one column matches the inputs
required for the scenario, and the check enforces that we see the expected behavior in
those specific columns.

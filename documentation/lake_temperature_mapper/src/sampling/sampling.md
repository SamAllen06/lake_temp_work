# Sampling
APP/src/sampling/

## Purpose
The sampling module serves as the interface between a sampling plugin and the
testing program.

Essentially, each sampling plugin must provide exactly one subclass of 
[Sampler](sampler.md) that returns a number of [SampleGroup(s).](sample_group.md)

See ["How To Create a Sampling Plugin"](../sampling_plugins/how_to_create_a_sampling_plugin.md)
for more details.

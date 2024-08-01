# Sampler
APP/sampling/sampler.py

## Purpose
Sampler is an abstract class requiring a get_sample_groups method which returns
a dictionary mapping each sample group's name to the [SampleGroup](sample_group.md)
object it is represented by.

Each sampling plugin must have exactly one subclass of Sampler, but that object
can return multiple [SampleGroup(s).](sample_group.md)

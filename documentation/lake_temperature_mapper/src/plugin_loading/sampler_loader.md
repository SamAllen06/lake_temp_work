# Sampler Loader (APP/src/plugin_loading/sampler_loader.py)

## Purpose
SamplerLoader is a subclass of [PluginLoader](plugin_loader.md) that loads
sampling plugins. It expects each plugin to have a "sampler_class" attribute,
which should contain a subclass of [Sampler](../sampling/sampler.md).

Additionally, it is able to collect [SampleGroup(s)](../sampling/sample_group.md)
from each plugin, and return them all in a dictionary mapping the name of the
group to the group itself.

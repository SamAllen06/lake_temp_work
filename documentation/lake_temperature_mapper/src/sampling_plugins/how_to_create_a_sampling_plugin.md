# How to create a sampling plugin

## Plugin Root Module
Each sampling plugin is to be contained inside a single module in the
sampling_plugins directory (single as in, there are no other modules for that
plugin in the sampling_plugins directory, however the plugin's module can be
a package.) This module will be referred to as the "plugin root module"
throughout this document.

## Naming
The name of the plugin root module will be used to determine the display name
of the plugin. All underscores will be replaced with spaces, and all words will
be capitalized. Thus, a plugin inside a module "my_sampling_plugin" will have
the display name "My Sampling Plugin".

## sampler_class Attribute
Each plugin must have a "sampler_class" attribute containing a reference to
a [Sampler](../sampling/sampler.md) subclass in the plugin. This class can
return one or more [SampleGroup(s),](../sampling/sample_group.md) which is how
the plugin is able to generate samples.

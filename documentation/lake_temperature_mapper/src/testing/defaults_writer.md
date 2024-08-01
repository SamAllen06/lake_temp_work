# Defaults Writer
APP/src/testing/defaults_writer.py

## Purpose
The DefaultsWriter class reads in a parameter defaults file (usually a copy of
the parameters file before it has been modified) and is able to write those
defaults to the parameters file on request. This serves a few
purposes. Firstly, it allows sampling plugins that generate incomplete samples
(samples that don't contain a value for each input parameter) to continue functioning,
since each parameter's value is reset to the default before a [SampleGroup](../sampling/sample_group.md)
begins. Secondly, it ensures that the parameters file will remain unchanged when 
testing is complete, as the defaults are written back to it when the program finishes.

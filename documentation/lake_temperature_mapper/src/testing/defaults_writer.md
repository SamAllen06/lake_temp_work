# Defaults Writer (APP/src/testing/defaults_writer.py)

## Purpose
The DefaultsWriter class reads in a parameter defaults file (usually a copy of
the parameters file before it has been modified) and is able to write those
defaults to the parameters file when instructed too. This serves a few
purposes. Firstly, it allows sampling plugins, like Order Sampling, that only
include values that should be changed since the last sample, to keep
functioning. These plugins can also assume that the parameters file will begin
with the default parameters, which this class ensures. Secondly, it ensures that
the parameters file will remain unchanged when testing is complete, as the
defaults are written back to it when the program finishes.

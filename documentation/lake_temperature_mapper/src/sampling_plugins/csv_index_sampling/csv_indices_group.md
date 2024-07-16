# CSV Indices Group (APP/src/sampling_plugins/csv_index_sampling/csv_indices_group.py)

## Purpose
CsvIndicesGroup is the CSV Index Sampling plugin's implementation of 
[SampleGroup.](../../sampling/sample_group.md) It reads in a csv file
containing indices that are used to linearly interpolate through ranges for
each of the parameters. See [CSV Index Sampling](csv_index_sampling.md) for an
example.

## Functionality
On instantiation, the CsvIndicesGroup will read its csv file, generating a
table of samples using indices. (The actual numbers written in the csv file.)
It will also keep track of the largest index in the file for each parameter.
Additionally, using this, it will generate a translation table. This table
includes lists of floating point values for each sample, treating index 0 as 
the lower bound specified in a parameter's range, and its largest index as the
upper bound. When the group is iterated through, it will convert each sample of
indices into a complete sample, containing a floating point value for each 
parameter, using the translation table. (This means the CsvIndicesGroup doesn't
have to recalculate where an index falls in its parameter's range, since that
value is stored in the translation table.)


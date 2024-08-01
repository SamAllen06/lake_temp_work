# CSV Indices Group
APP/src/sampling_plugins/csv_index_sampling/csv_indices_group.py

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
Additionally, treating the largest index it found as a parameter's upper bound
and index 0 as the parameter's lower bound, it will generate a lookup table.
This table a list of floating point values for each sample, meaning that
the CsvIndicesGroup does not have to repeat linear interpolation it has already
performed. When the group is iterated through, it will use the lookup table
to convert each sample of indices into a complete sample, containing a
floating point value for each parameter.

## Example
.csv file:
```
param1,param2,param3
0,1,0
1,0,2
2,1,3
```

Ranges file:
```
param1
0.0 - 1.0
param2
3.0 - 5.5
param3
1.0 - 2.5
```

Max Indices:
```
{param1: 2, param2: 1, param3: 3}
```

Lookup table:
```
{
    param1: [0.0, 0.5, 1.0],
    param2: [3.0, 5.5],
    param3: [1.0, 1.5, 2.0, 2.5],
}
```

Sample Group Contents:
```
[
    {param1: 0.0, param2: 5.5, param3: 1.0},
    {param1: 0.5, param2: 3.0, param3: 2.0},
    {param1: 1.0, param2: 5.5, param3: 2.5},
]
```
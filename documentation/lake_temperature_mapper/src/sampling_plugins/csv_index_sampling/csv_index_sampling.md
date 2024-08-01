# CSV Index Sampling
APP/src/sampling_plugins/csv_index_sampling/

## Purpose
The CSV Index Sampling plugin converts csv files containing indices (such as
those produced by ACTS) into [SampleGroup(s).](../../sampling/sample_group.md)
Each file contains a header of parameter names, and rows of indices under them.
These indices are used to linearly interpolate each parameter through a range
specified in another file.

## Example
This .csv file:
```
param1,param2
0,0
0,1
0,2
1,1
2,0
2,1
2,2
```
using this range file:
```
param1
0.0 - 1.0
param2
0.0 - 10.0
```
results in one sample group containing these samples:
```
{param1: 0.0, param2: 0.0}
{param1: 0.0, param2: 5.0}
{param1: 0.0, param2: 10.0}
{param1: 0.5, param2: 5.0}
{param1: 1.0, param2: 0.0}
{param1: 1.0, param2: 5.0}
{param1: 1.0, param2: 10.0}
```

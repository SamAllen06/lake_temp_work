# Sample Group (sample_group.py)

## Purpose

A sample group represents a group of samples to be tested. It is iterable, and
returns samples in the order that they should be tested. Samples are returned
in the format:
```
{"param": value, "param": value, ...}
```

A sample group must also be able to return the total count of samples it 
contains, as well as the minimum and maximum of each input parameter it changes.

# Output File Reader
APP/src/testing/output_file_reader.py

## Purpose
The OutputFileReader class reads in output data from the model and packages
it into a form that can be used by the analysis plugins.

## Functionality
OutputFileReader's public API consists of reading the reference data, reading
data for the most recent sample, and reading data for the most recent group.

### Reading Reference Data (get_reference_data)
Reference data is the data produced by the model when it is run using the 
default parameters. It is meant to be a baseline for comparing sample output.
This baseline is especially important to Lake Temperature, as we've set out to
analyze how each input parameter impacts the outputs, not simply analyze the
outputs independently. 

In OutputFileReader, since get_reference_data is called frequently despite the
reference data being constant, OutputFileReader reads the reference data once
when it is initialized and then stores it to respond to later requests.

### Reading Sample Test Data (read_sample_data)
Test data is the data produced by the model after it has run using a modified
parameters file. Sample test data is returned in the same format as the
reference data, but, unlike the reference data, it is read every time the
function is called. Additionally, this function has a side effect of adding the
sample's test data to the current group data.

### Reading Group Test Data (read_group_data)
Group test data is stored in a [Table](../util/table.md) using a dictionary as
its mapping and a [TransparentLayerList](../util/transparent_layer_list.md) as
its sequence. The base layer is always the reference data, meaning the
[TransparentLayerList(s)](../util/transparent_layer_list.md) only needs to
store test data in terms of how it differs from the reference data. (See the
documentation on [TransparentLayerList](../util/transparent_layer_list.md) for 
more details.)

Each sample's test data is added to the group data when read_sample_data is 
called. When read_group_data is called, it will return this table, then reset
the group data in preparation for the next [SampleGroup.](../sampling/sample_group.md)

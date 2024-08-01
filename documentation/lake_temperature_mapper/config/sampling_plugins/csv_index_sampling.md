# CSV Index Sampling 
APP/config/sampling_plugins/csv_index_sampling.ini

## Purpose
Configures the [CSV Index Sampling plugin.](../../src/sampling_plugins/csv_index_sampling/csv_index_sampling.md)

## Fields
All paths are relative to [APP_ROOT.](../../src/root.md)

| Field Name                | Type | Description                                                                     |
|---------------------------|:----:|---------------------------------------------------------------------------------|
| range_path                | Path | Path to the parameter ranges file (.txt) (Used as linear interpolation bounds.) |
| csv_index_files_directory | Path | Path to the directory containing the csv files storing the sample indices       |

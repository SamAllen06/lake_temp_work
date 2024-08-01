# CSV Index Sampler
APP/src/sampling_plugins/csv_index_sampling/csv_index_sampler.py

## Purpose
CSV Index Sampler is the [CSV Index Sampling](csv_index_sampling.md) plugin's
implementation of [Sampler](../../sampling/sampler.md). When loaded, it creates
the [RangeReader](../../sampling_libs/ranges/range_reader.md) that will be used
to read the range file. When sampled from, it assigns each csv file to its own
[CsvIndicesGroup](csv_indices_group.md).

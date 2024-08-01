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

## Example
Example Directory Structure (APP/src/sampling_plugins/example_plugin/):
```
example_plugin/
├── __init__.py
├── example_group.py
└── example_sampler.py
```

Contents of \_\_init__.py:
```python
from .example_sampler import ExampleSampler

sampler_class = ExampleSampler
```

Contents of example_group.py:
```python
from collections.abc import Mapping

from sampling import SampleGroup, SampleGroupIterator


class ExampleGroupIterator(SampleGroupIterator):
    def __init__(
        self,
        input_parameter: str,
        lower_bound: float,
        upper_bound: float,
        sample_count: int,
    ):
        self._input_parameter = input_parameter
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
        self._sample_count = sample_count
        self._index = 0

    def __next__(self) -> Mapping[str, float]:
        if self._index == self._sample_count:
            raise StopIteration

        time = self._index / (self._sample_count - 1)
        value = self._linear_interpolate(time)

        self._index += 1

        # Despite only containing one parameter, this is still a sample. The remaining
        # parameters will be set to the value they were in the previous sample. At the
        # start of every sample group, the parameters are reset to their default values.
        return {self._input_parameter: value}

    def _linear_interpolate(self, time: float) -> float:
        return self._lower_bound * (1.0 - time) + self._upper_bound * time


# While this SampleGroup only takes in values and passes them to the iterator,
# typically calculations that apply to all sample groups will be done in the Sampler,
# and calculations that apply to a single sample group will be done in the SampleGroup.
# The SampleGroupIterator should do calculations that apply to individual samples.
class ExampleGroup(SampleGroup):
    def __init__(
        self,
        input_parameter: str,
        lower_bound: float,
        upper_bound: float,
        sample_count: int,
    ):
        self._input_parameter = input_parameter
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
        self._sample_count = sample_count

    def get_sample_count(self) -> int:
        return self._sample_count

    def __iter__(self) -> ExampleGroupIterator:
        return ExampleGroupIterator(
            self._input_parameter,
            self._lower_bound,
            self._upper_bound,
            self._sample_count,
        )
```

Contents of example_sampler.py:
```python
from typing import Mapping

from sampling import SampleGroup, Sampler

from .example_group import ExampleGroup


class ExampleSampler(Sampler):
    # Typically information like this is encoded in files, but this is not a
    # requirement.
    _GROUP_NAMES = ["betavis_group", "za_lake_group"]
    _PARAMETERS = ["betavis", "za_lake"]
    _LOWER_BOUNDS = [0.0, 10.0]
    _UPPER_BOUNDS = [1.0, 15.0]
    _SAMPLE_COUNTS = [4, 7]

    # Most Sampler(s) that work with files will verify those files exist in an
    # __init__ method. When a sampling plugin is loaded, this class' __init__ method is
    # called, and should raise errors that involve loading the plugin. (Generation
    # errors should be raised from get_sample_groups.)

    def get_sample_groups(self) -> Mapping[str, ExampleGroup]:
        groups: dict[str, ExampleGroup] = {}

        for name, parameter, lower_bound, upper_bound, sample_count in zip(
            self._GROUP_NAMES,
            self._PARAMETERS,
            self._LOWER_BOUNDS,
            self._UPPER_BOUNDS,
            self._SAMPLE_COUNTS,
        ):
            groups[name] = ExampleGroup(
                parameter, lower_bound, upper_bound, sample_count
            )

        return groups
```
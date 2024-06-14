# Table (table.py)

## Purpose
Represents a dataset stored with keyed, unordered columns, and ordered rows.
Can be interacted with as either a MutableMapping or MutableSequence using
as_mapping and as_sequence methods.

## Functionality
Can store this dataset using an arbitrary MutableMapping and MutableSequence.
The methods as_mapping and as_sequence create a TableMapping and TableSequence 
object respectively. These objects share their data with the original Table
object and operations performed using them will all affect that original
dataset.

## Example

```
>>> from util import Table
>>>
>>> # Must pass an instance of the MutableMapping and MutableSequence, since
>>> # neither is garanteed to have a no-arg constructor.
>>> table = Table[dict, list]({}, [])
>>>
>>> table_mapping = table.as_mapping()
>>> table_mapping["key1"] = [0, 1, 2]
>>> table_mapping["key2"] = [2, 1, 0]
>>> table_mapping["key1"]
[0, 1, 2]
>>> 
>>> table_sequence = table.as_sequence()
>>> # Data is shared from the TableMapping.
>>> list(table_sequence[:])
[{'key1': 0, 'key2': 2}, {'key1': 1, 'key2': 1}, {'key1': 2, 'key2': 0}]
>>> table_sequence.append({"key1": 3, "key2": -1})
>>> list(table_sequence[:])
[{'key1': 0, 'key2': 2}, {'key1': 1, 'key2': 1}, {'key1': 2, 'key2': 0}, {'key1': 3, 'key2': -1}]
>>> 
>>> table_mapping["key1"]
[0, 1, 2, 3]
```

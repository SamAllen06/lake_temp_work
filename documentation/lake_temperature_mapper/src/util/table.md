# Table (APP/src/util/table.py)

## Purpose
Represents a dataset stored with keyed, unordered columns, and ordered rows.
(Think of a table with headers at the top.) A programmer can use both the
[MutableMapping](https://docs.python.org/3.10/library/collections.abc.html#collections.abc.MutableMapping)
and [MutableSequence](https://docs.python.org/3.10/library/collections.abc.html#collections.abc.MutableSequence)
interfaces to interact with it, by calling the as_mapping or as_sequence methods
to convert any Table (including its subclasses, TableMapping or TableSequence)
into one or the other. The table will maintain the same set of data even after
these methods are called.

## Functionality
A Table can store its dataset using an arbitrary
[MutableMapping](https://docs.python.org/3.10/library/collections.abc.html#collections.abc.MutableMapping)
and [MutableSequence,](https://docs.python.org/3.10/library/collections.abc.html#collections.abc.MutableSequence)
which are passed through the constructor.
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

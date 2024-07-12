# Transparent Layer List (APP/src/util/transparent_layer_list)

## Purpose
Serves as a data structure optimized for storing multiple sequences (layers) of
the same data with little changes between each. Has the same interface as a two
dimensional [Sequence.](https://docs.python.org/3.10/library/collections.abc.html#collections.abc.Sequence)

## Functionality
Stores a base layer, which is a Sequence of data that is, ideally, shares the
greatest percentage of data with the other layers. (In [OutputFileReader,](../testing/output_file_reader.md)
I've used the reference data as the base layer, since most output variables are
not changed by changes to individual inputs.)

On top of the base layer, it stores a dictionary for each additional layer,
mapping indices to their respective changed values. These dictionaries are
wrapped using TransparentLayer, which is an immutable [Sequence](https://docs.python.org/3.10/library/collections.abc.html#collections.abc.Sequence)
storing a reference to the base layer, as well as the dictionary itself.
The dictionary only stores differences from the base layer, and, as the name
would imply, is transparent for all indices not included in the dictionary,
allowing the programmer to access data as if it stored the full dataset.

## Examples
```
>>> from util import TransparentLayer
>>> 
>>> base = [1, 2, 3, 4, 5]
>>> layer = [1, 2, 4, 5, 5]
>>> 
>>> transparent_layer = TransparentLayer(base, layer)
>>> 
>>> [val for val in transparent_layer]
[1, 2, 4, 5, 5]
>>> transparent_layer.get_comparison_map()
{2: 4, 3: 5}
>>> # For understanding purposes
>>> transparent_layer._base_layer
[1, 2, 3, 4, 5]
```

```
>>> from util import TransparentLayerList
>>> 
>>> base = [1, 2, 3]
>>> layers = [[1, x, x % 3] for x in range(1, 7)]
>>> layers
[[1, 1, 1], [1, 2, 2], [1, 3, 0], [1, 4, 1], [1, 5, 2], [1, 6, 0]]
>>> 
>>> transparent_layer_list = TransparentLayerList()
>>> transparent_layer_list.append(base)
>>> for l in layers:
...     transparent_layer_list.append(l)
... 
>>> [list(l) for l in transparent_layer_list]
[[1, 2, 3], [1, 1, 1], [1, 2, 2], [1, 3, 0], [1, 4, 1], [1, 5, 2], [1, 6, 0]]
>>> # For understanding purposes
>>> [transparent_layer_list._base_layer] + [l.get_comparison_map for l in transparent_layer_list._layers]
[[1, 2, 3], {1: 1, 2: 1}, {2: 2}, {1: 3, 2: 0}, {1: 4, 2: 1}, {1: 5, 2: 2}, {1: 6, 2: 0}]
```

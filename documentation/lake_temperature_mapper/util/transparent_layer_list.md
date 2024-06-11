# Transparent Layer List (transparent_layer_list)

## Purpose

Serves as a data structure optimized for storing multiple sequences (layers) of
the same data with little changes between each. Has the same interface as a two
dimentional Sequence. (See collections.abc.Sequence).

## Functionality

Stores a base layer, which is a Sequence of data that is most similar to all of
the other layers. (In the Lake Temperature Mapper, I've used the reference data
as the base layer.) On top of that, it stores a dictionary for each layer,
mapping indices to their respective changed values. These dictionaries are
wrapped using TransparentLayer, which is an immutable Sequence storing a
reference to the base layer, as well as the dictionary. The dictionary only
stores differences from the base layer, and, as the name would imply,
transparent for all indices not included in the dictionary. 

## Examples

```
>>> from util import TransparentLayer
>>> base = [1, 2, 3, 4, 5]
>>> layer = [1, 2, 4, 5, 5]
>>> transparent_layer = TransparentLayer(base, layer)
>>> [val for val in transparent_layer]
[1, 2, 4, 5, 5]
>>> # For understanding purposes
>>> transparent_layer._comparison_map
{2: 4, 3: 5}
>>> transparent_layer._base_layer
[1, 2, 3, 4, 5]
```

```
>>> from util import TransparentLayerList
>>> base = [1, 2, 3]
>>> layers = [[1, x, x % 3] for x in range(1, 7)]
>>> layers
[[1, 1, 1], [1, 2, 2], [1, 3, 0], [1, 4, 1], [1, 5, 2], [1, 6, 0]]
>>> transparent_layer_list = TransparentLayerList()
>>> transparent_layer_list.append(base)
>>> for l in layers:
...     transparent_layer_list.append(l)
... 
>>> [list(l) for l in transparent_layer_list]
[[1, 2, 3], [1, 1, 1], [1, 2, 2], [1, 3, 0], [1, 4, 1], [1, 5, 2], [1, 6, 0]]
>>> # For understanding purposes
>>> [transparent_layer_list._base_layer] + [l._comparison_map for l in transparent_layer_list._layers]
[[1, 2, 3], {1: 1, 2: 1}, {2: 2}, {1: 3, 2: 0}, {1: 4, 2: 1}, {1: 5, 2: 2}, {1: 6, 2: 0}]
```

# Mixin Sequence Indices
APP/src/util/mixin_sequence_indices

## Purpose
MixinSequenceIndices is a [mixin class](https://www.pythontutorial.net/python-oop/python-mixin/)
that adds private methods to aid in interpreting slice and negative indices for
[Sequence(s).](https://docs.python.org/3.10/library/collections.abc.html#collections.abc.Sequence)
Intended for use inside the util package.

## Functionality
Can convert negative indices to positive ones, can raise IndexError in the event
that an index is out of bounds, can clamp indices for use in insert() methods,
and can convert a slice object into a range object.

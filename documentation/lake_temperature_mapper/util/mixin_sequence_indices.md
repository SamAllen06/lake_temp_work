# Mixin Sequence Indices (mixin_sequence_indices)

## Purpose
Mixin class that adds methods for interpreting indices for Sequence(s). For use
in util.

## Functionality
Can convert negative indices to positive ones, can raise IndexError in the event
that an index is out of bounds, can clamp indices for use in insert() methods,
and can convert a slice object into a range object.

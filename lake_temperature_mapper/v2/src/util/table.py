from __future__ import annotations

from collections.abc import (
    Callable,
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)
import copy
from typing import Any, Generic, overload, override, Self, TypeVar

from .mixin_sequence_indices import MixinSequenceIndices


S = TypeVar("S", bound=MutableSequence)
M = TypeVar("M", bound=MutableMapping)  # [Any, S]


class Table(Generic[M, S]):
    def __init__(self, mapping_object: M, sequence_object: S):
        self._mapping_object: M = copy.deepcopy(mapping_object)
        self._sequence_object: S = copy.deepcopy(sequence_object)

        self._mapping_object.clear()
        self._sequence_object.clear()

        self._data: M = copy.deepcopy(self._mapping_object)

        self.as_mapping: Callable[[], TableMapping[M, S]]
        self.as_sequence: Callable[[], TableSequence[M, S]]

    def is_empty(self) -> bool:
        return self.get_row_count() == 0 and self.get_column_count() == 0

    def get_row_count(self) -> int:
        if not self._data.keys():
            return 0

        first_key = next(iter(self._data.keys()))

        return len(self._data[first_key])

    def get_column_count(self) -> int:
        return len(self._data.keys())


class TableMapping(Table, MutableMapping, Generic[M, S]):
    def __init__(self, data: M, mapping_object: M, sequence_object: S):
        self._data: M = data

        self._mapping_object = mapping_object
        self._sequence_object = sequence_object

    def __getitem__(self, key: Any) -> S:
        self._check_key(key)

        return self._data[key]

    def __setitem__(self, key: Any, column: Sequence[Any]) -> None:
        row_count = self.get_row_count()

        if not len(column) == row_count and not self.is_empty():
            raise ValueError(
                f"Cannot set column {key} with size {len(column)} "
                f"while column size is currently {row_count}"
            )

        self._data[key] = copy.deepcopy(self._sequence_object)
        self._data[key].extend(column)

    def __delitem__(self, key: Any) -> None:
        self._check_key(key)

        del self._data[key]

    def __iter__(self) -> Iterator:
        return iter(self._data.keys())

    def __len__(self) -> int:
        return self.get_column_count()

    def _check_key(self, key: Any) -> None:
        if not key in self._data.keys():
            raise KeyError(f"key {key} not found in table")


def _as_mapping(self) -> TableMapping[M, S]:
    return TableMapping[M, S](self._data, self._mapping_object, self._sequence_object)


# Ignoring to prevent "self" being seen as Any type.
Table.as_mapping = _as_mapping  # type: ignore


class TableSequence(Table, MutableSequence, MixinSequenceIndices, Generic[M, S]):
    def __init__(self, data: M, mapping_object: M, sequence_object: S):
        self._data = data

        self._mapping_object = mapping_object
        self._sequence_object = sequence_object

    def initialize_keys(self, keys: Iterable[Any]) -> None:
        if not self.get_column_count() == 0:
            raise RuntimeError(
                "Can only initialize keys on an empty Table, use as_mapping to "
                "create or delete keys instead"
            )

        for key in keys:
            self._data[key] = copy.deepcopy(self._sequence_object)

    def insert(self, index: int, row: Mapping[Any, Any]) -> None:
        index = self._ensure_positive_index(index)
        index = self._clamp_insert_index(index)

        column_count = self.get_column_count()

        if not self._data.keys() == row.keys() and not column_count == 0:
            raise KeyError(
                f"New row keys {list(row.keys())} must match current table "
                f"keys {list(self._data.keys())}"
            )

        for key in row.keys():
            if not key in self._data:
                raise KeyError(
                    f"key {key} not found in current table, create it first "
                    f"by calling initialize_keys"
                )
            self._data[key].insert(index, row[key])

    @override
    @overload
    def __getitem__(self, index: int) -> M:
        pass

    @override
    @overload
    def __getitem__(self, index: slice) -> TableSequence:
        pass

    def __getitem__(self, index):
        if isinstance(index, int):
            return self._getitem_int(index)
        elif isinstance(index, slice):
            return self._getitem_slice(index)
        else:
            raise ValueError(
                "Indices must be either int or slice, " f"not {type(index).__name__}"
            )

    @override
    @overload
    def __setitem__(self, index: int, item: Any) -> None:
        pass

    @override
    @overload
    def __setitem__(self, index: slice, item: Iterable[Any]) -> None:
        pass

    def __setitem__(self, index, item):
        if isinstance(index, int):
            self._setitem_int(index, item)
        elif isinstance(index, slice):
            self._setitem_slice(index, item)
        else:
            raise ValueError(
                "Indices must be either int or slice, " f"not {type(index).__name__}"
            )

    @override
    @overload
    def __delitem__(self, index: int) -> None:
        pass

    @override
    @overload
    def __delitem__(self, index: slice) -> None:
        pass

    def __delitem__(self, index):
        if isinstance(index, int) or isinstance(index, slice):
            self._delitem(index)
        else:
            raise ValueError(
                "Indices must be either int or slice, " f"not {type(index).__name__}"
            )

    def __len__(self) -> int:
        return self.get_row_count()

    def _getitem_int(self, index: int) -> M:
        self._raise_index_error_if_out_of_bounds(index)

        row = copy.deepcopy(self._mapping_object)

        for key in self._data.keys():
            row[key] = self._data[key][index]

        return row

    def _getitem_slice(self, slice_index: slice) -> TableSequence[M, S]:
        table_mapping = self.as_mapping()

        new_data = copy.deepcopy(self._mapping_object)

        for key in self._data.keys():
            new_data[key] = table_mapping[key][slice_index]

        return TableSequence(new_data, self._mapping_object, self._sequence_object)

    def _setitem_int(self, index: int, row: M) -> None:
        self._raise_index_error_if_out_of_bounds(index)

        if not self._data.keys() == row.keys():
            raise KeyError(
                f"New row keys {list(row.keys())} must match current table "
                f"keys {list(self._data.keys())}"
            )

        for key in row.keys():
            self._data[key][index] = row[key]

    def _setitem_slice(self, slice_index: slice, rows: Sequence[M]) -> None:
        # Checking in advance so that table will be unmodified in the event of
        # a KeyError.
        for row in rows:
            if not self._data.keys() == row.keys():
                raise KeyError(
                    f"New row keys {list(row.keys())} must match current table "
                    f"keys {list(self._data.keys())}"
                )

        slice_range = self._slice_to_range(slice_index)

        for index in slice_range:
            self._setitem_int(index, rows[index])

    def _delitem(self, index: int | slice) -> None:
        if isinstance(index, int):
            self._raise_index_error_if_out_of_bounds(index)

        for key in self._data.keys():
            del self._data[key][index]


def _as_sequence(self) -> TableSequence:
    return TableSequence(self._data, self._mapping_object, self._sequence_object)


Table.as_sequence = _as_sequence  # type: ignore

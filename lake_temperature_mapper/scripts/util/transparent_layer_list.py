from abc import ABC
from collections.abc import Iterable, Mapping, MutableSequence, Sequence, Sized
from typing import Any, overload, override
from typing_extensions import Self


class _MixinIndices(ABC, Sized):
    def _get_as_valid_index(self, index: int) -> int:
        index = self._ensure_positive_index(index)
        if self._is_index_out_of_bounds(index):
            raise IndexError("Index out of bounds")

        return index

    def _slice_to_range(self, slice_object: slice) -> range:
        start = self._ensure_positive_index(slice_object.start)
        stop = (
            self.__len__() if slice_object.stop is None else
            self._ensure_positive_index(slice_object.stop)
        )
        step = 1 if slice_object.step is None else slice_object.step

        return range(start, stop, step)

    def _ensure_positive_index(self, index: int) -> int:
        if index < 0:
            return self.__len__() + index
        return index

    def _is_index_out_of_bounds(self, index: int) -> bool:
        return index < 0 or index >= self.__len__()


class TransparentLayer(Sequence, _MixinIndices):
    @overload
    def __init__(
            self,
            base_layer: Sequence[Any],
            comparison_layer: Sequence[Any]
    ):
        pass

    @overload
    def __init__(
            self,
            base_layer: Sequence[Any],
            comparison_layer: Mapping[int, Any]
    ):
        pass

    def __init__(self, base_layer, comparison_layer):
        self._base_layer = base_layer
        if issubclass(type(comparison_layer), Mapping):
            self._comparison_map = comparison_layer
        elif issubclass(type(comparison_layer), Sequence):
            self._comparison_map = self._generate_comparison_map(
                comparison_layer
            ) 
        else:
            raise TypeError(
                "Comparison layer must be a Sequence or Mapping[int, Any]"
            )

    @override
    @overload
    def __getitem__(self, index: int) -> Any:
        pass

    @override
    @overload
    def __getitem__(self, index: slice) -> Self:
        pass

    def __getitem__(self, index):
        if isinstance(index, int):
            return self._getitem_with_int_index(index)
        elif isinstance(index, slice):
            return self._getitem_with_slice(index)

        raise TypeError(
            "TransparentLayer indices must be int or slice, "
            f"but {type(index).__name__} was used"
        )

    @override
    def __len__(self) -> int:
        return len(self._base_layer)

    def _generate_comparison_map(
            self,
            comparison_layer: Sequence[Any]
    ) -> dict[int, Any]:
        comparison_map: dict[int, Any] = {}

        for index, (base_value, comparison_value) in enumerate(
            zip(self._base_layer, comparison_layer)
        ):
            if base_value is not comparison_value:
                comparison_map[index] = comparison_value

        return comparison_map

    def _getitem_with_int_index(self, index: int) -> Any:
        index = self._get_as_valid_index(index)

        if index in self._comparison_map:
            return self._comparison_map[index]
        return self._base_layer[index]

    def _getitem_with_slice(self, slice_index: slice) -> Self:
        return TransparentLayer(
            self._base_layer[slice_index],
            self._slice_comparison_map(slice_index)
        )


    def _slice_comparison_map(self, slice_object: slice) -> dict[int, Any]:
        new_comparison_map: dict[int, Any] = {}

        slice_range = self._slice_to_range(slice_object)
        for key in slice_range:
            if key in self._comparison_map:
                new_comparison_map[key - slice_range.start] = self._comparison_map[key]

        return new_comparison_map


class TransparentLayerList(MutableSequence, _MixinIndices):
    def __init__(self):
        self._base_layer = None
        self._layers = []

    def insert(self, index: int, layer: Sequence[Any]) -> None:
        self._verify_layer_type(layer)

        if index > self.__len__():
            index = self.__len__()
        elif index < 0:
            index = 0

        if index == 0:
            if self._base_layer is None:
                self.rebase(layer)
                return

            old_base_layer = self._base_layer
            self.rebase(layer)
            self.insert(1, old_base_layer)
            return

        self._layers.insert(
            index - 1,
            TransparentLayer(self._base_layer, layer)
        )

    def rebase(self, base_layer: Sequence) -> None:
        base_layer_list = list(base_layer)

        for index, layer in enumerate(self._layers):
            self._layers[index] = TransparentLayer(base_layer_list, layer)
        self._base_layer = base_layer_list

    @override
    @overload
    def __getitem__(self, index: int) -> TransparentLayer:
        pass

    @override
    @overload
    def __getitem__(self, index: slice) -> Self:
        pass

    def __getitem__(self, index):
        if isinstance(index, int):
            return self._getitem_with_int_index(index)
        elif isinstance(index, slice):
            return self._getitem_with_slice(index)

        raise TypeError(
            "TransparentLayerList indices must be either int or slice, "
            f"not {type(index).__name__}"
        )

    @override
    @overload
    def __setitem__(self, index: int, value: Any) -> None:
        pass

    @override
    @overload
    def __setitem__(self, index: slice, value: Iterable[Any]) -> None:
        pass

    def __setitem__(self, index, value):
        if isinstance(index, int):
            self._setitem_with_int_index(index, value)
        elif isinstance(index, slice):
            self._setitem_with_slice(index, value)
        else:
            raise TypeError(
                "TransparentLayerList indices must be either int or slice, "
                f"not {type(index).__name__}"
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
        if isinstance(index, int):
            self._delitem_with_int_index(index)
        elif isinstance(index, slice):
            self._delitem_with_slice(index)
        else:
            raise TypeError(
                "TransparentLayerList indices must be either int or slice, "
                f"not {type(index).__name__}"
            )

    def __len__(self) -> int:
        return len(self._layers) + (1 if self._base_layer is not None else 0)

    def _verify_layer_type(self, layer: Any) -> None:
        if not issubclass(type(layer), Sequence):
            raise TypeError(
                "TransparentLayerList elements can only be Sequences, not "
                f"{type(layer)}, add individual elements to a Sequence first"
            )

    def _getitem_with_int_index(self, index: int) -> Sequence[Any]:
        index = self._get_as_valid_index(index)

        if index == 0:
            return self._base_layer

        return self._layers[index - 1]

    def _getitem_with_slice(self, slice_index: slice) -> Self:
        slice_range = self._slice_to_range(slice_index)

        sliced_list = TransparentLayerList()

        for index in slice_range:
            sliced_list.append(self._getitem_with_int_index(index))

        return sliced_list

    def _setitem_with_int_index(self, index: int, value: Any) -> None:
        self._verify_layer_type(value)
        index = self._get_as_valid_index(index)

        if index == 0:
            self.rebase(value)
        else:
            self._layers[index - 1] = TransparentLayer(self._base_layer, value)

    def _setitem_with_slice(
            self,
            slice_index: slice,
            value_iterable: Iterable[Any]
    ) -> None:
        slice_range = self._slice_to_range(slice_index)

        if not issubclass(type(value_iterable), Iterable):
            raise TypeError(
                "Can only assign an Iterable when indexing with a slice"
            )

        for index, value in zip(slice_range, value_iterable):
            self._setitem_with_int_index(index, value)

    def _delitem_with_int_index(self, index: int) -> None:
        index = self._get_as_valid_index(index)

        if index == 0:
            try:
                new_base_layer = self.pop(1)
                self.rebase(new_base_layer)
            except IndexError:
                self._base_layer = []
        else:
            self._layers.pop(index - 1)

    def _delitem_with_slice(self, slice_index: slice) -> None:
        for index in reversed(self._slice_to_range(slice_index)):
            self._delitem_with_int_index(index)

    def _ensure_positive_index(self, index: int) -> int:
        if index < 0:
            return self.__len__() + index
        return index

    def _is_index_out_of_bounds(self, index: int) -> bool:
        return index < 0 or index >= self.__len__()



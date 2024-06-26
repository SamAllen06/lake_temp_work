from abc import ABC
from collections.abc import Sized


class MixinSequenceIndices(ABC, Sized):
    def _raise_index_error_if_out_of_bounds(self, index: int) -> None:
        index = self._ensure_positive_index(index)

        if self._is_index_out_of_bounds(index):
            raise IndexError("Index out of bounds")

    def _slice_to_range(self, slice_object: slice) -> range:
        start = (
            0
            if slice_object.start is None
            else self._ensure_positive_index(slice_object.start)
        )
        stop = (
            self.__len__()
            if slice_object.stop is None
            else self._ensure_positive_index(slice_object.stop)
        )
        step = 1 if slice_object.step is None else slice_object.step

        return range(start, stop, step)

    def _ensure_positive_index(self, index: int) -> int:
        if index < 0:
            return self.__len__() + index
        return index

    def _is_index_out_of_bounds(self, index: int) -> bool:
        return index < 0 or index >= self.__len__()

    def _clamp_insert_index(self, index: int) -> int:
        return max(0, min(index, self.__len__()))

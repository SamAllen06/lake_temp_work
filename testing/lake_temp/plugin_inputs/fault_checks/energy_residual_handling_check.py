import numpy as np
import numpy.typing as npt


def check_errsoi_almost_zero(
    test_col_ef_errsoi: npt.NDArray,
) -> None:
    assert np.all(test_col_ef_errsoi <= 1E-6), "Error is above tolerance"


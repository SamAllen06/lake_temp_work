import numpy as np
import numpy.typing as npt

from mtf_fault_finding import CheckStatus
from mtf_fault_finding import NonFiniteValuesHandler


def check_errsoi_almost_zero(
    test_col_ef_errsoi: npt.NDArray,
) -> None:
    if NonFiniteValuesHandler.is_all_not_finite(test_col_ef_errsoi):
        return CheckStatus.SKIPPED
    test_col_ef_errsoi = NonFiniteValuesHandler.mask_non_finite_values(
        test_col_ef_errsoi)

    assert np.all(np.abs(test_col_ef_errsoi) <= 1E-6), "Error is above tolerance"

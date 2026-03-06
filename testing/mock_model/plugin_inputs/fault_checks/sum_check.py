import numpy as np
import numpy.typing as npt

from mtf_fault_finding import CheckStatus


def check_passes(test_fakevar_sum: npt.NDArray):
    assert np.all(test_fakevar_sum > 0), f"fakevar_sum expected to be positive, was {test_fakevar_sum}"

def check_skips(test_fakevar_product: npt.NDArray):
    return CheckStatus.SKIPPED

def check_fails(test_fakevar_product: npt.NDArray):
    assert np.all(test_fakevar_product < 0), f"fakevar_product expected to be negative, was {test_fakevar_product}"

def check_errors(test_fakevar_sum: npt.NDArray):
    raise ValueError("boof")

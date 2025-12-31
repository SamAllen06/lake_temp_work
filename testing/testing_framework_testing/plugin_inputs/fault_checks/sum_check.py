import numpy as np


def check_passes(test_fakevar_sum: list[float]):
    assert np.all(test_fakevar_sum > 0), f"fakevar_sum expected to be positive, was {test_fakevar_sum}"

def check_fails(test_fakevar_product: list[float]):
    assert np.all(test_fakevar_product < 0), f"fakevar_product expected to be negative, was {test_fakevar_product}"

def check_errors(test_fakevar_sum: list[float]):
    raise ValueError("boof")

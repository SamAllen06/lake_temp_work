import utils


def check_passes(test_fakevar_sum: list[float]):
    assert utils.is_positive(test_fakevar_sum), f"fakevar_sum expected to be positive, was {test_fakevar_sum}"

def check_fails(test_fakevar_product: list[float]):
    assert not utils.is_positive(test_fakevar_product), f"fakevar_product expected to be negative, was {test_fakevar_product}"

def check_errors(test_fakevar_sum: list[float]):
    if utils.is_positive(test_fakevar_sum):
        raise ValueError("boof")

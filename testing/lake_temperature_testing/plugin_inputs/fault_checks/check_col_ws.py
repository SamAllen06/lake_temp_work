from collections.abc import Sequence

import utils


def check_h2osoi_ice_is_positive(
        test_col_ws_h2osoi_ice: Sequence[float]
) -> None:
    assert utils.are_all_positive(test_col_ws_h2osoi_ice, allow_zero=True), (
        "Expected all values of col_ws%h2osoi_ice to be positive"
    )


def check_h2osno_is_positive(
        test_col_ws_h2osno: Sequence[float]
) -> None:
    assert utils.are_all_positive(test_col_ws_h2osno, allow_zero=True), (
        "Expected all values of col_ws%h2osno to be positive"
    )


def check_frac_iceold_is_fraction(
        test_col_ws_frac_iceold: Sequence[float]
) -> None:
    assert utils.are_all_fraction(test_col_ws_frac_iceold), (
        "Expected all values of col_ws%frac_iceold to be in range [0.0, 1.0]"
    )


def check_snow_depth_is_positive(
        test_col_ws_snow_depth: Sequence[float]
) -> None:
    assert utils.are_all_positive(test_col_ws_snow_depth, allow_zero=True), (
        "Expected all values of col_ws%snow_depth to be positive"
    )

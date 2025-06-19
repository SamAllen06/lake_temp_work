from collections.abc import Sequence

import utils


def check_lake_icethick_col_is_positive(
        test_lakestate_vars_lake_icethick_col: Sequence[float]
) -> None:
    assert utils.are_all_positive(
        test_lakestate_vars_lake_icethick_col, allow_zero=True
    ), "Expected all values of lakestate_vars%lake_icethick_col to be positive"


def check_lake_icefrac_col_keeps_same_sign(
        test_lakestate_vars_lake_icefrac_col: Sequence[float]
) -> None:
    assert utils.are_all_positive(
        test_lakestate_vars_lake_icefrac_col, allow_zero=True
    ) or utils.are_all_negative(
        test_lakestate_vars_lake_icefrac_col, allow_zero=True
    ), "Expected all values of lakestate_vars%lake_icefrac_col to keep the same sign"


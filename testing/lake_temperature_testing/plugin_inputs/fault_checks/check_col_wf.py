from collections.abc import Sequence

import utils


def check_qflx_snofrz_lyr_is_positive(
        test_col_wf_qflx_snofrz_lyr: Sequence[float]
) -> None:
    assert utils.are_all_positive(
        test_col_wf_qflx_snofrz_lyr, allow_zero=True
    ), "Expected all values of col_wf%qflx_snofrz_lyr to be positive"


def check_qflx_snofrz_is_positive(
        test_col_wf_qflx_snofrz: Sequence[float]
) -> None:
    assert utils.are_all_positive(
        test_col_wf_qflx_snofrz, allow_zero=True
    ), "Expected all values of col_wf%qflx_snofrz to be positive"


def check_qflx_snomelt_is_positive(
        test_col_wf_qflx_snomelt: Sequence[float]
) -> None:
    assert utils.are_all_positive(
        test_col_wf_qflx_snomelt, allow_zero=True
    ), "Expected all values of col_wf%qflx_snomelt to be positive"


def check_qflx_snow_melt_equals_snomelt(
        test_col_wf_qflx_snow_melt: Sequence[float],
        test_col_wf_qflx_snomelt: Sequence[float]
) -> None:
    assert test_col_wf_qflx_snomelt == test_col_wf_qflx_snow_melt, (
        "Expected col_wf%qflx_snow_melt to equal col_wf%qflx_snomelt"
    )




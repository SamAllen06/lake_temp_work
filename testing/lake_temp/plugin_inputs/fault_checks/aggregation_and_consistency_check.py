import numpy as np
import numpy.typing as npt


def check_snofrz_lyr_sums_to_snofrz_col(
    test_col_wf_qflx_snofrz_lyr: npt.NDArray,
    test_col_wf_qflx_snofrz: npt.NDArray,
) -> None:
    tolerance = 1E-10

    lyr_sum = test_col_wf_qflx_snofrz_lyr.sum(axis=1)
    abs_diff = np.abs(test_col_wf_qflx_snofrz - lyr_sum)

    assert np.all(abs_diff <= tolerance), "Sum does not match expected values"


def check_icethick_col_is_sum(
    test_lakestate_vars_lake_icethick_col: npt.NDArray,
    test_lakestate_vars_lake_icefrac_col: npt.NDArray,
    test_col_pp_dz_lake: npt.NDArray,
    denh2o: float,
    denice: float,
) -> None:
    tolerance = 1E-9

    product = (
        test_lakestate_vars_lake_icefrac_col * test_col_pp_dz_lake * denh2o / denice
    )

    sum = product.sum(axis=1)
    abs_diff = np.abs(test_lakestate_vars_lake_icethick_col - sum)

    assert np.all(abs_diff <= tolerance), "Ice thickness is not consistent with other variables"

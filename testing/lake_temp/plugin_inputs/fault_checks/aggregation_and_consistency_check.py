import numpy as np
import numpy.typing as npt


def check_snofrz_lyr_sums_to_snofrz_col(
    test_col_wf_qflx_snofrz_lyr: npt.NDArray,
    test_col_wf_qflx_snofrz: npt.NDArray,
) -> None:
    if NonFiniteValuesHandler.is_all_not_finite(test_col_wf_qflx_snofrz_lyr, 
                                                test_col_wf_qflx_snofrz):
        return CheckStatus.SKIPPED
    test_col_wf_qflx_snofrz_lyr, test_col_wf_qflx_snofrz = (
        NonFiniteValuesHandler.mask_non_finite_values(test_col_wf_qflx_snofrz_lyr, 
                                               test_col_wf_qflx_snofrz))

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
    if NonFiniteValuesHandler.is_all_not_finite(test_lakestate_vars_lake_icethick_col, 
                                                test_lakestate_vars_lake_icefrac_col, 
                                                test_col_pp_dz_lake):
        return CheckStatus.SKIPPED
    (test_lakestate_vars_lake_icethick_col, test_lakestate_vars_lake_icefrac_col, 
     test_col_pp_dz_lake) = (NonFiniteValuesHandler.mask_non_finite_values(
         test_lakestate_vars_lake_icethick_col, test_lakestate_vars_lake_icefrac_col, 
         test_col_pp_dz_lake))

    tolerance = 1E-9

    product = (
        test_lakestate_vars_lake_icefrac_col * test_col_pp_dz_lake * denh2o / denice
    )

    sum = product.sum(axis=1)
    abs_diff = np.abs(test_lakestate_vars_lake_icethick_col - sum)

    assert (np.all(abs_diff <= tolerance), 
            "Ice thickness is not consistent with other variables")


def check_imelt_uses_valid_enum_values(
    test_col_ef_imelt: npt.NDArray,
) -> None:
    # Values of 2147483647 are uninitialized, and should be masked.
    masked_imelt = np.ma.masked_where(
        test_col_ef_imelt == 2147483647, test_col_ef_imelt
    )
    if NonFiniteValuesHandler.is_all_not_finite(masked_imelt):
        return CheckStatus.SKIPPED
    masked_imelt = NonFiniteValuesHandler.mask_non_finite_values(masked_imelt)

    assert np.all(masked_imelt >= 0) and np.all(masked_imelt <= 2)

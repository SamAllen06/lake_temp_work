import numpy as np
import numpy.typing as npt

from mtf_fault_finding import CheckStatus
from mtf_fault_finding import NonFiniteValuesHandler


def check_methane_conductance_gated_by_ice(
    use_lch4: npt.NDArray,
    test_lakestate_vars_lake_icefrac_col: npt.NDArray,
    test_ch4_vars_grnd_ch4_cond_col: npt.NDArray,
):
    if not use_lch4 == 1:
        return CheckStatus.SKIPPED

    if NonFiniteValuesHandler.is_all_not_finite(test_lakestate_vars_lake_icefrac_col, 
                                                test_ch4_vars_grnd_ch4_cond_col):
        return CheckStatus.SKIPPED
    test_lakestate_vars_lake_icefrac_col, test_ch4_vars_grnd_ch4_cond_col = (
        NonFiniteValuesHandler.mask_non_finite_values(
                                                test_lakestate_vars_lake_icefrac_col, 
                                                test_ch4_vars_grnd_ch4_cond_col))

    some_surface_ice = test_lakestate_vars_lake_icefrac_col[:, 0, :] > 0.1

    conducting_methane = test_ch4_vars_grnd_ch4_cond_col > 1e-12

    # Verify methane conductance is blocked by ice
    assert not np.any(some_surface_ice & conducting_methane), (
        "methane conductance is not blocked by ice")
    

def check_methane_conductance_not_negative(
    use_lch4: int,
    test_ch4_vars_grnd_ch4_cond_col: npt.NDArray,
) -> None:
    if not use_lch4:
        return CheckStatus.SKIPPED

    if NonFiniteValuesHandler.is_all_not_finite(test_ch4_vars_grnd_ch4_cond_col):
        return CheckStatus.SKIPPED
    test_ch4_vars_grnd_ch4_cond_col = (
        NonFiniteValuesHandler.mask_non_finite_values(test_ch4_vars_grnd_ch4_cond_col))

    assert np.all(test_ch4_vars_grnd_ch4_cond_col >= 0.0), "CH4 conductance is negative"

def check_methane_conductance_allowed_without_ice(
    use_lch4: npt.NDArray,
    test_lakestate_vars_lake_icefrac_col: npt.NDArray,
    test_ch4_vars_grnd_ch4_cond_col: npt.NDArray,
    test_lakestate_vars_lakeresist_col: npt.NDArray,
    test_lakestate_vars_lake_raw_col: npt.NDArray,
):
    if not use_lch4 == 1:
        return CheckStatus.SKIPPED
    
    if NonFiniteValuesHandler.is_all_not_finite(test_lakestate_vars_lake_icefrac_col,
            test_ch4_vars_grnd_ch4_cond_col, test_lakestate_vars_lakeresist_col,
            test_lakestate_vars_lake_raw_col):
        return CheckStatus.SKIPPED
    (test_lakestate_vars_lake_icefrac_col, test_ch4_vars_grnd_ch4_cond_col,
     test_lakestate_vars_lakeresist_col,test_lakestate_vars_lake_raw_col) = (
        NonFiniteValuesHandler.mask_non_finite_values(
            test_lakestate_vars_lake_icefrac_col, test_ch4_vars_grnd_ch4_cond_col,
             test_lakestate_vars_lakeresist_col,test_lakestate_vars_lake_raw_col))

    no_surface_ice = test_lakestate_vars_lake_icefrac_col[:, 0, :] == 0.1

    total_resistance = test_lakestate_vars_lakeresist_col + test_lakestate_vars_lake_raw_col
    usable = total_resistance > 0

    expected = np.ma.masked_where(~usable, 1.0 / np.ma.masked_where(
        ~usable, total_resistance))
    abs_diff = np.abs(test_ch4_vars_grnd_ch4_cond_col - expected)

    # Verify columns without ice conduct the expected methane.
    assert np.all(
        ~no_surface_ice | (abs_diff <= 1E-6)
    ), "columns without ice do not conduct the expected methane"

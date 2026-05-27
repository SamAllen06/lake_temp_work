import numpy as np
import numpy.typing as npt

from mtf_fault_finding import CheckStatus
from mtf_fault_finding import NonFiniteValuesHandler


def check_methane_conductance_frozen_lake(
    use_lch4: int,
    test_lakestate_vars_lake_icefrac_col: npt.NDArray,
    test_ch4_vars_grnd_ch4_cond_col: npt.NDArray,
) -> None:
    if NonFiniteValuesHandler.is_all_not_finite(use_lch4, 
            test_lakestate_vars_lake_icefrac_col, test_ch4_vars_grnd_ch4_cond_col):
        return CheckStatus.SKIPPED
    use_lch4, test_lakestate_vars_lake_icefrac_col, test_ch4_vars_grnd_ch4_cond_col = (
        NonFiniteValuesHandler.mask_non_finite_values(use_lch4, 
                test_lakestate_vars_lake_icefrac_col, test_ch4_vars_grnd_ch4_cond_col))

    if not use_lch4:
        return CheckStatus.SKIPPED

    top_layers = test_lakestate_vars_lake_icefrac_col[:, 0, :]

    frozen_top_layers = top_layers > 0.1

    if not np.any(frozen_top_layers):
        return CheckStatus.SKIPPED

    nonconducting_columns = np.isclose(test_ch4_vars_grnd_ch4_cond_col, 0.0)

    assert np.all(~frozen_top_layers | nonconducting_columns), (
        "Frozen columns are conducting ch4"
    )
    

def check_methane_conductance_non_negative(
    use_lch4: int,
    test_lakestate_vars_lake_icefrac_col: npt.NDArray,
    test_ch4_vars_grnd_ch4_cond_col: npt.NDArray,
) -> None:
    if NonFiniteValuesHandler.is_all_not_finite(use_lch4, 
            test_lakestate_vars_lake_icefrac_col, test_ch4_vars_grnd_ch4_cond_col):
        return CheckStatus.SKIPPED
    use_lch4, test_lakestate_vars_lake_icefrac_col, test_ch4_vars_grnd_ch4_cond_col = (
        NonFiniteValuesHandler.mask_non_finite_values(use_lch4, 
                test_lakestate_vars_lake_icefrac_col, test_ch4_vars_grnd_ch4_cond_col))

    if not use_lch4:
        return CheckStatus.SKIPPED

    assert np.all(test_ch4_vars_grnd_ch4_cond_col >= 0.0), "CH4 conductance is negative"

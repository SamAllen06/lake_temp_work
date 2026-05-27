import numpy as np
import numpy.typing as npt

from mtf_fault_finding import CheckStatus
from mtf_fault_finding import NonFiniteValuesHandler

# tfrz not in constants.
TFRZ = 273.15

def check_temp_around_freezing_where_lake_is_almost_frozen(
    test_col_es_t_lake: npt.NDArray,
    test_lakestate_vars_lake_icefrac_col: npt.NDArray,
) -> None:
<<<<<<< Updated upstream
    almost_frozen = (np.isclose(test_lakestate_vars_lake_icefrac_col, 1.0) 
              & (test_lakestate_vars_lake_icefrac_col != 1.0))
=======
    if NonFiniteValuesHandler.is_all_not_finite(test_col_es_t_lake, 
                                                test_lakestate_vars_lake_icefrac_col):
        return CheckStatus.SKIPPED
    test_col_es_t_lake, test_lakestate_vars_lake_icefrac_col = (
        NonFiniteValuesHandler.mask_non_finite_values(test_col_es_t_lake, 
                                               test_lakestate_vars_lake_icefrac_col))

    frozen = np.isclose(test_lakestate_vars_lake_icefrac_col, 1.0)
>>>>>>> Stashed changes

    if not np.any(almost_frozen):
        return CheckStatus.SKIPPED

    diff_to_freezing_temp = np.abs(TFRZ - test_col_es_t_lake)
    close_to_freezing_temp = diff_to_freezing_temp <= 1E-3

    assert np.all(~almost_frozen | close_to_freezing_temp), (
        "Columns are almost frozen but not close to the freezing temperature"
    )


def no_tke_when_surface_frozen(
    test_col_es_t_lake: npt.NDArray,
    test_col_pp_snl: npt.NDArray,
    test_lakestate_vars_savedtke1_col: npt.NDArray,
) -> None:
    if NonFiniteValuesHandler.is_all_not_finite(test_col_es_t_lake, 
                                                test_col_pp_snl, 
                                                test_lakestate_vars_savedtke1_col):
        return CheckStatus.SKIPPED
    test_col_es_t_lake, test_col_pp_snl, test_lakestate_vars_savedtke1_col = (
        NonFiniteValuesHandler.mask_non_finite_values(test_col_es_t_lake, 
                                               test_col_pp_snl, 
                                               test_lakestate_vars_savedtke1_col))

    tke_present = test_lakestate_vars_savedtke1_col > 0.0

    surface_frozen = test_col_es_t_lake[:, 0, :] <= TFRZ
    snow_present = test_col_pp_snl > 0
    unfrozen = ~surface_frozen & ~snow_present

    if not np.any(tke_present):
        return CheckStatus.SKIPPED

    assert np.all(~tke_present | unfrozen), (
        "Turbulant kinentic energy present on a frozen surface"
    )

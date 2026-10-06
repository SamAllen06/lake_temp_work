import numpy as np
import numpy.typing as npt

from mtf_fault_finding import CheckStatus
from mtf_fault_finding import NonFiniteValuesHandler

TFRZ = 273.15


def check_temp_around_freezing_where_lake_is_almost_frozen(
    test_col_es_t_lake: npt.NDArray,
    test_lakestate_vars_lake_icefrac_col: npt.NDArray,
) -> None:
    if NonFiniteValuesHandler.is_all_not_finite(test_col_es_t_lake, 
                                                test_lakestate_vars_lake_icefrac_col):
        return CheckStatus.SKIPPED
    test_col_es_t_lake, test_lakestate_vars_lake_icefrac_col = NonFiniteValuesHandler.mask_non_finite_values(
        test_col_es_t_lake, test_lakestate_vars_lake_icefrac_col)

    partially_frozen = (test_lakestate_vars_lake_icefrac_col > 0.0) & (
        test_lakestate_vars_lake_icefrac_col < 1.0)

    abs_temp_dif = np.abs(np.subtract(test_col_es_t_lake, TFRZ))
    assert np.all(~partially_frozen | (abs_temp_dif <= 1e-3))


def check_fully_frozen_layers_not_above_freezing(
    test_col_es_t_lake: npt.NDArray,
    test_lakestate_vars_lake_icefrac_col: npt.NDArray
) -> None:
    if NonFiniteValuesHandler.is_all_not_finite(test_col_es_t_lake, 
                                                test_lakestate_vars_lake_icefrac_col):
        return CheckStatus.SKIPPED
    test_col_es_t_lake, test_lakestate_vars_lake_icefrac_col = NonFiniteValuesHandler.mask_non_finite_values(
        test_col_es_t_lake, test_lakestate_vars_lake_icefrac_col)

    fully_frozen = test_lakestate_vars_lake_icefrac_col == 1
    temp_dif = np.subtract(test_col_es_t_lake, TFRZ)

    assert np.all(~fully_frozen | (temp_dif <= 1e-3))


def check_surface_unfrozen_when_tke_present(
    test_lakestate_vars_lake_icefrac_col: npt.NDArray,
    test_col_pp_snl: npt.NDArray,
    test_lakestate_vars_savedtke1_col: npt.NDArray,
) -> None:
    if NonFiniteValuesHandler.is_all_not_finite(test_lakestate_vars_lake_icefrac_col,
                                                test_col_pp_snl, 
                                                test_lakestate_vars_savedtke1_col):
        return CheckStatus.SKIPPED
    (test_lakestate_vars_lake_icefrac_col, test_col_pp_snl, 
     test_lakestate_vars_savedtke1_col)=NonFiniteValuesHandler.mask_non_finite_values(
         test_lakestate_vars_lake_icefrac_col, test_col_pp_snl, 
         test_lakestate_vars_savedtke1_col)


    surface_not_frozen = test_lakestate_vars_lake_icefrac_col[:, 0, :] < 1E-6
    snow_not_present = test_col_pp_snl == 0
    unfrozen = surface_not_frozen & snow_not_present

    if unfrozen.mask.all():
        return CheckStatus.SKIPPED

    tke_present = test_lakestate_vars_savedtke1_col > 0.0

    assert np.all(~tke_present | unfrozen), (
        "Turbulant kinetic energy present on a frozen surface"
    )

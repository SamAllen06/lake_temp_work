import numpy as np
import numpy.typing as npt

from mtf_fault_finding import CheckStatus
from mtf_fault_finding import NonFiniteValuesHandler


def assert_is_frac(variable: npt.NDArray, check_combinme: str) -> None:
    assert np.all((variable >= 0.0) & (variable <= 1.0)), (
        f"Non-fractional values found in {name}"
    )


def assert_not_negative(variable: npt.NDArray, name: str) -> None:
    assert np.all(variable >= 0.0), f"Negative values found in {name}"


def check_lake_layer_ice_fraction_is_fraction(
    test_lakestate_vars_lake_icefrac_col: npt.NDArray
) -> None:
    if NonFiniteValuesHandler.is_all_not_finite(test_lakestate_vars_lake_icefrac_col):
        return CheckStatus.SKIPPED
    test_lakestate_vars_lake_icefrac_col = (
        NonFiniteValuesHandler.mask_non_finite_values(
            test_lakestate_vars_lake_icefrac_col))

    assert_is_frac(
        test_lakestate_vars_lake_icefrac_col, "lakestate_vars%lake_icefrac_col"
    )


def check_surface_absorption_fraction_is_fraction(
    test_lakestate_vars_betaprime_col: npt.NDArray
) -> None:
    if NonFiniteValuesHandler.is_all_not_finite(test_lakestate_vars_betaprime_col):
        return CheckStatus.SKIPPED
    test_lakestate_vars_betaprime_col = NonFiniteValuesHandler.mask_non_finite_values(
        test_lakestate_vars_betaprime_col)

    assert_is_frac(test_lakestate_vars_betaprime_col, "lakestate_vars%betaprime_col")


def check_water_snow_equivilant_not_negative(
    test_col_ws_h2osno: npt.NDArray
) -> None:
    if NonFiniteValuesHandler.is_all_not_finite(test_col_ws_h2osno):
        return CheckStatus.SKIPPED
    test_col_ws_h2osno = NonFiniteValuesHandler.mask_non_finite_values(
        test_col_ws_h2osno)

    assert_not_negative(test_col_ws_h2osno, "col_ws%ws_h2osno")


def check_snow_depth_not_negative(
    test_col_ws_snow_depth: npt.NDArray
) -> None:
    if NonFiniteValuesHandler.is_all_not_finite(test_col_ws_snow_depth):
        return CheckStatus.SKIPPED
    test_col_ws_snow_depth = NonFiniteValuesHandler.mask_non_finite_values(
        test_col_ws_snow_depth)

    assert_not_negative(test_col_ws_snow_depth, "col_ws%snow_depth")


def check_snow_freeze_rate_not_negative(
    test_col_wf_qflx_snofrz_lyr: npt.NDArray
) -> None:
    if NonFiniteValuesHandler.is_all_not_finite(test_col_wf_qflx_snofrz_lyr):
        return CheckStatus.SKIPPED
    test_col_wf_qflx_snofrz_lyr = NonFiniteValuesHandler.mask_non_finite_values(
        test_col_wf_qflx_snofrz_lyr)

    assert_not_negative(test_col_wf_qflx_snofrz_lyr, "col_wf%qflx_snofrz_lyr")


def check_snow_melt_flux_not_negative(
    test_col_wf_qflx_snomelt: npt.NDArray
) -> None:
    if NonFiniteValuesHandler.is_all_not_finite(test_col_wf_qflx_snomelt):
        return CheckStatus.SKIPPED
    test_col_wf_qflx_snomelt = NonFiniteValuesHandler.mask_non_finite_values(
        test_col_wf_qflx_snomelt)

    assert_not_negative(test_col_wf_qflx_snomelt, "col_wf%qflx_snomelt")


def check_net_snow_melt_not_negative(
    test_col_wf_qflx_snow_melt: npt.NDArray
) -> None:
    if NonFiniteValuesHandler.is_all_not_finite(test_col_wf_qflx_snow_melt):
        return CheckStatus.SKIPPED
    test_col_wf_qflx_snow_melt = NonFiniteValuesHandler.mask_non_finite_values(
        test_col_wf_qflx_snow_melt)

    assert_not_negative(test_col_wf_qflx_snow_melt, "col_wf%qflx_snow_melt")


def check_snow_melt_heat_flux_not_negative(
    test_col_ef_eflx_snomelt: npt.NDArray
) -> None:
    if NonFiniteValuesHandler.is_all_not_finite(test_col_ef_eflx_snomelt):
        return CheckStatus.SKIPPED
    test_col_ef_eflx_snomelt = NonFiniteValuesHandler.mask_non_finite_values(
        test_col_ef_eflx_snomelt)

    assert_not_negative(test_col_ef_eflx_snomelt, "col_ef%eflx_snomelt")


def check_lake_water_transport_resistance_not_negative(
    test_lakestate_vars_lakeresist_col: npt.NDArray
) -> None:
    if NonFiniteValuesHandler.is_all_not_finite(test_lakestate_vars_lakeresist_col):
        return CheckStatus.SKIPPED
    test_lakestate_vars_lakeresist_col = NonFiniteValuesHandler.mask_non_finite_values(
        test_lakestate_vars_lakeresist_col)

    assert_not_negative(
        test_lakestate_vars_lakeresist_col, "lakestate_vars%lakeresist_col"
    )


def check_saved_eddy_conductivity_not_negative(
    test_lakestate_vars_savedtke1_col: npt.NDArray
) -> None:
    if NonFiniteValuesHandler.is_all_not_finite(test_lakestate_vars_savedtke1_col):
        return CheckStatus.SKIPPED
    test_lakestate_vars_savedtke1_col = NonFiniteValuesHandler.mask_non_finite_values(
        test_lakestate_vars_savedtke1_col)

    assert_not_negative(
        test_lakestate_vars_savedtke1_col, "lakestate_vars%savedtke1_col"
    )


def check_soil_heat_content_not_negative(
    test_col_es_hc_soi: npt.NDArray
) -> None:
    if NonFiniteValuesHandler.is_all_not_finite(test_col_es_hc_soi):
        return CheckStatus.SKIPPED
    test_col_es_hc_soi = NonFiniteValuesHandler.mask_non_finite_values(
        test_col_es_hc_soi)

    assert_not_negative(test_col_es_hc_soi, "col_es%hc_soi")


def check_combined_heat_content_not_less_than_soil_heat_content(
    test_col_es_hc_soi: npt.NDArray, test_col_es_hc_soisno: npt.NDArray
) -> None:
    if NonFiniteValuesHandler.is_all_not_finite(test_col_es_hc_soi, 
                                                test_col_es_hc_soisno):
        return CheckStatus.SKIPPED
    test_col_es_hc_soi, test_col_es_hc_soisno = (
        NonFiniteValuesHandler.mask_non_finite_values(test_col_es_hc_soi, 
                                                      test_col_es_hc_soisno))

    assert np.all(test_col_es_hc_soisno >= test_col_es_hc_soi)

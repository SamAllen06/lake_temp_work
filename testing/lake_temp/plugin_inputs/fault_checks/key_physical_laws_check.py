from enum import Enum

import numpy as np
import numpy.typing as npt

from mtf_fault_finding import CheckStatus
from mtf_fault_finding import NonFiniteValuesHandler

# tfrz not in constants.
TFRZ = 273.15

# imelt representation
class IMelt(Enum):
    NEW = 0
    MELTING = 1
    FREEZING = 2


def check_energy_conservation(
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_es_t_lake: npt.NDArray,
    test_lakestate_vars_lake_icefrac_col: npt.NDArray,

    test_col_ef_errsoi: npt.NDArray,
    test_col_es_hc_soisno: npt.NDArray,
    test_veg_ef_eflx_gnet: npt.NDArray,
    test_veg_ef_eflx_soil_grnd: npt.NDArray,
    test_veg_ef_eflx_sh_grnd: npt.NDArray,
):
    if NonFiniteValuesHandler.is_all_not_finite(test_col_pp_snl, test_col_ws_h2osno, 
            test_col_es_t_lake, test_lakestate_vars_lake_icefrac_col, 
            test_col_ef_errsoi, test_col_es_hc_soisno, test_veg_ef_eflx_gnet, 
            test_veg_ef_eflx_soil_grnd, test_veg_ef_eflx_sh_grnd):
        return CheckStatus.SKIPPED
    (test_col_pp_snl, test_col_ws_h2osno, test_col_es_t_lake, 
     test_lakestate_vars_lake_icefrac_col, test_col_ef_errsoi, test_col_es_hc_soisno, 
     test_veg_ef_eflx_gnet, test_veg_ef_eflx_soil_grnd, test_veg_ef_eflx_sh_grnd)=(
         NonFiniteValuesHandler.mask_non_finite_values(test_col_pp_snl, 
            test_col_ws_h2osno, test_col_es_t_lake, 
            test_lakestate_vars_lake_icefrac_col, test_col_ef_errsoi, 
            test_col_es_hc_soisno, test_veg_ef_eflx_gnet, test_veg_ef_eflx_soil_grnd, 
            test_veg_ef_eflx_sh_grnd))
    
    no_snow_layers = test_col_pp_snl == 0
    no_snow_water = test_col_ws_h2osno == 0.0
    surface_above_freezing = test_col_es_t_lake[:, 0, :] > TFRZ
    unfrozen_surface = test_lakestate_vars_lake_icefrac_col[:, 0, :] == 0.0

    # Skip unless lake is unfrozen.
    if not np.all(
        no_snow_layers & no_snow_water & surface_above_freezing & unfrozen_surface
    ):
        return CheckStatus.SKIPPED

    # Verify error is below threshold used in LakeTemperature.
    assert np.all(np.abs(test_col_ef_errsoi) < 1E-6), "error above threshold"

    # Difference between each time step.
    #change_in_combined_heat_content = np.diff(test_col_es_hc_soisno, axis=0)
    # change_in_individual_heat_contents_added = integral(fin + lake energy flux (probably veg_ef_eflx_soil_grnd) + soil energy flux (probably veg_ef_eflx_gnet))dt
    #change_in_individual_heat_contents_added = np.trapezoid(np.add(test_veg_ef_eflx_gnet,
    #                        test_veg_ef_eflx_soil_grnd, test_veg_ef_eflx_sh_grnd), axis=0)
    # assert |change_in_combined_heat_content - change_in_individual_heat_contents_added| < 1E-6
    #heat_content_diff = np.subtract(change_in_combined_heat_content,
    #                                 change_in_individual_heat_contents_added)
    #assert np.all(np.abs(heat_content_diff) < 1E-6)


def check_freezing_latent_heat(
    test_col_es_t_lake: npt.NDArray,
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_es_t_soisno: npt.NDArray,

    test_col_wf_qflx_snofrz_lyr: npt.NDArray,
    test_col_wf_qflx_snomelt: npt.NDArray,
    test_col_ef_imelt: npt.NDArray,
    test_col_ws_snow_depth: npt.NDArray,
    test_col_ws_h2osoi_ice: npt.NDArray,
    test_col_es_hc_soisno: npt.NDArray,
    hfus: npt.NDArray,
):
    if NonFiniteValuesHandler.is_all_not_finite(test_col_es_t_lake, test_col_pp_snl, 
            test_col_ws_h2osno, test_col_wf_qflx_snofrz_lyr, test_col_wf_qflx_snomelt, 
            test_col_ef_imelt, test_col_ws_snow_depth, test_col_ws_h2osoi_ice, 
            test_col_es_hc_soisno, test_col_es_t_soisno):
        return CheckStatus.SKIPPED
    (test_col_es_t_lake, test_col_pp_snl, test_col_ws_h2osno, 
     test_col_wf_qflx_snofrz_lyr, test_col_wf_qflx_snomelt, test_col_ef_imelt,
     test_col_ws_snow_depth, test_col_ws_h2osoi_ice, test_col_es_hc_soisno, 
     test_col_es_t_soisno)=(
         NonFiniteValuesHandler.mask_non_finite_values(
             test_col_es_t_lake, test_col_pp_snl, test_col_ws_h2osno,
             test_col_wf_qflx_snofrz_lyr, test_col_wf_qflx_snomelt, test_col_ef_imelt,
             test_col_ws_snow_depth, test_col_ws_h2osoi_ice, test_col_es_hc_soisno, 
             test_col_es_t_soisno))
    
    some_snow_layers = test_col_pp_snl > 0
    some_snow_water = test_col_ws_h2osno > 0.0

    lake_surface_is_at_or_below_freezing = np.all(test_col_es_t_lake <= TFRZ)
    soil_snow_layers_below_freezing = np.all(test_col_es_t_soisno < TFRZ)

    snow_present = some_snow_layers & some_snow_water
    if (not np.any(snow_present) or not lake_surface_is_at_or_below_freezing 
            or not soil_snow_layers_below_freezing):
        return CheckStatus.SKIPPED

    # Verify snow is freezing
    surface_snow_freezing = test_col_wf_qflx_snofrz_lyr[:, 0, :] > 0.0
    surface_snow_labeled_freezing = test_col_ef_imelt[:, 0, :] == IMelt.FREEZING.value
    assert surface_snow_freezing == snow_present, (
        "snow present does not match surface snow freezing")
    assert surface_snow_labeled_freezing == snow_present, (
        "snow present does not match surface snow labeled freezing")

    # Verify snow is not melting
    snow_not_melting = test_col_wf_qflx_snomelt == 0.0
    assert snow_not_melting == snow_present, (
        "snow present does not match snow not melting")

    # Verify snow water and depth are not decreasing
    snow_water_not_decreasing = np.diff(test_col_ws_h2osno, axis=0) >= 0.0
    assert np.all(snow_water_not_decreasing), "snow water is decreasing"
    snow_depth_not_decreasing = np.diff(test_col_ws_snow_depth, axis=0) >= 0.0
    assert np.all(snow_depth_not_decreasing), "snow depth is decreasing"

    # Verify sensible heat reflects latent heat released from freezing snow in MJ/m2
    # Ice content of snow (kg/m2) by column
    ice_content = np.sum(test_col_ws_h2osoi_ice, axis=1)
    # Change in ice content of snow (kg/m2) over each time step
    ice_content_diff = np.diff(ice_content, axis=0)
    # Change in latent heat (MJ/m2) per time step
    latent_heat_diff = ice_content_diff * hfus * 1E-6
    # Change in sensible heat (MJ/m2) per time step
    sensible_heat_diff = np.diff(test_col_es_hc_soisno, axis=0)

    assert np.isclose(latent_heat_diff, sensible_heat_diff), (
        "latent heat difference and sensible heat difference are not close")


def check_melting_latent_heat(
    test_col_es_t_lake: npt.NDArray,
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,

    hfus: npt.NDArray,
    dtime_mod: npt.NDArray,
    test_col_wf_qflx_snomelt: npt.NDArray,
    test_col_wf_qflx_snow_melt: npt.NDArray,
    test_col_ef_eflx_snomelt: npt.NDArray,
    test_col_ws_snow_depth: npt.NDArray,
):
    if NonFiniteValuesHandler.is_all_not_finite(test_col_es_t_lake, test_col_pp_snl, 
            test_col_ws_h2osno, test_col_wf_qflx_snomelt, test_col_wf_qflx_snow_melt, 
            test_col_ef_eflx_snomelt, test_col_ws_snow_depth):
        return CheckStatus.SKIPPED
    (test_col_es_t_lake, test_col_pp_snl, test_col_ws_h2osno, test_col_wf_qflx_snomelt, 
     test_col_wf_qflx_snow_melt, test_col_ef_eflx_snomelt, test_col_ws_snow_depth)=(
         NonFiniteValuesHandler.mask_non_finite_values(test_col_es_t_lake, 
            test_col_pp_snl,test_col_ws_h2osno, test_col_wf_qflx_snomelt, 
            test_col_wf_qflx_snow_melt, test_col_ef_eflx_snomelt, test_col_ws_snow_depth
            ))

    no_snow_layers = test_col_pp_snl == 0
    some_snow_water = test_col_ws_h2osno > 0.0

    lake_surface_above_freezing = test_col_es_t_lake[:, 0, :] > TFRZ

    soil_water_present = no_snow_layers & some_snow_water & lake_surface_above_freezing
    if not np.any(soil_water_present):
        return CheckStatus.SKIPPED

    # Verify snow is melting and has melted on all columns were soil water is present.
    snow_is_melting = test_col_wf_qflx_snomelt > 0.0
    assert np.all(snow_is_melting), "snow is not melting"
    snow_has_melted = test_col_wf_qflx_snow_melt > 0.0
    assert np.all(snow_has_melted), "snow has not melted"
    
    # Verify energy flux is consistent with latent heat from snow melt rate.
    assert np.all(test_col_ef_eflx_snomelt == test_col_wf_qflx_snomelt * hfus), (
        "energy flux is not consistent with latent heat from snow melt rate")

    # Verify snow depth (m) decreases consistently with snow melt rate (mm/s)
    assert (np.diff(test_col_ws_snow_depth * 1000.0, axis=0) / dtime_mod 
            == test_col_wf_qflx_snomelt), (
        "snow depth does not decrease consistently with now melt rate")


def check_methane_conductance_gated_by_ice(
    use_lch4: npt.NDArray,
    test_lakestate_vars_lake_icefrac_col: npt.NDArray,
    test_ch4_vars_grnd_ch4_cond_col: npt.NDArray,
):
    if NonFiniteValuesHandler.is_all_not_finite(test_lakestate_vars_lake_icefrac_col, 
                                                test_ch4_vars_grnd_ch4_cond_col):
        return CheckStatus.SKIPPED
    test_lakestate_vars_lake_icefrac_col, test_ch4_vars_grnd_ch4_cond_col = (
        NonFiniteValuesHandler.mask_non_finite_values(
                                                test_lakestate_vars_lake_icefrac_col, 
                                                test_ch4_vars_grnd_ch4_cond_col))

    some_surface_ice = test_lakestate_vars_lake_icefrac_col[:, 0, :] > 0.1

    if not use_lch4 == 1 or not np.any(some_surface_ice):
        return CheckStatus.SKIPPED

    conducting_methane = test_ch4_vars_grnd_ch4_cond_col > 0.0

    # Verify methane conductance is blocked by ice
    assert not np.any(some_surface_ice & conducting_methane), (
        "methane conductance is not blocked by ice")

def check_methane_conductance_allowed_without_ice(
    use_lch4: npt.NDArray,
    test_lakestate_vars_lake_icefrac_col: npt.NDArray,

    test_ch4_vars_grnd_ch4_cond_col: npt.NDArray,
    test_lakestate_vars_lakeresist_col: npt.NDArray,
    test_lakestate_vars_lake_raw_col: npt.NDArray,
):
    if NonFiniteValuesHandler.is_all_not_finite(test_lakestate_vars_lake_icefrac_col, 
            test_ch4_vars_grnd_ch4_cond_col, test_lakestate_vars_lakeresist_col, 
            test_lakestate_vars_lake_raw_col):
        return CheckStatus.SKIPPED
    (test_lakestate_vars_lake_icefrac_col, test_ch4_vars_grnd_ch4_cond_col,
     test_lakestate_vars_lakeresist_col, test_lakestate_vars_lake_raw_col) = (
        NonFiniteValuesHandler.mask_non_finite_values(
            test_lakestate_vars_lake_icefrac_col, test_ch4_vars_grnd_ch4_cond_col,
            test_lakestate_vars_lakeresist_col, test_lakestate_vars_lake_raw_col))

    no_surface_ice = test_lakestate_vars_lake_icefrac_col[:, 0, :] == 0.0

    if not use_lch4 == 1 or not np.any(no_surface_ice):
        return CheckStatus.SKIPPED

    expected_methane = 1.0 / (
        test_lakestate_vars_lakeresist_col + test_lakestate_vars_lake_raw_col
    )

    # Verify columns without ice conduct the expected methane.
    assert np.all(
        ~no_surface_ice | np.isclose(expected_methane, test_ch4_vars_grnd_ch4_cond_col)
    ), "columns without ice do not conduct the expected methane"

# Skipping radiation absorption for now because I'm not sure how patches and columns
# correspond.



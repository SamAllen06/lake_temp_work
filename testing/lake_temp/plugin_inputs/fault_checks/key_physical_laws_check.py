from enum import Enum

import numpy as np
import numpy.typing as npt

from mtf_fault_finding import CheckStatus

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
):
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
    assert np.all(test_col_ef_errsoi < 0.1)

    # Difference between each time step.
    #change_in_heat_content = np.diff(test_col_es_hc_soisno, axis=0)

    # Need to compare with lake and soil energy fluxes.


def check_freezing_latent_heat(
    test_col_es_t_lake: npt.NDArray,
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,

    test_col_wf_qflx_snofrz_lyr: npt.NDArray,
    test_col_wf_qflx_snomelt: npt.NDArray,
    test_col_ef_imelt: npt.NDArray,
    test_col_ws_snow_depth: npt.NDArray,
    test_col_wf_qflx_snofrz: npt.NDArray,
    test_col_ws_h2osoi_ice: npt.NDArray,
    test_col_es_hc_soisno: npt.NDArray,
    hfus: npt.NDArray,
):
    some_snow_layers = test_col_pp_snl > 0
    some_snow_water = test_col_ws_h2osno > 0.0

    lake_surface_is_at_or_below_freezing = np.all(test_col_es_t_lake <= TFRZ)

    snow_present = some_snow_layers & some_snow_water
    if not np.any(snow_present) or not lake_surface_is_at_or_below_freezing:
        return CheckStatus.SKIPPED

    # Verify snow is freezing
    surface_snow_freezing = test_col_wf_qflx_snofrz_lyr[:, 0, :] > 0.0
    surface_snow_labeled_freezing = test_col_ef_imelt[:, 0, :] == IMelt.FREEZING.value
    assert surface_snow_freezing == snow_present
    assert surface_snow_labeled_freezing == snow_present

    # Verify snow is not melting
    snow_not_melting = test_col_wf_qflx_snomelt == 0.0
    assert snow_not_melting == snow_present

    # Verify snow water and depth are not decreasing
    snow_water_not_decreasing = np.diff(test_col_ws_h2osno, axis=0) >= 0.0
    snow_depth_not_decreasing = np.diff(test_col_ws_snow_depth, axis=0) >= 0.0
    assert np.all(snow_water_not_decreasing & snow_depth_not_decreasing)

    # Verify sensible heat reflects latent heat released from freezing snow in MJ/m2
    # Ice content of snow (kg/m2) by column
    ice_content = np.sum(test_col_ws_h2osoi_ice, axis=1)
    # Change in ice content of snow (kg/m2) over each time step
    ice_content_diff = np.diff(ice_content, axis=0)
    # Change in latent heat (MJ/m2) per time step
    latent_heat_diff = ice_content_diff * hfus * 1E-6
    # Change in sensible heat (MJ/m2) per time step
    sensible_heat_diff = np.diff(test_col_es_hc_soisno, axis=0)

    assert np.isclose(latent_heat_diff, sensible_heat_diff)


def check_melting_latent_heat(
    test_col_es_t_lake: npt.NDArray,
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,

    hfus: npt.NDArray,
    dtime_mod: npt.NDArray,
    test_col_wf_qflx_snomelt: npt.NDArray,
    test_col_wf_qflx_snow_melt: npt.NDArray,
    test_col_ef_eflx_snomelt: npt.NDArray,
    test_col_ef_imelt: npt.NDArray,
    test_col_ws_snow_depth: npt.NDArray,
    test_col_wf_qflx_snofrz: npt.NDArray,
):
    no_snow_layers = test_col_pp_snl == 0
    some_snow_water = test_col_ws_h2osno > 0.0

    lake_surface_above_freezing = test_col_es_t_lake[:, 0, :] > TFRZ

    soil_water_present = no_snow_layers & some_snow_water & lake_surface_above_freezing
    if not np.any(soil_water_present):
        return CheckStatus.SKIPPED

    snow_is_melting = test_col_wf_qflx_snomelt > 0.0
    snow_has_melted = test_col_wf_qflx_snow_melt > 0.0
    
    # Verify snow is melting and has melted on all columns were soil water is present.
    assert np.all(~soil_water_present | (snow_is_melting & snow_has_melted))

    # Verify energy flux is consistent with latent heat from snow melt rate.
    assert np.all(test_col_ef_eflx_snomelt == test_col_wf_qflx_snomelt * hfus)

    # Verify snow depth (m) decreases consistently with snow melt rate (mm/s)
    assert (
        np.diff(test_col_ws_snow_depth * 1000.0, axis=0) / dtime_mod
        == test_col_wf_qflx_snomelt
    )

def check_latent_heat_from_lake(
    test_col_es_t_lake: npt.NDArray,
    test_lakestate_vars_lake_icefrac_col: npt.NDArray,
):
    almost_frozen = np.abs(1.0 - test_lakestate_vars_lake_icefrac_col) < 0.01
    almost_at_freezing = np.abs(TFRZ - test_col_es_t_lake) < 0.01

    if not np.any(almost_frozen):
        return CheckStatus.SKIPPED

    # Verify layers that are almost frozen are also almost at the freezing temperature.
    assert np.all(~almost_frozen | almost_at_freezing)

def check_methane_conductance_gated_by_ice(
    use_lch4: npt.NDArray,
    test_lakestate_vars_lake_icefrac_col: npt.NDArray,
    test_ch4_vars_grnd_ch4_cond_col: npt.NDArray,
):
    some_surface_ice = test_lakestate_vars_lake_icefrac_col[:, 0, :] > 0.1

    if not use_lch4 == 1 or not np.any(some_surface_ice):
        return CheckStatus.SKIPPED

    conducting_methane = test_ch4_vars_grnd_ch4_cond_col > 0.0

    # Verify methane conductance is blocked by ice
    assert not np.any(some_surface_ice & conducting_methane)

def check_methane_conductance_allowed_without_ice(
    use_lch4: npt.NDArray,
    test_lakestate_vars_lake_icefrac_col: npt.NDArray,

    test_ch4_vars_grnd_ch4_cond_col: npt.NDArray,
    test_lakestate_vars_lakeresist_col: npt.NDArray,
    test_lakestate_vars_lake_raw_col: npt.NDArray,
):
    no_surface_ice = test_lakestate_vars_lake_icefrac_col[:, 0, :] == 0.0

    if not use_lch4 == 1 or not np.any(no_surface_ice):
        return CheckStatus.SKIPPED

    expected_methane = 1.0 / (
        test_lakestate_vars_lakeresist_col + test_lakestate_vars_lake_raw_col
    )

    # Verify columns without ice conduct the expected methane.
    assert np.all(
        ~no_surface_ice | np.isclose(expected_methane, test_ch4_vars_grnd_ch4_cond_col)
    )

# Skipping radiation absorption for now because I'm not sure how patches and columns
# correspond.



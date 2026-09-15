from enum import Enum

import numpy as np
import numpy.typing as npt

from mtf_fault_finding import CheckStatus
from mtf_fault_finding import NonFiniteValuesHandler

# tfrz not in constants.
TFRZ = 273.15
# ELM fill value. Anything at or above this is spval, not data.
SPVAL_THRESHOLD = 1.0e30
ISTDLAK = 5              # lake column type, column_varcon.F90
HEAT_CONTENT_TOL = 9E-2  # MJ/m2; 3 sigma on baseline residual (8.2 W/m2 at dt=3600)

# imelt representation
class IMelt(Enum):
    NEW = 0
    MELTING = 1
    FREEZING = 2

def convert_patches_to_columns(
    patch_to_column_converter: npt.NDArray,
    num_columns: int,
    patch_variable: npt.NDArray,
    patch_weights: npt.NDArray = None,
    require_all_patches_valid: bool = True,
) -> np.ma.MaskedArray:
    """
    Aggregate a patch-level variable onto columns.
 
    patch_to_column_converter : (time, patch) 1-based column index per patch
    num_columns               : number of columns in the output
    patch_variable            : (time, patch) or (time, layer, patch)
    patch_weights             : optional (patch,) or (time, patch) weights.
                                None -> plain sum, matching the original.
    require_all_patches_valid : if True, a column is masked when ANY of its
                                patches is masked. If False, masked patches
                                are skipped and the remaining ones summed,
                                which is what the original did implicitly.
 
    Returns a masked array with the patch axis replaced by a column axis.
    """
    converter = np.ma.getdata(patch_to_column_converter)
 
    if converter.ndim == 2:
        if not np.all(converter == converter[0]):
            raise ValueError(
                "patch -> column map is not constant in time; "
                "using row 0 would be wrong"
            )
        column_of_patch = converter[0].astype(int) - 1
    else:
        column_of_patch = converter.astype(int) - 1
 
    if column_of_patch.min() < 0:
        raise ValueError(
            f"map minimum is {column_of_patch.min() + 1} before the 1-based "
            "correction; expected 1. Is the map already 0-based?"
        )
    if column_of_patch.max() >= num_columns:
        raise ValueError(
            f"map maximum {column_of_patch.max() + 1} exceeds num_columns "
            f"{num_columns}"
        )
 
    patch_axis = patch_variable.ndim - 1
    if patch_variable.shape[patch_axis] != column_of_patch.size:
        raise ValueError(
            f"patch axis is {patch_variable.shape[patch_axis]} but the map "
            f"covers {column_of_patch.size} patches"
        )
 
    # Mask NaN, inf AND spval. The original missed spval entirely.
    values = np.ma.masked_invalid(np.ma.asarray(patch_variable, dtype=float))
    values = np.ma.masked_greater_equal(values, SPVAL_THRESHOLD)
 
    weights = None
    if patch_weights is not None:
        weights = np.ma.masked_invalid(np.ma.asarray(patch_weights, dtype=float))
        if weights.ndim == 1:
            broadcast_shape = [1] * patch_variable.ndim
            broadcast_shape[patch_axis] = weights.size
            weights = weights.reshape(broadcast_shape)
 
    output_shape = list(patch_variable.shape)
    output_shape[patch_axis] = num_columns
    variable_by_column = np.ma.masked_all(tuple(output_shape), dtype=float)
 
    for column_index in range(num_columns):
        patch_indices = np.flatnonzero(column_of_patch == column_index)
        if patch_indices.size == 0:
            # Column has no patches. Leave it masked rather than zero.
            continue
 
        column_values = np.take(values, patch_indices, axis=patch_axis)
        value_mask = np.ma.getmaskarray(column_values)
 
        if require_all_patches_valid:
            drop = value_mask.any(axis=patch_axis)
        else:
            drop = value_mask.all(axis=patch_axis)
 
        if patch_weights is None:
            aggregated = np.ma.sum(column_values, axis=patch_axis)
        else:
            column_weights = np.ma.take(weights, patch_indices, axis=patch_axis)
            weight_total = np.ma.sum(
                np.ma.masked_where(value_mask, np.broadcast_to(
                    column_weights, column_values.shape)),
                axis=patch_axis,
            )
            aggregated = (
                np.ma.sum(column_values * column_weights, axis=patch_axis)
                / weight_total
            )
            drop = drop | np.ma.getmaskarray(weight_total) | (weight_total == 0)
 
        index = [slice(None)] * patch_variable.ndim
        index[patch_axis] = column_index
        variable_by_column[tuple(index)] = np.ma.masked_where(drop, aggregated)
 
    return variable_by_column


def is_passing_energy_conservation_preconditions(
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_es_t_lake: npt.NDArray,
    test_lakestate_vars_lake_icefrac_col: npt.NDArray,
) -> bool:
    if NonFiniteValuesHandler.is_all_not_finite(test_col_pp_snl, test_col_ws_h2osno, 
            test_col_es_t_lake, test_lakestate_vars_lake_icefrac_col):
        return False
    # (test_col_pp_snl, test_col_ws_h2osno, test_col_es_t_lake, 
    #  test_lakestate_vars_lake_icefrac_col
    #  )= NonFiniteValuesHandler.mask_non_finite_values(test_col_pp_snl, 
    #     test_col_ws_h2osno, test_col_es_t_lake, test_lakestate_vars_lake_icefrac_col)

    return True
    
    # no_snow_layers = test_col_pp_snl == 0
    # no_snow_water = test_col_ws_h2osno == 0.0
    # surface_above_freezing = test_col_es_t_lake[:, 0, :] > TFRZ
    # unfrozen_surface = test_lakestate_vars_lake_icefrac_col[:, 0, :] == 0.0

    # # Skip unless lake is unfrozen.
    # return np.all(
    #     no_snow_layers & no_snow_water & surface_above_freezing & unfrozen_surface
    # )


def is_passing_freezing_latent_heat_preconditions(
    test_col_es_t_lake: npt.NDArray,
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_es_t_soisno: npt.NDArray,
) -> bool:
    if NonFiniteValuesHandler.is_all_not_finite(test_col_es_t_lake, test_col_pp_snl, 
            test_col_ws_h2osno, test_col_es_t_soisno):
        return False
    (test_col_es_t_lake, test_col_pp_snl, test_col_ws_h2osno, test_col_es_t_soisno)=(
         NonFiniteValuesHandler.mask_non_finite_values(
             test_col_es_t_lake, test_col_pp_snl, test_col_ws_h2osno, 
             test_col_es_t_soisno))
    
    some_snow_layers = test_col_pp_snl < 0
    some_snow_water = test_col_ws_h2osno > 0.0
    some_snow_present = np.any(some_snow_layers & some_snow_water)

    soil_snow_layers_below_freezing = np.all(test_col_es_t_soisno[:, 0, :] < TFRZ)
    lake_surface_is_at_or_below_freezing = np.all(test_col_es_t_lake[:, 0, :] <= TFRZ)
    temp_below_freezing = soil_snow_layers_below_freezing and lake_surface_is_at_or_below_freezing

    return (some_snow_present and temp_below_freezing)


def is_passing_snow_melt_preconditions(
    test_col_es_t_lake: npt.NDArray,
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
) -> bool:
    if NonFiniteValuesHandler.is_all_not_finite(test_col_es_t_lake, test_col_pp_snl, 
            test_col_ws_h2osno):
        return False
    (test_col_es_t_lake, test_col_pp_snl, test_col_ws_h2osno)=(
         NonFiniteValuesHandler.mask_non_finite_values(test_col_es_t_lake, 
             test_col_pp_snl, test_col_ws_h2osno))
    
    no_snow_layers = test_col_pp_snl == 0 
    some_snow_water = test_col_ws_h2osno > 0.0
    some_snow_water_present = np.any(no_snow_layers & some_snow_water)

    lake_surface_above_freezing = np.all(test_col_es_t_lake[:, 0, :] > TFRZ)
    return some_snow_water_present and lake_surface_above_freezing


def check_errsoi_threshold(
    #variables used in preconditions method
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_es_t_lake: npt.NDArray,
    test_lakestate_vars_lake_icefrac_col: npt.NDArray,  

    #variables used only in check
    test_col_ef_errsoi: npt.NDArray,
):
    # preconditions method returns false if all values in any variable are not finite 
    if not is_passing_energy_conservation_preconditions(test_col_pp_snl, 
            test_col_ws_h2osno, test_col_es_t_lake, test_lakestate_vars_lake_icefrac_col
    ):
        return CheckStatus.SKIPPED
    # NonFinitevaluesHandler then only has to check the variables not passed to the 
    # preconditions method
    if NonFiniteValuesHandler.is_all_not_finite(test_col_ef_errsoi):
        return CheckStatus.SKIPPED
    # NonFiniteValuesHandler only has to mask values in the variable used from this 
    # point onward
    test_col_ef_errsoi=NonFiniteValuesHandler.mask_non_finite_values(test_col_ef_errsoi)

    no_snow_layers = test_col_pp_snl == 0
    no_snow_water = test_col_ws_h2osno == 0.0
    surface_above_freezing = test_col_es_t_lake[:, 0, :] > TFRZ
    unfrozen_surface = test_lakestate_vars_lake_icefrac_col[:, 0, :] == 0.0

    preconditions_met = no_snow_layers & no_snow_water & surface_above_freezing & unfrozen_surface

    # Verify error is below threshold used in LakeTemperature.
    assert np.all(~preconditions_met | (np.abs(test_col_ef_errsoi) <= 1E-6)), "error above threshold"


def check_heat_contents_close(
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_es_t_lake: npt.NDArray,
    test_lakestate_vars_lake_icefrac_col: npt.NDArray,

    test_col_es_hc_soisno: npt.NDArray,
    test_veg_pp_column: npt.NDArray,
    test_veg_ef_eflx_soil_grnd: npt.NDArray,
    test_col_pp_itype: npt.NDArray,
    dtime_mod,
):
    if not is_passing_energy_conservation_preconditions(test_col_pp_snl, 
            test_col_ws_h2osno, test_col_es_t_lake, test_lakestate_vars_lake_icefrac_col
    ):
          return CheckStatus.SKIPPED
    if NonFiniteValuesHandler.is_all_not_finite(test_col_es_hc_soisno, 
                                                test_veg_ef_eflx_soil_grnd):
        return CheckStatus.SKIPPED
    (test_col_es_hc_soisno, test_veg_ef_eflx_soil_grnd
     )=NonFiniteValuesHandler.mask_non_finite_values(
         test_col_es_hc_soisno, test_veg_ef_eflx_soil_grnd)

    total_time_steps = test_col_es_hc_soisno.shape[0]
    total_columns = test_col_es_hc_soisno.shape[1]
    # import pdb; pdb.set_trace()

    # MJ/(m^2)
    change_in_combined_heat_content = np.diff(test_col_es_hc_soisno, axis=0)

    # W/(m^2) 
    flux_col = convert_patches_to_columns(test_veg_pp_column, total_columns, test_veg_ef_eflx_soil_grnd)
    expected_flux_col = flux_col[1:, :]*dtime_mod/1e6

    heat_content_abs_diff = np.abs(np.subtract(change_in_combined_heat_content,
                            expected_flux_col))
    

    is_lake_column = test_col_pp_itype[0] == ISTDLAK

    snl_ok  = (test_col_pp_snl[:-1] == 0) & (test_col_pp_snl[1:] == 0)
    h2o_ok  = (test_col_ws_h2osno[:-1] == 0.0) & (test_col_ws_h2osno[1:] == 0.0)
    warm_ok = (test_col_es_t_lake[:-1, 0, :] > TFRZ) & (test_col_es_t_lake[1:, 0, :] > TFRZ)
    ice_ok  = (test_lakestate_vars_lake_icefrac_col[:-1, 0, :] == 0.0) & \
              (test_lakestate_vars_lake_icefrac_col[1:, 0, :] == 0.0)

    finite_ok = (~np.ma.getmaskarray(heat_content_abs_diff)
                 & np.isfinite(np.ma.getdata(heat_content_abs_diff)))

    preconditions_met = (is_lake_column[None, :] & snl_ok & h2o_ok
                         & warm_ok & ice_ok & finite_ok)

    if not preconditions_met.any():
        return CheckStatus.SKIPPED

    assert np.all(~preconditions_met
                  | (np.ma.getdata(heat_content_abs_diff) <= HEAT_CONTENT_TOL)), (
        "change in combined heat content not close to energy flux into column; "
        f"max residual {np.ma.getdata(heat_content_abs_diff)[preconditions_met].max():.4g} "
        f"MJ/m2 over {int(preconditions_met.sum())} samples"
    )


def check_surface_snow_freezing_where_snow_present(
    test_col_es_t_lake: npt.NDArray,
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_es_t_soisno: npt.NDArray,

    test_col_wf_qflx_snofrz_lyr: npt.NDArray,
):
    if not is_passing_freezing_latent_heat_preconditions(test_col_es_t_lake, 
            test_col_pp_snl, test_col_ws_h2osno, test_col_es_t_soisno):
        return CheckStatus.SKIPPED
    if NonFiniteValuesHandler.is_all_not_finite(test_col_wf_qflx_snofrz_lyr):
        return CheckStatus.SKIPPED
    (test_col_pp_snl, test_col_ws_h2osno, test_col_wf_qflx_snofrz_lyr)=(
        NonFiniteValuesHandler.mask_non_finite_values(test_col_pp_snl, 
            test_col_ws_h2osno, test_col_wf_qflx_snofrz_lyr))
    
    some_snow_layers = test_col_pp_snl < 0
    some_snow_water = test_col_ws_h2osno > 0.0
    snow_present = some_snow_layers & some_snow_water

    # Verify snow is freezing
    surface_snow_freezing = test_col_wf_qflx_snofrz_lyr[:, 0, :] > 0.0

    assert np.all(~snow_present | surface_snow_freezing), (
        "snow is not freezing where snow is present")
    

def check_snow_labeled_freezing_where_snow_present(
    test_col_es_t_lake: npt.NDArray,
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_es_t_soisno: npt.NDArray,

    test_col_ef_imelt: npt.NDArray,
):
    if not is_passing_freezing_latent_heat_preconditions(test_col_es_t_lake, 
            test_col_pp_snl, test_col_ws_h2osno, test_col_es_t_soisno):
        return CheckStatus.SKIPPED
    if NonFiniteValuesHandler.is_all_not_finite(test_col_ef_imelt):
        return CheckStatus.SKIPPED
    test_col_pp_snl, test_col_ws_h2osno, test_col_ef_imelt=(
        NonFiniteValuesHandler.mask_non_finite_values(test_col_pp_snl, 
            test_col_ws_h2osno, test_col_ef_imelt))
    
    surface_snow_labeled_freezing = test_col_ef_imelt[:, 0, :] == IMelt.FREEZING.value
    
    some_snow_layers = test_col_pp_snl < 0
    some_snow_water = test_col_ws_h2osno > 0.0

    snow_present = some_snow_layers & some_snow_water

    assert np.all(~snow_present | surface_snow_labeled_freezing), (
        "snow not labeled freezing where snow present")


def check_snow_not_melting_where_snow_present(
    test_col_es_t_lake: npt.NDArray,
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_es_t_soisno: npt.NDArray,

    test_col_wf_qflx_snomelt: npt.NDArray,
):
    if not is_passing_freezing_latent_heat_preconditions(test_col_es_t_lake, 
            test_col_pp_snl, test_col_ws_h2osno, test_col_es_t_soisno):
        return CheckStatus.SKIPPED
    if NonFiniteValuesHandler.is_all_not_finite(test_col_wf_qflx_snomelt):
        return CheckStatus.SKIPPED
    test_col_pp_snl, test_col_ws_h2osno, test_col_wf_qflx_snomelt=(
        NonFiniteValuesHandler.mask_non_finite_values(test_col_pp_snl, 
            test_col_ws_h2osno, test_col_wf_qflx_snomelt))
    
    # Verify snow is not melting
    snow_not_melting = test_col_wf_qflx_snomelt == 0.0
    some_snow_layers = test_col_pp_snl < 0
    some_snow_water = test_col_ws_h2osno > 0.0

    snow_present = some_snow_layers & some_snow_water

    assert np.all(~snow_present | snow_not_melting), (
        "snow melting where snow present")


def check_snow_water_not_decreasing(
    test_col_es_t_lake: npt.NDArray,
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_es_t_soisno: npt.NDArray,
):
    if not is_passing_freezing_latent_heat_preconditions(test_col_es_t_lake, 
            test_col_pp_snl, test_col_ws_h2osno, test_col_es_t_soisno):
        return CheckStatus.SKIPPED
    test_col_ws_h2osno=NonFiniteValuesHandler.mask_non_finite_values(test_col_ws_h2osno)
    
    # Verify snow water is not decreasing
    snow_water_not_decreasing = np.diff(test_col_ws_h2osno, axis=0) >= 0.0
    assert np.all(snow_water_not_decreasing), "snow water is decreasing"


def check_snow_depth_not_decreasing(
    test_col_es_t_lake: npt.NDArray,
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_es_t_soisno: npt.NDArray,

    test_col_ws_snow_depth: npt.NDArray,
):
    if not is_passing_freezing_latent_heat_preconditions(test_col_es_t_lake, test_col_pp_snl, 
            test_col_ws_h2osno, test_col_es_t_soisno):
        return CheckStatus.SKIPPED
    if NonFiniteValuesHandler.is_all_not_finite(test_col_ws_snow_depth):
        return CheckStatus.SKIPPED
    test_col_ws_snow_depth=NonFiniteValuesHandler.mask_non_finite_values(
        test_col_ws_snow_depth)
    
    # Verify snow depth is not decreasing
    snow_depth_not_decreasing = np.diff(test_col_ws_snow_depth, axis=0) >= 0.0
    assert np.all(snow_depth_not_decreasing), "snow depth is decreasing"


def check_heat_diff_close(
    test_col_es_t_lake: npt.NDArray,
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_es_t_soisno: npt.NDArray,

    test_col_ws_h2osoi_ice: npt.NDArray,
    test_col_es_hc_soisno: npt.NDArray,
    hfus: npt.NDArray,
):
    if not is_passing_freezing_latent_heat_preconditions(test_col_es_t_lake, 
            test_col_pp_snl, test_col_ws_h2osno, test_col_es_t_soisno):
        return CheckStatus.SKIPPED
    if NonFiniteValuesHandler.is_all_not_finite(test_col_ws_h2osoi_ice, 
                                                test_col_es_hc_soisno):
        return CheckStatus.SKIPPED
    test_col_ws_h2osoi_ice, test_col_es_hc_soisno=(
         NonFiniteValuesHandler.mask_non_finite_values(test_col_ws_h2osoi_ice, 
                                                       test_col_es_hc_soisno))

    # Verify sensible heat reflects latent heat released from freezing snow in MJ/m2
    # Ice content of snow (kg/m2) by column
    ice_content = np.sum(test_col_ws_h2osoi_ice, axis=1)
    # Change in ice content of snow (kg/m2) over each time step
    ice_content_diff = np.diff(ice_content, axis=0)
    # Change in latent heat (MJ/m2) per time step
    latent_heat_diff = ice_content_diff * hfus * 1E-6
    # Change in sensible heat (MJ/m2) per time step
    sensible_heat_diff = np.diff(test_col_es_hc_soisno, axis=0)

    abs_heat_diff = np.abs(np.subtract(latent_heat_diff, sensible_heat_diff))

    assert np.all(abs_heat_diff <= 1E-6), (
        "latent heat difference and sensible heat difference are not close")


def check_snow_melting_where_snow_water_present(
    test_col_es_t_lake: npt.NDArray,
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,

    test_col_wf_qflx_snomelt: npt.NDArray,
):
    if not is_passing_snow_melt_preconditions(test_col_es_t_lake, test_col_pp_snl, 
                                              test_col_ws_h2osno):
        return CheckStatus.SKIPPED
    if NonFiniteValuesHandler.is_all_not_finite(test_col_wf_qflx_snomelt):
        return CheckStatus.SKIPPED
    (test_col_pp_snl, test_col_ws_h2osno, test_col_wf_qflx_snomelt
     )=NonFiniteValuesHandler.mask_non_finite_values(test_col_pp_snl, 
                        test_col_ws_h2osno, test_col_wf_qflx_snomelt)
    
    snow_is_melting = test_col_wf_qflx_snomelt > 0.0

    no_snow_layers = test_col_pp_snl == 0 
    some_snow_water = test_col_ws_h2osno > 0.0
    snow_water_present = no_snow_layers & some_snow_water
    assert np.all(~snow_water_present | snow_is_melting), (
        'Snow not melting where snow water present')


def check_snow_melted_where_snow_water_present(
    test_col_es_t_lake: npt.NDArray,
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,

    test_col_wf_qflx_snow_melt: npt.NDArray,
):
    if not is_passing_snow_melt_preconditions(test_col_es_t_lake, test_col_pp_snl, 
                                              test_col_ws_h2osno):
        return CheckStatus.SKIPPED
    if NonFiniteValuesHandler.is_all_not_finite(test_col_wf_qflx_snow_melt):
        return CheckStatus.SKIPPED
    (test_col_pp_snl, test_col_ws_h2osno, test_col_wf_qflx_snow_melt
     )=NonFiniteValuesHandler.mask_non_finite_values(test_col_pp_snl, 
                    test_col_ws_h2osno, test_col_wf_qflx_snow_melt)
    
    snow_has_melted = test_col_wf_qflx_snow_melt > 0.0

    no_snow_layers = test_col_pp_snl == 0 
    some_snow_water = test_col_ws_h2osno > 0.0
    snow_water_present = no_snow_layers & some_snow_water

    assert np.all(~snow_water_present | snow_has_melted), (
        'Snow not melted where snow water present')
    

def check_energy_flux_consistent_with_latent_heat(
    test_col_es_t_lake: npt.NDArray,
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,

    hfus: npt.NDArray,
    test_col_wf_qflx_snomelt: npt.NDArray,
    test_col_ef_eflx_snomelt: npt.NDArray,
):
    if not is_passing_snow_melt_preconditions(test_col_es_t_lake, test_col_pp_snl, 
                                              test_col_ws_h2osno):
        return CheckStatus.SKIPPED
    if NonFiniteValuesHandler.is_all_not_finite(test_col_wf_qflx_snomelt, 
                                                test_col_ef_eflx_snomelt):
        return CheckStatus.SKIPPED
    (test_col_pp_snl, test_col_ws_h2osno, test_col_wf_qflx_snomelt, 
     test_col_ef_eflx_snomelt)=(NonFiniteValuesHandler.mask_non_finite_values(
         test_col_pp_snl, test_col_ws_h2osno, test_col_wf_qflx_snomelt, 
         test_col_ef_eflx_snomelt))
    
    no_snow_layers = test_col_pp_snl == 0 
    some_snow_water = test_col_ws_h2osno > 0.0
    snow_water_present = no_snow_layers & some_snow_water

    abs_diff_energy_flux_and_latent_heat = np.abs(np.subtract(
        test_col_ef_eflx_snomelt, test_col_wf_qflx_snomelt * hfus))

    # Verify energy flux is consistent with latent heat from snow melt rate.
    assert np.all(~snow_water_present | (abs_diff_energy_flux_and_latent_heat <= 1E-6)), (
        "energy flux is not consistent with latent heat from snow melt rate where snow "
        +"water present")


def check_snow_depth_decreases_with_snow_melt_rate(
    test_col_es_t_lake: npt.NDArray,
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,

    dtime_mod,
    test_col_wf_qflx_snomelt: npt.NDArray,
    test_col_ws_snow_depth: npt.NDArray,
):
    if not is_passing_snow_melt_preconditions(test_col_es_t_lake, test_col_pp_snl, 
                                              test_col_ws_h2osno):
        return CheckStatus.SKIPPED
    if NonFiniteValuesHandler.is_all_not_finite(test_col_wf_qflx_snomelt, 
                                                test_col_ws_snow_depth):
        return CheckStatus.SKIPPED
    (test_col_pp_snl, test_col_ws_h2osno, test_col_wf_qflx_snomelt, 
     test_col_ws_snow_depth)=(NonFiniteValuesHandler.mask_non_finite_values(
         test_col_pp_snl, test_col_ws_h2osno, test_col_wf_qflx_snomelt, 
         test_col_ws_snow_depth))

    no_snow_layers = test_col_pp_snl == 0 
    some_snow_water = test_col_ws_h2osno > 0.0
    snow_water_present = no_snow_layers & some_snow_water

    change_in_snow_depth_over_time = (np.diff(test_col_ws_snow_depth * 1000.0, axis=0) 
                                      / dtime_mod)
   
    # test_col_wf_qflx_snomelt is always 0 at timestep 0 because snow melt rate is
    # calculated from the previous timestep to the current one, so we can skip that 
    # timestep in the check.
    abs_diff_snow_depth_change_and_snow_melt_rate = np.abs(np.subtract(
        change_in_snow_depth_over_time, test_col_wf_qflx_snomelt[1:36,:]))
    
    # Verify snow depth (m) decreases consistently with snow melt rate (mm/s)
    # for snow melt rate to make sense, snow water has to be present at the initial 
    # timestep and the end timestep of the time interval over which the snow depth 
    # change is calculated.
    assert np.all(~(snow_water_present[0:35,:] & snow_water_present[1:36,:]) | 
                (abs_diff_snow_depth_change_and_snow_melt_rate <= 1E-3)),(
        "snow depth does not decrease consistently with snow melt rate where snow water"
        +" present")


def check_snow_water_equivalent_decreases_with_snow_melt_rate(
    test_col_es_t_lake: npt.NDArray,
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,

    dtime_mod,
    test_col_wf_qflx_snomelt: npt.NDArray,
):
    if not is_passing_snow_melt_preconditions(test_col_es_t_lake, test_col_pp_snl, 
                                              test_col_ws_h2osno):
        return CheckStatus.SKIPPED
    if NonFiniteValuesHandler.is_all_not_finite(test_col_wf_qflx_snomelt):
        return CheckStatus.SKIPPED
    (test_col_pp_snl, test_col_ws_h2osno, test_col_wf_qflx_snomelt)=(
        NonFiniteValuesHandler.mask_non_finite_values(test_col_pp_snl, 
                        test_col_ws_h2osno, test_col_wf_qflx_snomelt))

    no_snow_layers = test_col_pp_snl == 0 
    some_snow_water = test_col_ws_h2osno > 0.0
    snow_water_present = no_snow_layers & some_snow_water

    change_in_snow_water_equivalent_over_time = (np.diff(test_col_ws_h2osno * 1000.0, axis=0) 
                                      / dtime_mod)
   
    # test_col_wf_qflx_snomelt is always 0 at timestep 0 because snow melt rate is
    # calculated from the previous timestep to the current one, so we can skip that 
    # timestep in the check.
    abs_diff_snow_water_equivalent_change_and_snow_melt_rate = np.abs(np.subtract(
        change_in_snow_water_equivalent_over_time, test_col_wf_qflx_snomelt[1:36,:]))
    
    # Verify snow water equivalent (m) decreases consistently with snow melt rate (mm/s)
    # for snow melt rate to make sense, snow water has to be present at the initial 
    # timestep and the end timestep of the time interval over which the snow water 
    # equivalent change is calculated.
    assert np.all(~(snow_water_present[0:35,:] & snow_water_present[1:36,:]) | 
                (abs_diff_snow_water_equivalent_change_and_snow_melt_rate <= 1E-3)),(
        "snow water equivalent does not decrease consistently with snow melt rate where"
        +" snow water present")


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
    if not use_lch4 == 1:
        return CheckStatus.SKIPPED
    
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

    expected_methane = 1.0 / (
        test_lakestate_vars_lakeresist_col + test_lakestate_vars_lake_raw_col
    )

    abs_diff_expected_and_actual_methane = np.abs(np.subtract(
        expected_methane, test_ch4_vars_grnd_ch4_cond_col))

    # Verify columns without ice conduct the expected methane.
    assert np.all(
        ~no_surface_ice | (abs_diff_expected_and_actual_methane <= 1E-6)
    ), "columns without ice do not conduct the expected methane"


def check_betaprime_close_to_solar_rad_where_snow(
    test_col_pp_snl: npt.NDArray,
    test_solarabs_vars_sabg_patch: npt.NDArray,
    test_solarabs_vars_sabg_lyr_patch: npt.NDArray,
    test_lakestate_vars_betaprime_col: npt.NDArray,
    test_veg_pp_column: npt.NDArray
):
    if NonFiniteValuesHandler.is_all_not_finite(test_col_pp_snl, 
            test_solarabs_vars_sabg_patch, test_solarabs_vars_sabg_lyr_patch, 
            test_lakestate_vars_betaprime_col):
        return CheckStatus.SKIPPED
    (test_col_pp_snl, test_solarabs_vars_sabg_patch, test_solarabs_vars_sabg_lyr_patch,
     test_lakestate_vars_betaprime_col) = (
        NonFiniteValuesHandler.mask_non_finite_values(test_col_pp_snl, 
         test_solarabs_vars_sabg_patch, test_solarabs_vars_sabg_lyr_patch, 
         test_lakestate_vars_betaprime_col))
    
    #convert individual_heat_contents_by_patch_added from patches (681) to columns (345)
    radiation_lyr_patch_col = convert_patches_to_columns(test_veg_pp_column, 
        test_lakestate_vars_betaprime_col.shape[1], test_solarabs_vars_sabg_lyr_patch)
    radiation_patch_col = convert_patches_to_columns(test_veg_pp_column, 
        test_lakestate_vars_betaprime_col.shape[1], test_solarabs_vars_sabg_patch)

    #TODO see if I can use np. to simplify this
    top_snow_lyr_radiation = np.empty((radiation_lyr_patch_col.shape[0], radiation_lyr_patch_col.shape[2]))
    for i in range(radiation_lyr_patch_col.shape[0]):
        for j in range(0, radiation_lyr_patch_col.shape[2]-1):
                top_snow_lyr_radiation[i, j] = radiation_lyr_patch_col[i, test_col_pp_snl[i, j] + 5, j]
    top_snow_lyr_radiation_frac = top_snow_lyr_radiation/radiation_patch_col

    abs_diff_betaprime_and_solar_radiation = np.abs(np.subtract(
        test_lakestate_vars_betaprime_col, top_snow_lyr_radiation_frac))
    assert np.all(~(test_col_pp_snl < 0) | (abs_diff_betaprime_and_solar_radiation <= 1E-6)), (
        "betaprime not close to solar radiation absorbed into top layer where snow"
        +" present"
    )


def check_betaprime_close_to_solar_rad_where_no_snow(
    betavis,
    test_veg_pp_column: npt.NDArray,
    test_col_pp_snl: npt.NDArray,
    test_solarabs_vars_sabg_patch: npt.NDArray,
    test_lakestate_vars_betaprime_col: npt.NDArray,
    test_solarabs_vars_fsds_nir_d_patch: npt.NDArray,
    test_solarabs_vars_fsds_nir_i_patch: npt.NDArray,
    test_solarabs_vars_fsr_nir_d_patch: npt.NDArray,
    test_solarabs_vars_fsr_nir_i_patch: npt.NDArray
):
    if NonFiniteValuesHandler.is_all_not_finite(test_col_pp_snl, 
            test_solarabs_vars_sabg_patch, test_lakestate_vars_betaprime_col, 
            test_solarabs_vars_fsds_nir_d_patch, test_solarabs_vars_fsds_nir_i_patch, 
            test_solarabs_vars_fsr_nir_d_patch, test_solarabs_vars_fsr_nir_i_patch):
        return CheckStatus.SKIPPED
    (test_col_pp_snl, test_solarabs_vars_sabg_patch, test_lakestate_vars_betaprime_col, 
     test_solarabs_vars_fsds_nir_d_patch, test_solarabs_vars_fsds_nir_i_patch, 
     test_solarabs_vars_fsr_nir_d_patch, test_solarabs_vars_fsr_nir_i_patch) = (
        NonFiniteValuesHandler.mask_non_finite_values(test_col_pp_snl, 
            test_solarabs_vars_sabg_patch, test_lakestate_vars_betaprime_col, 
            test_solarabs_vars_fsds_nir_d_patch, test_solarabs_vars_fsds_nir_i_patch, 
            test_solarabs_vars_fsr_nir_d_patch, test_solarabs_vars_fsr_nir_i_patch))
    
    sabg_nir = ((test_solarabs_vars_fsds_nir_d_patch 
                 + test_solarabs_vars_fsds_nir_i_patch) 
                 - (test_solarabs_vars_fsr_nir_d_patch 
                    + test_solarabs_vars_fsr_nir_i_patch))
    NIR_frac = sabg_nir / test_solarabs_vars_sabg_patch
    NIR_betavis_blend_patches = NIR_frac + (1 - NIR_frac)*betavis
    NIR_betavis_blend_column = convert_patches_to_columns(test_veg_pp_column, 
            test_lakestate_vars_betaprime_col.shape[1], NIR_betavis_blend_patches)

    abs_dif_betaprime_NIR_betavis_blend = np.abs(np.subtract(test_lakestate_vars_betaprime_col, 
                                                     NIR_betavis_blend_column))
    assert np.all(~(test_col_pp_snl == 0) | (abs_dif_betaprime_NIR_betavis_blend <= 1E-6)), (
        "betaprime not close to NIR betavis blend where no snow present"
    )

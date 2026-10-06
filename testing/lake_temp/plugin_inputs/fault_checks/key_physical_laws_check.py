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

def snow_layer_count(test_col_pp_snl: npt.ArrayLike) -> np.ndarray:
    """Integer number of active snow layers per (time, column). 0..NLEVSNO."""
    snl = np.ma.filled(np.ma.asarray(test_col_pp_snl), 0)
    return np.clip(-np.rint(snl).astype(int), 0, 5)


def top_snow_layer(
    layered_variable: npt.ArrayLike,
    test_col_pp_snl: npt.ArrayLike,
) -> np.ma.MaskedArray:
    """Gather the topmost active snow layer of a (time, layer, column) field."""
    field = NonFiniteValuesHandler.mask_non_finite_values(layered_variable)

    layer_count = snow_layer_count(test_col_pp_snl)
    index = np.clip(5 - layer_count, 0, field.shape[1] - 1)

    times = np.arange(field.shape[0])[:, None]
    columns = np.arange(field.shape[2])[None, :]
    gathered = field[times, index, columns]

    return np.ma.masked_where(layer_count == 0, gathered)


def convert_patches_to_columns(
    patch_to_column_converter: npt.NDArray,
    num_columns: int,
    patch_variable: npt.NDArray
) -> np.ma.MaskedArray:
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
 
        drop = value_mask.any(axis=patch_axis)
 
        aggregated = np.ma.sum(column_values, axis=patch_axis)
 
        index = [slice(None)] * patch_variable.ndim
        index[patch_axis] = column_index
        variable_by_column[tuple(index)] = np.ma.masked_where(drop, aggregated)
 
    return variable_by_column

#replaces check_energy_conservation_preconditions
def unfrozen_open_water_selector(
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_es_t_lake: npt.NDArray,
    test_lakestate_vars_lake_icefrac_col: npt.NDArray,
    test_col_pp_itype
)  -> np.ndarray:

    (test_col_pp_snl, test_col_ws_h2osno, test_col_es_t_lake, 
     test_lakestate_vars_lake_icefrac_col, test_col_pp_itype
     )= NonFiniteValuesHandler.mask_non_finite_values(test_col_pp_snl, 
        test_col_ws_h2osno, test_col_es_t_lake, test_lakestate_vars_lake_icefrac_col, test_col_pp_itype)

    selector = (
        (test_col_pp_snl == 0)
        & (test_col_ws_h2osno == 0.0)
        & (test_col_es_t_lake[:, 0, :] > TFRZ)
        & (test_lakestate_vars_lake_icefrac_col[:, 0, :] == 0.0)
    )
    on_lake = test_col_pp_itype[0, :]==5

    return np.ma.filled(selector, False) & on_lake

# replaces is_passing_freezing_latent_heat_preconditions
def snow_freezing_selector(
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_es_t_soisno: npt.NDArray,
    test_col_es_t_lake: npt.NDArray,
    test_col_ws_h2osoi_liq: npt.NDArray,
    test_col_pp_itype: npt.NDArray,
) -> np.ndarray:
    (test_col_es_t_lake, test_col_pp_snl, test_col_ws_h2osno, test_col_es_t_soisno)=(
         NonFiniteValuesHandler.mask_non_finite_values(
             test_col_es_t_lake, test_col_pp_snl, test_col_ws_h2osno, 
             test_col_es_t_soisno))
    
    top_snow_temperature = top_snow_layer(test_col_es_t_soisno, test_col_pp_snl)
    top_snow_liquid = top_snow_layer(test_col_ws_h2osoi_liq, test_col_pp_snl)

    selector = (
        (test_col_pp_snl < 0)
        & (test_col_ws_h2osno > 0.0)
        & (top_snow_temperature < TFRZ)
        & (top_snow_liquid > 0.0)
        & (test_col_es_t_lake[:, 0, :] <= TFRZ)
    )
    on_lake = test_col_pp_itype[0, :]==5

    return np.ma.filled(selector, False) & on_lake

# replaces is_passing_snow_melt_preconditions
def snow_melt_selector(
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_es_t_lake: npt.NDArray,
    test_col_pp_itype: npt.NDArray,
) -> np.ndarray:
    (test_col_es_t_lake, test_col_pp_snl, test_col_ws_h2osno, test_col_pp_itype)=(
         NonFiniteValuesHandler.mask_non_finite_values(test_col_es_t_lake, 
             test_col_pp_snl, test_col_ws_h2osno, test_col_pp_itype))
    
    selector = ((test_col_pp_snl == 0) 
                & (test_col_ws_h2osno > 0.0) 
                & (test_col_es_t_lake[:, 0, :] > TFRZ))
    on_lake = test_col_pp_itype[0, :]==5
    return np.ma.filled(selector, False) & on_lake


def check_errsoi_threshold(
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_es_t_lake: npt.NDArray,
    test_lakestate_vars_lake_icefrac_col: npt.NDArray,  
    test_col_ef_errsoi: npt.NDArray,
    test_col_pp_itype: npt.NDArray
):
    if NonFiniteValuesHandler.is_all_not_finite(test_col_ws_h2osno, test_col_es_t_lake, 
            test_lakestate_vars_lake_icefrac_col, test_col_pp_snl, test_col_pp_itype, 
            test_col_ef_errsoi):
        return CheckStatus.SKIPPED
    test_col_ef_errsoi=NonFiniteValuesHandler.mask_non_finite_values(test_col_ef_errsoi)

    selector = unfrozen_open_water_selector(
        test_col_pp_snl,
        test_col_ws_h2osno,
        test_col_es_t_lake,
        test_lakestate_vars_lake_icefrac_col,
        test_col_pp_itype
    )
    # Verify error is below threshold used in LakeTemperature.
    assert np.all(~selector | (np.abs(test_col_ef_errsoi) <= 1E-6)), "error above threshold"


def check_surface_snow_freezing_where_snow_present(
    test_col_es_t_lake: npt.NDArray,
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_es_t_soisno: npt.NDArray,
    test_col_ws_h2osoi_liq: npt.NDArray,
    test_col_pp_itype: npt.NDArray,
    test_col_wf_qflx_snofrz_lyr: npt.NDArray,
):
    if NonFiniteValuesHandler.is_all_not_finite(test_col_wf_qflx_snofrz_lyr, 
            test_col_es_t_lake, test_col_ws_h2osno, test_col_es_t_soisno, 
            test_col_wf_qflx_snofrz_lyr, test_col_ws_h2osoi_liq, test_col_pp_itype):
        return CheckStatus.SKIPPED
    (test_col_wf_qflx_snofrz_lyr, test_col_es_t_lake, test_col_ws_h2osno, 
     test_col_es_t_soisno, test_col_wf_qflx_snofrz_lyr, test_col_ws_h2osoi_liq, 
     test_col_pp_itype)=NonFiniteValuesHandler.mask_non_finite_values(
         test_col_wf_qflx_snofrz_lyr, test_col_es_t_lake, test_col_ws_h2osno, 
         test_col_es_t_soisno, test_col_wf_qflx_snofrz_lyr, test_col_ws_h2osoi_liq, 
         test_col_pp_itype)

    scenario = snow_freezing_selector(
        test_col_pp_snl,
        test_col_ws_h2osno,
        test_col_es_t_soisno,
        test_col_es_t_lake,
        test_col_ws_h2osoi_liq,
        test_col_pp_itype,
    )

    freeze_rate = top_snow_layer(test_col_wf_qflx_snofrz_lyr, test_col_pp_snl)

    assert np.all(~scenario[:-1] | (freeze_rate[1:] > 0.0)), (
        "snow is not freezing where snow is present")
    

def check_snow_labeled_freezing_where_snow_present(
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_es_t_soisno: npt.NDArray,
    test_col_es_t_lake: npt.NDArray,
    test_col_ws_h2osoi_liq: npt.NDArray,
    test_col_pp_itype: npt.NDArray,
    test_col_ef_imelt: npt.NDArray,
):
    if NonFiniteValuesHandler.is_all_not_finite(test_col_pp_snl, test_col_ws_h2osno, 
            test_col_es_t_soisno, test_col_es_t_lake, test_col_ws_h2osoi_liq,
            test_col_pp_itype, test_col_ef_imelt):
        return CheckStatus.SKIPPED
    (test_col_pp_snl, test_col_ws_h2osno, test_col_es_t_soisno, test_col_es_t_lake, 
     test_col_ws_h2osoi_liq,test_col_pp_itype, test_col_ef_imelt
     )=NonFiniteValuesHandler.mask_non_finite_values(test_col_pp_snl, test_col_ws_h2osno, 
        test_col_es_t_soisno, test_col_es_t_lake, test_col_ws_h2osoi_liq,test_col_pp_itype, 
        test_col_ef_imelt)

    scenario = snow_freezing_selector(
        test_col_pp_snl,
        test_col_ws_h2osno,
        test_col_es_t_soisno,
        test_col_es_t_lake,
        test_col_ws_h2osoi_liq,
        test_col_pp_itype,
    )
    
    surface_snow_labeled_freezing = top_snow_layer(test_col_ef_imelt, test_col_pp_snl)[1:] == IMelt.FREEZING.value
    
    assert np.all(~scenario[:-1] | surface_snow_labeled_freezing), (
        "snow not labeled freezing where snow present")


def check_snow_water_not_decreasing(
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_es_t_soisno: npt.NDArray,
    test_col_es_t_lake: npt.NDArray,
    test_col_ws_h2osoi_liq: npt.NDArray,
    test_col_pp_itype: npt.NDArray,
) -> None:
    if NonFiniteValuesHandler.is_all_not_finite(test_col_es_t_lake, test_col_pp_snl, 
            test_col_ws_h2osno, test_col_es_t_soisno, test_col_ws_h2osoi_liq, test_col_pp_itype):
        return CheckStatus.SKIPPED
    (test_col_es_t_lake, test_col_pp_snl, test_col_ws_h2osno, test_col_es_t_soisno, 
     test_col_ws_h2osoi_liq, test_col_pp_itype)=NonFiniteValuesHandler.mask_non_finite_values(
         test_col_es_t_lake, test_col_pp_snl, test_col_ws_h2osno, test_col_es_t_soisno, 
         test_col_ws_h2osoi_liq, test_col_pp_itype)

    scenario = snow_freezing_selector(
        test_col_pp_snl,
        test_col_ws_h2osno,
        test_col_es_t_soisno,
        test_col_es_t_lake,
        test_col_ws_h2osoi_liq,
        test_col_pp_itype,
    )

    change = np.diff(test_col_ws_h2osno, axis=0)
    selector = scenario[:-1] & scenario[1:]

    # Verify snow water is not decreasing
    assert np.all(~selector | (change >= 1e-6)), (
        "h2osno decreases across an interval that stays in the freezing scenario"
    )


def check_snow_depth_not_decreasing(
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_es_t_soisno: npt.NDArray,
    test_col_es_t_lake: npt.NDArray,
    test_col_ws_h2osoi_liq: npt.NDArray,
    test_col_pp_itype: npt.NDArray,
    test_col_ws_snow_depth: npt.NDArray,
):
    if NonFiniteValuesHandler.is_all_not_finite(test_col_pp_snl, test_col_ws_h2osno,
            test_col_es_t_soisno, test_col_es_t_lake, test_col_ws_h2osoi_liq, 
            test_col_pp_itype, test_col_ws_snow_depth):
        return CheckStatus.SKIPPED
    (test_col_pp_snl, test_col_ws_h2osno,test_col_es_t_soisno, test_col_es_t_lake, 
     test_col_ws_h2osoi_liq, test_col_pp_itype, test_col_ws_snow_depth
     )=NonFiniteValuesHandler.mask_non_finite_values(
        test_col_pp_snl, test_col_ws_h2osno,test_col_es_t_soisno, test_col_es_t_lake, 
        test_col_ws_h2osoi_liq, test_col_pp_itype, test_col_ws_snow_depth)

    scenario = snow_freezing_selector(
        test_col_pp_snl,
        test_col_ws_h2osno,
        test_col_es_t_soisno,
        test_col_es_t_lake,
        test_col_ws_h2osoi_liq,
        test_col_pp_itype,
    )

    change = np.diff(test_col_ws_snow_depth, axis=0)
    selector = scenario[:-1] & scenario[1:]

    # Verify snow depth is not decreasing
    snow_depth_not_decreasing = np.diff(test_col_ws_snow_depth, axis=0) >= 0.0
    assert np.all(~selector | (change >= 1e-6)), (
        "snow_depth decreases across an interval that stays in the freezing scenario")


# Removed check because its logic is wrong and its physical content is already covered in other checks

# def check_heat_diff_close(
#     test_col_es_t_lake: npt.NDArray,
#     test_col_pp_snl: npt.NDArray,
#     test_col_ws_h2osno: npt.NDArray,
#     test_col_es_t_soisno: npt.NDArray,

#     test_col_ws_h2osoi_ice: npt.NDArray,
#     test_col_es_hc_soisno: npt.NDArray,
#     hfus: npt.NDArray,
# ):
#     if not is_passing_freezing_latent_heat_preconditions(test_col_es_t_lake, 
#             test_col_pp_snl, test_col_ws_h2osno, test_col_es_t_soisno):
#         return CheckStatus.SKIPPED
#     if NonFiniteValuesHandler.is_all_not_finite(test_col_ws_h2osoi_ice, 
#                                                 test_col_es_hc_soisno):
#         return CheckStatus.SKIPPED
#     test_col_ws_h2osoi_ice, test_col_es_hc_soisno=(
#          NonFiniteValuesHandler.mask_non_finite_values(test_col_ws_h2osoi_ice, 
#                                                        test_col_es_hc_soisno))

#     # Verify sensible heat reflects latent heat released from freezing snow in MJ/m2
#     # Ice content of snow (kg/m2) by column
#     ice_content = np.sum(test_col_ws_h2osoi_ice, axis=1)
#     # Change in ice content of snow (kg/m2) over each time step
#     ice_content_diff = np.diff(ice_content, axis=0)
#     # Change in latent heat (MJ/m2) per time step
#     latent_heat_diff = ice_content_diff * hfus * 1E-6
#     # Change in sensible heat (MJ/m2) per time step
#     sensible_heat_diff = np.diff(test_col_es_hc_soisno, axis=0)

#     abs_heat_diff = np.abs(np.subtract(latent_heat_diff, sensible_heat_diff))

#     assert np.all(abs_heat_diff <= 1E-6), (
#         "latent heat difference and sensible heat difference are not close")


def check_snow_not_melting_where_snow_present(
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_es_t_soisno: npt.NDArray,
    test_col_es_t_lake: npt.NDArray,
    test_col_ws_h2osoi_liq: npt.NDArray,
    test_col_pp_itype: npt.NDArray,
    test_col_wf_qflx_snomelt: npt.NDArray,
):
    if NonFiniteValuesHandler.is_all_not_finite(test_col_wf_qflx_snomelt):
        return CheckStatus.SKIPPED
    test_col_wf_qflx_snomelt=NonFiniteValuesHandler.mask_non_finite_values(
        test_col_wf_qflx_snomelt)

    scenario = snow_freezing_selector(
        test_col_pp_snl,
        test_col_ws_h2osno,
        test_col_es_t_soisno,
        test_col_es_t_lake,
        test_col_ws_h2osoi_liq,
        test_col_pp_itype,
    )
    
    # Verify snow is not melting
    snow_not_melting = test_col_wf_qflx_snomelt == 0.0

    assert np.all(~scenario[:-1] | snow_not_melting[1:]), (
        "snow melting where snow present")


def check_snow_melting_where_snow_water_present(
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_es_t_lake: npt.NDArray,
    test_col_pp_itype: npt.NDArray,
    test_col_wf_qflx_snomelt: npt.NDArray,
):
    if NonFiniteValuesHandler.is_all_not_finite(test_col_pp_snl, test_col_ws_h2osno, 
            test_col_es_t_lake, test_col_wf_qflx_snomelt, test_col_pp_itype):
        return CheckStatus.SKIPPED
    (test_col_pp_snl, test_col_ws_h2osno, test_col_es_t_lake, test_col_wf_qflx_snomelt, 
     test_col_pp_itype)=NonFiniteValuesHandler.mask_non_finite_values(
        test_col_pp_snl, test_col_ws_h2osno, test_col_es_t_lake, 
        test_col_wf_qflx_snomelt, test_col_pp_itype)
    
    scenario = snow_melt_selector(
        test_col_pp_snl, test_col_ws_h2osno, test_col_es_t_lake, test_col_pp_itype
    )

    snow_is_melting = test_col_wf_qflx_snomelt > 0.0

    assert np.all(~scenario[:-1] | snow_is_melting[1:]), (
        'Snow not melting where snow water present')


def check_snow_melted_where_snow_water_present(
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_es_t_lake: npt.NDArray,
    test_col_pp_itype: npt.NDArray,
    test_col_wf_qflx_snow_melt: npt.NDArray,
):
    if NonFiniteValuesHandler.is_all_not_finite(test_col_wf_qflx_snow_melt):
        return CheckStatus.SKIPPED
    (test_col_pp_snl, test_col_ws_h2osno, test_col_wf_qflx_snow_melt
     )=NonFiniteValuesHandler.mask_non_finite_values(test_col_pp_snl, 
                    test_col_ws_h2osno, test_col_wf_qflx_snow_melt)
    
    scenario = snow_melt_selector(test_col_pp_snl, test_col_ws_h2osno, 
                                  test_col_es_t_lake, test_col_pp_itype)

    snow_has_melted = test_col_wf_qflx_snow_melt > 0.0

    assert np.all(~scenario[:-1] | snow_has_melted[1:]), (
        'Snow not melted where snow water present')
    

def check_energy_flux_consistent_with_latent_heat(
    test_col_es_t_lake: npt.NDArray,
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,

    hfus: float,
    test_col_wf_qflx_snomelt: npt.NDArray,
    test_col_ef_eflx_snomelt: npt.NDArray,
    test_col_pp_itype: npt.NDArray,
):
    if NonFiniteValuesHandler.is_all_not_finite(test_col_es_t_lake, 
            test_col_wf_qflx_snomelt, test_col_pp_snl, test_col_ws_h2osno, 
            test_col_ef_eflx_snomelt, test_col_pp_itype):
        return CheckStatus.SKIPPED
    (test_col_es_t_lake, test_col_wf_qflx_snomelt, test_col_pp_snl, test_col_ws_h2osno, 
     test_col_ef_eflx_snomelt, test_col_pp_itype)=(NonFiniteValuesHandler.mask_non_finite_values(
         test_col_es_t_lake, test_col_wf_qflx_snomelt, test_col_pp_snl, 
         test_col_ws_h2osno, test_col_ef_eflx_snomelt, test_col_pp_itype))

    expected = test_col_wf_qflx_snomelt * hfus
    difference = test_col_ef_eflx_snomelt - expected
    
    abs_diff = np.abs(difference)

    on_lake = test_col_pp_itype[0, :]==5
    
    # Verify energy flux is consistent with latent heat from snow melt rate.
    assert np.all(~on_lake | (abs_diff <= 1E-6)), (
        "eflx_snomelt is not qflx_snomelt * hfus")

def check_betaprime_matches_nir_blend(
    betavis: float,
    test_veg_pp_column: npt.NDArray,
    test_solarabs_vars_sabg_patch: npt.NDArray,
    test_lakestate_vars_betaprime_col: npt.NDArray,
    test_solarabs_vars_fsds_nir_d_patch: npt.NDArray,
    test_solarabs_vars_fsds_nir_i_patch: npt.NDArray,
    test_solarabs_vars_fsr_nir_d_patch: npt.NDArray,
    test_solarabs_vars_fsr_nir_i_patch: npt.NDArray,
    test_col_pp_itype: npt.NDArray,
) -> None:
    if NonFiniteValuesHandler.is_all_not_finite(test_veg_pp_column, 
            test_solarabs_vars_sabg_patch, test_lakestate_vars_betaprime_col, 
            test_solarabs_vars_fsds_nir_d_patch, test_solarabs_vars_fsds_nir_i_patch, 
            test_solarabs_vars_fsr_nir_d_patch, test_solarabs_vars_fsr_nir_i_patch,
            test_col_pp_itype):
        return CheckStatus.SKIPPED
    (test_veg_pp_column, test_solarabs_vars_sabg_patch, test_lakestate_vars_betaprime_col, 
     test_solarabs_vars_fsds_nir_d_patch, test_solarabs_vars_fsds_nir_i_patch, 
     test_solarabs_vars_fsr_nir_d_patch, test_solarabs_vars_fsr_nir_i_patch, 
     test_col_pp_itype) = NonFiniteValuesHandler.mask_non_finite_values(
            test_veg_pp_column, test_solarabs_vars_sabg_patch, test_lakestate_vars_betaprime_col, 
            test_solarabs_vars_fsds_nir_d_patch, test_solarabs_vars_fsds_nir_i_patch, 
            test_solarabs_vars_fsr_nir_d_patch, test_solarabs_vars_fsr_nir_i_patch, 
            test_col_pp_itype)
    
    sabg_nir = (test_solarabs_vars_fsds_nir_d_patch + test_solarabs_vars_fsds_nir_i_patch 
                 - (test_solarabs_vars_fsr_nir_d_patch + test_solarabs_vars_fsr_nir_i_patch))
    sabg_nir = np.ma.minimum(sabg_nir, test_solarabs_vars_sabg_patch)
    NIR_frac = sabg_nir / np.ma.maximum(test_solarabs_vars_sabg_patch, 1e-5) #1e-5 is SABG floor
    blend_by_patch = NIR_frac + (1.0 - NIR_frac)*betavis
    blend_by_column = convert_patches_to_columns(test_veg_pp_column, 
            test_lakestate_vars_betaprime_col.shape[1], blend_by_patch)

    abs_dif = np.abs(np.subtract(test_lakestate_vars_betaprime_col, blend_by_column))
    
    on_lake = test_col_pp_itype[0, :]==5
    
    assert np.all(~on_lake | (abs_dif <= 1E-6)), (
        "betaprime not close to NIR betavis blend"
    )


# Replaced check_snow_depth_decreases_with_snow_melt_rate with check_snow_depth_not_increasing_while_melting

def check_snow_depth_not_increasing_while_melting(
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_es_t_lake: npt.NDArray,
    test_col_pp_itype: npt.NDArray,
    test_col_wf_qflx_snomelt: npt.NDArray,
    test_col_ws_snow_depth: npt.NDArray,
) -> None:
    if NonFiniteValuesHandler.is_all_not_finite(test_col_ws_snow_depth, test_col_wf_qflx_snomelt):
        return CheckStatus.SKIPPED
    test_col_ws_snow_depth, test_col_wf_qflx_snomelt = NonFiniteValuesHandler.mask_non_finite_values(
        test_col_ws_snow_depth, test_col_wf_qflx_snomelt)

    snow_depth_change = np.diff(test_col_ws_snow_depth, axis=0)
    scenario = snow_melt_selector(
        test_col_pp_snl, test_col_ws_h2osno, test_col_es_t_lake, test_col_pp_itype)
    melting = np.ma.filled(test_col_wf_qflx_snomelt[1:] > 0.0, False)
    selector = scenario[:-1] & scenario[1:] & melting

    assert np.all(~selector | (snow_depth_change<=1e-6))


# Removed checks that used dtime_mod to analyze change over time, as dtime_mod was not 
# consistant with the spacing between records for the time dimensions and 

# def check_heat_contents_close(
#     test_col_pp_snl: npt.NDArray,
#     test_col_ws_h2osno: npt.NDArray,
#     test_col_es_t_lake: npt.NDArray,
#     test_lakestate_vars_lake_icefrac_col: npt.NDArray,

#     test_col_es_hc_soisno: npt.NDArray,
#     test_veg_pp_column: npt.NDArray,
#     test_veg_ef_eflx_soil_grnd: npt.NDArray,
#     test_col_pp_itype: npt.NDArray,
#     dtime_mod,
# ):
#     if not is_passing_energy_conservation_preconditions(test_col_pp_snl, 
#             test_col_ws_h2osno, test_col_es_t_lake, test_lakestate_vars_lake_icefrac_col
#     ):
#           return CheckStatus.SKIPPED
#     if NonFiniteValuesHandler.is_all_not_finite(test_col_es_hc_soisno, 
#                                                 test_veg_ef_eflx_soil_grnd):
#         return CheckStatus.SKIPPED
#     (test_col_es_hc_soisno, test_veg_ef_eflx_soil_grnd
#      )=NonFiniteValuesHandler.mask_non_finite_values(
#          test_col_es_hc_soisno, test_veg_ef_eflx_soil_grnd)

#     total_time_steps = test_col_es_hc_soisno.shape[0]
#     total_columns = test_col_es_hc_soisno.shape[1]
#     # import pdb; pdb.set_trace()

#     # MJ/(m^2)
#     change_in_combined_heat_content = np.diff(test_col_es_hc_soisno, axis=0)

#     # W/(m^2) 
#     flux_col = convert_patches_to_columns(test_veg_pp_column, total_columns, test_veg_ef_eflx_soil_grnd)
#     expected_flux_col = flux_col[1:, :]*dtime_mod/1e6

#     heat_content_abs_diff = np.abs(np.subtract(change_in_combined_heat_content,
#                             expected_flux_col))
    

#     is_lake_column = test_col_pp_itype[0] == ISTDLAK

#     snl_ok  = (test_col_pp_snl[:-1] == 0) & (test_col_pp_snl[1:] == 0)
#     h2o_ok  = (test_col_ws_h2osno[:-1] == 0.0) & (test_col_ws_h2osno[1:] == 0.0)
#     warm_ok = (test_col_es_t_lake[:-1, 0, :] > TFRZ) & (test_col_es_t_lake[1:, 0, :] > TFRZ)
#     ice_ok  = (test_lakestate_vars_lake_icefrac_col[:-1, 0, :] == 0.0) & \
#               (test_lakestate_vars_lake_icefrac_col[1:, 0, :] == 0.0)

#     finite_ok = (~np.ma.getmaskarray(heat_content_abs_diff)
#                  & np.isfinite(np.ma.getdata(heat_content_abs_diff)))

#     preconditions_met = (is_lake_column[None, :] & snl_ok & h2o_ok
#                          & warm_ok & ice_ok & finite_ok)

#     if not preconditions_met.any():
#         return CheckStatus.SKIPPED

#     assert np.all(~preconditions_met
#                   | (np.ma.getdata(heat_content_abs_diff) <= HEAT_CONTENT_TOL)), (
#         "change in combined heat content not close to energy flux into column; "
#         f"max residual {np.ma.getdata(heat_content_abs_diff)[preconditions_met].max():.4g} "
#         f"MJ/m2 over {int(preconditions_met.sum())} samples"
#     )

# def check_snow_depth_decreases_with_snow_melt_rate(
#     test_col_es_t_lake: npt.NDArray,
#     test_col_pp_snl: npt.NDArray,
#     test_col_ws_h2osno: npt.NDArray,

#     dtime_mod,
#     test_col_wf_qflx_snomelt: npt.NDArray,
#     test_col_ws_snow_depth: npt.NDArray,
# ):
#     if not is_passing_snow_melt_preconditions(test_col_es_t_lake, test_col_pp_snl, 
#                                               test_col_ws_h2osno):
#         return CheckStatus.SKIPPED
#     if NonFiniteValuesHandler.is_all_not_finite(test_col_wf_qflx_snomelt, 
#                                                 test_col_ws_snow_depth):
#         return CheckStatus.SKIPPED
#     (test_col_pp_snl, test_col_ws_h2osno, test_col_wf_qflx_snomelt, 
#      test_col_ws_snow_depth)=(NonFiniteValuesHandler.mask_non_finite_values(
#          test_col_pp_snl, test_col_ws_h2osno, test_col_wf_qflx_snomelt, 
#          test_col_ws_snow_depth))

#     no_snow_layers = test_col_pp_snl == 0 
#     some_snow_water = test_col_ws_h2osno > 0.0
#     snow_water_present = no_snow_layers & some_snow_water

#     change_in_snow_depth_over_time = (np.diff(test_col_ws_snow_depth * 1000.0, axis=0) 
#                                       / dtime_mod)
   
#     # test_col_wf_qflx_snomelt is always 0 at timestep 0 because snow melt rate is
#     # calculated from the previous timestep to the current one, so we can skip that 
#     # timestep in the check.
#     abs_diff_snow_depth_change_and_snow_melt_rate = np.abs(np.subtract(
#         change_in_snow_depth_over_time, test_col_wf_qflx_snomelt[1:36,:]))
    
#     # Verify snow depth (m) decreases consistently with snow melt rate (mm/s)
#     # for snow melt rate to make sense, snow water has to be present at the initial 
#     # timestep and the end timestep of the time interval over which the snow depth 
#     # change is calculated.
#     assert np.all(~(snow_water_present[0:35,:] & snow_water_present[1:36,:]) | 
#                 (abs_diff_snow_depth_change_and_snow_melt_rate <= 1E-3)),(
#         "snow depth does not decrease consistently with snow melt rate where snow water"
#         +" present")


# def check_snow_water_equivalent_decreases_with_snow_melt_rate(
#     test_col_es_t_lake: npt.NDArray,
#     test_col_pp_snl: npt.NDArray,
#     test_col_ws_h2osno: npt.NDArray,

#     dtime_mod,
#     test_col_wf_qflx_snomelt: npt.NDArray,
# ):
#     if not is_passing_snow_melt_preconditions(test_col_es_t_lake, test_col_pp_snl, 
#                                               test_col_ws_h2osno):
#         return CheckStatus.SKIPPED
#     if NonFiniteValuesHandler.is_all_not_finite(test_col_wf_qflx_snomelt):
#         return CheckStatus.SKIPPED
#     (test_col_pp_snl, test_col_ws_h2osno, test_col_wf_qflx_snomelt)=(
#         NonFiniteValuesHandler.mask_non_finite_values(test_col_pp_snl, 
#                         test_col_ws_h2osno, test_col_wf_qflx_snomelt))

#     no_snow_layers = test_col_pp_snl == 0 
#     some_snow_water = test_col_ws_h2osno > 0.0
#     snow_water_present = no_snow_layers & some_snow_water

#     change_in_snow_water_equivalent_over_time = (np.diff(test_col_ws_h2osno * 1000.0, axis=0) 
#                                       / dtime_mod)
   
#     # test_col_wf_qflx_snomelt is always 0 at timestep 0 because snow melt rate is
#     # calculated from the previous timestep to the current one, so we can skip that 
#     # timestep in the check.
#     abs_diff_snow_water_equivalent_change_and_snow_melt_rate = np.abs(np.subtract(
#         change_in_snow_water_equivalent_over_time, test_col_wf_qflx_snomelt[1:36,:]))
    
#     # Verify snow water equivalent (m) decreases consistently with snow melt rate (mm/s)
#     # for snow melt rate to make sense, snow water has to be present at the initial 
#     # timestep and the end timestep of the time interval over which the snow water 
#     # equivalent change is calculated.
#     assert np.all(~(snow_water_present[0:35,:] & snow_water_present[1:36,:]) | 
#                 (abs_diff_snow_water_equivalent_change_and_snow_melt_rate <= 1E-3)),(
#         "snow water equivalent does not decrease consistently with snow melt rate where"
#         +" snow water present")
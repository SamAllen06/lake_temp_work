import numpy as np
import numpy.typing as npt


def assert_variable_is_finite(variable: npt.NDArray, name: str) -> None:
    assert np.all(np.isfinite(variable)), f"Infinite or NaN values found in {name}"


def check_lake_temperature_finite(test_col_es_t_lake: npt.NDArray) -> None:
    assert_variable_is_finite(test_col_es_t_lake, "col_es%t_lake")
   

def check_soil_snow_temperature_finite(test_col_es_t_soisno: npt.NDArray) -> None:
    assert_variable_is_finite(test_col_es_t_soisno, "col_es%t_soisno")


def check_ground_net_heat_flux_finite(test_veg_ef_eflx_gnet: npt.NDArray) -> None:
    assert_variable_is_finite(test_veg_ef_eflx_gnet, "veg_ef%eflx_gnet")


def check_ground_sensible_heat_flux_finite(test_veg_ef_eflx_sh_grnd: npt.NDArray) -> None:
    assert_variable_is_finite(test_veg_ef_eflx_sh_grnd, "veg_ef%eflx_sh_grnd")


def check_total_sensible_heat_flux_finite(test_veg_ef_eflx_sh_tot: npt.NDArray) -> None:
    assert_variable_is_finite(test_veg_ef_eflx_sh_tot, "veg_ef%eflx_sh_tot")


def check_ground_heat_flux_finite(test_veg_ef_eflx_soil_grnd: npt.NDArray) -> None:
    assert_variable_is_finite(test_veg_ef_eflx_soil_grnd, "veg_ef%eflx_soil_grnd")


def check_snow_melt_heat_flux_finite(test_col_ef_eflx_snomelt: npt.NDArray) -> None:
    assert_variable_is_finite(test_col_ef_eflx_snomelt, "col_ef%eflx_snomelt")


def check_snow_freeze_rate_finite(test_col_wf_qflx_snofrz_lyr: npt.NDArray) -> None:
    assert_variable_is_finite(test_col_wf_qflx_snofrz_lyr, "col_wf%qflx_snofrz_lyr")


def check_snow_melt_water_flux_finite(test_col_wf_qflx_snomelt: npt.NDArray) -> None:
    assert_variable_is_finite(test_col_wf_qflx_snomelt, "col_wf%qflx_snomelt")


def check_new_snow_melt_rate_finite(test_col_wf_qflx_snow_melt: npt.NDArray) -> None:
    assert_variable_is_finite(test_col_wf_qflx_snow_melt, "col_wf%qflx_snow_melt")


def check_snow_water_equivalent_finite(test_col_ws_h2osno: npt.NDArray) -> None:
    assert_variable_is_finite(test_col_ws_h2osno, "col_ws%h2osno")


def check_snow_depth_finite(test_col_ws_snow_depth: npt.NDArray) -> None:
    assert_variable_is_finite(test_col_ws_snow_depth, "col_ws%snow_depth")


def check_lake_transport_resistance_finite(test_lakestate_vars_lakeresist_col: npt.NDArray) -> None:
    assert_variable_is_finite(test_lakestate_vars_lakeresist_col, "lakestate_vars%lakeresist_col")


def check_saved_eddy_conductivity_finite(test_lakestate_vars_savedtke1_col: npt.NDArray) -> None:
    assert_variable_is_finite(test_lakestate_vars_savedtke1_col, "lakestate_vars%savedtke1_col")


def check_ground_methane_conductance_finite(
    test_ch4_vars_grnd_ch4_cond_col: npt.NDArray,
    use_lch4: int
) -> None:
    if use_lch4:
        assert_variable_is_finite(test_ch4_vars_grnd_ch4_cond_col, "ch4_vars%grnd_ch4_cond_col")

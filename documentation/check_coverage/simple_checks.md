# Simple Checks

These are the bounds and properties pertaining to the LakeTemperature inputs and outputs
provided by the file `LaketempatureOutput` we recieved from Dali.

## Dimensions and Indices
We don't have written checks for these because we assume they would cause other checks
to fail, and are not something that would change with the constants.

## Finite Values

`col_es%t_lake` is finite
- `finite_values_check.check_lake_temperature_finite`

`col_es%t_soisno` is finite
- `finite_values_check.check_soil_snow_temperature_finite`

`veg_ef%eflx_gnet` is finite
- `finite_values_check.check_ground_net_heat_flux_finite`

`veg_ef%eflx_sh_tot` is finite
- `finite_values_check.check_total_sensible_heat_flux_finite`

`veg_ef%eflx_soil_grnd` is finite
- `finite_values_check.check_ground_sensible_heat_flux_finite`

`col_ef%eflx_snomelt` is finite
- `finite_values_check.check_snow_melt_heat_flux_finite`

`col_wf%qflx_snofrz_lyr` is finite
- `finite_values_check.check_snow_freeze_rate_finite`

`col_wf%qflx_snomelt` is finite
- `finite_values_check.check_snow_melt_water_flux_finite`

`col_wf%qflx_snow_melt` is finite
- `finite_values_check.check_new_snow_melt_rate_finite`

`col_ws%h2osno` is finite
- `finite_values_check.check_snow_water_equivalent_finite`

`col_ws%snow_depth` is finite
- `finite_values_check.check_snow_depth_finite`

`lakestate_vars%lakeresist_col` is finite
- `finite_values_check.check_lake_transport_resistance_finite`

`lakestate_vars%savedtke1_col` is finite
- `finite_values_check.check_saved_eddy_conductivity_finite`

`lakestate_vars%grnd_ch4_cond_col` is finite
- `finite_values_check.check_ground_methane_conductance_finite`
- Condition: `use_lch4` is true

`col_ef%errsoi` is finite
- `finite_values_check.check_energy_conservation_residual_finite`

`col_ef%imelt` is finite
- `finite_values_check.check_snow_layer_flag_finite`

`col_es%hc_soi` is finite
- `finite_values_check.check_soil_heat_content_finite`

`col_es%hc_soisno` is finite
- `finite_values_check.check_combined_heat_content_finite`

`lakestate_vars%betaprime_col` is finite
- `finite_values_check.check_surface_absorption_finite`

`lakestate_vars%lake_icefrac_col` is finite
- `finite_values_check.check_ice_mass_fraction_finite`

`lakestate_vars%lake_icethick_col` is finite
- `finite_values_check.check_ice_thickness_finite`

## Physical Bounds

`lakestate_vars%lake_icefrac_col` $\in [0, 1]$
- `physical_bounds_check.check_lake_layer_ice_fraction_is_fraction`

`lakestate_vars%betaprime_col` $\in [0, 1]$
- `physical_bounds_check.check_surface_absorption_fraction_is_fraction`

`col_ws%h2osno` $\ge 0$
- `physical_bounds_check.check_water_snow_equivilant_not_negative`

`col_ws%snow_depth` $\ge 0$
- `physical_bounds_check.check_snow_depth_not_negative`

`col_wf%qflx_snofrz_lyr` $\ge 0$
- `physical_bounds_check.check_snow_freeze_rate_not_negative`

`col_wf%qflx_snomelt` $\ge 0$
- `physical_bounds_check.check_snow_melt_flux_not_negative`

`col_wf%qflx_snow_melt` $\ge 0$
- `physical_bounds_check.check_net_snow_melt_not_negative`

`col_ef%eflx_snomelt` $\ge 0$
- `physical_bounds_check.check_snow_melt_heat_flux_not_negative`

`lakestate_vars%lakeresist_col` $\ge 0$
- `physical_bounds_check.check_lake_water_transport_resistance_not_negative`

`lakestate_vars%savedtke1_col` $\ge 0$
- `physical_bounds_check.check_saved_eddy_conductivity_not_negative`

`col_es%hc_soi` $\ge 0$
- `physical_bounds_check.check_soil_heat_content_not_negative`

`col_es%hc_soisno` $\ge 0$
- Mathematically covered by:
  - `physical_bounds_check.check_soil_heat_content_not_negative`
  - `physical_bounds_check.check_combined_heat_content_not_less_than_soil_heat_content`

`col_es%hc_soisno` $\ge$ `col_es%hc_soi`
- `physical_bounds_check.check_combined_heat_content_not_less_than_soil_heat_content`

## Aggregation and Consistency

$\sum\limits_j$ `col_wf%qflx_snofrz_lyr(:, j, :)` $=$ `col_wf%qflx_snofrz(:, :)`
- `aggregation_and_consistency_check.check_snofrz_lyr_sums_to_snofrz_col`
- Tolerance (provided): $10^{-10}$

$\sum\limits_j$ `lakestate_vars%lake_icefrac_col(:, j, :)` `col_pp%dz_lake(:, j, :)`
(`denh2o` $/$ `denice`) $=$ `lakestate_vars%lake_icethick_col`
- `aggregation_and_consistency_check.check_icethick_col_is_sum`
- Tolerance (provided): $10^{-9}$

`col_ef%imelt` $\in {0, 1, 2}$ per snow layer
- `aggregation_and_consistency_check.check_imelt_uses_valid_enum_values`

## CH4 Conductance Behavior

`lakestate_vars%lake_icefrac_col(:, 0, :)` $> 0.1 \rightarrow$
`ch4_vars%grnd_ch4_cond_col` $= 0$
- `ch4_conductance_check.check_methane_conductance_frozen_lake`
- Condition: `use_lch4` is true
- Tolerance (not provided): `np.isclose` used

`ch4_vars%grnd_ch4_cond_col` $\ge 0$
- `ch4_conductance_check.check_methane_conductance_non_negative`
- Condition: `use_lch4` is true

## Flux Sign Conventions

Skipped because we are unsure how to check these.

## Physics Sanity

`lakestate_vars%lake_icefrac_col` $\approx 1 \rightarrow$
`|col_es%t_lake - tfrz|` $\le 10^{-3}$
- `physics_check.check_temp_at_freezing_where_lake_is_frozen`
- Condition: `lakestate_vars%lake_icefrac_col` $\approx 1$ somewhere

`lakestate_vars%savedtke1_col` $> 0 \rightarrow$
`col_es%t_lake` $>$ `tfrz` and `col_pp%snl` $= 0$
- `physics_check.no_tke_when_surface_frozen`
- Condition: `lakestate_vars%savedtke1_col` $> 0$ somewhere

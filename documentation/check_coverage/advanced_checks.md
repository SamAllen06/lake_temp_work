# Advanced Checks

These checks are derived from the focused test scenarios provided by Dali in the file
`LakeTemperatureTestPlan`. These tests included setup preconditions that would require us
to modify input variables, which we currently do not have the ability to do. Instead, we
make these setups the preconditions for running the check.

## Energy Conservation (Unfrozen Lake)

Preconditions:
- `col_pp%snl` $= 0$
- `col_ws%h2osno` $= 0$
- `col_es%t_lake[:, 0, :]` $>$ `tfrz`
- `lakestate_vars%lake_icefrac_col[:, 0, :]` $= 0$

Checks:
- `col_ef%errsoi` $\approx 0$
  - Handled by `key_physical_laws_check.check_errsoi_threshold`
  - Tolerance (not provided): 1E-6
- All temps finite
  - Handled by `finite_values_check.check_lake_temperature_finite`
- `lakestate_vars%saved_tke1_col` $> 0$
  - Handled by `physical_bounds_check.check_saved_eddy_conductivity_not_negative`

## Snow Freezing (Latent Heat)

Preconditions:
- `col_pp%snl` $< 0$
- `col_es%t_soisno[:, top_snow_layer, :]` $<$ `tfrz`
- `col_ws%h2osoi_liq[:, top_snow_layer, :]` $>0$
- `col_ws%h2osno` $> 0$
- `col_es%t_lake[:, 0, :]` $\le$ `tfrz`

Checks:
- `col_wf%qflx_snofrz_lyr[:, 0, :]` $> 0$
  - Handled by `key_physical_laws_check.check_surface_snow_freezing_where_snow_present`
- `col_ef%imelt[:, 0, :]` $= 2$ (freezing)
  - Handled by `key_physical_laws_check.check_snow_labeled_freezing_where_snow_present`
- `col_wf%qflx_snomelt[:,:]` $= 0$
  - Handled by `key_physical_laws_check.check_snow_not_melting_where_snow_present`
- ($\Delta$(`col_ws%h2osno[t,c]`) $/\Delta$ t) $≥ 0$
  - Handled by `key_physical_laws_check.check_snow_water_not_decreasing`
- ($\Delta$(`col_ws%snow_depth[t,c]`) $/\Delta$ t) $≥ 0$
  - Handled by `key_physical_laws_check.check_snow_depth_not_decreasing`
- $\sum\limits_j$ `col_wf%qflx_snofrz_lyr[:, j, :]` $\approx$ `col_wf%qflx_snofrz[:, :]`
  - Handled by `aggregation_and_consistency_check.check_snofrz_lyr_sums_to_snofrz_col`
  - Tolerance (provided): 1E-10

## Snow Melting (Latent Heat)

Preconditions:
- `snl` $= 0$
- `h2osno` $> 0$
- `t_lake(1)` $>$ `tfrz`

Checks:
- `col_wf%qflx_snomelt[:,:]` $> 0$
  - Handled by `key_physical_laws_check.check_snow_melting_where_snow_water_present`
- `col_wf%qflx_snow_melt[:,:]` $> 0$
  - Handled by `key_physical_laws_check.check_snow_melted_where_snow_water_present`
- `col_ef%eflx_snomelt` $\approx$ `col_wf%qflx_snomelt*hfus`
  - Handled by `key_physical_laws_check.check_energy_flux_consistent_with_latent_heat`
  - Tolerance (not provided): 1E-6
- ($\Delta$(`col_ws%snow_depth[t,c]`) $/\Delta$ t) $≤ 0$
  - Handled by `key_physical_laws_check.check_snow_depth_not_increasing_while_melting`
  - Tolerance: 1E-6


## Radiation Absorption

Checks:
- NIR_frac $+(1-$ NIR_frac $)*$ `betavis` $\approx$ `lakestate_vars%betaprime_col`, for NIR_frac = min((`solarabs_vars%fsds_nir_d_patch` + `solarabs_vars%fsds_nir_i_patch` + `solarabs_vars%fsr_nir_d_patch` + `solarabs_vars%fsr_nir_i_patch`), `solarabs_vars%sabg_patch`) / max(`solarabs_vars%sabg_patch`, $1E-5$)
  - Handled by `key_physical_laws_check.check_betaprime_matches_nir_blend`
  - Tolerance: 1E-6
- `col_es%t_lake` $\leq 273.15$
  - Handled by `physics_check.check_fully_frozen_layers_not_above_freezing`
  - Tolerance: 1E-3
  
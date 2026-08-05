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
- $\Delta$ `col_es%hc_soisno`/ $\Delta$ t $\approx \int$ (`veg_ef%eflx_gnet` + `veg_ef%eflx_soil_grnd` + `veg_ef%eflx_sh_grnd`)dt
  - Handled by `key_physical_laws_check.check_heat_contents_close`
  - Tolerance (not provided): 1E-6
- All temps finite
  - Handled by `finite_values_check.check_lake_temperature_finite`
- `lakestate_vars%saved_tke1_col` $> 0$
  - Handled by `physical_bounds_check.check_saved_eddy_conductivity_not_negative`

## Snow Freezing (Latent Heat)

Preconditions:
- `col_pp%snl` $< 0$
- `col_es%t_soisno[:, 0, :]` $<$ `tfrz`
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
- ($\Delta$ ($\sum\limits_j$ `col_ws%h2osoi_ice[:,:,:]`)/ $\Delta$ t) $* $`hfus` $* 1E-6 \approx$ $\Delta$ (`col_es%hc_soisno[:,:]`)/ $\Delta$ t
  - Increase in snow ice content multiplied by heat of fusion matches reduction in 
sensible energy within a tolerance.
  - Implemented by aggregating `col_ws_h2osoi_ice` from `(time, layer, column)` to
  `(time, column)`, then finding the difference between each time step, and multiplying
  that by `hfus`. Difference by time step for `col_es%hc_soisno` was computed and these
  were compared for equality.
  - Handled by `key_physical_laws_check.check_heat_diff_close`
  - Tolerance (not provided): 1E-6

## Snow Melting (Latent Heat)

Preconditions:
- `snl` $= 0$
- `h2osno` $> 0$
- `t_lake(1)` $>$ `tfrz`

Checks:
- `col_pp%snl[:,0,:]` $= 0$ and `col_ws%h2osno[:,:]` $> 0$ and `col_es%t_lake[:,0,:]` $>$ `tfrz` $\rightarrow$ `col_wf%qflx_snomelt[:,:]` $> 0$
  - Handled by `key_physical_laws_check.check_snow_melting_where_snow_water_present`
- `col_pp%snl[:,0,:]` $= 0$ and `col_ws%h2osno[:,:]` $> 0$ and `col_es%t_lake[:,0,:]` $>$ `tfrz` $\rightarrow$ `col_wf%qflx_snow_melt[:,:]` $> 0$
  - Handled by `key_physical_laws_check.check_snow_melted_where_snow_water_present`
- `col_ef%eflx_snomelt` $\approx$ `col_wf%qflx_snomelt*hfus`
  - Handled by `key_physical_laws_check.check_energy_flux_consistent_with_latent_heat`
  - Tolerance (not provided): 1E-6
- ($\Delta$ (`col_ws%snow_depth`$* 1000)/ \Delta t)/$`dtime_mod` $\approx$ `col_wf%qflx_snomelt`
  - Handled by `key_physical_laws_check.check_snow_depth_decreases_with_snow_melt_rate`
  - Tolerance (not provided): 1E-3
- ($\Delta$ (`col_ws%h2osno`$* 1000)/ \Delta t)/$`dtime_mod` $\approx$ `col_wf%qflx_snomelt`
  - Handled by `key_physical_laws_check.check_snow_water_equivalent_decreases_with_snow_melt_rate`
  - Tolerance (not provided): 1E-3

## Radiation Absorption

Checks:
- `lakestate_vars%betaprime_col` $\approx$ `solarabs_vars%sabg_lyr_patch[:, 0, :]` $/$ `solarabs_vars%sabg_patch[:, :]`
  - Handled by `key_physical_laws_check.check_betaprime_close_to_solar_rad_with_snow`
  - Tolerance (not provided): 1E-6
  - Preconditions: `col_pp%snl[:, :]` $= 0$ and `solarabs_vars%sabg_lyr_patch[:, 0, :]` $!= 0$
- *Unfinished check*
  - Will be Handled by `key_physical_laws_check.check_betaprime_close_to_solar_rad_without_snow`
- *Unfinished check*
  - Will be Handled by `key_physical_laws_check.check_flux_allocation`
- *Unfinished check*
  - Will be Handled by `key_physical_laws_check.check_energy_consistency`
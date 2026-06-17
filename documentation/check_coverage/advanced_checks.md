# Advanced Checks

These checks are derived from the focused test scenarios provided by Dali in the file
`LakeTemperatureTestPlan`. These tests included setup conditions that would require us
to modify input variables, which we currently do not have the ability to do. Instead, we
make these setups the conditions for running the check.

## Energy Conservation (Unfrozen Lake)

Conditions:
- `col_pp%snl` $= 0$
- `col_ws%h2osno` $= 0$
- `col_es%t_lake(:, 0, :)` $>$ `tfrz`
- `lakestate_vars%lake_icefrac_col(:, 0, :)` $= 0$

Checks:
- `col_ef%errsoi` $\approx 0$ after correction
  - Handled by `key_physical_laws_check.check_energy_conservation`
- `col_es%hc_soisno`$(t + dt)$ - `col_es%hc_soisno`$(t) \approx \int(
f_{\text{in}} + \phi_{\text{lake}} + \phi_{\text{soil}}
)dt$
  - We are given that $f_{\text{in}}$ is `veg_ef%eflx_gnet`. However, we don't know what
$\phi_{\text{lake}}$ and $\phi_{\text{soil}}$ are represented by, so we've skipped this
check.
  - Will be handled by `key_physical_laws_check.check_energy_conservation`
- All temps finite
  - Handled by `finite_values_check.check_lake_temperature_finite`
- `lakestate_vars%saved_tke1_col` $> 0$
  - Handled by `physical_bounds_check.check_saved_eddy_conductivity_not_negative`

## Snow Freezing (Latent Heat)

Conditions:
- `col_pp%snl` $< 0$
- `col_es%t_soisno(:, 0, :)` $<$ `tfrz`
- `col_ws%h2osno` $> 0$
- `col_es%t_lake(:, 0, :)` $\le$ `tfrz`

Checks:
- `col_wf%qflx_snofrz_lyr(:, 0, :)` $> 0$
- `col_ef%imelt(:, 0, :)` $= 2$ (freezing)
- `col_wf%qflx_snomelt` not melting
- `col_ws%h2osno` non-decreasing
- `col_ws%snow_depth` non-decreasing
- $\sum\limits_j$ `col_wf%qflx_snofrz_lyr(:, j, :)` $=$ `col_wf%qflx_snofrz(:, :)`
  - Handled by `aggregation_and_consistency_check.check_snofrz_lyr_sums_to_snofrz_col`
- Increase in snow ice content multiplied by heat of fusion matches reduction in 
sensible energy within a tolerance.
  - Implemented by aggregating `col_ws_h2osoi_ice` from `(time, layer, column)` to
  `(time, column)`, then finding the difference between each time step, and multiplying
  that by `hfus`. Difference by time step for `col_es%hc_soisno` was computed and these
  were compared for equality.
- Other listed checks performed in `key_physical_laws_check.check_freezing_latent_heat`

## Snow Melting (Latent Heat)

Conditions:
- `snl` $= 0$
- `h2osno` $> 0$
- `t_lake(1)` $>$ `tfrz`

Checks:
- `col_wf%qflx_snomelt` $> 0$
- `col_wf%qflx_snow_melt` $> 0$
- `col_ef%eflx_snomelt` $=$ `col_wf%qflx_snomelt*hfus`
- `col_ws%snow_depth`$* 1000/$`dtime_mod` $=$ `col_wf%qflx_snomelt`
- All listed checks performed in `key_physical_laws_check.check_melting_latent_heat`

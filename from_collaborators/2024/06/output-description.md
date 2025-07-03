# Variables
- col_ws%h2osoi_ice 
 ice lens kg/m2, density of type of permafrost layer. Should be positive?
  col_ws%h2osno 
 - snow water (mm H2O) should be positive?
  
lakestate_vars%lake_icethick_col
- col ice thickness (m)
- Positive
  
lakestate_vars%savedtke1_col
- col top level eddy conductivity (W/mK)

<!-- lakestate_vars%lakeresist_col
ch4_vars%grnd_ch4_cond_col -->

col_ws%frac_iceold
 - fraction of ice relative to the tot water.
 - Should have range [0,1]

col_wf%qflx_snofrz_lyr
- snow freezing rate  (col,lyr) [kg m-2 s-1]
- positive definite

col_wf%qflx_snofrz
- column-integrated snow freezing rate (kg m-2 s-1) 
- Should be positive

col_ws%snow_depth
- snow height (m)
- Positive

col_wf%qflx_snomelt
- snow melt (mm H2O /s)
- Model appears to assume it's positive?

col_wf%qflx_snow_melt
- Appears to be identical to col_wf%qflx_snomelt for LakeTemperature

col_es%hc_soi
- soil heat content (MJ/m2)
- should be positive

col_es%t_lake
- lake temperature (Kelvin)
- Positive

col_es%hc_soisno
- Positive

col_es%t_soisno
- soil (or snow) temperature (Kelvin)

lakestate_vars%betaprime_col
- NIR fraction of absorbed solar (W/m2)
- Should all be the same sign or zero.
- Related to `betavis` parameter

lakestate_vars%lake_icefrac_col
- mass fraction of lake layer that is frozen

<!-- veg_ef%eflx_soil_grnd
veg_ef%eflx_gnet
veg_ef%eflx_sh_grnd
veg_ef%eflx_sh_tot
col_ef%errsoi
col_ef%eflx_snomelt -->

# Parameters
betavis
- fraction, so should be between [0,1]


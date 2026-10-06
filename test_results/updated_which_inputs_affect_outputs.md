# Which inputs affect which outputs?

Date: 9/28/26

After reviewing and updating a couple constant ranges, this test had to be run again. It also took out all lake layer constants, as the input data we are using requires us to use the default values for nlevgrnd, nlevlak, nlevsoi, and nlevsno or else the output data won't make physical sense. Additionally, iulog was excluded as it is simply a Fortran logical unit number. Using the same method as the outdated version of the results, did not change. Additionally, when looking into why certain constants had no effect on output, it was discovered that they only had an effect when certain conditions were met. If the test cases used did not meet these conditions, some of the constants would appear to cause no observable change in the output. Once a strategy has been made to solve this problem, this test will be run once again. 

## Outputs that had observed changes

This is a list of outputs that changed in response to a change in at least one variable.
There are 17 in total.

```
ch4_vars__grnd_ch4_cond_col
col_ef__eflx_snomelt
col_es__hc_soi
col_es__hc_soisno
col_es__t_lake
col_es__t_soisno
col_wf__qflx_snomelt
col_wf__qflx_snow_melt
lakestate_vars__betaprime_col
lakestate_vars__lake_icefrac_col
lakestate_vars__lake_icethick_col
lakestate_vars__lakeresist_col
lakestate_vars__savedtke1_col
veg_ef__eflx_gnet
veg_ef__eflx_sh_grnd
veg_ef__eflx_sh_tot
veg_ef__eflx_soil_grnd
```

## Outputs with no observed changes

This is a list of outputs that did not change at all. There are 58 in total. However, it is 
important to keep in mind that we expect some of the model outputs to stay the same, like bounds variables, so these results would have to be interpreted by someone with domain knowledge to find the potential issues they expose in LakeTemperature. 

```
bounds__begg
bounds__endg
bounds__begt
bounds__endt
bounds__begl
bounds__endl
bounds__begc
bounds__endc
bounds__begp
bounds__endp
top_pp__active
lun_pp__topounit
lun_pp__itype
lun_pp__lakpoi
lun_pp__urbpoi
lun_pp__active
lakestate_vars__etal_col
lakestate_vars__lake_raw_col
lakestate_vars__ks_col
lakestate_vars__ws_col
soilstate_vars__watsat_col
soilstate_vars__tkmg_col
soilstate_vars__tkdry_col
soilstate_vars__tksatu_col
soilstate_vars__csol_col
solarabs_vars__sabg_patch
solarabs_vars__sabg_lyr_patch
solarabs_vars__fsds_nir_d_patch
solarabs_vars__fsds_nir_i_patch
solarabs_vars__fsr_nir_d_patch
solarabs_vars__fsr_nir_i_patch
col_pp__gridcell
col_pp__topounit
col_pp__landunit
col_pp__itype
col_pp__active
col_pp__snl
col_pp__dz
col_pp__z
col_pp__zi
col_pp__dz_lake
col_pp__z_lake
col_pp__lakedepth
col_es__t_grnd
col_ef__errsoi
col_ef__imelt
col_ws__h2osno
col_ws__snow_depth, 
col_ws__h2osoi_liq
col_ws__h2osoi_ice
col_ws__frac_iceold
col_wf__qflx_snofrz
col_wf__qflx_snofrz_lyr
veg_pp__topounit
veg_pp__landunit
veg_pp__column
veg_pp__itype
veg_pp__active
```

## Outputs by inputs

This is a list of inputs mapped to the outputs they affected.

### betavis (11/22)
```
ch4_vars__grnd_ch4_cond_col
col_es__hc_soi
col_es__hc_soisno
col_es__t_lake
col_es__t_soisno
lakestate_vars__betaprime_col
lakestate_vars__lakeresist_col
veg_ef__eflx_gnet
veg_ef__eflx_sh_grnd
veg_ef__eflx_sh_tot
veg_ef__eflx_soil_grnd
```

### cnfac (12/22)
```
ch4_vars__grnd_ch4_cond_col
col_es__hc_soi
col_es__hc_soisno
col_es__t_lake
col_es__t_soisno
lakestate_vars__lake_icefrac_col
lakestate_vars__lake_icethick_col
lakestate_vars__lakeresist_col
veg_ef__eflx_gnet
veg_ef__eflx_sh_grnd
veg_ef__eflx_sh_tot
veg_ef__eflx_soil_grnd
```

### cpliq (11/22)
```
ch4_vars__grnd_ch4_cond_col
col_es__hc_soi
col_es__hc_soisno
col_es__t_lake
col_es__t_soisno
lakestate_vars__lakeresist_col
lakestate_vars__savedtke1_col
veg_ef__eflx_gnet
veg_ef__eflx_sh_grnd
veg_ef__eflx_sh_tot
veg_ef__eflx_soil_grnd
```

### denh2o (11/22)
```
ch4_vars__grnd_ch4_cond_col
col_es__hc_soi
col_es__hc_soisno
col_es__t_lake
col_es__t_soisno
lakestate_vars__lakeresist_col
lakestate_vars__savedtke1_col
veg_ef__eflx_gnet
veg_ef__eflx_sh_grnd
veg_ef__eflx_sh_tot
veg_ef__eflx_soil_grnd
```

### dtime_mod (13/22)
```
ch4_vars__grnd_ch4_cond_col
col_ef__eflx_snomelt
col_es__hc_soi
col_es__hc_soisno
col_es__t_lake
col_es__t_soisno
col_wf__qflx_snomelt
col_wf__qflx_snow_melt
lakestate_vars__lakeresist_col
veg_ef__eflx_gnet
veg_ef__eflx_sh_grnd
veg_ef__eflx_sh_tot
veg_ef__eflx_soil_grnd
```

### grav (11/22)
```
ch4_vars__grnd_ch4_cond_col
col_es__hc_soi
col_es__hc_soisno
col_es__t_lake
col_es__t_soisno
lakestate_vars__lakeresist_col
lakestate_vars__savedtke1_col
veg_ef__eflx_gnet
veg_ef__eflx_sh_grnd
veg_ef__eflx_sh_tot
veg_ef__eflx_soil_grnd
```

### hfus (7/22)
```
col_ef__eflx_snomelt
col_es__hc_soisno
col_es__t_lake
veg_ef__eflx_gnet
veg_ef__eflx_sh_grnd
veg_ef__eflx_sh_tot
veg_ef__eflx_soil_grnd
```

### lake_no_ed (11/22)
```
ch4_vars__grnd_ch4_cond_col
col_es__hc_soi
col_es__hc_soisno
col_es__t_lake
col_es__t_soisno
lakestate_vars__lakeresist_col
lakestate_vars__savedtke1_col
veg_ef__eflx_gnet
veg_ef__eflx_sh_grnd
veg_ef__eflx_sh_tot
veg_ef__eflx_soil_grnd
```

### lakepuddling (8/22)
```
ch4_vars__grnd_ch4_cond_col
col_es__hc_soisno
col_es__t_lake
lakestate_vars__lakeresist_col
veg_ef__eflx_gnet
veg_ef__eflx_sh_grnd
veg_ef__eflx_sh_tot
veg_ef__eflx_soil_grnd
```

### thk_bedrock (7/22)
```
col_es__hc_soi
col_es__hc_soisno
col_es__t_soisno
veg_ef__eflx_gnet
veg_ef__eflx_sh_grnd
veg_ef__eflx_sh_tot
veg_ef__eflx_soil_grnd
```

### tkwat (11/22)
```
ch4_vars__grnd_ch4_cond_col
col_es__hc_soi
col_es__hc_soisno
col_es__t_lake
col_es__t_soisno
lakestate_vars__lakeresist_col
lakestate_vars__savedtke1_col
veg_ef__eflx_gnet
veg_ef__eflx_sh_grnd
veg_ef__eflx_sh_tot
veg_ef__eflx_soil_grnd
```

### use_lch4 (2/22)
```
ch4_vars__grnd_ch4_cond_col
lakestate_vars__lakeresist_col
```

### vkc (11/22)
```
ch4_vars__grnd_ch4_cond_col
col_es__hc_soi
col_es__hc_soisno
col_es__t_lake
col_es__t_soisno
lakestate_vars__lakeresist_col
lakestate_vars__savedtke1_col
veg_ef__eflx_gnet
veg_ef__eflx_sh_grnd
veg_ef__eflx_sh_tot
veg_ef__eflx_soil_grnd
```

### Inputs with no outputs affected

These inputs did not affect any outputs:
```
cpice
denice
depthcrit
mixfact
pudz
tkair
tkice
```

## Inputs by outputs
This is a list of outputs mapped to the inputs that affected their values.

### ch4_vars__grnd_ch4_cond_col (13/17)
```
betavis
cnfac
cpliq
denh2o
dtime_mod
grav
lake_no_ed
lakepuddling
tkwat
use_lch4
vkc
```

### col_ef__eflx_snomelt (4/17)
```
dtime_mod
hfus
```

### col_es__hc_soi (13/17)
```
betavis
cnfac
cpliq
denh2o
dtime_mod
grav
lake_no_ed
thk_bedrock
tkwat
vkc
```

### col_es__hc_soisno (15/17)
```
betavis
cnfac
cpliq
denh2o
dtime_mod
grav
hfus
lake_no_ed
lakepuddling
thk_bedrock
tkwat
vkc
```

### col_es__t_lake (14/17)
```
betavis
cnfac
cpliq
denh2o
dtime_mod
grav
hfus
lake_no_ed
lakepuddling
tkwat
vkc
```

### col_es__t_soisno (13/17)
```
betavis
cnfac
cpliq
denh2o
dtime_mod
grav
lake_no_ed
thk_bedrock
tkwat
vkc
```

### col_wf__qflx_snomelt (3/17)
```
dtime_mod
```

### col_wf__qflx_snow_melt (3/17)
```
dtime_mod
```

### lakestate_vars__betaprime_col (1/17)
```
betavis
```

### lakestate_vars__lake_icefrac_col (2/17)
```
cnfac
```

### lakestate_vars__lake_icethick_col (2/17)
```
cnfac
```

### lakestate_vars__lakeresist_col (13/17)
```
betavis
cnfac
cpliq
denh2o
dtime_mod
grav
lake_no_ed
lakepuddling
tkwat
use_lch4
vkc
```

### lakestate_vars__savedtke1_col (6/17)
```
cpliq
denh2o
grav
lake_no_ed
tkwat
vkc
```

### veg_ef__eflx_gnet (15/17)
```
betavis
cnfac
cpliq
denh2o
dtime_mod
grav
hfus
lake_no_ed
lakepuddling
thk_bedrock
tkwat
vkc
```

### veg_ef__eflx_sh_grnd (15/17)
```
betavis
cnfac
cpliq
denh2o
dtime_mod
grav
hfus
lake_no_ed
lakepuddling
thk_bedrock
tkwat
vkc
```

### veg_ef__eflx_sh_tot (15/17)
```
betavis
cnfac
cpliq
denh2o
dtime_mod
grav
hfus
lake_no_ed
lakepuddling
thk_bedrock
tkwat
vkc
```

### veg_ef__eflx_soil_grnd (15/17)
```
betavis
cnfac
cpliq
denh2o
dtime_mod
grav
hfus
lake_no_ed
lakepuddling
thk_bedrock
tkwat
vkc
```

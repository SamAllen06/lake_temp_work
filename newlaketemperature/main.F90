program main()
   
  !#define USEMPI 
  use shr_kind_mod    , only : r8 => shr_kind_r8
  use update_accMod
  use elm_varctl
  use filterMod
  use decompMod ,only : get_clump_bounds_gpu, gpu_clumps,gpu_procinfo
  use decompMod , only : get_proc_bounds, get_clump_bounds,procinfo,clumps, init_proc_clump_info
  use verificationMod
  use cudafor
  use landunit_varcon      , only : istice, istice_mec, istsoil
  use soilorder_varcon
  use timeInfoMod
  use pftvarcon
  use GridcellType
  use TopounitType
  use LandunitType
  use ColumnType
  use VegetationType
  use VegetationPropertiesType
  use elm_instMod
  use elm_initializeMod
  use LakeCon
  use ReadInputParamsMod  
  #ifdef USEMPI 
  use mpiMod
  #endif

  !#USE_START
  !#py use elm_varorb
  !#py use GridcellDataType
  use TopounitDataType
  !#py use LandunitDataType
  use ColumnDataType
  use VegetationDataType
  !#py use dynPriorWeightsMod
  use SharedParamsMod
  !#py use SoilLittDecompMod
  !#py use DecompCascadeCNMod
  !#py use DecompCascadeBGCMod
  !#py use AllocationMod
  !#py use NitrifDenitrifMod
  use CNDecompCascadeConType
  !#py use GapMortalityMod
  !#py use SoilLittVertTranspMod
  use UrbanParamsType
  use CH4Mod
  !#py use PhotosynthesisMod
  use domainMod
  !#py use DaylengthMod
  !#py use atm2lndMod
  !#py use CanopyHydrologyMod
  !#py use SurfaceRadiationMod
  !#py use UrbanRadiationMod
  !#py use CanopyFluxesMod
  !#py use CanopyTemperatureMod
  !#py use BareGroundFluxesMod
  !#py use UrbanFluxesMod
  !#py use LakeFluxesMod
  !#py use DUSTMod
  use LakeTemperatureMod
  !#py use SoilTemperatureMod
  !#py use SoilFluxesMod
  !#py use HydrologyNoDrainageMod
  !#py use AerosolMod
  !#py use SnowSnicarMod
  !#py use LakeHydrologyMod
  !#py use EcosystemDynMod
  !#py use SedYieldMod
  !#py use AnnualUpdateMod
  !#py use DryDepVelocity
  !#py use Ch4Mod
  !#py use dynInitColumnsMod
  !#py use dynConsBiogeophysMod
  !#py use dynConsBiogeochemMod
  !#py use reweightMod
  !#py use subgridWeightsMod
  !#py use NitrogenDynamicsMod
  !#py use CarbonStateUpdate1Mod
  !#py use NitrogenStateUpdate1Mod
  !#py use PhosphorusStateUpdate1Mod
  !#py use FireMod
  !#py use dynPriorWeightsMod
  !#py use dynSubgridDriverMod
  !#py use dynPatchStateUpdaterMod
  !#py use dynColumnStateUpdaterMod
  !#py use BalanceCheckMod
  !#py use EcosystemBalanceCheckMod
  !#py use SurfaceAlbedoMod
  !#py use UrbanAlbedoMod
  !#py use VerticalProfileMod
  !#py use glc2lndMod
  !#py use shr_orb_mod_elm
  !#USE_END

  !=======================================!
  implicit none
  type(bounds_type)  ::  bounds_clump, bounds_proc
  integer :: beg=1,fin=10, p, nclumps, nc, step_count
  real*8 :: temp
  integer :: err
#if _CUDA
      integer(kind=cuda_count_kind) :: heapsize,free1,free2,total
      integer  :: istat, val
#endif
  character(len=50) :: clump_input_char,pproc_input_char
  integer :: clump_input,pproc_input, fc, c, l, fp,g,j
  logical :: found_thawlayer
  integer :: k_frz, t 
  real(r8) :: declin, declinp1
  real :: startt, stopt
  #ifdef USEMPI 
  call initialize_mpi()
  #endif 
  !========================== Initialize/Allocate variables =======================!
  !First, make sure the right number of inputs have been provided
  IF(COMMAND_ARGUMENT_COUNT() == 1) THEN
    WRITE(*,*)'ONE COMMAND-LINE ARGUMENT DETECTED, Defaulting to 1 site per clump'
    call get_command_argument(1,clump_input_char)
    READ(clump_input_char,*) clump_input
    pproc_input = 1 !1 site per clump

  ELSEIF(COMMAND_ARGUMENT_COUNT() == 2) THEN
     call get_command_argument(1,clump_input_char)
     call get_command_argument(2,pproc_input_char)
     READ(clump_input_char,*) clump_input
     READ(pproc_input_char,*) pproc_input
     !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  END IF

  call elm_init(clump_input,pproc_input, dtime_mod, year_curr)
  declin = -0.4030289369547867
  step_count = 0
  nclumps = procinfo%nclumps
  print *, "number of clumps", nclumps
  print *, "step:", step_count
  
  call read_laketemp_params() 
  
  print *, "new Parameter values for LakeTemp:"
  print *, "betavis", betavis   
  print *, "za_lake", za_lake 
  print *, "n2min  ", n2min   
  print *, "tdmax  ", tdmax   
  print *, "pudz   ", pudz    
  print *, "mixfact", mixfact 
  print *, "depthcrit", depthcrit 
  stop 
  if(step_count == 0 ) then
    print *, "transferring data to GPU"
      call init_proc_clump_info()
    #ifdef _CUDA
      istat = cudaMemGetInfo(free1, total)
      print *, "Free1:",free1
    #endif
     !$acc update device( &
     !$acc        spinup_state            &
     !$acc       , nyears_ad_carbon_only   &
     !$acc       , spinup_mortality_factor &
     !$acc       , carbon_only &
     !$acc       , carbonphosphorus_only &
     !$acc       , carbonnitrogen_only &
     !$acc       ,use_crop            &
     !$acc       ,use_snicar_frc      &
     !$acc       ,use_snicar_ad       &
     !$acc       ,use_vancouver       &
     !$acc       ,use_mexicocity      &
     !$acc       ,use_noio            &
     !$acc       ,use_var_soil_thick  &
     !$acc       ,NFIX_PTASE_plant &
     !$acc       ,tw_irr &
     !$acc       ,use_erosion &
     !$acc       ,ero_ccycle  &
     !$acc       ,anoxia &
     !$acc       , glc_do_dynglacier &
     !$acc       , all_active &
     !$acc       , co2_ppmv &
     !$acc       , const_climate_hist &
     !$acc     )
     !$acc update device( &
     !$acc     KM_DECOMP_NH4        &
     !$acc     ,KM_DECOMP_NO3        &
     !$acc     ,KM_DECOMP_P          &
     !$acc     ,KM_NIT               &
     !$acc     ,KM_DEN               &
     !$acc     ,decompmicc_patch_vr(:,:) &
     !$acc     ,alpha_nfix(:)            &
     !$acc     ,alpha_ptase(:)           &
     !$acc     ,ccost_nfix(:)            &
     !$acc     ,pcost_nfix(:)            &
     !$acc     ,ccost_ptase(:)           &
     !$acc     ,ncost_ptase(:)           &
     !$acc     ,VMAX_NFIX(:)       &
     !$acc     ,KM_NFIX(:)         &
     !$acc     ,VMAX_PTASE(:)      &
     !$acc     ,KM_PTASE           &
     !$acc     ,lamda_ptase        &
     !$acc     ,i_vc(:)            &
     !$acc     ,s_vc(:)            &
     !$acc     ,leafcn_obs(:)          &
     !$acc     ,frootcn_obs(:)         &
     !$acc     ,livewdcn_obs(:)        &
     !$acc     ,deadwdcn_obs(:)        &
     !$acc     ,leafcp_obs(:)          &
     !$acc     ,frootcp_obs(:)         &
     !$acc     ,livewdcp_obs(:)        &
     !$acc     ,deadwdcp_obs(:)        &
     !$acc     ,leafcn_obs_flex(:,:)   &
     !$acc     ,frootcn_obs_flex(:,:)  &
     !$acc     ,livewdcn_obs_flex(:,:) &
     !$acc     ,deadwdcn_obs_flex(:,:) &
     !$acc     ,leafcp_obs_flex(:,:)   &
     !$acc     ,frootcp_obs_flex(:,:)  &
     !$acc     ,livewdcp_obs_flex(:,:) &
     !$acc     ,deadwdcp_obs_flex(:,:) &
     !$acc     ,fnr(:)        &
     !$acc     ,act25(:)      &
     !$acc     ,kcha(:)       &
     !$acc     ,koha(:)       &
     !$acc     ,cpha(:)       &
     !$acc     ,vcmaxha(:)    &
     !$acc     ,jmaxha(:)     &
     !$acc     ,tpuha(:)      &
     !$acc     ,lmrha(:)      &
     !$acc     ,vcmaxhd(:)    &
     !$acc     ,jmaxhd(:)     &
     !$acc     ,tpuhd(:)      &
     !$acc     ,lmrhd(:)      &
     !$acc     ,lmrse(:)      &
     !$acc     ,qe(:)         &
     !$acc     ,theta_cj(:)   &
     !$acc     ,bbbopt(:)     &
     !$acc     ,mbbopt(:)     &
     !$acc     ,nstor(:)      &
     !$acc     ,br_xr(:)      &
     !$acc     ,tc_stress     &
     !$acc     ,vcmax_np1(:)  &
     !$acc     ,vcmax_np2(:)  &
     !$acc     ,vcmax_np3(:)  &
     !$acc     ,vcmax_np4(:)  &
     !$acc     ,jmax_np1      &
     !$acc     ,jmax_np2      &
     !$acc     ,jmax_np3      &
     !$acc     ,laimax        &
     !$acc    ,rsub_top_globalmax &
     !------------- LakeCon ------------------!
     !$acc    ,fcrit      &
     !$acc    ,minz0lake  &
     !$acc     ,pudz &
     !$acc     ,depthcrit &
     !$acc     ,mixfact &
     !$acc     ,betavis &
     !$acc     ,lakepuddling &
     !$acc     ,lake_no_ed )
     !!!$acc update device(first_step, nlevgrnd, eccen, obliqr, lambm0, mvelpp )
     call update_acc_variables()

     !#ACC_COPYIN
     !$acc enter data copyin( &
     !$acc ch4_vars     , &
     !$acc col_ef     , &
     !$acc col_es     , &
     !$acc col_pp     , &
     !$acc col_wf     , &
     !$acc col_ws     , &
     !$acc grc_pp     , &
     !$acc lakestate_vars     , &
     !$acc lun_pp     , &
     !$acc soilstate_vars     , &
     !$acc solarabs_vars     , &
     !$acc top_pp     , &
     !$acc veg_ef     , &
     !$acc veg_pp      &
     !$acc   )

     call get_proc_bounds(bounds_proc)
     !$acc enter data copyin(filter(:),gpu_clumps(:), gpu_procinfo, proc_filter, bounds_proc )
     call setProcFilters(bounds_proc, proc_filter, .false.)

#if _CUDA
    !istat = cudaDeviceGetLimit(heapsize, cudaLimitMallocHeapSize)
    !print *, "SETTING Heap Limit from", heapsize
    ! heapsize = 3000_8*1024_8*1024_8
    !print *, "TO:",heapsize
    !istat = cudaDeviceSetLimit(cudaLimitMallocHeapSize,heapsize)
    !istat = cudaMemGetInfo(free1, total)
    !print *, "Free1:",free1/1.E+9
#endif
    end if
    !$acc enter data copyin( doalb, declinp1, declin )
    !$acc serial default(present)
    doalb = .true.
    nstep_mod = 788412 - 1
    year_curr  = 91
    mon_curr = 1
    day_curr = 1
    secs_curr = 43200 - 3600
    declin = -0.4023686267583503
    declinp1 = -0.4023686267583503
    !$acc end serial
    print *, "bounds_proc columns:", bounds_proc%begc, bounds_proc%endc
    
    #if _CUDA
      istat = cudaMemGetInfo(free1, total)
      print *, "free before kernel:",free1/1.E+9
    #endif
    call cpu_time(startt) 
    call LakeTemperature(bounds_proc,             &
         proc_filter%num_lakec, proc_filter%lakec,   &
         proc_filter%num_lakep, proc_filter%lakep,   &
         solarabs_vars, soilstate_vars,  ch4_vars, &
         lakestate_vars)
    call cpu_time(stopt)
   print *, "LakeTemperature Total: ",(stopt-startt)*1.E+3,"ms" 
    #if _CUDA
      istat = cudaMemGetInfo(free1, total)
      print *, "free after kernel:",free1/1.E+9
    #endif
    print *, "done with unit-test execution"
    #ifdef USEMPI 
    call mpi_barrier(MPI_COMM_WORLD)
    #endif 
    !$acc exit data finalize
end Program main

FC=nvfortran
FC_FLAGS_ACC= -fast -ta=tesla:deepcopy -Minfo=accel -acc -Mcuda
FC_FLAGS_DEBUG =  -g -O0 -Mbounds -Mchkptr -Mchkstk
FC_FLAGS_CPU = -fast 
MODEL_FLAGS=  -DMODAL_AER -DCPL_BYPASS -DCH4MOD
FC_FLAGS = $(FC_FLAGS_DEBUG) $(MODEL_FLAGS)
objects = shr_kind_mod.o shr_const_mod.o seq_drydep_mod_elm.o timeinfoMod.o elm_varctl.o elm_varsur.o landunit_varcon.o elm_varpar.o elm_varcon.o pftvarcon.o column_varcon.o soilorder_varcon.o CH4varcon.o domainMod.o decompMod.o VegetationType.o ColumnType.o TopounitType.o LandunitType.o GridcellType.o UrbanParamsType.o filterMod.o Tracer_varcon.o CanopyStateType.o subgridAveMod.o VegetationPropertiesType.o CNStateType.o SpeciesMod.o CNDecompCascadeConType.o ColumnDataType.o VegetationDataType.o TopounitDataType.o subgridMod.o decompInitMod.o atm2lndType.o SharedParamsMod.o SoilStateType.o SolarAbsorbedType.o AnnualFluxDribbler.o LakeStateType.o lnd2atmType.o QSatMod.o EnergyFluxType.o LakeCon.o SoilHydrologyType.o TridiagonalMod.o CH4Mod.o elm_instMod.o verificationMod.o LakeTemperatureMod-NonCompact.o fileio_mod.o readConstants.o update_accMod.o readMod.o initializeParameters.o duplicateMod.o  ReadInputParamsMod.o  elm_initializeMod.o main.o

elmtest.exe : $(objects)
	$(FC) $(FC_FLAGS) -o elmtest.exe $(objects)
#.SUFFIXES: .o .F90
fileio_mod.o : fileio_mod.F90
	$(FC) -O0 -c $<
readConstants.o : readConstants.F90
	$(FC) -O0 -c $<
readMod.o : readMod.F90
	$(FC) -O0 -c $<
duplicateMod.o : duplicateMod.F90
	$(FC) -O0 -c $<
%.o : %.F90
	$(FC) $(FC_FLAGS) -c $<

.PHONY: clean
clean:
	rm -f *.mod *.o *.exe

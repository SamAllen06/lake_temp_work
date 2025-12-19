FROM debian:bookworm

RUN apt update && apt install -y gfortran libnetcdff-dev libblas-dev liblapack-dev \
	python3 python3-venv less vim netcdf-bin zip

WORKDIR /app

RUN ["python3", "-m", "venv", "venv"]
RUN ["/app/venv/bin/pip", "install", "numpy", "netCDF4"]

COPY netcdf_lake_temp_testing/model/ /app/model/
COPY netcdf_lake_temp_testing/config/ /app/config/
COPY netcdf_lake_temp_testing/plugin_inputs/ /app/plugin_inputs/
COPY model_testing_framework/src/ /app/src/

# Unzip datasets and make the reference output.
WORKDIR /app/model
RUN ["unzip", "datasets.zip"]
RUN ["cp", "spel-constant-defaults0001.nc", "spel-constants0001.nc"]
RUN ["./elmtest", "1"]
RUN ["mv", "fut-outputs0001.nc", "spel-outputs0001.nc"]

WORKDIR /app

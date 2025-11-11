FROM debian:bookworm

RUN apt update && apt install -y gfortran libnetcdff-dev libblas-dev liblapack-dev \
	python3 python3-venv less vim netcdf-bin

WORKDIR /app

RUN ["python3", "-m", "venv", "venv"]
RUN ["/app/venv/bin/pip", "install", "numpy", "netCDF4"]

COPY netcdf_lake_temp_testing/ /app/
COPY model_testing_framework/src/ /app/src/

FROM alpine:latest

RUN apk add python3 hdf5-dev netcdf-dev gcc musl-dev python3-dev

WORKDIR /app

RUN ["python3", "-m", "venv", "venv"]
RUN ["/app/venv/bin/pip", "install", "numpy", "netCDF4"]

COPY netcdf_lake_temp_testing/ /app/
COPY model_testing_framework/src/ /app/src/

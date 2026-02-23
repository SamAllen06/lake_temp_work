FROM python:3.14-bookworm

RUN apt update && apt install -y gfortran libnetcdff-dev libblas-dev liblapack-dev \
	less vim netcdf-bin zip wget git cmake

# Compile Elmtest

WORKDIR /app/build

# Download and unzip E3SM
RUN wget 'https://github.com/E3SM-Project/E3SM/archive/refs/tags/v3.0.2.zip'
RUN unzip v3.0.2.zip
RUN mv E3SM-3.0.2 E3SM

# Download SPEL
RUN git clone 'https://github.com/peterdschwartz/SPEL_OpenACC.git'

# Fix the version
WORKDIR /app/build/SPEL_OpenACC
RUN git reset --hard a0929e97
RUN git clean -df

# Make a virtual environment for installing SPEL
WORKDIR /app/build
RUN python3 -m venv spel_venv
RUN /app/build/spel_venv/bin/python -m pip install -e ./SPEL_OpenACC/

WORKDIR /app/build/SPEL_OpenACC

# Configure SPEL with the correct path to E3SM
RUN sed -i 's:"\.\./repo/E3SM":"\.\./E3SM":' './scripts/config.py'

# Patch SPEL to avoid crash from grep warning
#RUN sed -i 's:"namelist\\s\*\\/":"namelist\\s\*/":' ./scripts/nml/analyze_namelist.py

# Create the LakeTemperature unit test
RUN /app/build/spel_venv/bin/spel create -s LakeTemperature

# Updating the input file path for the test
RUN sed -i 's:"/home/mrgex/SPEL_Openacc/unit-tests/input-data/":"./":' \
	'./unit-tests/fut/main.F90'

# Limiting the test's time steps
RUN sed -i 's:io_inputs%end_run:io_inputs%end_run \.or\. step > max_step:' \
	'./unit-tests/fut/main.F90'
RUN sed -i 's:max_step = 1000:max_step = 35:' './unit-tests/fut/main.F90'

WORKDIR /app/build/SPEL_OpenACC/unit-tests/fut/

# Add this include directory so CMake correctly finds netcdf.mod.
RUN sed -i '/add_executable(elmtest ${SOURCES})/a include_directories(/usr/include)' \
	'./CMakeLists.txt'

RUN cmake -S . -B build

WORKDIR /app/build/SPEL_OpenACC/unit-tests/fut/build
RUN make

# Move elmtest to model directory
RUN mkdir /app/model
RUN mv elmtest /app/model/

# Set up Model Testing Framework

WORKDIR /app

# Delete elmtest build directory
RUN rm -rf /app/build/

COPY lake_temp/model/ /app/model/

# Unzip datasets and make the reference output.
WORKDIR /app/model
RUN unzip datasets.zip
RUN rm datasets.zip
RUN cp spel-constant-defaults0001.nc spel-constants0001.nc
RUN ./elmtest 1
RUN mv fut-outputs0001.nc spel-outputs0001.nc
# Install python dependencies for model testing framework.

WORKDIR /app
RUN pip install numpy netCDF4

COPY model_testing_framework/src/ /app/src/
COPY lake_temp/config/ /app/config/
COPY lake_temp/plugin_inputs/ /app/plugin_inputs/

CMD ["bash"]

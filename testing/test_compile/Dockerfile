FROM alpine:3.23

# Updating and installing tools needed to download SPEL and E3SM.
RUN ["apk", "update", "&&", "apk", "add", "wget", "zip", "git"]

WORKDIR /home/app

# Download and unzip E3SM
RUN ["wget", "https://github.com/E3SM-Project/E3SM/archive/refs/tags/v3.0.2.zip"]
RUN ["unzip", "v3.0.2.zip"]
RUN ["mv", "E3SM-3.0.2", "E3SM"]

# Download SPEL
RUN git clone 'https://github.com/peterdschwartz/SPEL_OpenACC.git'

# Install SPEL dependencies and venv (plus gfortran so SPEL knows about it)
RUN ["apk", "add", "python3", "py3-virtualenv", "gfortran"]

# Make a virtual environment for installing SPEL
RUN ["python3", "-m", "venv", "spel_venv"]
RUN ["/home/app/spel_venv/bin/python", "-m", "pip", "install", "-e", "./SPEL_OpenACC/"]

WORKDIR /home/app/SPEL_OpenACC

# Configure SPEL with the correct path to E3SM
RUN ["sed", "-i", 's:"\.\./repo/E3SM":"\.\./E3SM":', "./scripts/config.py"]

# Patch SPEL to avoid crash from grep warning
#RUN sed -i 's:"namelist\\s\*\\/":"namelist\\s\*/":' ./scripts/nml/analyze_namelist.py

# Create the LakeTemperature unit test
RUN ["/home/app/spel_venv/bin/spel", "create", "-s", "LakeTemperature"]

# Installing elmtest dependencies
RUN ["apk", "add", "cmake", "pkgconf", "netcdf-fortran-dev", "blas-dev", "lapack-dev"]

# Updating the input file path for the test
RUN ["sed", "-i", 's:"/home/mrgex/SPEL_Openacc/unit-tests/input-data/":"./":', "./unit-tests/fut/main.F90"]

# Limiting the test's time steps
RUN ["sed", "-i", 's:io_inputs%end_run:io_inputs%end_run \.or\. step > max_step:', "./unit-tests/fut/main.F90"]
RUN ["sed", "-i", 's:max_step = 1000:max_step = 35:', "./unit-tests/fut/main.F90"]

WORKDIR /home/app/SPEL_OpenACC/unit-tests/fut/

# Add this include directory so CMake correctly finds netcdf.mod.
RUN ["sed", "-i", '/add_executable(elmtest ${SOURCES})/a include_directories(/usr/include)', "./CMakeLists.txt"]

RUN cmake -S . -B build

WORKDIR /home/app/SPEL_OpenACC/unit-tests/fut/build
RUN make

# Move elmtest to result directory
RUN mkdir /mnt/result
CMD ["mv", "elmtest", "/mnt/result/"]


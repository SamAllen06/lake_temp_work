# Lake Temperature Testing
## Purpose
Our goal is to determine how changing the values of certain constants in
[Docker4SPEL's](https://github.com/daliwang/Docker4SPEL) LakeTemperature unit
test module impact that module's outputs. We are looking to identify the
overall most impactful constants on the test's outputs, as well as looking to
find faults in the module, such as impossible output values.

## Lake Temperature Mapper
Lake Temperature Mapper is a Python program written to enable us to rapidly 
test many specific input combinations and quickly analyze the outputs.

Lake Temperature Mapper includes support for both sampling plugins and analysis
plugins. Sampling plugins can be used to generate sets of input values to pass
to the LakeTemperature module. Analysis plugins take sets of output values and
analyze them accordingly, generating human-readable and file output enabling 
researchers to easily interpret the results.

## Get Started
1. Enter the Lake Temperature Mapper directory
```
cd lake_temperature_mapper/
```
2. Build the Docker image
```
docker buildx build . -t lake_temp
```
3. Run the Docker image
```
docker run -it lake_temp
```
4. Run Lake Temperature Mapper
```
python src/cli.py
```
5. Review output (file output is in `/app/testing_output/`)

## Fake Model
Fake Model (fake_model.exe) is an C executable with the same interface as the
LakeTemperature executable (elmtest.exe), but it does not depend on the
shared objects in the Docker image, and generates known output, enabling
developers to test Lake Temperature Mapper on it, without needing to constantly
enter a Docker image.

## Run Lake Temperature Mapper on Fake Model
1. Enter the Lake Temperature Mapper directory
```
cd lake_temperature_mapper/
```
2. Verify your Python version is at least 3.10
```
python --version
```
3. Run Lake Temperature Mapper
```
python src/cli.py
```
4. Review output (file output is in `./testing_output/`)

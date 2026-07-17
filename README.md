# Lake Temperature Testing
## Purpose
Our goal is to determine how changing the values of certain constants in
[Docker4SPEL's](https://github.com/daliwang/Docker4SPEL) LakeTemperature unit
test module impacts that module's outputs. We are looking to identify the
constants that impact the test's outputs as well as looking to
find faults in the module, such as impossible output values.

## Model Testing Framework
The Model Testing Framework is a Python program written to enable us to rapidly 
test many specific input combinations and quickly analyze the outputs.

It includes support for both sampling and analysis plugins. Sampling plugins can
be used to generate sets of input values to pass to the LakeTemperature model.
Analysis plugins take sets of output values and analyze them accordingly,
generating human-readable (console) and file output, enabling researchers to
easily interpret the results.

## Dependencies

You will need Python 3 and Docker installed for this.

## Get Started
1. Download and open the zip file of the latest release. If there's no release, use the main branch.
```
git clone https://github.com/SamAllen06/lake_temp_work.git
```
2. Enter the testing directory
```
cd testing
```
3. Run the Lake Temperature testing script.
```
python test_laketemperature.py
```
4. Choose the desired plugins.
```
vim /app/config/plugin_whitelist/json
```
6. Run the Lake Temperature Mapper
```
mtf config
```
6. Review output (file output is in `/app/testing_output/`)

## Test Model
Test Model (test_model.exe) is an executable with the same interface as the
LakeTemperature executable (elmtest.exe), but it does not depend on the
shared objects in the Docker image. Additionally, it generates known output,
enabling developers to test the Model Testing Framework on it, without needing
to constantly enter a Docker image.

## Run the Model Testing Framework on the Test Model
1. Enter the testing directory
```
cd testing/
```
2. Verify your Python version is at least 3.10
```
python --version
```
3. Run Lake Temperature Mapper
```
python model_testing_framework/src/cli.py mock_model/config
```
4. Review output (file output is in `mock_model/testing_output/`)

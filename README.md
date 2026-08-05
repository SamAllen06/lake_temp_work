# Lake Temperature Testing
## Purpose
Our goal is to determine how changing the values of certain constants in
[SPEL's](https://github.com/peterdschwartz/SPEL) LakeTemperature unit
test module impacts that module's outputs. We are looking to identify the 
constants that impact the outputs as well as to find faults in the module
that result in physically impossible output values.

## Model Testing Framework
Our environmental model testing framework is a Python program written to rapidly 
test many specific input combinations and quickly analyze the outputs. 

It includes support for both sampling and analysis plugins. Sampling plugins can 
be used to generate sets of input values to pass to the LakeTemperature model. 
Analysis plugins take sets of output values and analyze them accordingly, 
generating human-readable console and file output, enabling researchers to 
easily interpret the results. 

## Installation
Follow these steps to install the testing framework. 
1. Get the dependencies: Python and Docker.
2. Download and open the zip file of this repository. Use the latest release or, if there are no releases, use the main branch.
```
git clone https://github.com/SamAllen06/lake_temp_work.git
```

## Get Started
Follow these steps to run the model testing framework on the LakeTemperature module. 
1. Open Docker
```
open -a Docker
```
2. Run the LakeTemperature testing script.
```
python testing/test_laketemperature.py
```
3. Set the whitelist to the plugins you want.
```
vim /app/config/plugin_whitelist/json
```
4. Run the model testing framework using the current configurations. 
```
mtf config
```
5. If you wish to run the loaded plugins, confirm using 'y' or 'Yes'.
6. Wait for the testing to finish. 
7. Examine the output
```
cd /app/testing/output/
```
8. Exit the framework and delete the Docker container.
```
exit
```

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

# Lake Temperature Testing
## Purpose
Our goal is to determine how changing the values of certain constants in
[Docker4SPEL's](https://github.com/daliwang/Docker4SPEL) LakeTemperature unit
test module impact that module's outputs. We are looking to identify the
overall most impactful constants on the test's outputs, as well as looking to
find faults in the module, such as impossible output values.

## Model Testing Framework
The Model Testing Framework is a Python program written to enable us to rapidly 
test many specific input combinations and quickly analyze the outputs.

It includes support for both sampling and analysis plugins. Sampling plugins can
be used to generate sets of input values to pass to the LakeTemperature model.
Analysis plugins take sets of output values and analyze them accordingly,
generating human-readable (console) and file output, enabling researchers to
easily interpret the results.

## Get Started
1. Enter the testing directory
```
cd testing/
```
2. Run the Lake Temperature testing script (if on Linux or OSX). Alternatively,
see [manually building and running the image in docker](#manually-running-docker).
```
sh test_laketemperature.sh
```
3. Run Lake Temperature Mapper
```
python src/cli.py config/
```
4. Review output (file output is in `/app/testing_output/`)

### Manually Running Docker
If you cannot run the shell script, you can simply do everything in the script
manually. This can also be done if you need finer control over the process.

1. Build the image
```
docker buildx build -t lake_temp .
```
2. Run the image
```
docker run -it lake_temp --name lake_temp
```
3. Run the Model Testing Framework and view output as needed (see steps 3 and 4
of [Get Started](#get-started)).
4. (Optional) Delete the container
```
docker rm lake_temp
```
5. (Optional) Delete the image
```
docker rmi lake_temp
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
python model_testing_framework/src/cli.py testing_framework_testing/config
```
4. Review output (file output is in `testing_framework_testing/testing_output/`)

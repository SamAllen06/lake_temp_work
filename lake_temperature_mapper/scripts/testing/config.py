from config.field import Field
from config.input_verifiers import *
from config.root import CONFIG_ROOT
from sample_generation import Sampler

FILE_PATH = CONFIG_ROOT / "mapper.conf"

FIELDS = [
    Field(
        "binary_path",
        "Enter the path to the binary you wish to map (Ex: elmtest.exe): ",
        PathInputVerifier(True, True)
    ),
    Field(
        "params_path",
        "Enter the path to the parameters file (Ex: lakeparams.txt): ",
        PathInputVerifier(True, True)
    ),
    Field(
        "defaults_path",
        "Enter the path to the parameter defaults file (Ex: lakeparams_defaults.txt): ",
        PathInputVerifier(True, True)
    ),
    Field(
        "ref_output",
        "Enter the path to the reference output file (Ex: cpu_LakeTemperatureRef.txt): ",
        PathInputVerifier(True, True)
    ),
    Field(
        "test_output",
        "Enter the path to the test output file (Ex: cpu_LakeTemperatureTest.txt): ",
        PathInputVerifier(False, True)
    ),
    Field(
        "sampler_class",
        "Enter the name of the class to use for sample generation (Ex: sample_generation.order_sampler:OrderSampler): ",
        ClassInputVerifier(Sampler)
    ),
    Field(
        "output_directory",
        "Enter the path to the directory storing mapper output files (Ex: mapping_output/): ",
        PathInputVerifier(False, False)
    ),
    Field(
        "binary_args",
        "Enter the arguments you'd like to pass to the binary (optional) (Ex: 1): ",
        NoCheckInputVerifier()
    ),
]

from config.field import Field
from config.no_check_input_verifier import NoCheckInputVerifier
from config.path_input_verifier import PathInputVerifier

FIELDS = [
    Field(
        "binary_path",
        "Enter the path to the binary you wish to map (Ex: elmtest.exe): ",
        PathInputVerifier(True, True)
    ),
    Field(
        "range_path",
        "Enter the path to the parameter ranges file (Ex: FUT_lake_range.txt): ",
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
        "order_directory",
        "Enter the path to the directory storing mapping orders (Ex: mapping_orders/): ",
        PathInputVerifier(True, False)
    ),
    Field(
        "binary_args",
        "Enter the arguments you'd like to pass to the binary (optional) (Ex: 1): ",
        NoCheckInputVerifier()
    ),
]

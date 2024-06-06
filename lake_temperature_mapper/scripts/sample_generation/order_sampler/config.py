from config import Field
from config.input_verifiers import PathInputVerifier
from config.root import CONFIG_ROOT


FILE_PATH = CONFIG_ROOT / "sample_generation" / "order_sampler.conf"

FIELDS = [
    Field(
        "range_path",
        "Enter the path to the parameter ranges file (Ex: FUT_lake_range.txt): ",
        PathInputVerifier(True, True)
    ),
    Field(
        "order_directory",
        "Enter the path to the directory storing mapping orders (Ex: mapping_orders/): ",
        PathInputVerifier(True, False)
    ),
]

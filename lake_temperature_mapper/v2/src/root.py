from pathlib import Path


APP_ROOT = Path(__file__).parent.parent
CONFIG_ROOT = APP_ROOT / "config"
SOURCE_ROOT = APP_ROOT / "src"

SAMPLING_PLUGIN_CONFIG_DIRECTORY = CONFIG_ROOT / "sampling_plugins"
ANALYSIS_PLUGIN_CONFIG_DIRECTORY = CONFIG_ROOT / "analysis_plugins"

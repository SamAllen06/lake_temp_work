from enum import Enum


# mypy: disable-error-code="var-annotated"
class Event(Enum):
    LOADING_BINARY = {"binary_name": str}
    BINARY_LOAD_SUCCESS = {}
    BINARY_LOAD_FAILURE = {"reason": Exception}

    BEGAN_LOADING_SAMPLING_PLUGINS = {}
    LOADING_SAMPLING_PLUGIN = {"plugin_name": str}
    SAMPLING_PLUGIN_LOAD_SUCCESS = {"plugin_name": str}
    SAMPLING_PLUGIN_LOAD_FAILURE = {"plugin_name": str, "reason": Exception}
    SAMPLING_PLUGINS_LOAD_SUCCESS = {"count": int}
    SAMPLING_PLUGINS_LOAD_FAILURE = {}

    BEGAN_LOADING_ANALYSIS_PLUGINS = {}
    LOADING_ANALYSIS_PLUGIN = {"plugin_name": str}
    ANALYSIS_PLUGIN_LOAD_SUCCESS = {"plugin_name": str}
    ANALYSIS_PLUGIN_LOAD_FAILURE = {"plugin_name": str, "reason": Exception}
    ANALYSIS_PLUGINS_LOAD_SUCCESS = {"count": int}
    ANALYSIS_PLUGINS_LOAD_FAILURE = {}

    BEGAN_SAMPLE_GENERATION = {}
    BEGAN_SAMPLING_FROM_PLUGIN = {"plugin_name": str}
    SAMPLING_FROM_PLUGIN_SUCCESS = {
        "plugin_name": str,
        "group_sample_counts": dict[str, int],
    }
    SAMPLING_FROM_PLUGIN_FAILURE = {"plugin_name": str, "reason": Exception}
    SAMPLING_FROM_PLUGINS_SUCCESS = {"group_count": int, "sample_count": int}
    SAMPLING_FROM_PLUGINS_FAILURE = {}

    BEGAN_TIMING_BINARY = {"binary_name": str}
    TIMING_BINARY_SUCCESS = {"seconds_estimate": float}
    TIMING_BINARY_FAILURE = {"exit_code": int}

    BEGAN_SAMPLING_FROM_GROUP = {
        "group_name": str,
        "group_index": int,
        "group_count": int,
    }
    SAMPLE_GENERATED = {
        "sample_index": int,
        "sample_count": int,
        "values": dict[str, float],
    }
    RUNNING_BINARY = {"binary_name": str}
    BINARY_EXITED = {"exit_code": int}
    BEGAN_BY_SAMPLE_ANALYSIS = {}
    BEGAN_BY_SAMPLE_ANALYSIS_WITH_PLUGIN = {"plugin_name": str}
    # View logic handled inside analysis plugins to offer them better flexibility
    # with their output. Helper classes are avaliable to handle specific forms of
    # output, at the cost of flexibility.
    BY_SAMPLE_ANALYSIS_WITH_PLUGIN_SUCCESS = {
        "console_output": str,
        "file_output": bytes,
    }
    BY_SAMPLE_ANALYSIS_WITH_PLUGIN_FAILURE = {"reason": Exception}

    BEGAN_SAMPLE_GROUP_ANALYSIS = {}
    BEGAN_SAMPLE_GROUP_ANALYSIS_WITH_PLUGIN = {"plugin_name": str}
    SAMPLE_GROUP_ANALYSIS_WITH_PLUGIN_SUCCESS = {
        "console_output": str,
        "file_output": bytes,
    }
    SAMPLE_GROUP_ANALYSIS_WITH_PLUGIN_FAILURE = {"reason": Exception}

    TESTING_COMPLETED = {}

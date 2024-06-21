from enum import Enum


class Event(Enum):
    LOADING_BINARY = 0
    BINARY_LOAD_SUCCESS = 1
    BINARY_LOAD_FAILURE = 2

    BEGAN_LOADING_SAMPLING_PLUGINS = 3
    LOADING_SAMPLING_PLUGIN = 4
    SAMPLING_PLUGIN_LOAD_SUCCESS = 5
    SAMPLING_PLUGIN_LOAD_FAILURE = 6
    SAMPLING_PLUGINS_LOAD_SUCCESS = 7
    SAMPLING_PLUGINS_LOAD_FAILURE = 8

    BEGAN_LOADING_ANALYSIS_PLUGINS = 9
    LOADING_ANALYSIS_PLUGIN = 10
    ANALYSIS_PLUGIN_LOAD_SUCCESS = 11
    ANALYSIS_PLUGIN_LOAD_FAILURE = 12
    ANALYSIS_PLUGINS_LOAD_SUCCESS = 13
    ANALYSIS_PLUGINS_LOAD_FAILURE = 14

    BEGAN_SAMPLE_GENERATION = 15
    BEGAN_SAMPLING_FROM_PLUGIN = 16
    SAMPLING_FROM_PLUGIN_SUCCESS = 17
    SAMPLING_FROM_PLUGIN_FAILURE = 18
    SAMPLING_FROM_PLUGINS_SUCCESS = 19
    SAMPLING_FROM_PLUGINS_FAILURE = 20

    BEGAN_TIMING_BINARY = 21
    TIMING_BINARY_SUCCESS = 22
    TIMING_BINARY_FAILURE = 23

    BEGAN_SAMPLING_FROM_GROUP = 24
    SAMPLE_GENERATED = 25
    RUNNING_BINARY = 26
    BINARY_EXITED = 27
    BEGAN_BY_SAMPLE_ANALYSIS = 28
    BEGAN_BY_SAMPLE_ANALYSIS_WITH_PLUGIN = 29
    BY_SAMPLE_ANALYSIS_WITH_PLUGIN_SUCCESS = 30
    BY_SAMPLE_ANALYSIS_WITH_PLUGIN_FAILURE = 31

    BEGAN_SAMPLE_GROUP_ANALYSIS = 32
    BEGAN_SAMPLE_GROUP_ANALYSIS_WITH_PLUGIN = 33
    SAMPLE_GROUP_ANALYSIS_WITH_PLUGIN_SUCCESS = 34
    SAMPLE_GROUP_ANALYSIS_WITH_PLUGIN_FAILURE = 35

    TESTING_COMPLETED = 36


EVENT_PARAMETERS: dict[Event, dict[str, type]] = {
    Event.LOADING_BINARY: {"binary_name": str},
    Event.BINARY_LOAD_SUCCESS: {},
    Event.BINARY_LOAD_FAILURE: {"reason": Exception},
    Event.BEGAN_LOADING_SAMPLING_PLUGINS: {},
    Event.LOADING_SAMPLING_PLUGIN: {"plugin_name": str},
    Event.SAMPLING_PLUGIN_LOAD_SUCCESS: {"plugin_name": str},
    Event.SAMPLING_PLUGIN_LOAD_FAILURE: {"plugin_name": str, "reason": Exception},
    Event.SAMPLING_PLUGINS_LOAD_SUCCESS: {"count": int},
    Event.SAMPLING_PLUGINS_LOAD_FAILURE: {},
    Event.BEGAN_LOADING_ANALYSIS_PLUGINS: {},
    Event.LOADING_ANALYSIS_PLUGIN: {"plugin_name": str},
    Event.ANALYSIS_PLUGIN_LOAD_SUCCESS: {"plugin_name": str},
    Event.ANALYSIS_PLUGIN_LOAD_FAILURE: {"plugin_name": str, "reason": Exception},
    Event.ANALYSIS_PLUGINS_LOAD_SUCCESS: {"count": int},
    Event.ANALYSIS_PLUGINS_LOAD_FAILURE: {},
    Event.BEGAN_SAMPLE_GENERATION: {},
    Event.BEGAN_SAMPLING_FROM_PLUGIN: {"plugin_name": str},
    Event.SAMPLING_FROM_PLUGIN_SUCCESS: {
        "plugin_name": str,
        "group_sample_counts": dict[str, int],
    },
    Event.SAMPLING_FROM_PLUGIN_FAILURE: {"plugin_name": str, "reason": Exception},
    Event.SAMPLING_FROM_PLUGINS_SUCCESS: {"group_count": int, "sample_count": int},
    Event.SAMPLING_FROM_PLUGINS_FAILURE: {},
    Event.BEGAN_TIMING_BINARY: {"binary_name": str},
    Event.TIMING_BINARY_SUCCESS: {"seconds_estimate": float},
    Event.TIMING_BINARY_FAILURE: {"exit_code": int},
    Event.BEGAN_SAMPLING_FROM_GROUP: {
        "group_name": str,
        "group_index": int,
        "group_count": int,
    },
    Event.SAMPLE_GENERATED: {
        "sample_index": int,
        "sample_count": int,
        "values": dict[str, float],
    },
    Event.RUNNING_BINARY: {"binary_name": str},
    Event.BINARY_EXITED: {"exit_code": int},
    Event.BEGAN_BY_SAMPLE_ANALYSIS: {},
    Event.BEGAN_BY_SAMPLE_ANALYSIS_WITH_PLUGIN: {"plugin_name": str},
    # View logic is handled inside analysis plugins to offer them better flexibility
    # with their output. Helper classes are avaliable to handle specific forms of
    # output, at the cost of flexibility.
    Event.BY_SAMPLE_ANALYSIS_WITH_PLUGIN_SUCCESS: {
        "console_output": str,
        "file_output": bytes,
    },
    Event.BY_SAMPLE_ANALYSIS_WITH_PLUGIN_FAILURE: {"reason": Exception},
    Event.BEGAN_SAMPLE_GROUP_ANALYSIS: {},
    Event.BEGAN_SAMPLE_GROUP_ANALYSIS_WITH_PLUGIN: {"plugin_name": str},
    Event.SAMPLE_GROUP_ANALYSIS_WITH_PLUGIN_SUCCESS: {
        "console_output": str,
        "file_output": bytes,
    },
    Event.SAMPLE_GROUP_ANALYSIS_WITH_PLUGIN_FAILURE: {"reason": Exception},
    Event.TESTING_COMPLETED: {},
}

from enum import auto, Enum

from output.file_utils import FileSystemTree


class Event(Enum):
    INITIALIZE = auto()

    LOADING_BINARY = auto()
    BINARY_LOAD_SUCCESS = auto()
    BINARY_LOAD_FAILURE = auto()

    BEGAN_LOADING_SAMPLING_PLUGINS = auto()
    LOADING_SAMPLING_PLUGIN = auto()
    SAMPLING_PLUGIN_LOAD_SUCCESS = auto()
    SAMPLING_PLUGIN_LOAD_FAILURE = auto()
    SAMPLING_PLUGINS_LOAD_SUCCESS = auto()
    SAMPLING_PLUGINS_LOAD_FAILURE = auto()

    BEGAN_LOADING_ANALYSIS_PLUGINS = auto()
    LOADING_ANALYSIS_PLUGIN = auto()
    ANALYSIS_PLUGIN_LOAD_SUCCESS = auto()
    ANALYSIS_PLUGIN_LOAD_FAILURE = auto()
    ANALYSIS_PLUGINS_LOAD_SUCCESS = auto()
    ANALYSIS_PLUGINS_LOAD_FAILURE = auto()

    BEGAN_SAMPLE_GENERATION = auto()
    BEGAN_SAMPLING_FROM_PLUGIN = auto()
    SAMPLING_FROM_PLUGIN_SUCCESS = auto()
    SAMPLING_FROM_PLUGIN_FAILURE = auto()
    SAMPLING_FROM_PLUGINS_SUCCESS = auto()
    SAMPLING_FROM_PLUGINS_FAILURE = auto()

    BEGAN_TIMING_BINARY = auto()
    TIMING_BINARY_SUCCESS = auto()
    TIMING_BINARY_FAILURE = auto()

    BEGAN_SAMPLING_FROM_GROUP = auto()
    SAMPLE_GENERATED = auto()
    RUNNING_BINARY = auto()
    BINARY_EXITED = auto()
    BEGAN_SAMPLE_ANALYSIS = auto()
    BEGAN_SAMPLE_ANALYSIS_WITH_PLUGIN = auto()
    SAMPLE_ANALYSIS_WITH_PLUGIN_SUCCESS = auto()
    SAMPLE_ANALYSIS_WITH_PLUGIN_FAILURE = auto()

    BEGAN_GROUP_ANALYSIS = auto()
    BEGAN_GROUP_ANALYSIS_WITH_PLUGIN = auto()
    GROUP_ANALYSIS_WITH_PLUGIN_SUCCESS = auto()
    GROUP_ANALYSIS_WITH_PLUGIN_FAILURE = auto()

    TESTING_COMPLETED = auto()


EVENT_PARAMETERS: dict[Event, dict[str, type]] = {
    Event.INITIALIZE: {},

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
    Event.BEGAN_SAMPLE_ANALYSIS: {},
    Event.BEGAN_SAMPLE_ANALYSIS_WITH_PLUGIN: {"plugin_name": str},
    # View logic is handled inside analysis plugins to offer them better flexibility
    # with their output. Helper classes are avaliable to handle specific forms of
    # output, at the cost of flexibility.
    Event.SAMPLE_ANALYSIS_WITH_PLUGIN_SUCCESS: {
        "plugin_name": str,
        "console_output": str,
        "file_output": FileSystemTree,
    },
    Event.SAMPLE_ANALYSIS_WITH_PLUGIN_FAILURE: {
        "plugin_name": str,
        "reason": Exception
    },

    Event.BEGAN_GROUP_ANALYSIS: {},
    Event.BEGAN_GROUP_ANALYSIS_WITH_PLUGIN: {"plugin_name": str},
    Event.GROUP_ANALYSIS_WITH_PLUGIN_SUCCESS: {
        "plugin_name": str,
        "console_output": str,
        "file_output": FileSystemTree,
    },
    Event.GROUP_ANALYSIS_WITH_PLUGIN_FAILURE: {
        "plugin_name": str,
        "reason": Exception
    },

    Event.TESTING_COMPLETED: {},
}

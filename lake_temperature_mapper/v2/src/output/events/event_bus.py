import inspect
from types import GenericAlias, MethodType
from typing import Any

from output.events import Event

subscriptions: dict[Event, list[MethodType]] = {event: [] for event in Event}


def subscribe(event: Event, callback: MethodType) -> None:
    _validate_callback_for_event(callback, event)
    subscriptions[event].append(callback)


def unsubscribe(event: Event, callback: MethodType) -> None:
    subscriptions[event].remove(callback)


def fire_event(event: Event, **kwargs) -> None:
    _validate_provided_args_for_event(event, kwargs)

    for callback in subscriptions[event]:
        callback(**kwargs)


def _validate_callback_for_event(callback: MethodType, event: Event) -> None:
    callback_spec = inspect.getfullargspec(callback)

    if not _arg_list_is_valid_length_for_event(event, callback_spec.args):
        raise ValueError(
            f"Callback has {len(callback_spec.args)} arguments, "
            f"but event expects {len(event.value)}"
        )

    missing_args = _get_missing_arg_names_for_event(event, callback_spec.args)
    if missing_args:
        raise ValueError(
            f"Event expects arguments: {missing_args}, but callback is missing them"
        )

    incorrectly_typed_args = _get_incorrectly_typed_arguments_for_event(
        event, callback_spec.annotations
    )
    if incorrectly_typed_args:
        error_message = "These callback arguments are incorrectly typed:"

        for arg_name, expected_type, actual_type in incorrectly_typed_args:
            error_message += (
                f"\n{arg_name} expected to be {expected_type.__name__}, "
                f"but was {actual_type.__name__}"
            )
            raise ValueError(error_message)


def _validate_provided_args_for_event(event: Event, args: dict[str, Any]) -> None:
    arg_list = list(args.keys())
    arg_types = {arg: type(args[arg]) for arg in args}

    if not _arg_list_is_valid_length_for_event(event, arg_list):
        raise TypeError(
            f"Event expected {len(event.value)} arguments, "
            f"but {len(args)} were provided"
        )

    missing_args = _get_missing_arg_names_for_event(event, arg_list)
    if missing_args:
        raise TypeError(
            f"Missing keyword arguments {missing_args}, which are expected by event"
        )

    incorrectly_typed_args = _get_incorrectly_typed_arguments_for_event(
        event, arg_types
    )
    if incorrectly_typed_args:
        error_message = "The following keyword arguments have an incorrect type:"

        for arg, expected_type, actual_type in incorrectly_typed_args:
            error_message += (
                f"\n{arg} expected {expected_type.__name__}, "
                f"but was {actual_type.__name__}"
            )

        raise TypeError(error_message)


def _arg_list_is_valid_length_for_event(event: Event, arg_list: list[str]) -> bool:
    return len(event.value) == len(arg_list)


def _get_missing_arg_names_for_event(event: Event, arg_list: list[str]) -> list[str]:
    missing_args: list[str] = []

    for event_arg in event.value:
        if event_arg not in arg_list:
            missing_args.append(event_arg)

    return missing_args


def _get_incorrectly_typed_arguments_for_event(
    event: Event, arg_types: dict[str, type]
) -> list[tuple[str, type, type]]:
    incorrect_args: list[tuple[str, type, type]] = []

    for arg_name in arg_types:
        arg_type = arg_types[arg_name]
        expected_type = event.value[arg_name]

        if isinstance(expected_type, GenericAlias):
            continue

        if not arg_type == expected_type:
            incorrect_args.append((arg_name, expected_type, arg_type))

    return incorrect_args


#        raise ValueError(
#            f"Event argument {event_arg_name} is of type {event_arg_type}, "
#            f"but callback argument {event_arg_name} expects "
#            f"type {callback_arg_type}"
#        )

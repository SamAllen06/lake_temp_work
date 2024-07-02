from collections.abc import Iterable as _Iterable
from enum import Enum as _Enum

from output.events import event_bus as _event_bus
from output.views import console, file


class View(_Enum):
    CONSOLE = console
    FILE = file


def _enable(view: View) -> None:
    view_subscriptions = view.value.SUBSCRIPTIONS
    for event in view_subscriptions:
        _event_bus.subscribe(event, view_subscriptions[event])


def enable_views(views: _Iterable[View]) -> None:
    for view in views:
        _enable(view)

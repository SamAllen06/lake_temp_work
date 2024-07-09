from collections.abc import Iterable
from enum import Enum

from output.events import event_bus
from output.views import View


def _enable(view: View) -> None:
    view_subscriptions = view.value.SUBSCRIPTIONS
    for event in view_subscriptions:
        event_bus.subscribe(event, view_subscriptions[event])


def enable_views(views: Iterable[View]) -> None:
    for view in views:
        _enable(view)

# Event (APP/src/output/events/event.py)

## Purpose
The event module includes an Event enum that provides a name for each possible
event, and the EVENT_PARAMETERS constant, which provides the keyword arguments
for each event.

## Functionality
EVENT_PARAMETERS' keyword arguments are required to be passed with the
[event_bus](event_bus.md).fire_event function call, and are optionally able to
be received by callback functions subscribed to a certain event.

See [event_bus](event_bus.md) for details surrounding subscribing to and firing
events.

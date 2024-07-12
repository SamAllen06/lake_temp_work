# Views (APP/src/output/views/)

## Purpose
Views are modules that subscribe to [events](../events/events.md) and produce
output that can be used the user later.

## Functionality
This module provides a View enum which allows a controller to enable the views
it wants using [view_manager.](../view_manager.md)

Each view module must have a SUBSCRIPTIONS constant, mapping [Event(s)](../events/event.md)
to a callback function. Views do not have to subscribe to all events, nor do
they have to accept all keyword arguments that an event provides to its
callbacks.

The SUBSCRIPTIONS constant is used by [view_manager](../view_manager.md) to
subscribe a view's callbacks to each event when it is enabled.

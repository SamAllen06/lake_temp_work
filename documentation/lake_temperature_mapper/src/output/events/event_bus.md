# Event Bus 
APP/src/events/event_bus.py

## Purpose
The event_bus module allows subscribing to, unsubscribing from, and firing
events.

## Example
```
>>> from output.events import Event, event_bus
>>> 
>>> # Callback accepting an argument.
>>> # Type annotations are optional, but checked when present.
>>> def call_me(binary_name: str):
...     print(f"Binary loaded: {binary_name}")
... 
>>> # Callback without an argument.
>>> def call_me_no_arg():
...     print("I've been called!")
... 
>>> event_bus.subscribe(Event.LOADING_BINARY, call_me)
>>> event_bus.subscribe(Event.LOADING_BINARY, call_me_no_arg)
>>> 
>>> # Arguments are not optional when firing the event.
>>> event_bus.fire_event(Event.LOADING_BINARY, binary_name="cool_binary.exe")
Binary loaded: cool_binary.exe
I've been called!
```

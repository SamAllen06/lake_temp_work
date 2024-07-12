# View Manager (APP/src/output/view_manager.py)

## Purpose
The view_manager module enables views when its enable_view function is called.

## Example
```
>>> from output.views import View
>>> from output import view_manager
>>> 
>>> wanted_views = [View.CONSOLE]
>>> 
>>> view_manager.enable_views(wanted_views)
>>> 
>>> 
>>> from output.events import Event, event_bus
>>> 
>>> event_bus.fire_event(Event.BEGAN_LOADING_SAMPLING_PLUGINS)
Loading sampling plugins:
```

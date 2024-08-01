# Logs 
APP/src/output/views/logs.py

## Purpose
Generates a log file each time the program is run. The file is timestamped and
written inside the log directory, the location of which can be configured in
the [logs config file.](../../../config/output/logs.md)
Additionally, you can configure how many log files you want to keep.

## Functionality
The log view subscribes to all events, and generates at least one line for each
event. This view uses Python's [logging](https://docs.python.org/3.10/library/logging.html)
module, and thus has four logging levels: info, warning, error, and critical.

Critical lines are used when the program encounters a fatal error and thus
cannot continue testing. Error logs are generated when something doesn't work
as intended (such as a plugin failing to load), but doesn't require the program
to stop. Warning logs are generated when something happens that may indicate
a future problem, but isn't one currently. All other cases use info logs.

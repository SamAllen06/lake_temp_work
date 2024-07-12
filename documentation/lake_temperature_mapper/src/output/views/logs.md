# Logs (APP/src/output/views/logs.py)

## Purpose
Generates a log file each time the program is run. The file is timestamped and
written inside of the log directory, the location of which can be configured in
APP/config/output/logs.ini.

## Functionality
The log view subscribes to all events, and generates at least one line for each
event. This view uses Python's [logging](https://docs.python.org/3.10/library/logging.html)
module, and thus has four logging levels: info, warning, error, and critical.

Critical lines are used when the program encounters a fatal error and thus
cannot continue testing. Error logs are generated when something doesn't work
as intended (such as a plugin failing to load), but doesn't require the program
to stop. Warning logs are generated when something happens that may indicate
a future problem, but isn't one currently. (Currently the only log that uses
this level is the one indicating that the binary exited with a non-zero exit
code when running it with the default parameters.) All other cases use info
logs.

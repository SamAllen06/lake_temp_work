# Root (root.py)

## Purpose

Stores a reference to the app root (lake_temperature_mapper/ in the
repository and /app/ in the docker image) for other scripts to reference.

Additionally, it stores a reference to the config root (APP_ROOT/config/) and 
the script root (APP_ROOT/scripts/), which are used less often.

This module is the only one that determines the app root relative to itself.
This ensures, as other modules are moved around, their filesystem references
don't need to be updated.

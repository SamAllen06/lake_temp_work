# Console Output Writer

## Purpose
Writes output from the Mapper to the console.

## Functionality
Prints the order being executed in this format:
```
Executing order: [order_name]
```

Prints each change to an input parameter's value as so:
```
Set [parameter_name] to [new_value]
```

Prints changes to the output variables like so (only variable *with* changes
are printed):
```
[variable_name]
reference_value   -> test_value   by difference   at indices
[reference_value] -> [test_value] by [difference] at [indices]
[reference_value] -> [test_value] by [difference] at [indices]
...
```

Or, if no output variables changed:
```
"No differences"
```

If the binary crashed (returned an exit code other than 0):
```
Binary exited with code [code]
```

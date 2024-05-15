# Order Reader (order_reader.py)

## Purpose
Reads in orders from a specified order directory. Orders provide instructions
for how to sample an input parameter.

## Functionality
Reads an order files (json) in the specified directory. Order files use the
following format:
```
{
  "param":"param_name"
  "samples": # of samples
  "start": start_value
  "end": end_value
}
```

This, along with the filename (minus the .json extension) is stored in an Order.

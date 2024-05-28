# Order Reader (order_reader.py)

## Purpose
Reads in orders from a specified order directory. Orders provide instructions
for how to sample an input parameter.

## Functionality
Reads order files (json) in the specified directory. Order files use the
following format:
```
{
  "param":"param_name",
  "samples": # of samples,
  "ranges": [
    {
      "param":"param_name",
      "start":"start_value",
      "end":"end_value"
    }
  ]
}
```

This, along with the filename (minus the .json extension) is stored in an Order.

The values of the start and end fields are converted into a float using 
BoundTranslator.


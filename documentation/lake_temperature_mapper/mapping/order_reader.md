# Order Reader (order_reader.py)

## Purpose
Reads in orders from a specified order directory. Orders provide instructions
for how to sample an input parameter.

## Functionality
Reads an order files (json) in the specified directory. Order files use the
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

## r Notation

In the start and end fields, "r(t)" where t is a decimal, can be used to
reference range information in an expression.

For example, if the range (from FUT_lake_range.txt) is 1.0 - 3.0, r(1.0)
represents 3.0, and r(0.0) represents 1.0. t is used as a time value in an 
unbounded linear interpolation between these two values, so r(0.5) evaluates to
2.0, and r(-0.5) evaluates to 0.0.

Since these can be used in an expression, testing 0.2 above and below the range
of a parameter could be done with the following range:

```
{
  "param":"param_name"
  "start": "r(0) - 0.2"
  "end": "r(1) + 0.2"
}
```

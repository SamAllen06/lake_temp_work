# Bound Translator (APP/src/sampling_libs/range_interpolation/bound_translator.py)

## Purpose
Converts the start and end strings of an order into a float. This includes 
computing expressions and r-notation.

## Functionality
Evaluates all r-notation terms of an expression first, using unbounded linear
interpolation as described below. Second, multiplication and division operators
are applied, and finally, addition and subtraction is applied. Parenthesis are 
not supported, though negative numbers are (for multiplication and division
purposes).

## r Notation
In the start and end fields, "r(t)" where t is a decimal, can be used to
reference range information in an expression.

For example, if the range (from FUT_lake_range.txt) is 2.0 - 4.0, r(1.0)
represents 4.0, and r(0.0) represents 2.0. t is used as a time value in an 
unbounded linear interpolation between these two values, so r(0.5) evaluates to
3.0, and r(-0.5) evaluates to 1.0.

Since these can be used in an expression, testing 0.2 above and below the range
of a parameter could be done with the following range:

```
{
  "param":"param_name"
  "start": "r(0) - 0.2"
  "end": "r(1) + 0.2"
}
```

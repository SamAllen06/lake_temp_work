# Bound Translator
APP/src/sampling_libs/range_interpolation/bound_translator.py

## Purpose
Converts strings into floats, including expression evaluation and r-notation.

## Functionality
Evaluates all r-notation terms first, using unbounded linear interpolation and
a range file as described below. Second, multiplication and division operators
are evaluated, and finally, addition and subtraction is evaluated. Parenthesis are 
not supported, though negative numbers are (for multiplication and division
purposes).

## r Notation
In the start and end fields, "r(t)" where t is a decimal, can be used to
reference range information in an expression.

For example, if the range of an input parameter (from a range text file) is
2.0 - 4.0, r(1.0) represents 4.0, and r(0.0) represents 2.0. The input to the
r function is used as a time value in an unbounded linear interpolation between
the range file's bounds, meaning r(0.5) would evaluate to 3.0, and r(-0.5)
would evaluate to 1.0.

These r-notation terms can still be used in an expression, so `3.4 - r(0.2)`
would evaluate to `1.0`.
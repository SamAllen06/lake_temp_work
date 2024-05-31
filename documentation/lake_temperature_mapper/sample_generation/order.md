# Order (order.py)

## Purpose
Stores instructions for modifying input parameters. Can be iterated across to
obtain ordered "samples", which specify what value to set each parameter to.

## Functionality
Samples are returned in this form: `{"param1": float, "param2": float, ...}`

In a box order, samples only include values that should be changed that
iteration, not values that keep their previous value.

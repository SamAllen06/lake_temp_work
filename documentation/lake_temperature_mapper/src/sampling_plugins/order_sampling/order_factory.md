# Order Factory
APP/src/sampling_plugins/order_sampling/order_factory.py

## Purpose
Accepts data from a parsed order file and determines which type of order should
be created. Then, it creates the [Order](order.md) using the data.

## Functionality
It can differentiate between [line](line_order.md) and [box](box_order.md)
orders by checking if there is a root level "samples" key, which would
indicate the total number of samples in a line order, but is not present in
a box order, since each axis has its own sample count.

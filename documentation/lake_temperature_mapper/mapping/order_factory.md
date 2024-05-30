# Order Factory (order_factory.py)

## Purpose
Accepts data from a parsed order and determines which type of order should be 
created. Then, it creates an Order using the data accordingly.

## Functionality
Can differentiate between line and box orders by checking if there is a root 
level "samples" key, which would indicate the total number of samples in a line
order.

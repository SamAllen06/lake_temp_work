# Combinatorial Timing

Date: 06/09/26

Using the same steps as the `REPO:/test_results/outdated_combinatorial_timing.md`, new 
combinatorial tests were created that included all of the model constants instead of 
just the ones with confirmed effects on the model output. However, all of the timing and
generation was done on a different device than previous timings and generations,
resulting in differences of estimated and actual timing statistics. 

## Cases per Degree of Interaction

| Degree of Interaction | Case Count  | Estimated Execution Time (days, hrs:mins:secs)|
|:---------------------:|:-----------:|:---------------------------------------------:|
| 2                     | 231         | 0 days, 00:02:90                              |
| 3                     | 4,706       | 0 days, 00:50:44                              |
| 4                     | 72,964      | 0 days, 11:50:14                              |
| 5                     | 1,009,602   | 6 days, 08:44:35                              |

For ten samples, the mean time it takes to run `elmtest` is ... seconds, with a 
standard deviation of ... This time is used to estimate how long testing each 
interaction level would take, assuming tests run sequentially as they do in the current
version of our testing framework.

## Timing Statistics

### ACTS

| Degree of Interaction | Time (seconds) Mean | Sample Standard Deviation |
|-----------------------|---------------------|---------------------------|
| 2                     | 0.962               | 0.180                     |
| 3                     | 19.763              | 4.720                     |
| 4                     | 408.981             | 23.126                    |
| 5                     |             |                       |

### csv2nc

| Degree of Interaction | Time (seconds) Mean | Sample Standard Deviation |
|-----------------------|---------------------|---------------------------|
| 2                     |                |                      |
| 3                     |                |                      |
| 4                     |               |                      |
| 5                     |              |                      |



## Raw Data: ACTS CSV Generation

Raw data is also included in this report as, when doing multiple runs of Acts, the time
for subsequent runs is likely reduced due to caching, so the distribution is not 
necessarily normal.

### DOI: 2

| Time (seconds) |
|----------------|
| 1.389          |
| 0.913          |
| 0.946          |
| 0.925          |
| 0.828          |
| 0.909          |
| 0.824          |

### DOI: 3

| Time (seconds) |
|----------------|
| 27.864          |
| 24.125          |
| 16.274          |
| 19.503          |
| 20.956          |
| 12.737          |
| 16.883          |

### DOI: 4

| Time (seconds) |
|----------------|
| 421.491        |
| 446.563        |
| 405.734        |
| 391.971        |
| 378.567        |
| 431.061        |
| 387.477        |

### DOI: 5

| Time (seconds) |
|----------------|
|           |
|           |
|           |
|           |
|           |
|           |
|           |

## Raw Data: csv2nc

### DOI: 2

| Time (seconds) |
|----------------|
|           |
|           |
|           |
|           |
|           |
|           |
|           |

### DOI: 3

| Time (seconds) |
|----------------|
|           |
|           |
|           |
|           |
|           |
|           |
|           |

### DOI: 4

| Time (seconds) |
|----------------|
|           |
|           |
|           |
|           |
|           |
|           |
|           |

### DOI: 5

| Time (seconds) |
|----------------|
|           |
|           |
|           |
|           |
|           |
|           |
|           |

## Raw Data: Running Elmtest

This is time data from running `elmtest`. The mean is used to approximate the total
testing time from the number of test cases.

| Time (seconds) |
|----------------|
|           |
|           |
|           |
|           |
|           |
|           |
|           |
|           |
|           |
|           |



# Combinatorial Timing

Date: 03/31/26

When generating combinatorial test cases using ACTS and our csv2nc Python script, we
timed each stage with different degrees of interaction. The configuration file used with
ACTS is `REPO:/test_resources/acts/lake_temp_combinatorial.conf`. Seven iterations were
run for each degree of interaction using a bash for loop. Note that the time was
collected using `real` time from the `time` command, not ACTS reported time. We suspect
the difference is because ACTS's measurement does not include the time it takes to write
the cases to a CSV file.

## Cases per Degree of Interaction

| Degree of Interaction | Case Count  | Estimated Execution Time   |
|:---------------------:|:-----------:|:--------------------------:|
| 2                     | 231         | 0 days, 00:01:45           |
| 3                     | 3,685       | 0 days, 00:28:00           |
| 4                     | 53,170      | 0 days, 06:44:06           |
| 5                     | 688,290     | 3 days, 15:11:00           |

For ten samples, the mean time it takes to run `elmtest` is 0.456 seconds, with a 
standard deviation of 0.040. This time is used to estimate how long testing each 
interaction level would take, assuming tests run sequentially as they do in the current
version of our testing framework.

## Timing Statistics

### ACTS

| Degree of Interaction | Time (seconds) Mean | Sample Standard Deviation |
|-----------------------|---------------------|---------------------------|
| 2                     | 0.126               | 0.068                     |
| 3                     | 0.397               | 0.005                     |
| 4                     | 8.706               | 0.184                     |
| 5                     | 644.581*            | N/A*                      |

*DOI of 5 was only ran once since it took so long. All others were run seven times.

### csv2nc

| Degree of Interaction | Time (seconds) Mean | Sample Standard Deviation |
|-----------------------|---------------------|---------------------------|
| 2                     | 0.213               | 0.012                     |
| 3                     | 1.593               | 0.019                     |
| 4                     | 21.430              | 0.279                     |
| 5                     | 274.740             | 4.582                     |



## Raw Data: ACTS CSV Generation

Raw data is also included in this report as, when doing multiple runs of Acts, the time
for subsequent runs is likely reduced due to caching, so the distribution is not 
necessarily normal.

### DOI: 2

| Time (seconds) |
|----------------|
| 0.281          |
| 0.103          |
| 0.099          |
| 0.099          |
| 0.100          |
| 0.099          |
| 0.099          |

### DOI: 3

| Time (seconds) |
|----------------|
| 0.401          |
| 0.401          |
| 0.392          |
| 0.400          |
| 0.388          |
| 0.393          |
| 0.404          |

### DOI: 4

| Time (seconds) |
|----------------|
| 8.375          |
| 8.713          |
| 8.806          |
| 8.645          |
| 8.819          |
| 8.629          |
| 8.954          |

## Raw Data: csv2nc

### DOI: 2

| Time (seconds) |
|----------------|
| 0.222          |
| 0.207          |
| 0.207          |
| 0.207          |
| 0.205          |
| 0.208          |
| 0.236          |

### DOI: 3

| Time (seconds) |
|----------------|
| 1.577          |
| 1.596          |
| 1.609          |
| 1.590          |
| 1.620          |
| 1.595          |
| 1.562          |

### DOI: 4

| Time (seconds) |
|----------------|
| 21.687         |
| 21.505         |
| 20.974         |
| 21.425         |
| 21.643         |
| 21.655         |
| 21.126         |

### DOI: 5

| Time (seconds) |
|----------------|
| 280.010        |
| 277.960        |
| 270.218        |
| 277.262        |
| 270.402        |
| 269.200        |
| 278.132        |

## Raw Data: Running Elmtest

This is time data from running `elmtest`. The mean is used to approximate the total
testing time from the number of test cases.

| Time (seconds) |
|----------------|
| 0.569          |
| 0.444          |
| 0.447          |
| 0.440          |
| 0.445          |
| 0.440          |
| 0.440          |
| 0.445          |
| 0.442          |
| 0.447          |



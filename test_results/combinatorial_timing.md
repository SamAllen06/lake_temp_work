# Combinatorial Timing

Date: 06/16/26

When generating combinatorial test cases using ACTS and our csv2nc Python script, we
timed each stage with different degrees of interaction. The configuration file used with
ACTS is `REPO:/test_resources/acts/lake_temp_combinatorial.conf`. Seven iterations were
run for each degree of interaction using a bash for loop. Note that the time was
collected using `real` time from the `time` command, not ACTS reported time. We suspect
the difference is because ACTS's measurement does not include the time it takes to write
the cases to a CSV file. All of the timings and generations were done using Cluster, 
Ball State's supercomputer

## Cases per Degree of Interaction

For ten samples, the mean time it takes to run `elmtest` is ... seconds, with a 
standard deviation of .... This time is used to estimate how long testing each 
interaction level would take, assuming tests run sequentially as they do in the current
version of our testing framework.

### Cases Including All Constants

| DoI | Cases   | Expected Execution Time | Actual Execution Time |
|:---:|:-------:|:-----------------------:|:---------------------:|
| 1   | 11      | 0 days, 00:00:00        | 0 days, 00:00:00      | 
| 2   | 232     | 0 days, 00:00:00        | 0 days, 00:00:00      | 
| 3   | 4,253   | 0 days, 00:00:00        | 0 days, 00:00:00      | 
| 4   | 64,149  | 0 days, 00:00:00        | 0 days, 00:00:00      | 
| 5   |         | 0 days, 00:00:00        | 0 days, 00:00:00      | 

*Actual Execution Time was based on a single run of the test cases.

## Timing Statistics

### ACTS

| Degree of Interaction | Time (seconds) Mean | Sample Standard Deviation |
|-----------------------|---------------------|---------------------------|
| 1                     | 0.000               | 0.000                     |
| 2                     | 0.000               | 0.000                     |
| 3                     | 0.000               | 0.000                     |
| 4                     | 0.000               | 0.000                     |
| 5                     | 0.000               | 0.000                     |

### csv2nc

| Degree of Interaction | Time (seconds) Mean | Sample Standard Deviation |
|-----------------------|---------------------|---------------------------|
| 1                     | 0.000               | 0.000                     |
| 2                     | 0.000               | 0.000                     |
| 3                     | 0.000               | 0.000                     |
| 4                     | 0.000               | 0.000                     |
| 5                     | 0.000               | 0.000                     |

## Raw Data

Raw data is also included in this report as, when doing multiple runs of ACTS, the time
for subsequent runs is likely reduced due to caching, so the distribution is not 
necessarily normal.

### ACTS CSV Generation

#### DOI: 1

| Time (seconds) |
|----------------|
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |

#### DOI: 2

| Time (seconds) |
|----------------|
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |

#### DOI: 3

| Time (seconds) |
|----------------|
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |

#### DOI: 4

| Time (seconds) |
|----------------|
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |

#### DOI: 5

| Time (seconds) |
|----------------|
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |

### csv2nc

#### DOI: 1

| Time (seconds) |
|----------------|
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |

#### DOI: 2

| Time (seconds) |
|----------------|
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |

#### DOI: 3

| Time (seconds) |
|----------------|
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |

#### DOI: 4

| Time (seconds) |
|----------------|
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |

#### DOI: 5

| Time (seconds) |
|----------------|
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |
| 0.000          |


# Combinatorial Timing

Date: 06/16/26

When generating combinatorial test cases using ACTS and our csv2nc Python script, we
timed each stage with different degrees of interaction. The configuration file used with
ACTS is `REPO:/test_resources/acts/lake_temp_combinatorial.conf`. Seven iterations were
run for each degree of interaction using a bash for loop. Note that the time was
collected using `real` time from the `time` command, not ACTS reported time. We suspect
the difference is because ACTS's measurement does not include the time it takes to write
the cases to a CSV file. All of the timings and generations were done using Cluster, 
Ball State's supercomputer. The exact commands we used can be seen below, changing -Ddoi from 1 to 5 and lake_temp_i{1,2,3,4,5}. 
```
for item in [1 2 3 4 5 6 7]; do time java -jar -Ddoi=1 -Doutput=csv -Dchandler=forbiddentuples -Dcheck=on 'acts_3.3.jar' 'lake_temp_work/test_resources/acts/lake_temp/lake_temp_combinatorial.conf'; done

for item in [1 2 3 4 5 6 7]; do time csv2nc test_resources/acts/lake_temp/lake_temp_i1.csv test_resources/acts/lake_temp/lake_temp_partition.nc ../../test.nc; done
```

## Cases per Degree of Interaction

For seven samples, the mean time it takes to run `elmtest` is 0.934 seconds, with a 
standard deviation of 0.009. This time is used to estimate how long testing each 
interaction level would take, assuming tests run sequentially as they do in the current
version of our testing framework.

| DoI | Cases   | Expected Execution Time | Actual Execution Time |
|:---:|:-------:|:-----------------------:|:---------------------:|
| 1   | 11      | 0 days, 00:00:10        | 0 days, 00:00:16      | 
| 2   | 232     | 0 days, 00:03:37        | 0 days, 00:05:02      | 
| 3   | 4,253   | 0 days, 01:06:12        | 0 days, 00:52:30      | 
| 4   | 64,149  | 0 days, 16:38:35        | 0 days, 00:00:00      | 
| 5   | 869,835 | 9 days, 09:40:26        | 0 days, 00:00:00      | 

*Actual Execution Time was based on a single run of the test cases.

## Timing Statistics

### ACTS

| Degree of Interaction | Time (seconds) Mean | Sample Standard Deviation |
|-----------------------|---------------------|---------------------------|
| 1                     | 0.226               | 0.003                     |
| 2                     | 0.345               | 0.006                     |
| 3                     | 3.305               | 0.029                     |
| 4                     | 373.978             | 4.900                     |
| 5*                    | 4311.719            | 54.021                    |

*Degree of Interaction 5 was run using -Dcheck=off to avoid running out of java heap space

### csv2nc

| Degree of Interaction | Time (seconds) Mean | Sample Standard Deviation |
|-----------------------|---------------------|---------------------------|
| 1                     | 0.115               | 0.001                     |
| 2                     | 0.307               | 0.004                     |
| 3                     | 3.873               | 0.082                     |
| 4                     | 59.630              | 3.912                     |
| 5                     | 763.368             | 7.505                     |

## Raw Data

Raw data is also included in this report as, when doing multiple runs of ACTS, the time
for subsequent runs is likely reduced due to caching, so the distribution is not 
necessarily normal.

### ACTS CSV Generation

#### DOI: 1

| Time (seconds) |
|----------------|
| 0.223          |
| 0.222          |
| 0.226          |
| 0.227          |
| 0.229          |
| 0.229          |
| 0.227          |

#### DOI: 2

| Time (seconds) |
|----------------|
| 0.357          |
| 0.342          |
| 0.342          |
| 0.345          |
| 0.338          |
| 0.345          |
| 0.348          |

#### DOI: 3

| Time (seconds) |
|----------------|
| 3.307          |
| 3.371          |
| 3.314          |
| 3.289          |
| 3.295          |
| 3.285          |
| 3.276          |

#### DOI: 4

| Time (seconds) |
|----------------|
| 380.484        |
| 380.892        |
| 375.253        |
| 369.696        |
| 373.389        |
| 371.233        |
| 366.900        |

#### DOI: 5

*Degree of Interaction 5 was run using -Dcheck=off to avoid running out of java heap space

| Time (seconds) |
|----------------|
| 4400.119       |
| 4387.883       |
| 4254.525       |
| 4299.205       |
| 4281.309       |
| 4293.336       |
| 4265.658       |

### csv2nc

#### DOI: 1

| Time (seconds) |
|----------------|
| 0.114          |
| 0.114          |
| 0.114          |
| 0.115          |
| 0.114          |
| 0.114          |
| 0.117          |

#### DOI: 2

| Time (seconds) |
|----------------|
| 0.309          |
| 0.311          |
| 0.304          |
| 0.300          |
| 0.305          |
| 0.311          |
| 0.307          |

#### DOI: 3

| Time (seconds) |
|----------------|
| 3.875          |
| 3.851          |
| 3.918          |
| 4.025          |
| 3.897          |
| 3.756          |
| 3.787          |

#### DOI: 4

| Time (seconds) |
|----------------|
| 58.362         |
| 57.016         |
| 56.702         |
| 56.896         |
| 56.916         |
| 65.528         |
| 65.992         |

#### DOI: 5

| Time (seconds) |
|----------------|
| 769.526        |
| 765.063        |
| 769.400        |
| 764.212        |
| 750.436        |
| 771.058        |
| 753.883        |


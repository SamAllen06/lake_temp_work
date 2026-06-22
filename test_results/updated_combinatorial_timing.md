# Combinatorial Timing

Date: 06/16/26

Using the same steps as the `REPO:/test_results/outdated_combinatorial_timing.md` except
using the Powershell `Measure-Command{}` instead of the bash `time` command, new 
combinatorial tests were created that included all of the model constants instead of 
just the ones with confirmed effects on the model outputs. However, this timing was done
on all of the model constants rather than just the ones confirmed to have an effect on 
model outputs. All of the timings and generations were done on a different device than
previous timings and generations, resulting in differences of estimated and actual 
timing statistics. 

## Cases per Degree of Interaction

For ten samples, the mean time it takes to run `elmtest` is 0.622 seconds, with a 
standard deviation of 0.030. This time is used to estimate how long testing each 
interaction level would take, assuming tests run sequentially as they do in the current
version of our testing framework.

### Cases Including All Constants

| Degree of Interaction | Case Count  | Estimated Execution Time | Actual Execution Time* |
|:---------------------:|:-----------:|:------------------------:|:----------------------:|
| 2                     | 231         | 0 days, 00:02:24         | 0 days, 00:02:17       |
| 3                     | 4,706       | 0 days, 00:48:47         | 0 days, 00:46:50       |
| 4                     | 72,964      | 0 days, 12:36:24         | - days, --:--:--       |
| 5                     | 1,009,602   | 7 days, 06:26:12         | - days, --:--:--       |

### Cases Including Only Constants Originally Believed to Affect Outputs

| Degree of Interaction | Case Count  | Estimated Execution Time | Actual Execution Time* |
|:---------------------:|:-----------:|:------------------------:|:----------------------:|
| 2                     | 231         | 0 days, 00:02:24         | 0 days, 00:02:20       |
| 3                     | 3,685       | 0 days, 00:38:12         | 0 days, 00:37:28       |
| 4                     | 53,170      | 0 days, 09:11:12         | - days, --:--:--       |
| 5                     | 688,290     | 4 days, 22:55:16         | - days, --:--:--       |

*Actual Execution Time was based on a single run of the test cases.

## Timing Statistics

### Cases Including All Constants

#### ACTS

| Degree of Interaction | Time (seconds) Mean | Sample Standard Deviation |
|-----------------------|---------------------|---------------------------|
| 2                     | 0.303               | 0.016                     |
| 3                     | 1.638               | 0.027                     |
| 4                     | 201.699             | 2.937                     |
| 5                     | 15431.431           | 171.548                   |

#### csv2nc

| Degree of Interaction | Time (seconds) Mean | Sample Standard Deviation |
|-----------------------|---------------------|---------------------------|
| 2                     | 0.671               | 0.030                     |
| 3                     | 6.187               | 0.102                     |
| 4                     | 88.892              | 0.382                     |
| 5                     | 1155.359            | 16.407                    |

### Cases Including Only Constants Originally Believed to Affect Outputs

#### ACTS

| Degree of Interaction | Time (seconds) Mean | Sample Standard Deviation |
|-----------------------|---------------------|---------------------------|
| 2                     | 0.213               | 0.006                     |
| 3                     | 0.632               | 0.024                     |
| 4                     | 12.641              | 0.197                     |
| 5                     | 1107.923            | 16.651                    |

#### csv2nc

| Degree of Interaction | Time (seconds) Mean | Sample Standard Deviation |
|-----------------------|---------------------|---------------------------|
| 2                     | 0.648               | 0.114                     |
| 3                     | 3.226               | 0.054                     |
| 4                     | 41.233              | 1.146                     |
| 5                     | 501.764             | 2.276                     |


## Raw Data

### Cases with All Constants

Raw data is also included in this report as, when doing multiple runs of ACTS, the time
for subsequent runs is likely reduced due to caching, so the distribution is not 
necessarily normal.

#### ACTS CSV Generation

##### DOI: 2

| Time (seconds) |
|----------------|
| 0.317          |
| 0.326          |
| 0.294          |
| 0.287          |
| 0.305          |
| 0.312          |
| 0.279          |

##### DOI: 3

| Time (seconds) |
|----------------|
| 1.692          |
| 1.631          |
| 1.603          |
| 1.618          |
| 1.660          |
| 1.627          |
| 1.634          |

##### DOI: 4

| Time (seconds) |
|----------------|
| 203.710        |
| 197.572        |
| 203.893        |
| 197.274        |
| 204.056        |
| 204.612        |
| 200.777        |

##### DOI: 5

| Time (seconds) |
|----------------|
| 15798.454      |
| 15445.166      |
| 15480.388      |
| 15319.431      |
| 15444.483      |
| 15291.458      |
| 15240.636      |

#### csv2nc

##### DOI: 2

| Time (seconds) |
|----------------|
| 0.664          |
| 0.717          |
| 0.657          |
| 0.646          |
| 0.717          |
| 0.665          |
| 0.634          |

##### DOI: 3

| Time (seconds) |
|----------------|
| 6.325          |
| 6.329          |
| 6.224          |
| 6.054          |
| 6.143          |
| 6.152          |
| 6.081          |

##### DOI: 4

| Time (seconds) |
|----------------|
| 88.384         |
| 88.738         |
| 89.301         |
| 88.967         |
| 88.360         |
| 89.116         |
| 89.378         |

##### DOI: 5

| Time (seconds) |
|----------------|
| 1194.269       |
| 1157.351       |
| 1145.222       |
| 1150.183       |
| 1147.288       |
| 1149.613       |
| 1143.587       |

### Cases Including Only Constants Originally Believed to Affect Outputs

#### ACTS CSV Generation

##### DOI: 2

| Time (seconds) |
|----------------|
| 0.221          |
| 0.208          |
| 0.218          |
| 0.209          |
| 0.217          |
| 0.205          |
| 0.216          |

##### DOI: 3

| Time (seconds) |
|----------------|
| 0.617          |
| 0.595          |
| 0.661          |
| 0.658          |
| 0.619          |
| 0.619          |
| 0.658          |

##### DOI: 4

| Time (seconds) |
|----------------|
| 12.742         |
| 12.691         |
| 13.015         |
| 12.628         |
| 12.409         |
| 12.617         |
| 12.388         |

##### DOI: 5

| Time (seconds) |
|----------------|
| 1089.139       |
| 1109.389       |
| 1133.250       |
| 1097.063       |
| 1131.170       |
| 1091.484       |
| 1103.965       |

#### csv2nc

##### DOI: 2

| Time (seconds) |
|----------------|
| 0.882          |
| 0.567          |
| 0.634          |
| 0.619          |
| 0.625          |
| 0.717          |
| 0.493          |

##### DOI: 3

| Time (seconds) |
|----------------|
| 3.149          |
| 3.284          |
| 3.277          |
| 3.196          |
| 3.297          |
| 3.193          |
| 3.186          |

##### DOI: 4

| Time (seconds) |
|----------------|
| 42.346         |
| 42.915         |
| 42.027         |
| 40.674         |
| 41.066         |
| 39.637         |
| 39.964         |

##### DOI: 5

| Time (seconds) |
|----------------|
| 502.536        |
| 498.589        |
| 505.882        |
| 499.876        |
| 502.675        |
| 502.802        |
| 499.989        |

### Running Elmtest

This is time data from running `elmtest`. The mean is used to approximate the total
testing time from the number of test cases.

| Time (seconds) |
|----------------|
| 0.671          |
| 0.614          |
| 0.607          |
| 0.622          |
| 0.600          |
| 0.611          |
| 0.612          |
| 0.688          |
| 0.593          |
| 0.604          |



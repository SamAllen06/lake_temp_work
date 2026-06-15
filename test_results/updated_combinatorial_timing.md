# Combinatorial Timing

Date: 06/14/26

Using the same steps as the `REPO:/test_results/outdated_combinatorial_timing.md` except
using the Powershell `Measure-Command{}` instead of the bash `time` command, new 
combinatorial tests were created that included all of the model constants instead of 
just the ones with confirmed effects on the model output. However, this timing was done
on all of the model constants rather than just the ones confirmed to have an effect on 
model outputall of the timing and generation was done on a different device than
previous timings and generations, resulting in differences of estimated and actual 
timing statistics. 

## Cases per Degree of Interaction

| Degree of Interaction | Case Count  | Estimated Execution Time (days, hrs:mins:secs)|
|:---------------------:|:-----------:|:---------------------------------------------:|
| 2                     | 231         | 0 days, 00:02:24                              |
| 3                     | 4,706       | 0 days, 00:48:47                              |
| 4                     | 72,964      | 0 days, 12:36:24                              |
| 5                     | 1,009,602   | 7 days, 06:26:12                              |

For ten samples, the mean time it takes to run `elmtest` is 0.622 seconds, with a 
standard deviation of 0.030. This time is used to estimate how long testing each 
interaction level would take, assuming tests run sequentially as they do in the current
version of our testing framework.

## Timing Statistics

### ACTS

| Degree of Interaction | Time (seconds) Mean | Sample Standard Deviation |
|-----------------------|---------------------|---------------------------|
| 2                     | 0.303               | 0.016                     |
| 3                     | 1.638               | 0.027                     |
| 4                     | 201.699             | 2.937                     |
| 5                     | 15431.431           | 171.548                   |

### csv2nc

| Degree of Interaction | Time (seconds) Mean | Sample Standard Deviation |
|-----------------------|---------------------|---------------------------|
| 2                     | 0.671               | 0.030                     |
| 3                     | 6.187               | 0.102                     |
| 4                     | 88.892              | 0.382                     |
| 5                     | 1155.359            | 16.407                    |



## Raw Data: ACTS CSV Generation

Raw data is also included in this report as, when doing multiple runs of Acts, the time
for subsequent runs is likely reduced due to caching, so the distribution is not 
necessarily normal.

### DOI: 2

| Time (seconds) |
|----------------|
| 0.317          |
| 0.326          |
| 0.294          |
| 0.287          |
| 0.305          |
| 0.312          |
| 0.279          |

### DOI: 3

| Time (seconds) |
|----------------|
| 1.692          |
| 1.631          |
| 1.603          |
| 1.618          |
| 1.660          |
| 1.627          |
| 1.634          |

### DOI: 4

| Time (seconds) |
|----------------|
| 203.710        |
| 197.572        |
| 203.893        |
| 197.274        |
| 204.056        |
| 204.612        |
| 200.777        |

### DOI: 5

| Time (seconds) |
|----------------|
| 15798.454      |
| 15445.166      |
| 15480.388      |
| 15319.431      |
| 15444.483      |
| 15291.458      |
| 15240.636      |

## Raw Data: csv2nc

### DOI: 2

| Time (seconds) |
|----------------|
| 0.664          |
| 0.717          |
| 0.657          |
| 0.646          |
| 0.717          |
| 0.665          |
| 0.634          |

### DOI: 3

| Time (seconds) |
|----------------|
| 6.325          |
| 6.329          |
| 6.224          |
| 6.054          |
| 6.143          |
| 6.152          |
| 6.081          |

### DOI: 4

| Time (seconds) |
|----------------|
| 88.384         |
| 88.738         |
| 89.301         |
| 88.967         |
| 88.360         |
| 89.116         |
| 89.378         |

### DOI: 5

| Time (seconds) |
|----------------|
| 1194.269       |
| 1157.351       |
| 1145.222       |
| 1150.183       |
| 1147.288       |
| 1149.613       |
| 1143.587       |

## Raw Data: Running Elmtest

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



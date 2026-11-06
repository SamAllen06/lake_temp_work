# Boundary Testing
Date: 10/13/26

This document provides the results for runs of the Model Testing Framework on
LakeTemperature via SPEL. These results used the Order sampling plugin in combination 
with the fault checks analysis plugin. Checks were rules we implemented based
on guidance provided by our collaborators. These runs were completed using commit
``. Everything was run using Cluster, Ball State's supercomputer.  

## Sampling

The samples used for these runs were orders. In order to generate them, we created a json
order file which interpolated over a range to create three samples and altered the order
sampling ini file to use first [the lower boundary](testing/lake_temp/model/lower_boundary_lake_range.txt)
and then [the upper boundary](testing/lake_temp/model/upper_boundary_lake_range.txt)

| Model Constant   | Lower Range Used | Upper Range Used |
|:----------------:|:-----------------|:-----------------|
| betavis          | -0.1 - 0.1       | 0.9 - 1.1        |
| cnfac            | -0.1 - 0.1       | 0.9 - 1.1        |

## Results:

### betavis
| Check Failed                                    | Values           |
|:-----------------------------------------------:|:----------------:|
| `check_surface_absorption_fraction_is_fraction` | -0.1, 1.1        |
| None                                            | 0, 0.1, 0.9, 1.0 |

### cnfac
| Check Failed                                             | Values            |
|:--------------------------------------------------------:|:-----------------:|
| `check_surface_unfrozen_when_tke_present`                | 1.0, 1.1          |
| `check_temp_around_freezing_where_lake_is_almost_frozen` | 1.0, 1.1          |
| None                                                     | -0.1, 0, 0.1, 0.9 |
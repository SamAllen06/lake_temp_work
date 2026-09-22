# Range Changes in the [Lake Range Text File](testing/lake_temp/model/FUT_lake_range.txt)

| Model        | Original Range | Updated Range      | Data Type | Notes                                                                                                                                                                      |
| ------------ | -------------- | ------------------ | --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| iulog        | 95-100         | --                 | --        | Excluded since it's a fortran logical unit number, remains at default of 97                                                                                                |
| nlevgrnd     | 0-25           | __                 | --        | Excluded because the input data is constructed based on the default of 15. Would need different SPEL input files captured from ELM runs with different lake layer settings |
| nlevlak      | 1-15           | __                 | --        | Excluded because the input data is constructed based on the default of 10. Would need different SPEL input files captured from ELM runs with different lake layer settings |
| nlevsoi      | 0-15           | __                 | --        | Excluded because the input data is constructed based on the default of 10. Would need different SPEL input files captured from ELM runs with different lake layer settings |
| nlevsno      | 0-5            | __                 | --        | Excluded because the input data is constructed based on the default of 5. Would need different SPEL input files captured from ELM runs with different lake layer settings  |
| tkwat        | 0-1            | (0.513, 0.627)     | double    | ±10% around the default 0.57                                                                                                                                               |
| cpice        | 2216-2218      | (2011.41, 2223.13) | double    | ±5% around the default 2117.27                                                                                                                                             |
| cnfac        | 0-1            | (0, 1)             | double    | Stays the same                                                                                                                                                             |
| pudz         | 8-14           | (0, 0.5)           | double    | Default is 0 and 0.5 is a reasonable perturbation                                                                                                                          |
| vkc          | 0-1            | (0.35, 0.45)       | double    | 0.05 perturbation around default 0.4                                                                                                                                       |
| mixfact      | 0.2-0.9        | (5, 15)            | double    | 5 perturbation around default 10                                                                                                                                           |
| cpliq        | 4180-4190      | (4180, 4190)       | double    | Recommended in the pdf and default is 4188                                                                                                                                 |
| depthcrit    | 15-35          | (15, 35)           | double    | Defualt is 25 and 10 is a reasonable perturbation                                                                                                                          |
| tkice        | 1-3            | (2.061, 2.519)     | double    | ±10% perturbation around the default 2.29                                                                                                                                  |
| betavis      | 0-1            | (0, 1)             | double    | Recommended in the pdf, default is 0                                                                                                                                       |
| denice       | 915-920        | (915, 920)         | double    | Reasonable perturbation around the default of 917                                                                                                                          |
| dtime_mod    | 3500-3700      | (1800, 3600)       | double    | Recommended in the pdf and default is 3600                                                                                                                                 |
| hfus         | 333500-334000  | (333500, 334000)   | double    | Reasonable perturbation around the default of 333700                                                                                                                       |
| grav         | 5-15           | (9.708, 9.904)     | double    | Small perturbation (±1%) around the default of 9.80616                                                                                                                     |
| lakepuddling | 0-1            | {0, 1}             | int       | It's boolean                                                                                                                                                               |
| denh2o       | 980-1020       | (980, 1020)        | double    | Reasonable perturbation around the default of 1000                                                                                                                         |
| lake_no_ed   | 0-1            | {0, 1}             | int       | boolean                                                                                                                                                                    |
| use_lch4     | 0-1            | {0, 1}             | int       | boolean                                                                                                                                                                    |
| tkair        | 0.01-0.03      | (0.01, 0.03)       | double    | Small perturbation around the default 0.023                                                                                                                                |
| thk_bedrock  | 2-4            | (2, 4)             | double    | Small perturbation around the default of 3                                                                                                                                 |
  
#### Constraints
Constraint:
- lakepuddling = 0 => pudz = 0
Reasoning:
- pudz is only read when lakepuddling is true so leaving out this constraint would possibly waste test cases meant to test interactions between pudz and other variables |

#### Files used to come to these conclusions:
- [LakeTemperatureInput pdf from Collaborators](documentation/from_collaborators/2025/12/LakeTemperatureInput.pdf)
- SPEL odel Constant Defaults netcdf file created by SPEL and stored in /app/model when the test_laketemperature.py script is ran
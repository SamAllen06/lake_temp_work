# Fault Check Summarize Script
testing/utils/fault_check_summarize/

The Fault Check Summarize script is used to take all the output from the 
[Fault Finding analysis plugin](../../../../testing/lake_temp/plugin_inputs/fault_checks) and output how many sample runs exited with an error, how
many samples passed, skipped, failed, and errored for every check, and a list of which
samples passed, skipped, failed, and errored for every single fault check. 

It requires two arguments: a path to the directory containing the Fault Finding sample
output and the number of samples that were run. To get the directory containing the
Fault Finding sample output, use Docker to copy the output directory into your own
directory. 

## Example Workflow
\> docker cp container_id:/app/testing_output/analysis/sample/lake_temp_i2/"Mtf Fault Finding" my_local_directory
\> python testing/utils/fault_check_summarize/src/fcsum/main.py my_local_directory 231
0 out of 231 runs exited with an error.
| Check                                                       | Passed | Skipped | Failed | Errored |
| check_combined_heat_content_finite                          | 115    | 0       | 116    | 0       |
| check_combined_heat_content_not_less_than_soil_heat_content | 221    | 0       | 10     | 0       |
| check_energy_conservation_residual_finite                   | 115    | 0       | 116    | 0       |
<p align=center>$\vdots$\<p>
| check_temp_around_freezing_where_lake_is_almost_frozen      | 0      | 231     | 0      | 0       |
| check_total_sensible_heat_flux_finite                       | 231    | 0       | 0      | 0       |
| check_water_snow_equivalent_not_negative                    | 231    | 0       | 0      | 0       |

Samples per result:
| check_combined_heat_content_finite FAILED:                                                        |
|     7, 8, 9, 10, 11, 16, 17, 18, 19, 20, 25, 26, 27, 28, 29, 30, 34, 35, 36, 37, 38, 39, 40, 45,  |
|     46, 48, 49, 50, 54, 55, 58, 59, 60, 63, 64, 65, 66, 68, 69, 70, 72, 73, 74, 75, 78, 79, 80,   |
|     81, 82, 83, 84, 89, 90, 91, 92, 93, 99, 100, 101, 102, 109, 110, 111, 119, 120, 121, 128,     |
|     129, 130, 131, 132, 138, 139, 140, 141, 142, 148, 149, 150, 151, 152, 158, 159, 160, 161,     |
|     162, 168, 169, 170, 171, 172, 178, 179, 180, 181, 182, 188, 189, 190, 191, 192, 199, 200,     |
|     201, 202, 209, 210, 211, 212, 219, 220, 221, 222, 229, 230, 231                               |
<p align=center>$\vdots$\<p>
| check_water_snow_equivalent_not_negative PASSED:                                                  |
|     1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,    |
|     26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48,   |
|     49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71,   |
|     72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94,   |
|     95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113,     |
|     114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131,     |
|     132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149,     |
|     150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167,     |
|     168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185,     |
|     186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203,     |
|     204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221,     |
|     222, 223, 224, 225, 226, 227, 228, 229, 230, 231                                              |

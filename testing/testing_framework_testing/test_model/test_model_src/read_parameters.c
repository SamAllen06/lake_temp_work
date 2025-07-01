#include "read_parameters.h"

#include <stdio.h>
#include <stdlib.h>

double *read_params(const char *params_file_path, int param_count)
{
  FILE *params_file = fopen(params_file_path, "r");

  double *params = (double*) malloc(sizeof(double) * param_count);

  for (int param_index = 0; param_index < param_count; param_index++)
  {
    fscanf(params_file, "%*s\n%lf\n", params + param_index);
  }

  fclose(params_file);

  return params;
}

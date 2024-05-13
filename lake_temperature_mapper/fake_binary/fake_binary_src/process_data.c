#include "process_data.h"

#include <stdio.h>
#include <stdlib.h>

const int OUTPUT_COUNT = 4;

double *generate_outputs(double *inputs, int param_count)
{
  double sum = 0.0;
  double product = 1.0;

  for (int param_index = 0; param_index < param_count; param_index++)
  {
    sum += inputs[param_index];
    product *= inputs[param_index];
  }

  double *outputs = (double*) malloc(sizeof(double) * OUTPUT_COUNT);
  outputs[0] = sum;
  outputs[1] = sum * 2;
  outputs[2] = product;
  outputs[3] = product * product;

  return outputs;
}

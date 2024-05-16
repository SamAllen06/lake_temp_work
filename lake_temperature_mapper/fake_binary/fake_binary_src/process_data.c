#include "process_data.h"

#include <stdio.h>
#include <stdlib.h>

const int OUTPUT_COUNT = 8;

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
  outputs[2] = sum * 0.1;
  outputs[3] = sum * 0.5;
  outputs[4] = product;
  outputs[5] = product * product;
  outputs[6] = product * sum;
  outputs[7] = product * product * sum;

  return outputs;
}

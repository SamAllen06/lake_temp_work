#include "write_outputs.h"

#include <stdio.h>
#include <stdlib.h>

void save_outputs_to_file(
  double* outputs,
  const char output_names[][25],
  int output_count,
  const char *output_file_name)
{
  FILE* output_file = fopen(output_file_name, "w");

  for (int output_var_index = 0; output_var_index < output_count / 4; output_var_index++)
  {
    const char *NAME = output_names[output_var_index];
    fprintf(
      output_file, "%s\n  %lf %lf\n  %lf %lf\n",
      NAME,
      outputs[output_var_index * 2],
      outputs[output_var_index * 2 + 1],
      outputs[output_var_index * 2 + 2],
      outputs[output_var_index * 2 + 3]
    );
  }

  fclose(output_file);
}

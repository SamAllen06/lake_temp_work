#include <stdio.h>
#include <stdlib.h>

const char PARAMS_FILE_NAME[] = "lakeparams.txt";
const char OUTPUT_FILE_NAME[] = "fake_LakeTemperatureTest.txt";

const char OUTPUT_VARIABLE_NAMES[][25] = {"fakevar%sum", "fakevar%product"};

const int PARAM_COUNT = 7;
const int OUTPUT_COUNT = 4;

double* read_params()
{
  FILE* params_file = fopen(PARAMS_FILE_NAME, "r");

  double *params = (double*) malloc(sizeof(double) * PARAM_COUNT);

  for (int param_index = 0; param_index < PARAM_COUNT; param_index++)
  {
    fscanf(params_file, "%*s\n%lf\n", params + param_index);
  }

  fclose(params_file);

  return params;
}

double* generate_outputs(double* inputs)
{
  double sum = 0.0;
  double product = 1.0;

  for (int param_index = 0; param_index < PARAM_COUNT; param_index++)
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

void save_outputs_to_file(double* outputs)
{
  FILE* output_file = fopen(OUTPUT_FILE_NAME, "w");

  for (int output_var_index = 0; output_var_index < OUTPUT_COUNT / 2; output_var_index++)
  {
    const char *NAME = OUTPUT_VARIABLE_NAMES[output_var_index];
    fprintf(
      output_file, "%s\n  %lf %lf\n",
      NAME,
      outputs[output_var_index * 2],
      outputs[output_var_index * 2 + 1]
    );
  }

  fclose(output_file);
}

int main()
{
  printf("Some output for stdout\n");
  fprintf(stderr, "Some output for stderr\n");

  double *params = read_params();
  double *outputs = generate_outputs(params);

  save_outputs_to_file(outputs);

  free(params);
  free(outputs);
}

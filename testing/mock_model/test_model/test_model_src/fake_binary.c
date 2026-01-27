#include <stdio.h>
#include <stdlib.h>

#include "process_data.h"
#include "read_parameters.h"
#include "write_outputs.h"

const char PARAMS_FILE_NAME[] = "lakeparams.txt";
const char OUTPUT_FILE_NAME[] = "fake_LakeTemperatureTest.txt";

const char OUTPUT_VARIABLE_NAMES[][25] = {
  "fakevar%sum",
  "fakevar%product"
};

const int PARAM_COUNT = 7;

void print_output()
{
  printf("Some output for stdout\n");
  fprintf(stderr, "Some output for stderr\n");
}

void process_input_and_write_output()
{
  double *params = read_params(PARAMS_FILE_NAME, PARAM_COUNT);
  double *outputs = generate_outputs(params, PARAM_COUNT);

  save_outputs_to_file(
    outputs,
    OUTPUT_VARIABLE_NAMES,
    OUTPUT_COUNT,
    OUTPUT_FILE_NAME
  );

  free(params);
  free(outputs);
}

int main()
{
  print_output();
  process_input_and_write_output();

  return 0;
}

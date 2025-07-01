#ifndef WRITE_OUTPUTS_H_
#define WRITE_OUTPUTS_H_

void save_outputs_to_file(
  double* outputs,
  const char output_names[][25],
  int output_count,
  const char *output_file_name
);

#endif

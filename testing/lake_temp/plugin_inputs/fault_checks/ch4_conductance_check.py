import numpy as np
import numpy.typing as npt


def check_methane_conductance(
    use_lch4: int,
    test_lakestate_vars_lake_icefrac_col: npt.NDArray,
    test_ch4_vars_grnd_ch4_cond_col: npt.NDArray,
) -> None:
    if not use_lch4:
        return

    top_layers = test_lakestate_vars_lake_icefrac_col[:, 1, :]

    frozen_top_layers = top_layers > 0.1

    conducting_columns = test_ch4_vars_grnd_ch4_cond_col > 0.0

    conducting_frozen_columns = frozen_top_layers & conducting_columns

    assert not np.any(conducting_frozen_columns), "Frozen columns are conducting ch4"
    

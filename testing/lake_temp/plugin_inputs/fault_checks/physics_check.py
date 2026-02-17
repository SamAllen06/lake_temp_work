import numpy as np
import numpy.typing as npt

# tfrz not in constants.
TFRZ = 273.15


def check_temp_at_freezing_where_lake_is_frozen(
#    tfrz: float,
    test_col_es_t_lake: npt.NDArray,
    test_lakestate_vars_lake_icefrac_col: npt.NDArray,
) -> None:
    diff_to_frozen = np.abs(test_lakestate_vars_lake_icefrac_col - 1.0)
    frozen = diff_to_frozen <= 1E-6

    diff_to_freezing_temp = np.abs(TFRZ - test_col_es_t_lake)
    close_to_freezing = diff_to_freezing_temp <= 1E-3

    frozen_and_freezing = frozen & close_to_freezing
    not_frozen_or_frozen_and_freezing = frozen_and_freezing | ~frozen

    assert np.all(not_frozen_or_frozen_and_freezing), "Columns are frozen but not at freezing point"


def no_eddies_when_surface_frozen(
    test_col_es_t_lake: npt.NDArray,
    test_lakestate_vars_savedtke1_col: npt.NDArray,
) -> None:
    surface_frozen = test_col_es_t_lake[:, 1, :] <= TFRZ

    eddies_present = test_lakestate_vars_savedtke1_col > 0.0

    frozen_and_eddies = surface_frozen & eddies_present

    assert not np.any(frozen_and_eddies), "Eddies are present on a frozen surface"

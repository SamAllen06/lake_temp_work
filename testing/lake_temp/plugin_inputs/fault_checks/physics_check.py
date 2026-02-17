import numpy as np
import numpy.typing as npt


# tfrz not in constants.
#def check_temp_at_freezing_where_lake_is_frozen(
#    tfrz: float,
#    test_col_es_t_lake: npt.NDArray,
#    test_lakestate_vars_lake_icefrac_col: npt.NDArray,
#) -> None:
#    diff_to_frozen = np.abs(test_lakestate_vars_lake_icefrac_col - 1.0)
#    frozen = diff_to_frozen <= 1E-6
#
#    diff_to_freezing_temp = np.abs(tfrz - test_col_es_t_lake)
#    close_to_freezing = diff_to_freezing_temp <= 1E-3
#
#    # frozen -> freezing
#    # not freezing -> not frozen
#    # 0 0 | 1
#    # 0 1 | 1
#    # 1 0 | 0
#    # 1 1 | 1
#
#    frozen_and_freezing = frozen & close_to_freezing
#    not_frozen_or_frozen_and_freezing = frozen_and_freezing | ~frozen
#
#    assert np.all(not_frozen_or_frozen_and_freezing), "Columns are frozen but not at freezing point"

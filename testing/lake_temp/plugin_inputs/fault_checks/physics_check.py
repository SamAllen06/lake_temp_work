import numpy as np
import numpy.typing as npt

from mtf_fault_finding import CheckStatus

# tfrz not in constants.
TFRZ = 273.15


def check_temp_at_freezing_where_lake_is_frozen(
    test_col_es_t_lake: npt.NDArray,
    test_lakestate_vars_lake_icefrac_col: npt.NDArray,
) -> None:
    frozen = np.isclose(test_lakestate_vars_lake_icefrac_col, 1.0)

    if not np.any(frozen):
        return CheckStatus.SKIPPED

    diff_to_freezing_temp = np.abs(TFRZ - test_col_es_t_lake)
    close_to_freezing_temp = diff_to_freezing_temp <= 1E-3

    assert np.all(~frozen | close_to_freezing_temp), (
        "Columns are frozen but not at freezing point"
    )


def no_tke_when_surface_frozen(
    test_col_es_t_lake: npt.NDArray,
    test_col_pp_snl: npt.NDArray,
    test_lakestate_vars_savedtke1_col: npt.NDArray,
) -> None:
    tke_present = test_lakestate_vars_savedtke1_col > 0.0

    surface_frozen = test_col_es_t_lake[:, 0, :] <= TFRZ
    snow_present = test_col_pp_snl > 0
    unfrozen = ~surface_frozen & ~snow_present

    if not np.any(tke_present):
        return CheckStatus.SKIPPED

    assert np.all(~tke_present | unfrozen), (
        "Turbulant kinentic energy present on a frozen surface"
    )

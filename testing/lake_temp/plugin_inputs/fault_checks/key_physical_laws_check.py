from enum import Enum

import numpy as np
import numpy.typing as npt

from mtf_fault_finding import CheckStatus

# tfrz not in constants.
TFRZ = 273.15


class IMelt(Enum):
    NONE = 0
    MELTING = 1
    FREEZING = 2


def check_energy_conservation(
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_es_t_lake: npt.NDArray,
    test_lakestate_vars_lake_icefrac_col: npt.NDArray,
):
    no_snow_layers = test_col_pp_snl == 0
    no_snow_water = test_col_ws_h2osno == 0.0
    surface_above_freezing = test_col_es_t_lake[:, 1, :] > TFRZ
    unfrozen_surface = test_lakestate_vars_lake_icefrac_col[:, 1, :] == 0.0

    # Skip unless lake is unfrozen.
    if not np.all(
        no_snow_layers & no_snow_water & surface_above_freezing & unfrozen_surface
    ):
        return CheckStatus.SKIPPED

    # Needs energy conservation check here.


def snow_freezing_produces_latent_heat(
    test_col_pp_snl: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_es_t_lake: npt.NDArray,

    test_col_wf_qflx_snofrz: npt.NDArray,
    test_col_wf_qflx_snofrz_lyr: npt.NDArray,
    test_col_wf_qflx_snomelt: npt.NDArray,
    test_col_ef_imelt: npt.NDArray,
    test_col_ws_h2osno: npt.NDArray,
    test_col_ws_snow_depth: npt.NDArray,
):
    pass


from collections.abc import Sequence

import utils


def check_hc_soi_is_positive(
        test_col_es_hc_soi: Sequence[float]
) -> None:
    assert utils.are_all_positive(test_col_es_hc_soi, allow_zero=True), (
        "Expected all values of col_es%hc_soi to be positive"
    )


def check_t_lake_is_positive(
        test_col_es_t_lake : Sequence[float]
) -> None:
    assert utils.are_all_positive(test_col_es_t_lake, allow_zero=True), (
        "Expected all values of col_es%t_lake to be positive"
    )


def check_hc_soisno_is_positive(
        test_col_es_hc_soisno : Sequence[float]
) -> None:
    assert utils.are_all_positive(test_col_es_hc_soisno, allow_zero=True), (
        "Expected all values of col_es%hc_soisno to be positive"
    )

# This one is not listed as required to be positive, but given its in Kelvin, I'm
# confident it is.
def check_t_soisno_is_positive(
        test_col_es_t_soisno : Sequence[float]
) -> None:
    assert utils.are_all_positive(test_col_es_t_soisno, allow_zero=True), (
        "Expected all values of col_es%t_soisno to be positive"
    )

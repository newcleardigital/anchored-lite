import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from fees.charge import fx_fee, within_daily_limit


def test_fx_fee_is_1_5_percent():
    assert fx_fee(100) == 1.5


def test_fx_fee_never_below_minimum():
    assert fx_fee(1) == 0.25


def test_daily_limit():
    assert within_daily_limit(4900, 100)
    assert not within_daily_limit(4900, 101)


if __name__ == "__main__":
    test_fx_fee_is_1_5_percent(); test_fx_fee_never_below_minimum(); test_daily_limit()
    print("3 tests passed")

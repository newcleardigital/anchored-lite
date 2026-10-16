from fees.limits import FX_FEE_PCT, MIN_FEE_EUR, DAILY_LIMIT_EUR


def fx_fee(amount_eur: float) -> float:
    """Fee for a card payment in a foreign currency."""
    return round(max(amount_eur * FX_FEE_PCT / 100, MIN_FEE_EUR), 2)


def within_daily_limit(spent_today_eur: float, amount_eur: float) -> bool:
    """A cardholder may not spend more than the daily limit."""
    return spent_today_eur + amount_eur <= DAILY_LIMIT_EUR

from decimal import Decimal

from actions.openbb_fx_rates import get_fx_rate
from actions.openbb_prices import get_price


def display_balance(ctx) -> None:
    """Calculate and print total portfolio value in base currency."""
    base = ctx.config.base_currency
    total = Decimal("0")

    for currency, amount in ctx.wallet.holdings.items():
        rate = get_fx_rate(currency.code, base, ctx.processing_date)
        total += amount * rate

    for ticker, quantity in ctx.portfolio.positions.items():
        price = get_price(ticker.symbol, ctx.processing_date)
        value = quantity * price
        rate = get_fx_rate(ticker.currency.code, base, ctx.processing_date)
        total += value * rate

    total = total.quantize(Decimal("0.01"))
    print(f"\n=== Balance ({ctx.processing_date}) ===")
    print(f"  Total ({base}): {total}")

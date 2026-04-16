from decimal import Decimal

from actions.mock_fx_rates import get_fx_rate
from actions.mock_prices import get_price
from core.models import Currency, Ticker, Transaction


def rebalance(ctx, target_tickers: list[str]) -> list[Transaction]:
    """Diff-based equal-weight rebalancing.

    Computes total portfolio value, divides equally among target tickers,
    and generates minimal buy/sell transactions.
    """
    base = ctx.config.base_currency
    d = ctx.processing_date
    transactions = []

    # Calculate total portfolio value in base currency
    total_value = Decimal("0")
    for currency, amount in ctx.wallet.holdings.items():
        rate = get_fx_rate(currency.code, base, d)
        total_value += amount * rate
    for ticker, quantity in ctx.portfolio.positions.items():
        price = get_price(ticker.symbol, d)
        rate = get_fx_rate(ticker.currency.code, base, d)
        total_value += quantity * price * rate

    # Calculate target quantities
    target_quantities: dict[str, Decimal] = {}
    if target_tickers:
        value_per_ticker = total_value / len(target_tickers)
        for symbol in target_tickers:
            price = get_price(symbol, d)
            target_qty = (value_per_ticker / price).quantize(Decimal("1"))
            target_quantities[symbol] = target_qty

    # Build map of current positions by symbol
    current_by_symbol: dict[str, tuple[Ticker, Decimal]] = {}
    for ticker, quantity in ctx.portfolio.positions.items():
        current_by_symbol[ticker.symbol] = (ticker, quantity)

    # Generate sell transactions for tickers not in target
    for symbol, (ticker, quantity) in current_by_symbol.items():
        if symbol not in target_quantities:
            price = get_price(symbol, d)
            transactions.append(Transaction(
                date=d, action="sell", ticker=ticker,
                quantity=quantity, price=price,
            ))

    # Generate buy/sell transactions for target tickers
    for symbol in target_tickers:
        target_qty = target_quantities[symbol]
        if symbol in current_by_symbol:
            ticker, current_qty = current_by_symbol[symbol]
            diff = target_qty - current_qty
        else:
            ticker = Ticker(symbol=symbol, currency=Currency(code=base))
            diff = target_qty

        price = get_price(symbol, d)
        if diff > 0:
            transactions.append(Transaction(
                date=d, action="buy", ticker=ticker,
                quantity=diff, price=price,
            ))
        elif diff < 0:
            transactions.append(Transaction(
                date=d, action="sell", ticker=ticker,
                quantity=abs(diff), price=price,
            ))

    return transactions

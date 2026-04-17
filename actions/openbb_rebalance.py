from decimal import Decimal

from actions.openbb_fx_rates import get_fx_rate
import actions.openbb_prices as _prices_module
from actions.openbb_prices import get_price
from core.models import Currency, Ticker, Transaction


def rebalance(ctx, target_tickers: list[str]) -> list[Transaction]:
    """Diff-based equal-weight rebalancing using OpenBB prices and FX rates."""
    base = ctx.config.base_currency
    d = ctx.processing_date
    transactions = []

    # Tell price module the full backtest range so bulk fetches cover all dates
    if _prices_module.backtest_start is None:
        _prices_module.backtest_start = ctx.config.start_date
        _prices_module.backtest_end = ctx.config.end_date

    # Calculate total portfolio value in base currency — skip unpriceable positions
    total_value = Decimal("0")
    for currency, amount in ctx.wallet.holdings.items():
        rate = get_fx_rate(currency.code, base, d)
        total_value += amount * rate
    held_prices: dict[str, Decimal] = {}
    for ticker, quantity in ctx.portfolio.positions.items():
        try:
            price = get_price(ticker.symbol, d)
            rate = get_fx_rate(ticker.currency.code, base, d)
            total_value += quantity * price * rate
            held_prices[ticker.symbol] = price
        except RuntimeError:
            continue

    # Calculate target quantities — skip tickers with no price data
    target_quantities: dict[str, Decimal] = {}
    prices: dict[str, Decimal] = {}
    if target_tickers:
        valid_tickers = []
        for symbol in target_tickers:
            try:
                prices[symbol] = get_price(symbol, d)
                valid_tickers.append(symbol)
            except RuntimeError:
                continue

        if valid_tickers:
            value_per_ticker = total_value / len(valid_tickers)
            for symbol in valid_tickers:
                target_qty = (value_per_ticker / prices[symbol]).quantize(Decimal("1"))
                target_quantities[symbol] = target_qty

    # Build map of current positions by symbol
    current_by_symbol: dict[str, tuple[Ticker, Decimal]] = {}
    for ticker, quantity in ctx.portfolio.positions.items():
        current_by_symbol[ticker.symbol] = (ticker, quantity)

    # Generate sell transactions for tickers not in target — skip if unpriceable
    for symbol, (ticker, quantity) in current_by_symbol.items():
        if symbol not in target_quantities:
            if symbol not in held_prices:
                continue  # can't price it, leave in portfolio
            transactions.append(Transaction(
                date=d, action="sell", ticker=ticker,
                quantity=quantity, price=held_prices[symbol],
            ))

    # Generate buy/sell transactions for target tickers
    for symbol in target_quantities:
        target_qty = target_quantities[symbol]
        if symbol in current_by_symbol:
            ticker, current_qty = current_by_symbol[symbol]
            diff = target_qty - current_qty
        else:
            ticker = Ticker(symbol=symbol, currency=Currency(code=base))
            diff = target_qty

        price = prices[symbol]
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

from decimal import Decimal

from actions.openbb_fx_rates import get_fx_rate
from actions.openbb_prices import get_price


def calculate_stats(ctx) -> None:
    """Compute current total balance, append to ctx.balance_history, update ctx.cost_basis."""
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

    ctx.balance_history.append((ctx.processing_date, total.quantize(Decimal("0.01"))))

    # Process only transactions added since last stats call
    already_processed = getattr(ctx, "_stats_tx_count", 0)
    new_txs = ctx.all_transactions[already_processed:]
    ctx._stats_tx_count = len(ctx.all_transactions)

    for tx in new_txs:
        if tx.action == "buy":
            symbol = tx.ticker.symbol
            prev_qty, prev_cost = ctx.cost_basis.get(symbol, (Decimal("0"), Decimal("0")))
            ctx.cost_basis[symbol] = (prev_qty + tx.quantity, prev_cost + tx.quantity * tx.price)

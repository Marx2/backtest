from decimal import Decimal

from core.models import Transaction


def execute_transactions(ctx, transactions: list[Transaction]) -> None:
    """Execute transactions: update wallet and portfolio, record in history."""
    for tx in transactions:
        cash_currency = tx.ticker.currency
        cash_amount = tx.quantity * tx.price

        if tx.action == "buy":
            ctx.wallet.holdings[cash_currency] -= cash_amount
            current = ctx.portfolio.positions.get(tx.ticker, Decimal("0"))
            ctx.portfolio.positions[tx.ticker] = current + tx.quantity
        elif tx.action == "sell":
            current_cash = ctx.wallet.holdings.get(cash_currency, Decimal("0"))
            ctx.wallet.holdings[cash_currency] = current_cash + cash_amount
            current = ctx.portfolio.positions.get(tx.ticker, Decimal("0"))
            new_qty = current - tx.quantity
            if new_qty <= 0:
                ctx.portfolio.positions.pop(tx.ticker, None)
            else:
                ctx.portfolio.positions[tx.ticker] = new_qty

        ctx.all_transactions.append(tx)

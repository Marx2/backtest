from core.context import BacktestContext


def run(ctx: BacktestContext) -> None:
    """Basic equal-weight strategy using mock (deterministic) data."""
    while ctx.advance():
        screened = ctx.mock_screen_stocks()
        transactions = ctx.mock_rebalance(screened)
        ctx.execute_transactions(transactions)
        ctx.display_wallet()
        ctx.display_portfolio()
        ctx.mock_display_balance()

    transactions = ctx.mock_rebalance([])
    ctx.execute_transactions(transactions)
    ctx.display_portfolio()
    ctx.mock_display_balance()

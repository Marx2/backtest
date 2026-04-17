from core.context import BacktestContext


def run(ctx: BacktestContext) -> None:
    """Basic equal-weight strategy using live OpenBB data (yfinance/FMP)."""
    while ctx.advance():
        screened = ctx.openbb_screen_stocks()
        transactions = ctx.openbb_rebalance(screened)
        ctx.execute_transactions(transactions)
        ctx.display_wallet()
        ctx.display_portfolio()
        ctx.openbb_display_balance()

    transactions = ctx.openbb_rebalance([])
    ctx.execute_transactions(transactions)
    ctx.display_portfolio()
    ctx.openbb_display_balance()

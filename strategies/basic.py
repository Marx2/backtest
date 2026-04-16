from core.context import BacktestContext


def run(ctx: BacktestContext) -> None:
    """Basic equal-weight strategy.

    Screens stocks each period, rebalances to equal weight,
    then sells everything at the end.
    """
    # loop
    while ctx.advance():
        screened = ctx.screen_stocks()
        transactions = ctx.rebalance(screened)
        ctx.execute_transactions(transactions)
        ctx.display_wallet()
        ctx.display_portfolio()
        ctx.display_balance()

    # finish
    transactions = ctx.rebalance([])
    ctx.execute_transactions(transactions)
    ctx.display_portfolio()
    ctx.display_balance()

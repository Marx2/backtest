def display_portfolio(ctx) -> None:
    """Print portfolio positions."""
    print(f"\n=== Portfolio ({ctx.processing_date}) ===")
    if not ctx.portfolio.positions:
        print("  (empty)")
        return
    for ticker, quantity in ctx.portfolio.positions.items():
        print(f"  {ticker.symbol}: {quantity}")

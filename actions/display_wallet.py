def display_wallet(ctx) -> None:
    """Print wallet contents."""
    print(f"\n=== Wallet ({ctx.processing_date}) ===")
    if not ctx.wallet.holdings:
        print("  (empty)")
        return
    for currency, amount in ctx.wallet.holdings.items():
        print(f"  {currency.code}: {amount}")

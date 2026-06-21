from decimal import Decimal


def display_config(ctx) -> None:
    cfg = ctx.config
    base = cfg.base_currency
    cash_total = sum(
        v for k, v in cfg.initial_cash.items() if k == base
    ) or next(iter(cfg.initial_cash.values()), Decimal("0"))

    print("=== Backtest Configuration ===")
    print(f"  Period:         {cfg.start_date} → {cfg.end_date}")
    print(f"  Interval:       {cfg.interval}")
    print(f"  Base currency:  {base}")
    print(f"  Initial cash:   {base} {cash_total:,.2f}")
    if cfg.screening:
        print()
        print("  Screening:")
        for k, v in cfg.screening.items():
            print(f"    {k:<14}{v}")
    print()

from decimal import Decimal
import math


def display_summary(ctx) -> None:
    cfg = ctx.config
    summary_cfg = getattr(cfg, "summary", {})

    def show(key: str) -> bool:
        entry = summary_cfg.get(key, {})
        if isinstance(entry, dict):
            return entry.get("enabled", True)
        return bool(entry)

    def hint_for(key: str, value: float) -> str:
        """Pick hint string from threshold bands defined in config."""
        entry = summary_cfg.get(key, {})
        if not isinstance(entry, dict):
            return ""
        # Simple fixed hint (no thresholds)
        if "hint" in entry:
            return entry["hint"]
        thresholds = entry.get("thresholds", {})
        if not thresholds:
            return ""
        # Bands ordered: excellent → good → weak → bad (fallback)
        for band in ("excellent", "good", "weak"):
            band_cfg = thresholds.get(band, {})
            mn = band_cfg.get("min")
            mx = band_cfg.get("max")
            if mn is not None and value >= mn:
                return band_cfg.get("hint", "")
            if mx is not None and value <= mx:
                return band_cfg.get("hint", "")
        return thresholds.get("bad", {}).get("hint", "")

    def emit(lines: list, value_line: str, hint: str) -> None:
        lines.append(value_line)
        if hint:
            lines.append(f"                    {hint}")

    initial = sum(cfg.initial_cash.values())
    final = ctx.balance_history[-1][1] if ctx.balance_history else initial

    start = cfg.start_date
    end = cfg.end_date
    years = (end - start).days / 365.25

    print("=== Summary ===")
    print(f"  Period:         {start} → {end}  ({years:.1f} years)")
    print(f"  Initial value:  {cfg.base_currency} {initial:>12,.2f}")
    print(f"  Final value:    {cfg.base_currency} {final:>12,.2f}")

    # Returns
    total_return = float((final - initial) / initial * 100) if initial else 0.0
    cagr = (float(final / initial) ** (1.0 / years) - 1) * 100 if initial and years > 0 else 0.0

    returns_lines = []
    if show("total_return"):
        sign = "+" if total_return >= 0 else ""
        emit(returns_lines, f"  Total return:   {sign}{total_return:.2f}%", hint_for("total_return", total_return))
    if show("cagr"):
        sign = "+" if cagr >= 0 else ""
        emit(returns_lines, f"  CAGR:           {sign}{cagr:.1f}%", hint_for("cagr", cagr))
    if returns_lines:
        print()
        print("  [Returns]")
        for line in returns_lines:
            print(line)

    # Risk metrics from balance history
    risk_lines = []
    if ctx.balance_history and len(ctx.balance_history) > 1:
        balances = [b for _, b in ctx.balance_history]
        period_returns = [
            float((balances[i] - balances[i - 1]) / balances[i - 1])
            for i in range(1, len(balances))
        ]

        if show("max_drawdown"):
            peak = balances[0]
            max_dd = 0.0
            for b in balances:
                if b > peak:
                    peak = b
                dd = float((b - peak) / peak) * 100
                if dd < max_dd:
                    max_dd = dd
            emit(risk_lines, f"  Max drawdown:   {max_dd:.1f}%", hint_for("max_drawdown", max_dd))

        if show("volatility") or show("sharpe_ratio"):
            n = len(period_returns)
            mean_r = sum(period_returns) / n
            variance = sum((r - mean_r) ** 2 for r in period_returns) / n
            std_period = math.sqrt(variance)
            periods_per_year = _periods_per_year(cfg.interval)
            vol_ann = std_period * math.sqrt(periods_per_year) * 100

            if show("volatility"):
                emit(risk_lines, f"  Volatility:     {vol_ann:.1f}% (annualized)", hint_for("volatility", vol_ann))

            if show("sharpe_ratio"):
                sharpe = (mean_r * periods_per_year) / (std_period * math.sqrt(periods_per_year)) if std_period > 0 else 0.0
                emit(risk_lines, f"  Sharpe ratio:   {sharpe:.2f}", hint_for("sharpe_ratio", sharpe))

    if risk_lines:
        print()
        print("  [Risk]")
        for line in risk_lines:
            print(line)

    # Trades
    sells = [tx for tx in ctx.all_transactions if tx.action == "sell"]
    buys = [tx for tx in ctx.all_transactions if tx.action == "buy"]

    trade_lines = []
    if show("total_trades"):
        emit(trade_lines, f"  Total trades:   {len(ctx.all_transactions)}", hint_for("total_trades", len(ctx.all_transactions)))
    if show("buy_trades") or show("sell_trades"):
        emit(trade_lines, f"  Buy / Sell:     {len(buys)} / {len(sells)}", "")
    if show("win_rate") and sells:
        wins = 0
        for tx in sells:
            symbol = tx.ticker.symbol
            if symbol in ctx.cost_basis:
                qty, cost = ctx.cost_basis[symbol]
                avg_cost = cost / qty if qty else Decimal("0")
                if tx.price > avg_cost:
                    wins += 1
        win_rate = wins / len(sells) * 100
        emit(trade_lines, f"  Win rate:       {win_rate:.1f}%", hint_for("win_rate", win_rate))
    if show("profit_factor") and sells:
        gross_profit = 0.0
        gross_loss = 0.0
        for tx in sells:
            basis = ctx.cost_basis.get(tx.ticker.symbol)
            if not basis:
                continue
            qty, cost = basis
            avg_cost = float(cost / qty) if qty else 0.0
            pnl = (float(tx.price) - avg_cost) * float(tx.quantity)
            if pnl > 0:
                gross_profit += pnl
            else:
                gross_loss += abs(pnl)
        pf = gross_profit / gross_loss if gross_loss > 0 else float("inf")
        value_line = f"  Profit factor:  {pf:.2f}" if pf != float("inf") else "  Profit factor:  ∞"
        emit(trade_lines, value_line, hint_for("profit_factor", pf if pf != float("inf") else 999))

    if trade_lines:
        print()
        print("  [Trades]")
        for line in trade_lines:
            print(line)

    print()


def _periods_per_year(interval: str) -> float:
    mapping = {"day": 252.0, "week": 52.0, "month": 12.0, "quarter": 4.0, "year": 1.0}
    return mapping.get(interval.lower(), 12.0)

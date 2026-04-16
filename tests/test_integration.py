from datetime import date
from decimal import Decimal

from core.context import BacktestContext
from core.models import BacktestConfig


def _make_config():
    return BacktestConfig(
        start_date=date(2025, 1, 1),
        end_date=date(2025, 3, 31),
        interval="month",
        base_currency="USD",
        initial_cash={"USD": Decimal("10000")},
        screening={"min_score": 0.5},
    )


def test_full_backtest_runs_without_error(capsys):
    """Run full backtest with basic strategy and verify it completes."""
    from strategies.basic import run

    config = _make_config()
    ctx = BacktestContext(config)
    run(ctx)

    assert len(ctx.portfolio.positions) == 0
    assert len(ctx.all_transactions) > 0
    total_cash = sum(ctx.wallet.holdings.values())
    assert total_cash > 0

    output = capsys.readouterr().out
    assert "Wallet" in output
    assert "Portfolio" in output
    assert "Balance" in output


def test_full_backtest_deterministic():
    """Two runs with same config produce same results."""
    from strategies.basic import run

    config1 = _make_config()
    ctx1 = BacktestContext(config1)
    run(ctx1)

    config2 = _make_config()
    ctx2 = BacktestContext(config2)
    run(ctx2)

    assert len(ctx1.all_transactions) == len(ctx2.all_transactions)
    for tx1, tx2 in zip(ctx1.all_transactions, ctx2.all_transactions):
        assert tx1.ticker.symbol == tx2.ticker.symbol
        assert tx1.action == tx2.action
        assert tx1.quantity == tx2.quantity
        assert tx1.price == tx2.price


def test_backtest_cli_end_to_end(capsys):
    """Test via main.load_config + strategy load."""
    from main import load_config, load_strategy

    config = load_config("config/backtest.yaml")
    ctx = BacktestContext(config)
    strategy = load_strategy("strategies/basic.py")
    strategy.run(ctx)

    assert len(ctx.portfolio.positions) == 0
    assert len(ctx.all_transactions) > 0

from datetime import date
from decimal import Decimal

from core.context import BacktestContext
from core.models import BacktestConfig, Currency


def _make_config():
    return BacktestConfig(
        start_date=date(2025, 1, 1),
        end_date=date(2025, 12, 31),
        interval="month",
        base_currency="USD",
        initial_cash={"USD": Decimal("10000")},
        screening={"min_score": 0.5},
    )


def test_context_initializes_wallet_from_config():
    ctx = BacktestContext(_make_config())
    usd = Currency(code="USD")
    assert ctx.wallet.holdings[usd] == Decimal("10000")


def test_context_initializes_empty_portfolio():
    ctx = BacktestContext(_make_config())
    assert len(ctx.portfolio.positions) == 0


def test_context_initializes_empty_transactions():
    ctx = BacktestContext(_make_config())
    assert ctx.all_transactions == []


def test_context_processing_date_starts_none():
    ctx = BacktestContext(_make_config())
    assert ctx.processing_date is None


def test_context_advance_delegates():
    ctx = BacktestContext(_make_config())
    result = ctx.advance()
    assert result is True
    assert ctx.processing_date == date(2025, 1, 1)


def test_context_screen_stocks_delegates():
    ctx = BacktestContext(_make_config())
    ctx.processing_date = date(2025, 3, 1)
    result = ctx.mock_screen_stocks()
    assert isinstance(result, list)


def test_context_display_wallet_delegates(capsys):
    ctx = BacktestContext(_make_config())
    ctx.processing_date = date(2025, 3, 1)
    ctx.display_wallet()
    output = capsys.readouterr().out
    assert "USD" in output


def test_context_display_portfolio_delegates(capsys):
    ctx = BacktestContext(_make_config())
    ctx.processing_date = date(2025, 3, 1)
    ctx.display_portfolio()
    output = capsys.readouterr().out
    assert output


def test_context_display_balance_delegates(capsys):
    ctx = BacktestContext(_make_config())
    ctx.processing_date = date(2025, 3, 1)
    ctx.mock_display_balance()
    output = capsys.readouterr().out
    assert "10000" in output

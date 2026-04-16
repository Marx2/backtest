import sys
from datetime import date
from decimal import Decimal
from unittest.mock import patch

from core.models import BacktestConfig


def test_load_config():
    from main import load_config

    config = load_config("config/backtest.yaml")
    assert isinstance(config, BacktestConfig)
    assert config.start_date == date(2025, 1, 1)
    assert config.end_date == date(2025, 12, 31)
    assert config.interval == "month"
    assert config.base_currency == "USD"
    assert config.initial_cash["USD"] == Decimal("10000")
    assert config.screening == {"min_score": 0.5}


def test_load_strategy():
    from main import load_strategy

    strategy = load_strategy("strategies/basic.py")
    assert hasattr(strategy, "run")
    assert callable(strategy.run)


def test_parse_args():
    from main import parse_args

    with patch.object(
        sys,
        "argv",
        ["main.py", "-config=config/backtest.yaml", "-strategy=strategies/basic.py"],
    ):
        args = parse_args()
        assert args.config == "config/backtest.yaml"
        assert args.strategy == "strategies/basic.py"

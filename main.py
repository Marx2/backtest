import argparse
import importlib.util
from datetime import date
from decimal import Decimal

import yaml

from core.context import BacktestContext
from core.models import BacktestConfig


def parse_args():
    parser = argparse.ArgumentParser(description="Run backtest")
    parser.add_argument("-config", required=True, help="Path to YAML config file")
    parser.add_argument("-strategy", required=True, help="Path to strategy Python file")
    return parser.parse_args()


def load_config(path: str) -> BacktestConfig:
    with open(path) as f:
        raw = yaml.safe_load(f)

    return BacktestConfig(
        start_date=date.fromisoformat(raw["start_date"]),
        end_date=date.fromisoformat(raw["end_date"]),
        interval=raw["interval"],
        base_currency=raw["base_currency"],
        initial_cash={
            k: Decimal(str(v)) for k, v in raw["initial_cash"].items()
        },
        screening=raw.get("screening", {}),
    )


def load_strategy(path: str):
    spec = importlib.util.spec_from_file_location("strategy", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    args = parse_args()
    config = load_config(args.config)
    ctx = BacktestContext(config)
    strategy = load_strategy(args.strategy)
    strategy.run(ctx)


if __name__ == "__main__":
    main()

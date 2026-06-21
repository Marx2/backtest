import argparse
import importlib.util
from datetime import date
from decimal import Decimal

import yaml

from core.cache import configure as configure_cache, clear as clear_cache
from core.context import BacktestContext
from core.models import BacktestConfig


def parse_args():
    parser = argparse.ArgumentParser(description="Run backtest")
    parser.add_argument("-config", required=True, help="Path to YAML config file")
    parser.add_argument("-strategy", required=True, help="Path to strategy Python file")
    parser.add_argument("--clear-cache", action="store_true", help="Clear cache before running")
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
        summary=raw.get("summary", {}),
        cache=raw.get("cache", {}),
    )


def load_strategy(path: str):
    spec = importlib.util.spec_from_file_location("strategy", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    args = parse_args()
    config = load_config(args.config)

    cache_cfg = config.cache
    configure_cache(
        enabled=cache_cfg.get("enabled", False),
        ttl_days=cache_cfg.get("ttl_days", 7),
        cache_dir=cache_cfg.get("dir", "cache"),
    )
    if args.clear_cache:
        clear_cache()

    ctx = BacktestContext(config)
    strategy = load_strategy(args.strategy)
    strategy.run(ctx)


if __name__ == "__main__":
    main()

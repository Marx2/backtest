from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class Currency:
    code: str


@dataclass(frozen=True)
class Ticker:
    symbol: str
    currency: Currency


@dataclass
class Wallet:
    holdings: dict[Currency, Decimal] = field(default_factory=dict)


@dataclass
class Portfolio:
    positions: dict[Ticker, Decimal] = field(default_factory=dict)


@dataclass
class Transaction:
    date: date
    action: str
    ticker: Ticker
    quantity: Decimal
    price: Decimal


@dataclass
class BacktestConfig:
    start_date: date
    end_date: date
    interval: str
    base_currency: str
    initial_cash: dict[str, Decimal]
    screening: dict

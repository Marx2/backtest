from actions.advance import advance as _advance
from actions.display_balance import display_balance as _display_balance
from actions.display_portfolio import display_portfolio as _display_portfolio
from actions.display_wallet import display_wallet as _display_wallet
from actions.execute_transactions import execute_transactions as _execute_transactions
from actions.rebalance import rebalance as _rebalance
from actions.screen_stocks import screen_stocks as _screen_stocks
from core.models import BacktestConfig, Currency, Portfolio, Transaction, Wallet


class BacktestContext:
    def __init__(self, config: BacktestConfig):
        self.config = config
        self.processing_date = None
        self.all_transactions: list[Transaction] = []

        self.wallet = Wallet(holdings={})
        for currency_code, amount in config.initial_cash.items():
            self.wallet.holdings[Currency(code=currency_code)] = amount

        self.portfolio = Portfolio(positions={})

    def advance(self) -> bool:
        return _advance(self)

    def screen_stocks(self) -> list[str]:
        return _screen_stocks(self)

    def rebalance(self, target_tickers: list[str]) -> list[Transaction]:
        return _rebalance(self, target_tickers)

    def execute_transactions(self, transactions: list[Transaction]) -> None:
        _execute_transactions(self, transactions)

    def display_wallet(self) -> None:
        _display_wallet(self)

    def display_portfolio(self) -> None:
        _display_portfolio(self)

    def display_balance(self) -> None:
        _display_balance(self)

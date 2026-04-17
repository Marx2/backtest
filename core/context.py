from actions.advance import advance as _advance
from actions.display_balance import display_balance as _mock_display_balance
from actions.display_portfolio import display_portfolio as _display_portfolio
from actions.display_wallet import display_wallet as _display_wallet
from actions.execute_transactions import execute_transactions as _execute_transactions
from actions.openbb_display_balance import display_balance as _openbb_display_balance
from actions.openbb_rebalance import rebalance as _openbb_rebalance
from actions.openbb_screener import screen_stocks as _openbb_screen_stocks
from actions.rebalance import rebalance as _mock_rebalance
from actions.screen_stocks import screen_stocks as _mock_screen_stocks
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

    def execute_transactions(self, transactions: list[Transaction]) -> None:
        _execute_transactions(self, transactions)

    def display_wallet(self) -> None:
        _display_wallet(self)

    def display_portfolio(self) -> None:
        _display_portfolio(self)

    # Mock-backed
    def mock_screen_stocks(self) -> list[str]:
        return _mock_screen_stocks(self)

    def mock_rebalance(self, target_tickers: list[str]) -> list[Transaction]:
        return _mock_rebalance(self, target_tickers)

    def mock_display_balance(self) -> None:
        _mock_display_balance(self)

    # OpenBB-backed
    def openbb_screen_stocks(self) -> list[str]:
        return _openbb_screen_stocks(self.processing_date, self.config.screening)

    def openbb_rebalance(self, target_tickers: list[str]) -> list[Transaction]:
        return _openbb_rebalance(self, target_tickers)

    def openbb_display_balance(self) -> None:
        _openbb_display_balance(self)

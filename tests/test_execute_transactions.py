from datetime import date
from decimal import Decimal

from actions.execute_transactions import execute_transactions
from core.models import Currency, Portfolio, Ticker, Transaction, Wallet

USD = Currency(code="USD")
AAPL = Ticker(symbol="AAPL", currency=USD)
MSFT = Ticker(symbol="MSFT", currency=USD)


class FakeContext:
    def __init__(self, wallet_holdings=None, positions=None):
        self.wallet = Wallet(holdings=wallet_holdings or {USD: Decimal("10000")})
        self.portfolio = Portfolio(positions=positions or {})
        self.all_transactions = []


def test_execute_buy_updates_wallet_and_portfolio():
    ctx = FakeContext()
    tx = Transaction(
        date=date(2025, 3, 1), action="buy", ticker=AAPL,
        quantity=Decimal("10"), price=Decimal("100"),
    )
    execute_transactions(ctx, [tx])
    assert ctx.portfolio.positions[AAPL] == Decimal("10")
    assert ctx.wallet.holdings[USD] == Decimal("9000")


def test_execute_sell_updates_wallet_and_portfolio():
    ctx = FakeContext(positions={AAPL: Decimal("10")})
    tx = Transaction(
        date=date(2025, 3, 1), action="sell", ticker=AAPL,
        quantity=Decimal("10"), price=Decimal("150"),
    )
    execute_transactions(ctx, [tx])
    assert AAPL not in ctx.portfolio.positions or ctx.portfolio.positions[AAPL] == Decimal("0")
    assert ctx.wallet.holdings[USD] == Decimal("11500")


def test_execute_appends_to_all_transactions():
    ctx = FakeContext()
    tx = Transaction(
        date=date(2025, 3, 1), action="buy", ticker=AAPL,
        quantity=Decimal("5"), price=Decimal("100"),
    )
    execute_transactions(ctx, [tx])
    assert len(ctx.all_transactions) == 1
    assert ctx.all_transactions[0] is tx


def test_execute_multiple_transactions():
    ctx = FakeContext(wallet_holdings={USD: Decimal("20000")})
    txs = [
        Transaction(
            date=date(2025, 3, 1), action="buy", ticker=AAPL,
            quantity=Decimal("10"), price=Decimal("100"),
        ),
        Transaction(
            date=date(2025, 3, 1), action="buy", ticker=MSFT,
            quantity=Decimal("5"), price=Decimal("200"),
        ),
    ]
    execute_transactions(ctx, txs)
    assert ctx.portfolio.positions[AAPL] == Decimal("10")
    assert ctx.portfolio.positions[MSFT] == Decimal("5")
    assert ctx.wallet.holdings[USD] == Decimal("18000")
    assert len(ctx.all_transactions) == 2


def test_execute_sell_removes_zero_positions():
    ctx = FakeContext(
        wallet_holdings={USD: Decimal("0")},
        positions={AAPL: Decimal("10")},
    )
    tx = Transaction(
        date=date(2025, 3, 1), action="sell", ticker=AAPL,
        quantity=Decimal("10"), price=Decimal("100"),
    )
    execute_transactions(ctx, [tx])
    assert AAPL not in ctx.portfolio.positions

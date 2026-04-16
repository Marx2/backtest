from datetime import date
from decimal import Decimal

from actions.display_wallet import display_wallet
from core.models import Currency, Wallet


class FakeContext:
    def __init__(self, wallet):
        self.wallet = wallet
        self.processing_date = date(2025, 3, 1)


def test_display_wallet_single_currency(capsys):
    usd = Currency(code="USD")
    wallet = Wallet(holdings={usd: Decimal("10000.50")})
    ctx = FakeContext(wallet)
    display_wallet(ctx)
    output = capsys.readouterr().out
    assert "USD" in output
    assert "10000.50" in output


def test_display_wallet_multiple_currencies(capsys):
    usd = Currency(code="USD")
    eur = Currency(code="EUR")
    wallet = Wallet(holdings={usd: Decimal("10000"), eur: Decimal("5000")})
    ctx = FakeContext(wallet)
    display_wallet(ctx)
    output = capsys.readouterr().out
    assert "USD" in output
    assert "EUR" in output


def test_display_wallet_empty(capsys):
    wallet = Wallet(holdings={})
    ctx = FakeContext(wallet)
    display_wallet(ctx)
    output = capsys.readouterr().out
    assert output

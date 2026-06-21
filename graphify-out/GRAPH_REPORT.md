# Graph Report - backtest  (2026-06-21)

## Corpus Check
- 48 files · ~13,019 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 466 nodes · 614 edges · 63 communities (40 shown, 23 thin omitted)
- Extraction: 77% EXTRACTED · 23% INFERRED · 0% AMBIGUOUS · INFERRED: 144 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a49b6146`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Advance & Config|Advance & Config]]
- [[_COMMUNITY_Core Models & Context|Core Models & Context]]
- [[_COMMUNITY_Strategy & Context Interface|Strategy & Context Interface]]
- [[_COMMUNITY_BacktestContext Methods|BacktestContext Methods]]
- [[_COMMUNITY_Rebalance Tests|Rebalance Tests]]
- [[_COMMUNITY_Rebalance Actions|Rebalance Actions]]
- [[_COMMUNITY_Advance Tests|Advance Tests]]
- [[_COMMUNITY_Entry Point|Entry Point]]
- [[_COMMUNITY_Main Module (AST)|Main Module (AST)]]
- [[_COMMUNITY_OpenBB Screener Tests|OpenBB Screener Tests]]
- [[_COMMUNITY_Mock Prices Tests|Mock Prices Tests]]
- [[_COMMUNITY_Mock FX Rates Tests|Mock FX Rates Tests]]
- [[_COMMUNITY_Mock Screener Tests|Mock Screener Tests]]
- [[_COMMUNITY_OpenBB Prices Tests|OpenBB Prices Tests]]
- [[_COMMUNITY_OpenBB FX Rates Tests|OpenBB FX Rates Tests]]
- [[_COMMUNITY_Mock Prices Provider|Mock Prices Provider]]
- [[_COMMUNITY_Advance Action|Advance Action]]
- [[_COMMUNITY_OpenBB Prices Provider|OpenBB Prices Provider]]
- [[_COMMUNITY_Basic Strategy|Basic Strategy]]
- [[_COMMUNITY_Mock Strategy|Mock Strategy]]
- [[_COMMUNITY_Screen Stocks Action|Screen Stocks Action]]
- [[_COMMUNITY_OpenBB Display Balance|OpenBB Display Balance]]
- [[_COMMUNITY_Execute Transactions|Execute Transactions]]
- [[_COMMUNITY_Display Balance|Display Balance]]
- [[_COMMUNITY_Display Portfolio|Display Portfolio]]
- [[_COMMUNITY_Display Wallet|Display Wallet]]
- [[_COMMUNITY_OpenBB FX Rates Provider|OpenBB FX Rates Provider]]
- [[_COMMUNITY_Screener Return Type Tests|Screener Return Type Tests]]
- [[_COMMUNITY_Price Decimal Tests|Price Decimal Tests]]
- [[_COMMUNITY_FX Decimal Tests|FX Decimal Tests]]
- [[_COMMUNITY_Core Init|Core Init]]
- [[_COMMUNITY_Tests Init|Tests Init]]
- [[_COMMUNITY_Actions Init|Actions Init]]
- [[_COMMUNITY_Advance Month Test|Advance Month Test]]
- [[_COMMUNITY_Rebalance Weight Test|Rebalance Weight Test]]
- [[_COMMUNITY_Execute Sell Test|Execute Sell Test]]
- [[_COMMUNITY_Screen Stocks Return Test|Screen Stocks Return Test]]
- [[_COMMUNITY_Display Portfolio (AST)|Display Portfolio (AST)]]
- [[_COMMUNITY_Display Wallet (AST)|Display Wallet (AST)]]
- [[_COMMUNITY_Requirements|Requirements]]
- [[_COMMUNITY_Agents Config|Agents Config]]
- [[_COMMUNITY_Claude Config|Claude Config]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]

## God Nodes (most connected - your core abstractions)
1. `BacktestContext` - 33 edges
2. `Currency` - 23 edges
3. `BacktestContext` - 18 edges
4. `Wallet` - 17 edges
5. `Portfolio` - 16 edges
6. `File Structure` - 16 edges
7. `BacktestConfig` - 14 edges
8. `FakeContext` - 14 edges
9. `Ticker` - 12 edges
10. `Transaction` - 12 edges

## Surprising Connections (you probably didn't know these)
- `Decimal for Financial Precision` --rationale_for--> `mock_prices.get_price`  [INFERRED]
  docs/superpowers/specs/2026-04-16-backtest-engine-design.md → actions/mock_prices.py
- `Decimal for Financial Precision` --rationale_for--> `mock_fx_rates.get_fx_rate`  [INFERRED]
  docs/superpowers/specs/2026-04-16-backtest-engine-design.md → actions/mock_fx_rates.py
- `config/backtest.yaml` --references--> `screen_stocks (action)`  [INFERRED]
  config/backtest.yaml → actions/screen_stocks.py
- `Dual Provider Pattern (mock vs OpenBB)` --rationale_for--> `mock_screener.screen_stocks`  [INFERRED]
  README.md → actions/mock_screener.py
- `Dual Provider Pattern (mock vs OpenBB)` --rationale_for--> `openbb_fx_rates.get_fx_rate`  [INFERRED]
  README.md → actions/openbb_fx_rates.py

## Hyperedges (group relationships)
- **Core Domain Models** — models_currency, models_ticker, models_wallet, models_portfolio, models_transaction, models_backtestconfig [EXTRACTED 1.00]
- **BacktestContext Public API** — context_backtestcontext_advance, context_backtestcontext_execute_transactions, context_backtestcontext_display_wallet, context_backtestcontext_display_portfolio, context_backtestcontext_mock_screen_stocks, context_backtestcontext_mock_rebalance, context_backtestcontext_mock_display_balance, context_backtestcontext_openbb_screen_stocks, context_backtestcontext_openbb_rebalance, context_backtestcontext_openbb_display_balance [EXTRACTED 1.00]
- **Strategy Backtest Loop Pattern** — basic_run, mock_run, context_backtestcontext_advance, context_backtestcontext_execute_transactions [INFERRED 0.95]
- **Mock Data Provider Tests** — test_mock_screener_test_screen_stocks_returns_list, test_mock_prices_test_get_price_returns_decimal, test_mock_fx_rates_test_get_fx_rate_returns_decimal [INFERRED 0.85]
- **OpenBB Data Provider Tests** — test_openbb_screener_test_screen_stocks_returns_list, test_openbb_prices_test_get_price_returns_decimal, test_openbb_fx_rates_test_get_fx_rate_returns_decimal [INFERRED 0.85]
- **Mock Data Providers** — mock_prices_get_price, mock_fx_rates_get_fx_rate, mock_screener_screen_stocks [INFERRED 0.95]
- **OpenBB Data Providers** — openbb_prices_get_price, openbb_fx_rates_get_fx_rate, openbb_screener_screen_stocks [INFERRED 0.95]
- **Display Actions** — display_balance_display_balance, display_portfolio_display_portfolio, display_wallet_display_wallet [INFERRED 0.95]
- **Core Backtest Actions** — advance_advance, screen_stocks_screen_stocks, rebalance_rebalance, execute_transactions_execute_transactions [INFERRED 0.95]

## Communities (63 total, 23 thin omitted)

### Community 0 - "Advance & Config"
Cohesion: 0.1
Nodes (36): Diff-based equal-weight rebalancing using OpenBB prices and FX rates., rebalance(), Diff-based equal-weight rebalancing.      Computes total portfolio value, divide, rebalance(), BacktestConfig, Currency, Portfolio, Ticker (+28 more)

### Community 1 - "Core Models & Context"
Cohesion: 0.08
Nodes (35): advance.advance, advance._next_date, config/backtest.yaml, Decimal for Financial Precision, Diff-Based Equal-Weight Rebalancing, display_balance (mock variant), docs/draft.txt, Dual Provider Pattern (mock vs OpenBB) (+27 more)

### Community 2 - "Strategy & Context Interface"
Cohesion: 0.1
Nodes (34): basic.run, BacktestContext, BacktestContext.advance, BacktestContext.display_portfolio, BacktestContext.display_wallet, BacktestContext.execute_transactions, BacktestContext.mock_display_balance, BacktestContext.mock_rebalance (+26 more)

### Community 3 - "BacktestContext Methods"
Cohesion: 0.1
Nodes (16): BacktestContext, _make_config(), test_context_advance_delegates(), test_context_display_balance_delegates(), test_context_display_portfolio_delegates(), test_context_display_wallet_delegates(), test_context_initializes_empty_portfolio(), test_context_initializes_empty_transactions() (+8 more)

### Community 4 - "Rebalance Tests"
Cohesion: 0.07
Nodes (29): Actions, advance.py, Architecture, Backtest Engine — Design Spec, BacktestContext, code:python (@dataclass), code:yaml (start_date: "2025-01-01"), code:python (# strategies/basic.py) (+21 more)

### Community 5 - "Rebalance Actions"
Cohesion: 0.16
Nodes (14): FakeContext, _make_config(), Each transaction has correct price set., From 10000 cash, buy 2 tickers equally., Each ticker gets equal share of total value., Ticker no longer in target → sell all., Empty target list → sell all positions., Already holding correct amount → no transaction for that ticker. (+6 more)

### Community 6 - "Advance Tests"
Cohesion: 0.12
Nodes (15): Architecture, code:bash (python main.py -config=config/backtest.yaml -strategy=strate), code:yaml (start_date: "2022-01-01"), code:python (def run(ctx):), code:block4 (actions/        # one file per action; mock + OpenBB data pr), code:bash (pip install -r requirements.txt), code:bash (pytest tests/), Configuration (+7 more)

### Community 7 - "Entry Point"
Cohesion: 0.33
Nodes (11): FakeContext, _make_config(), Jan 31 + 1 month = Feb 28., If next date would be past end, return False without advancing., test_advance_day_interval(), test_advance_exact_end_date_returns_false(), test_advance_first_call_sets_start_date(), test_advance_month_end_clamping() (+3 more)

### Community 8 - "Main Module (AST)"
Cohesion: 0.15
Nodes (12): Agent Behaviors, Agent Configuration, Applied Learning, Code Style, code:bash (# Install dependencies), code:bash (python main.py -config=config/backtest.yaml -strategy=strate), Development Commands, Documentation (context7 MCP) (+4 more)

### Community 9 - "OpenBB Screener Tests"
Cohesion: 0.15
Nodes (12): Backtest Engine Implementation Plan, code:block1 (backtest/), code:python (from datetime import date), code:python (import re), code:bash (git add actions/advance.py tests/test_advance.py), code:python (from core.context import BacktestContext), code:bash (git add strategies/basic.py), code:bash (git add -A) (+4 more)

### Community 10 - "Mock Prices Tests"
Cohesion: 0.18
Nodes (12): load_config, load_strategy, main, parse_args, BacktestConfig, FakeContext (advance test), test_advance_first_call_sets_start_date, test_backtest_cli_end_to_end (+4 more)

### Community 11 - "Mock FX Rates Tests"
Cohesion: 0.29
Nodes (9): load_config(), load_strategy(), main(), parse_args(), Test via main.load_config + strategy load., test_backtest_cli_end_to_end(), test_load_config(), test_load_strategy() (+1 more)

### Community 15 - "OpenBB FX Rates Tests"
Cohesion: 0.25
Nodes (8): code:python (from datetime import date), code:python (def display_wallet(ctx) -> None:), code:python (from datetime import date), code:python (def display_portfolio(ctx) -> None:), code:python (from datetime import date), code:python (from decimal import Decimal), code:bash (git add actions/display_wallet.py actions/display_portfolio.), Task 6: Display Actions (Wallet, Portfolio, Balance)

### Community 16 - "Mock Prices Provider"
Cohesion: 0.48
Nodes (5): FakeContext, _make_config(), test_screen_stocks_deterministic(), test_screen_stocks_returns_list(), test_screen_stocks_uses_config_params()

### Community 20 - "Advance Action"
Cohesion: 0.38
Nodes (6): _date_variation(), get_price(), Deterministic base price from ticker symbol. Range: 20-500., Deterministic daily variation from ticker+date. Range: -0.20 to +0.20., Generate a deterministic mock price using seeded random walk.      Uses hash of, _ticker_base_price()

### Community 21 - "OpenBB Prices Provider"
Cohesion: 0.38
Nodes (6): _date_variation(), get_fx_rate(), _pair_base_rate(), Deterministic base rate for currency pair. Range: 0.5-2.0., Deterministic daily variation. Range: -0.05 to +0.05., Generate a deterministic mock FX rate.      Same currency returns 1. Otherwise u

### Community 22 - "Basic Strategy"
Cohesion: 0.53
Nodes (5): _apply_fundamental_filters(), _get_fundamentals(), # NOTE: obb.equity.screener does not support historical screening., _run_screener(), screen_stocks()

### Community 23 - "Mock Strategy"
Cohesion: 0.5
Nodes (4): Deterministic score for ticker on given date. Range: 0.0-1.0., Screen stocks from hardcoded universe based on date and params.      Each ticker, screen_stocks(), _ticker_score()

### Community 24 - "Screen Stocks Action"
Cohesion: 0.5
Nodes (4): advance(), _next_date(), Calculate next date based on interval string., Advance processing_date by interval. Return False if past end boundary.

### Community 25 - "OpenBB Display Balance"
Cohesion: 0.4
Nodes (5): code:block2 (PyYAML>=6.0), code:python (from datetime import date), code:python (from dataclasses import dataclass, field), code:bash (git add requirements.txt core/ tests/), Task 1: Project Setup & Data Models

### Community 26 - "Execute Transactions"
Cohesion: 0.4
Nodes (5): code:yaml (start_date: "2025-01-01"), code:python (import sys), code:python (import argparse), code:bash (git add main.py config/backtest.yaml tests/test_main.py), Task 11: YAML Config Loading & main.py

### Community 27 - "Display Balance"
Cohesion: 0.67
Nodes (3): get_price(), Fetch full price history for a ticker and populate cache., _warm_ticker()

### Community 28 - "Display Portfolio"
Cohesion: 0.5
Nodes (4): code:python (from datetime import date), code:python (import hashlib), code:bash (git add actions/ tests/test_mock_prices.py), Task 2: Mock Prices Provider

### Community 29 - "Display Wallet"
Cohesion: 0.5
Nodes (4): code:python (import hashlib), code:bash (git add actions/mock_fx_rates.py tests/test_mock_fx_rates.py), code:python (from datetime import date), Task 3: Mock FX Rates Provider

### Community 30 - "OpenBB FX Rates Provider"
Cohesion: 0.5
Nodes (4): code:python (from datetime import date), code:python (import hashlib), code:bash (git add actions/mock_screener.py tests/test_mock_screener.py), Task 4: Mock Screener Provider

### Community 31 - "Screener Return Type Tests"
Cohesion: 0.5
Nodes (4): code:python (from datetime import date), code:python (from decimal import Decimal), code:bash (git add actions/execute_transactions.py tests/test_execute_t), Task 9: Execute Transactions Action

### Community 32 - "Price Decimal Tests"
Cohesion: 0.5
Nodes (4): code:python (from datetime import date), code:python (from actions.mock_screener import screen_stocks as mock_scre), code:bash (git add actions/screen_stocks.py tests/test_screen_stocks.py), Task 7: Screen Stocks Action

### Community 33 - "FX Decimal Tests"
Cohesion: 0.5
Nodes (4): code:python (from datetime import date), code:python (from decimal import Decimal), code:bash (git add core/context.py tests/test_context.py), Task 10: BacktestContext

### Community 34 - "Core Init"
Cohesion: 0.5
Nodes (4): code:python (from datetime import date), code:python (from decimal import Decimal), code:bash (git add actions/rebalance.py tests/test_rebalance.py), Task 8: Rebalance Action

### Community 45 - "Claude Config"
Cohesion: 0.67
Nodes (3): code:python (from datetime import date), code:bash (git add tests/test_integration.py), Task 13: Integration Test

## Knowledge Gaps
- **157 isolated node(s):** `Basic equal-weight strategy using live OpenBB data (yfinance/FMP).`, `Basic equal-weight strategy using mock (deterministic) data.`, `From 10000 cash, buy 2 tickers equally.`, `Each ticker gets equal share of total value.`, `Ticker no longer in target → sell all.` (+152 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BacktestContext` connect `BacktestContext Methods` to `Advance & Config`, `Mock FX Rates Tests`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `BacktestConfig` connect `Advance & Config` to `BacktestContext Methods`, `Rebalance Actions`, `Entry Point`, `Mock FX Rates Tests`, `Mock Prices Provider`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `FakeContext` connect `Rebalance Actions` to `Advance & Config`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `BacktestContext` (e.g. with `BacktestConfig` and `Currency`) actually correct?**
  _`BacktestContext` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `Currency` (e.g. with `BacktestContext` and `FakeContext`) actually correct?**
  _`Currency` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `Wallet` (e.g. with `BacktestContext` and `FakeContext`) actually correct?**
  _`Wallet` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `Portfolio` (e.g. with `BacktestContext` and `FakeContext`) actually correct?**
  _`Portfolio` has 15 INFERRED edges - model-reasoned connections that need verification._
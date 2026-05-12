# Graph Report - .  (2026-05-12)

## Corpus Check
- Corpus is ~12,153 words - fits in a single context window. You may not need a graph.

## Summary
- 332 nodes · 485 edges · 46 communities (27 shown, 19 thin omitted)
- Extraction: 70% EXTRACTED · 30% INFERRED · 0% AMBIGUOUS · INFERRED: 144 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

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
- [[_COMMUNITY_Mock Prices Tests|Mock Prices Tests]]
- [[_COMMUNITY_Mock FX Rates Tests|Mock FX Rates Tests]]
- [[_COMMUNITY_Screen Stocks Tests|Screen Stocks Tests]]
- [[_COMMUNITY_Mock Prices Provider|Mock Prices Provider]]
- [[_COMMUNITY_Mock FX Rates Provider|Mock FX Rates Provider]]
- [[_COMMUNITY_OpenBB Screener Provider|OpenBB Screener Provider]]
- [[_COMMUNITY_Mock Screener Provider|Mock Screener Provider]]
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
- [[_COMMUNITY_Screener Return Type Tests|Screener Return Type Tests]]
- [[_COMMUNITY_Price Decimal Tests|Price Decimal Tests]]
- [[_COMMUNITY_FX Decimal Tests|FX Decimal Tests]]
- [[_COMMUNITY_Advance Month Test|Advance Month Test]]
- [[_COMMUNITY_Rebalance Weight Test|Rebalance Weight Test]]
- [[_COMMUNITY_Execute Sell Test|Execute Sell Test]]
- [[_COMMUNITY_Screen Stocks Return Test|Screen Stocks Return Test]]
- [[_COMMUNITY_Display Portfolio (AST)|Display Portfolio (AST)]]
- [[_COMMUNITY_Display Wallet (AST)|Display Wallet (AST)]]

## God Nodes (most connected - your core abstractions)
1. `BacktestContext` - 30 edges
2. `Currency` - 23 edges
3. `BacktestContext` - 18 edges
4. `Wallet` - 17 edges
5. `Portfolio` - 16 edges
6. `BacktestConfig` - 14 edges
7. `FakeContext` - 14 edges
8. `Ticker` - 12 edges
9. `Transaction` - 12 edges
10. `FakeContext` - 12 edges

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

## Communities (46 total, 19 thin omitted)

### Community 0 - "Advance & Config"
Cohesion: 0.08
Nodes (35): advance.advance, advance._next_date, config/backtest.yaml, Decimal for Financial Precision, Diff-Based Equal-Weight Rebalancing, display_balance (mock variant), docs/draft.txt, Dual Provider Pattern (mock vs OpenBB) (+27 more)

### Community 1 - "Core Models & Context"
Cohesion: 0.14
Nodes (25): BacktestConfig, Currency, Portfolio, Ticker, Wallet, FakeContext, _make_config(), test_display_balance_cash_only() (+17 more)

### Community 2 - "Strategy & Context Interface"
Cohesion: 0.1
Nodes (34): basic.run, BacktestContext, BacktestContext.advance, BacktestContext.display_portfolio, BacktestContext.display_wallet, BacktestContext.execute_transactions, BacktestContext.mock_display_balance, BacktestContext.mock_rebalance (+26 more)

### Community 3 - "BacktestContext Methods"
Cohesion: 0.12
Nodes (16): BacktestContext, _make_config(), test_context_advance_delegates(), test_context_display_balance_delegates(), test_context_display_portfolio_delegates(), test_context_display_wallet_delegates(), test_context_initializes_empty_portfolio(), test_context_initializes_empty_transactions() (+8 more)

### Community 4 - "Rebalance Tests"
Cohesion: 0.16
Nodes (14): FakeContext, _make_config(), Each transaction has correct price set., From 10000 cash, buy 2 tickers equally., Each ticker gets equal share of total value., Ticker no longer in target → sell all., Empty target list → sell all positions., Already holding correct amount → no transaction for that ticker. (+6 more)

### Community 5 - "Rebalance Actions"
Cohesion: 0.25
Nodes (11): Diff-based equal-weight rebalancing using OpenBB prices and FX rates., rebalance(), Diff-based equal-weight rebalancing.      Computes total portfolio value, divide, rebalance(), Transaction, FakeContext, test_execute_appends_to_all_transactions(), test_execute_buy_updates_wallet_and_portfolio() (+3 more)

### Community 6 - "Advance Tests"
Cohesion: 0.33
Nodes (11): FakeContext, _make_config(), Jan 31 + 1 month = Feb 28., If next date would be past end, return False without advancing., test_advance_day_interval(), test_advance_exact_end_date_returns_false(), test_advance_first_call_sets_start_date(), test_advance_month_end_clamping() (+3 more)

### Community 7 - "Entry Point"
Cohesion: 0.18
Nodes (12): load_config, load_strategy, main, parse_args, BacktestConfig, FakeContext (advance test), test_advance_first_call_sets_start_date, test_backtest_cli_end_to_end (+4 more)

### Community 8 - "Main Module (AST)"
Cohesion: 0.29
Nodes (9): load_config(), load_strategy(), main(), parse_args(), Test via main.load_config + strategy load., test_backtest_cli_end_to_end(), test_load_config(), test_load_strategy() (+1 more)

### Community 12 - "Screen Stocks Tests"
Cohesion: 0.48
Nodes (5): FakeContext, _make_config(), test_screen_stocks_deterministic(), test_screen_stocks_returns_list(), test_screen_stocks_uses_config_params()

### Community 16 - "Mock Prices Provider"
Cohesion: 0.38
Nodes (6): _date_variation(), get_price(), Deterministic base price from ticker symbol. Range: 20-500., Deterministic daily variation from ticker+date. Range: -0.20 to +0.20., Generate a deterministic mock price using seeded random walk.      Uses hash of, _ticker_base_price()

### Community 17 - "Mock FX Rates Provider"
Cohesion: 0.38
Nodes (6): _date_variation(), get_fx_rate(), _pair_base_rate(), Deterministic base rate for currency pair. Range: 0.5-2.0., Deterministic daily variation. Range: -0.05 to +0.05., Generate a deterministic mock FX rate.      Same currency returns 1. Otherwise u

### Community 18 - "OpenBB Screener Provider"
Cohesion: 0.53
Nodes (5): _apply_fundamental_filters(), _get_fundamentals(), # NOTE: obb.equity.screener does not support historical screening., _run_screener(), screen_stocks()

### Community 19 - "Mock Screener Provider"
Cohesion: 0.5
Nodes (4): Deterministic score for ticker on given date. Range: 0.0-1.0., Screen stocks from hardcoded universe based on date and params.      Each ticker, screen_stocks(), _ticker_score()

### Community 20 - "Advance Action"
Cohesion: 0.5
Nodes (4): advance(), _next_date(), Calculate next date based on interval string., Advance processing_date by interval. Return False if past end boundary.

### Community 21 - "OpenBB Prices Provider"
Cohesion: 0.67
Nodes (3): get_price(), Fetch full price history for a ticker and populate cache., _warm_ticker()

## Knowledge Gaps
- **74 isolated node(s):** `Basic equal-weight strategy using live OpenBB data (yfinance/FMP).`, `Basic equal-weight strategy using mock (deterministic) data.`, `From 10000 cash, buy 2 tickers equally.`, `Each ticker gets equal share of total value.`, `Ticker no longer in target → sell all.` (+69 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BacktestContext` connect `BacktestContext Methods` to `Main Module (AST)`, `Core Models & Context`, `Rebalance Actions`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Why does `BacktestConfig` connect `Core Models & Context` to `BacktestContext Methods`, `Rebalance Tests`, `Advance Tests`, `Main Module (AST)`, `Screen Stocks Tests`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `FakeContext` connect `Rebalance Tests` to `Core Models & Context`, `Rebalance Actions`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `BacktestContext` (e.g. with `BacktestConfig` and `Currency`) actually correct?**
  _`BacktestContext` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `Currency` (e.g. with `BacktestContext` and `FakeContext`) actually correct?**
  _`Currency` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `Wallet` (e.g. with `BacktestContext` and `FakeContext`) actually correct?**
  _`Wallet` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `Portfolio` (e.g. with `BacktestContext` and `FakeContext`) actually correct?**
  _`Portfolio` has 15 INFERRED edges - model-reasoned connections that need verification._
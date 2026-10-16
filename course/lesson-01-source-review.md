# Lesson 1 source review and LEAN trace

Review date: 5 October 2026. Selected sources were inspected; upstream engines and research results were not replicated. Implementations below informed concepts and tests rather than copied code. Quant Lab's source is original.

## A complete framework path in LEAN

Pinned LEAN revision: `705b9551be1aaa821c7f77896a7eb8fcd07b92ee`.

1. [Regression setup](https://github.com/QuantConnect/Lean/blob/705b9551be1aaa821c7f77896a7eb8fcd07b92ee/Algorithm.Python/BaseFrameworkRegressionAlgorithm.py) configures hourly raw-price data and a changing equity universe. It chooses equal-weight portfolio construction, immediate execution and **NullRiskManagementModel**. The absence of active risk adjustment is important; do not infer protective stops from the framework's existence.
2. [EMA regression algorithm](https://github.com/QuantConnect/Lean/blob/705b9551be1aaa821c7f77896a7eb8fcd07b92ee/Algorithm.Python/EmaCrossAlphaModelFrameworkRegressionAlgorithm.py) replaces the setup's constant alpha with an EMA crossover alpha.
3. [EMA alpha](https://github.com/QuantConnect/Lean/blob/705b9551be1aaa821c7f77896a7eb8fcd07b92ee/Algorithm.Framework/Alphas/EmaCrossAlphaModel.py) uses separate fast/slow indicators, explicit warm-up and readiness. It produces directional insights on crossings, not repeated orders every observation. Removed symbols clean up consolidators. [Tests](https://github.com/QuantConnect/Lean/blob/705b9551be1aaa821c7f77896a7eb8fcd07b92ee/Tests/Algorithm/Framework/Alphas/EmaCrossAlphaModelTests.cs) verify warm-up and expected insight directions for Python and C# models.
4. [Equal weighting](https://github.com/QuantConnect/Lean/blob/705b9551be1aaa821c7f77896a7eb8fcd07b92ee/Algorithm.Framework/Portfolio/EqualWeightingPortfolioConstructionModel.py) maps active insights into signed target percentages respecting portfolio bias. A predictive insight and an allocation are different objects.
5. [Immediate execution](https://github.com/QuantConnect/Lean/blob/705b9551be1aaa821c7f77896a7eb8fcd07b92ee/Algorithm/Execution/ImmediateExecutionModel.py) tracks targets, computes unordered quantity and checks minimum order margins before submitting market orders. Submitting an order is not proof of a fill at the signal price.
6. [Equity fills](https://github.com/QuantConnect/Lean/blob/705b9551be1aaa821c7f77896a7eb8fcd07b92ee/Common/Orders/Fills/EquityFillModel.cs) apply side-dependent prices and slippage, session checks and stale-price policies. The inspected market/stop sections also handle gaps beyond stops; OHLC does not resolve every intrabar ordering question. These are distinct from this lab's simplified next-open fill assumption. [Constant fees](https://github.com/QuantConnect/Lean/blob/705b9551be1aaa821c7f77896a7eb8fcd07b92ee/Common/Orders/Fees/ConstantFeeModel.cs) demonstrate a separate fee boundary, not the lab's basis-point cost model.
7. [Execution tests](https://github.com/QuantConnect/Lean/blob/705b9551be1aaa821c7f77896a7eb8fcd07b92ee/Tests/Algorithm/Framework/Execution/ImmediateExecutionModelTests.cs) cover absent targets, outstanding orders, partially filled quantities and lot-size handling. Their lesson is to reconcile intended and already ordered exposure. They were read, not executed here.

The lab's rule is intentionally simpler and different: a completed close relative to a three-close simple mean, long-only stock or cash, without universes, directional insights or an EMA implementation. It teaches causality and a readable ledger. It is not a port of LEAN's EMA strategy or a reproduction of its regression results.

## Required benchmark comparison

The earlier selected review covered all five repository benchmarks required by AGENTS.md, plus QuantStats for risk calculations. Source revisions and paths are recorded in [the source catalogue](research/source-manifest.json).

| Reference | Retained principle | Small Lesson 1 decision |
|---|---|---|
| LEAN TradeBar and framework models | Interval semantics, readiness and separate responsibilities | End-labelled bars; explicit warm-up; signal/target/fill/equity trail |
| NautilusTrader bar-execution documentation | OHLC paths require assumptions | Explain ambiguity; avoid intrabar stop claims |
| Zipline slippage implementation | Execution is distinct from a signal | State adverse fills and limitations |
| VectorBT walk-forward notebook | Training choices and evaluation periods differ | No optimized winner or holdout claim for the fixture |
| backtesting.py engine | Order timing and costs must be explicit | Declare the simplified open-fill assumption |
| QuantStats statistics | Metric frequency and missing-data choices matter | Undefined first return; no annualized statistic from twelve bars |

Quant Lab defers exchange calendars, real providers, a general execution engine and full research validation to their existing roadmap lessons. The generated offline contract is the smallest useful boundary for this slice, not a new backend architecture.

## Academic and teaching evidence

The [Deflated Sharpe Ratio paper](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf) motivates recording the search history. The lesson does not calculate DSR or imply that a holdout alone solves repeated selection.

The [QuantInsti 2023 workshop](https://www.youtube.com/watch?v=u3aJCJSunWA) was examined through selected auto-caption sections, not a complete visual/code audit. Its demonstration explicitly sets costs and slippage to zero around 55:37. The lesson therefore displays a cost comparison and labels the fixture's limits rather than treating a tutorial curve as evidence of profitability. Promotional material is excluded.

The wider [GitHub review](research/github-review.md) and [academic evidence map](research/academic-evidence.md) contain useful portfolio and ML ideas for later lessons. The catalogue now records 54 selected files across 28 repositories, including nine additional LEAN trace sources. Counts describe inspected sources, not complete repository audits. The academic map records inspection depth per source; full paper reviews and replication remain pending where stated.

Covariance shrinkage, cost-aware optimization, multiple testing, attribution and stressed strategy correlations should be introduced only with their prerequisites and reproducible experiments. More advanced algorithms do not remove data timing or evaluation obligations.

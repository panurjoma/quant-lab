# Quant Lab Roadmap

The roadmap deliberately interleaves **financial theory, statistics and software construction**. Each phase leaves the repository more capable than before.

## Phase 0 — Foundation

### Bootstrap
Define vision, architecture, AI-agent guardrails and the lesson workflow.

### Lesson 1 — Market Data, Returns & Research Environment
**Learn:** instruments, exchanges, OHLCV bars, timeframes, adjusted prices, simple returns, log returns, missing data and time-series ordering.

**Build:** Python package scaffold, test environment, OHLCV/data contracts, return functions, provider abstraction and first research notebook.

**Exit criterion:** ingest a small historical dataset, validate it, calculate returns correctly and explain every column/transformation.

## Phase 1 — Signals from price

### Lesson 2 — Moving averages and features
Rolling windows, SMA/EMA, lagging, normalization and feature timing.

### Lesson 3 — Momentum
Absolute/time-series momentum, relative momentum and cross-sectional ranking.

### Lesson 4 — Breakouts
Ranges, rolling highs/lows, trend-following intuition and false breakouts.

### Lesson 5 — Mean reversion
Equilibrium assumptions, deviations from rolling baselines and why falling prices are not automatically bargains.

### Lesson 6 — Bollinger Bands, RSI and Z-scores
Volatility-scaled deviation, oscillator interpretation and combined-signal experiments.

**Phase output:** a common Strategy/Signal interface and several intentionally simple baseline strategies.

## Phase 2 — Relative value and statistical trading

### Lesson 7 — Pairs trading
Spreads, hedge ratios and market-relative hypotheses.

### Lesson 8 — Cointegration
Stationarity vs correlation, ADF-style testing, residual behavior and half-life intuition.

### Lesson 9 — Statistical arbitrage
Multi-asset relative value, PCA/factor residuals, clustering and Ornstein-Uhlenbeck-style mean reversion.

**Phase output:** statistical tests and relative-value strategy components with explicit assumptions.

## Phase 3 — Cross-sectional factors and portfolios

### Lesson 10 — Factors
Momentum, value, quality, size and volatility; ranking and portfolio formation.

### Lesson 11 — Portfolio construction
Weights, diversification, covariance, constraints and optimization.

### Lesson 12 — Risk management
Exposure, drawdown, volatility targeting, position sizing, concentration and risk budgets.

**Phase output:** signals become portfolios rather than isolated trades.

## Phase 4 — Honest experimentation

### Lesson 13 — Backtesting correctly
Event timing, fills, fees, spreads, slippage, survivorship bias, corporate actions and benchmark selection.

### Lesson 14 — Overfitting and multiple testing
Parameter searches, selection bias, data snooping and why the best historical strategy is suspicious.

### Lesson 15 — Walk-forward validation
Train/validation/test splits for time series, rolling/expanding windows and out-of-sample evaluation.

**Phase output:** a repeatable experiment protocol and comparable performance/risk reports.

## Phase 5 — Adaptive systems

### Lesson 16 — Regime detection
Trend/mean-reversion, volatility and risk-off regimes; rules, clustering/HMM-like approaches as appropriate.

### Lesson 17 — Machine learning
Define targets without leakage, feature pipelines, baseline models and probabilistic outputs.

### Lesson 18 — Strategy selection
Meta-models that choose/weight strategies based on observable state rather than asking an LLM to predict prices.

**Phase output:** adaptive allocation between validated strategies.

## Phase 6 — Execution

### Lesson 19 — Broker APIs
Orders, positions, account state, idempotency and broker abstraction. Compare development/paper environments and design the IBKR adapter.

### Lesson 20 — Paper trading
Connect the research system to simulated execution and reconcile expected vs observed fills/positions.

### Lesson 21 — Live execution and operations
Operational safeguards, reconciliation, retries, kill switches, observability and controlled deployment.

**Phase output:** the same strategy interfaces can move from backtest to paper/live without embedding broker logic.

## Phase 7 — Product and AI layer

### Lesson 22 — Multi-strategy orchestration and UI
Expose the system through Python APIs and a TypeScript/React interface. Add experiment inspection, portfolio/risk views and operational monitoring.

Evaluate AI for bounded tasks such as research synthesis, diagnostics, natural-language querying and strategy-selection support. Deterministic/statistical components remain deterministic/statistical when that is the right tool.

## Definition of done for a strategy

A strategy is not “done” until we can state:
- the economic/statistical hypothesis;
- exact information available at decision time;
- entry, exit and sizing rules;
- transaction-cost assumptions;
- risk constraints;
- in-sample vs out-of-sample procedure;
- benchmark;
- failure modes and invalidation conditions;
- reproducible experiment configuration.

## Delivery cadence

Prefer one focused issue and PR per lesson/milestone. Large lessons can be split into theory/research and infrastructure increments, but the Git history should preserve *why* each capability was added.

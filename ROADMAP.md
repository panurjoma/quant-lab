# Quant Lab — Prerequisite-Driven Roadmap

This roadmap is ordered for **learning**, not feature marketing. Each stage introduces only concepts needed by the next one, and every strategy is treated as a falsifiable hypothesis rather than an indicator recipe.

## Stage 0 — Bootstrap: understand the system we are building

### Lesson 0 — Systematic trading mental model
Markets, instruments, exchanges, orders, positions, P&L; discretionary vs systematic trading; signal vs portfolio vs execution; research/backtest/paper/live environments.

**Build:** repository conventions and architecture.  
**Product:** Learn tab skeleton/content model.

## Stage 1 — Data and measurement

### Lesson 1 — Market data, returns and research environment
OHLCV, bid/ask concept, bars/ticks, timeframes, timestamps/timezones, adjusted prices, missing/duplicate data, simple vs log returns. Introduce canonical instrument identity and explicit time semantics so vendor symbols and wall-clock assumptions do not leak into research.

**Build:** Python package, tests, canonical bar/data contracts, return functions, capability-based provider interfaces designed for the two v1 connectors (IBKR and QuantConnect), and Jupyter research environment.  
**Product:** Learn lesson page + first historical chart.

### Lesson 2 — Descriptive statistics and performance
Mean/variance/std, distributions, compounding, covariance/correlation, volatility, drawdown, CAGR, Sharpe/Sortino intuition, benchmark and risk-free-rate concepts.

**Build:** reusable metrics module and tests.  
**Why now:** we need a language for evaluating every later strategy.

### Lesson 3 — Backtesting mechanics before strategies
Information sets, lagging, event/order timing, fills, fees, bid/ask spread, slippage, turnover, warm-up, survivorship/corporate-action concepts. Establish the principle that the **same strategy contract and clock/event semantics should survive backtest → replay → paper → live**, while execution adapters change.

**Build:** deliberately small baseline backtest/event contract; benchmark buy-and-hold experiment; deterministic synthetic fixtures that require no external data.  
**Exit:** explain why a backtest can be wrong even when code is correct.

## Stage 2 — First strategy families

### Lesson 4 — Rolling windows, moving averages and trend
SMA/EMA, rolling calculations, lagging, normalization; trend as a hypothesis rather than a chart pattern.

**Build:** feature interface + MA crossover baseline.

### Lesson 5 — Momentum
Time-series/absolute momentum, relative momentum, cross-sectional ranking; horizons and turnover.

**Evidence anchor:** Moskowitz–Ooi–Pedersen and classic momentum literature.  
**Build:** first reusable Strategy/Signal contract and momentum experiment.

### Lesson 6 — Breakouts and trend following
Rolling highs/lows, breakout rules, false breakouts, volatility scaling and relation to momentum.

**Build:** breakout strategy under the same interface.

### Lesson 7 — Mean reversion
Equilibrium assumptions, deviations from rolling baselines, Z-score and half-life intuition; why a falling asset is not automatically cheap.

**Build:** simple Z-score mean-reversion strategy.

### Lesson 8 — RSI and Bollinger Bands as features, not magic rules
Derive/understand RSI and volatility bands; compare redundant/correlated features; test incremental information rather than stack indicators.

**Build:** controlled feature-ablation experiment.

**Stage checkpoint:** compare trend/momentum vs mean-reversion under identical metrics/cost assumptions and identify market conditions where each fails.

## Stage 3 — Time-series statistics and relative value

### Lesson 9 — Stationarity, autocorrelation and regression
Stationarity intuition, ACF, linear regression, residuals, hypothesis tests and multiple-comparison caution.

### Lesson 10 — Pairs trading
Relative-value hypothesis, normalized-distance pairing, spread construction, hedge ratio and market-neutral intuition.

**Evidence anchor:** Gatev–Goetzmann–Rouwenhorst.

### Lesson 11 — Cointegration
Correlation vs cointegration, unit roots/ADF intuition, Engle-Granger workflow, residual stationarity and dynamic breakdown.

**Build:** pairs selection/validation pipeline with formation vs trading periods.

## Stage 4 — Assets, factors and portfolios

### Lesson 12 — Cross-sectional factors
Momentum, value, size, quality/profitability, investment and low-volatility concepts; ranks, quantiles and factor exposure.

**Evidence anchors:** Fama/French and momentum literature.

### Lesson 13 — Portfolio construction
Weights, long/short vs long-only, diversification, covariance, constraints, rebalancing and turnover.

### Lesson 14 — Risk management and sizing
Volatility targeting, concentration, exposure, drawdown, position sizing, risk budgets and leverage/margin concepts. Add **tail-risk measures** (VaR/CVaR/Expected Shortfall intuition) and **Monte Carlo/bootstrap stress analysis** as risk tools, not return-prediction tools.

**Build:** portfolio + risk layers between strategies and execution.

## Stage 5 — Research that survives contact with reality

### Lesson 15 — Transaction costs and execution realism
Commission, spread, slippage, liquidity/market impact intuition, order types and fill assumptions.

### Lesson 16 — Biases and overfitting
Look-ahead, survivorship, selection/data-snooping bias, repeated backtests, parameter proliferation and multiple testing.

**Evidence anchor:** Probability of Backtest Overfitting; Deflated Sharpe Ratio.

### Lesson 17 — Out-of-sample, walk-forward and parameter robustness
Chronological train/validation/test, expanding/rolling windows, sensitivity/stability, robustness across assets/timeframes. Visualize parameter surfaces/heatmaps and prefer broad stable regions over isolated historical optima; optimization is a research tool, never proof of edge.

### Lesson 18 — Experiment registry, tear sheets and strategy promotion
Introduce experiment IDs/manifests capturing Git/code version, strategy/config version, data identity/range, universe, costs, split, metrics and artifacts. Produce a standard **strategy tear sheet** with benchmark comparison, equity curve, drawdowns, rolling risk/return, exposure, turnover, costs and trade/period diagnostics. Define promotion gates from idea → researched → validated → paper candidate.

**Stage checkpoint:** no strategy can become a paper bot without passing documented validation and risk gates.

## Stage 6 — Advanced statistical strategies

### Lesson 19 — PCA, factors and statistical arbitrage
PCA as common-factor extraction, residual/idiosyncratic returns, mean-reverting residual models and market neutrality.

**Evidence anchor:** Avellaneda–Lee.

### Lesson 20 — Clustering and universe construction
Similarity metrics, clustering, universe stability and how discovery itself can overfit.

### Lesson 21 — Stochastic mean reversion
Ornstein–Uhlenbeck intuition, parameter estimation, half-life and model misspecification.

## Stage 7 — Adaptive/ML systems

### Lesson 22 — Regime detection
Trend/mean-reversion, volatility and risk-off states; rule-based baseline first, then clustering/HMM-like approaches where justified.

### Lesson 23 — ML foundations for trading
Targets/labels, feature timing, leakage, class imbalance, probabilistic predictions, calibration and time-aware validation. Compare every ML model to simple baselines.

### Lesson 24 — Strategy selection / meta-models
Use observable state to allocate among already validated strategies. LLMs do not directly decide prices/orders.

## Stage 8 — Real-time observation and execution engineering

### Lesson 25 — Real-time market data
Streaming/subscriptions, stale data, reconnects, clocks, state and persistence. Introduce **data lineage and quality telemetry**: source, ingestion time, event time, freshness, gaps, duplicates and normalization/corporate-action policy. Use the supported capabilities of the two v1 connectors only: IBKR and QuantConnect. Normalize vendor data before it reaches the domain.

**Product:** Market tab becomes real-time/read-only where the configured connector/data entitlement supports real-time delivery.

### Lesson 26 — Broker abstraction and order lifecycle
Orders, IDs, partial fills, cancellations, positions, account state, reconciliation, retries/idempotency. Cover practical order semantics needed for realistic simulation/execution: market/limit/stop, time-in-force, rejection/cancel states and deterministic fill-model contracts.

### Lesson 27 — External platform integrations
**IBKR:** TWS/IB Gateway concepts, API session management, market/account data, order lifecycle and paper/live separation.  
**QuantConnect:** research/data/backtest integration behind capability-specific interfaces.  

**Build:** IBKR market/account + broker adapters and the QuantConnect research/data adapter. IBKR remains the only execution broker for v1.

## Stage 9 — Paper trading

### Lesson 28 — Paper bot runtime
Run independently configured strategy bots; formalize StrategyDefinition → StrategyVersion → BotConfiguration → BotInstance → Run identity; scheduler/event loop; clock abstraction; health/status; persisted state.

### Lesson 29 — Attribution, persistence and monitoring
P&L per bot/strategy/run, per asset and total; realized/unrealized P&L; orders/fills; equity curves; persistence boundaries; structured health/telemetry and reconciliation diagnostics.

**Product:** Paper Trading + Strategies/Control tabs.

### Lesson 30 — Operational safety and audit
Per-bot activate/deactivate, graceful stop, cancel-open-orders policy, exposure checks, audited lifecycle commands and a global kill switch independent of strategy/LLM logic.

**Exit:** extended paper-trading observation and reconciliation before any live promotion.

## Stage 10 — Live observation and controlled deployment

### Lesson 31 — Live read-only observation
Connect live account state without enabling autonomous live orders.

**Product:** Live Trading tab initially observation-only.

### Lesson 32 — Controlled live execution
Only after explicit user decision: credentials/secrets, deployment isolation, pre-trade risk, confirmations where appropriate, alerts, audit log, recovery and kill switches.

No strategy reaches live because it “won” a backtest. Promotion is a separate governed decision.

## Stage 11 — Product maturity and AI assistance

### Lesson 33 — Multi-strategy orchestration
Capital allocation among bots, aggregate risk, correlated strategies, conflicts and portfolio-level constraints.

### Lesson 34 — AI-assisted research and tutoring
AI tutor in Learn; paper/reference synthesis; experiment explanation; anomaly diagnostics. Keep deterministic risk/execution controls outside LLM authority.

### Lesson 35 — Production hardening
Observability, deployment, migrations, security, disaster recovery, data retention and reproducibility. Add **CI quality gates**, coverage for critical quantitative logic, dependency/security checks, environment/container reproducibility, performance benchmarks for hot paths and documented recovery/runbooks.

---

## Strategy definition of done

A strategy must document:
- economic/statistical hypothesis and evidence;
- universe and data requirements;
- exact decision-time information;
- signal, entry/exit and sizing rules;
- benchmark;
- cost/slippage assumptions;
- risk constraints;
- research trials/parameters;
- in-sample/out-of-sample protocol;
- robustness/sensitivity;
- failure/invalidation conditions;
- version and reproducible configuration;
- paper/live eligibility status.

## Product delivery / unlocking order

Tabs are unlocked by course capabilities rather than all being built upfront:

1. **Learn** — unlocked first and grows every lesson.
2. **Market** — historical observation unlocks with the data layer; real-time unlocks in Stage 8; always read-only.
3. **Strategies / Control** — strategy catalogue unlocks as strategies are learned; bot controls remain locked until runtimes exist.
4. **Paper Trading** — unlocks only after execution foundations and IBKR paper integration.
5. **Live Trading** — unlocks only after paper validation; read-only first; execution is the final gated capability.

V1 external financial-platform connectors are **IBKR + QuantConnect only**. Additional providers are intentionally out of scope until there is a demonstrated need.

This order deliberately makes understanding and measurement prerequisites for automation.


## LEAN integration track across the roadmap

LEAN is introduced incrementally rather than deferred to the final integration lesson:

- **Lessons 1–3:** trace bars, subscriptions, time, returns, fills, fees, slippage, portfolio accounting and statistics; retain the small Python simulator as a hand-checkable oracle.
- **Lessons 4–14:** express strategies through LEAN's Algorithm Framework where its separation fits: Universe -> Alpha -> Portfolio Construction -> Risk -> Execution. Use classic/hybrid algorithms when the finance logic cannot be separated honestly.
- **Lessons 15–18:** run reproducible LEAN experiments and normalize orders, fills, equity, drawdown, costs and statistics into the Quant Lab experiment contract.
- **Lessons 25–30:** add the supervised LEAN runtime adapter, IBKR paper integration, reconciliation, monitoring and kill controls.
- **Live stages:** reuse the validated strategy/run contract; live remains disabled by default and requires an explicit promotion decision.

The immutable initial upstream snapshot is `80e7843f645673bcbeaab963049f76f20f6785e1` (2026-10-06). A pin update is a dedicated reviewed change with contract tests and migration notes.

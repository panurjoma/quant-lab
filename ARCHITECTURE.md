# Quant Lab Architecture

## Goals

Quant Lab separates education/research, market observation and automated execution. It deliberately limits v1 integration complexity to **two external financial-platform connectors: Interactive Brokers and QuantConnect**.

The architecture below is a **target map, not a request to scaffold everything immediately**. Boundaries are introduced only when a lesson creates a real requirement.

## Progressive UI

```text
Stage 1+          later                 execution stage        final gated stage
 Learn  ------>  Market  ---------->  Paper + Control  ----->  Live
(always grows)   (read-only)           (IBKR paper)            (read-only first)
```

The five conceptual tabs are Learn, Market, Paper Trading, Live Trading and Strategies/Control. Locked means the underlying capability is not yet supported rather than showing a misleading empty/unsafe control.

## Exactly two v1 connectors

### Interactive Brokers
IBKR provides market/account-data capabilities where supported and is the **only v1 execution broker**. Paper and live use separate runtime configuration/connections. Vendor objects cannot leak into strategy/domain interfaces.

### QuantConnect
QuantConnect is a **research/data/backtesting integration**, not the v1 execution broker. It is used for historical/research data and comparative research/backtest workflows.

### Capability-specific ports

Do not force both platforms into one oversized interface. Prefer ports such as:

```text
HistoricalDataProvider
SnapshotDataProvider
StreamingDataProvider
ResearchBacktestProvider
AccountProvider
ExecutionBroker
```

Adapters implement only capabilities they genuinely support. All external data is normalized before reaching the domain.

## User interface

```text
+-------------------------------------------------------------------+
| Learn | Market | Paper Trading | Live Trading | Strategies/Control |
+-------------------------------+-----------------------------------+
                                |
                           TypeScript/React
                                |
                         Application/API
                                |
                              Python
```

- **Learn:** course, examples, experiments, references and AI tutoring.
- **Market:** read-only historical/real-time observation; no order commands.
- **Paper:** IBKR paper account, positions, orders/fills and attribution.
- **Live:** separate live view; initially read-only.
- **Strategies/Control:** strategy catalogue and, later, bot lifecycle/control.

## Target backend boundaries

```text
                         Application/API
        +---------------------+-----------------------+
        |                     |                       |
     Learning              Market                Trading control
        +---------------------+-----------------------+
                              |
+----------------------------- Domain -----------------------------+
| Instrument | Market Data | Events | Signals | Orders | Portfolio |
+-------------------------------+----------------------------------+
                                |
+--------------------------- Services ------------------------------+
| Research | Features | Strategies | Backtesting | Risk | Attribution|
| Runtime/Bots | Experiment Registry | Configuration               |
+-------------------------------+----------------------------------+
                                |
+------------------------ Infrastructure ---------------------------+
| IBKR | QuantConnect | Persistence | Telemetry | Clock adapters    |
+------------------------------------------------------------------+
```

## Foundational domain concepts

### Instrument / security master

A ticker is not a durable identity. Quant Lab needs a canonical `Instrument` independent of vendors, with fields introduced as needed such as:
- internal ID;
- symbol;
- asset class;
- currency;
- exchange/venue;
- vendor identifiers/mappings.

IBKR and QuantConnect identifiers map to the canonical instrument at adapter boundaries. This is essential for comparing feeds and reconciling research with execution.

### Time and Clock

Time is a dependency, not a global utility. Domain/runtime code should not casually call the machine clock.

Conceptually support:
- `HistoricalClock` / backtest clock;
- `ReplayClock`;
- `RealTimeClock`.

This makes historical runs deterministic and lets the same decision logic move toward real time without changing its notion of “now”.

### Canonical event model

As capabilities appear, converge on explicit domain events such as:

```text
MarketDataEvent
 -> Signal
 -> TargetPosition
 -> OrderIntent
 -> Order
 -> Fill
 -> PositionSnapshot
 -> PnLEvent
```

Not every event must exist in Lesson 1. The objective is one vocabulary across backtest, replay, paper and live.

### Versioned configuration

Strategy parameters, universe, provider selection, risk limits and runtime environment belong in explicit configuration rather than constants hidden in code.

A reproducible run should ultimately identify at least:

```text
code/git version
+ strategy version
+ configuration version
+ data identity/range
+ environment
= reproducible run context
```

## Backtest-to-live semantic parity

A recurring lesson from mature trading engines is to minimize semantic divergence between simulation and execution. Quant Lab should therefore keep **strategy logic, canonical events, clock semantics, portfolio/risk decisions and order intent** common across environments. Backtest, replay, paper and live differ through clocks, data sources and execution/fill adapters—not by rewriting strategies.

This does **not** imply that backtests reproduce live markets perfectly. Latency, venue behavior, transport failures, external account activity and broker reconciliation remain explicit live concerns.

## Data lineage and quality

Market data should eventually carry enough metadata to explain where a result came from:
- provider/source and canonical instrument mapping;
- event timestamp vs ingestion/observation timestamp where relevant;
- timezone/calendar/session policy;
- adjusted/raw and corporate-action policy;
- missing/duplicate/out-of-order policy;
- freshness/gap diagnostics;
- dataset/version or reproducible query identity for experiments.

Research artifacts should make these assumptions visible rather than hiding them inside adapters.

## Research and experiment identity

Every meaningful backtest/experiment eventually receives an `experiment_id`. Its manifest should capture:
- code/Git commit;
- strategy + version;
- configuration/parameters;
- universe/instruments;
- provider/data range and relevant data identity;
- timeframe;
- costs/slippage;
- evaluation split;
- metrics/benchmark;
- creation timestamp and result artifacts.

This lets Learn link a lesson directly to the experiment that demonstrated—or falsified—the concept.

### Standard research report / tear sheet

Comparable experiments should render a common report containing, as appropriate:
- benchmark and cumulative/equity curves;
- drawdown depth/duration;
- rolling volatility and risk-adjusted metrics;
- exposure, leverage and turnover;
- commissions/slippage/fees;
- trade-level and period-level diagnostics kept semantically distinct;
- parameter/configuration summary;
- in-sample vs out-of-sample/walk-forward partitions;
- sensitivity/parameter-surface views when optimization was performed.

Optimization outputs must expose the search space and number of trials; a best historical parameter set is not treated as evidence by itself.

## Strategy, bot and run identity

Keep these concepts distinct:

```text
StrategyDefinition
       |
StrategyVersion
       |
BotConfiguration
       |
BotInstance
       |
Run
       |
Orders / Fills / Positions / P&L
```

A strategy is reusable logic. A bot is a configured runtime instance. A run is one execution history. Attribution can therefore answer P&L by asset, bot, strategy version and total portfolio.

## Persistence and state

Persistence is an explicit architectural boundary, introduced incrementally. Likely persistent information includes:
- course/progress state;
- experiment manifests/results;
- strategy/configuration versions;
- bot lifecycle state;
- orders/fills/positions;
- attribution/P&L snapshots;
- audit events;
- cached market data where appropriate.

Start simple. A relational database such as PostgreSQL is a likely later choice, but no database is required merely to complete Lesson 1.

## Control plane and audit

Lifecycle commands are separate from strategy logic. Every material control action should eventually record actor/source, timestamp, requested action, previous/new state and result.

A bot stop must distinguish:
1. prevent new orders;
2. cancel open orders;
3. liquidate positions.

The global kill switch is independent of bot/strategy code and cannot be bypassed by an LLM.

## Observability

Operational observability is distinct from financial charts. Eventually expose:
- connector connected/disconnected state;
- data freshness/staleness;
- bot heartbeat/status;
- order rejection/failure;
- reconciliation mismatches;
- API/provider latency;
- last successful synchronization;
- application errors and relevant metrics.

Observability should use structured logs/metrics and feed UI health indicators when those stages arrive.

## Core quantitative boundaries

- **Data:** canonical schemas, instrument mapping, time, validation, corporate actions and caching/persistence.
- **Features:** pure/time-aware transformations.
- **Strategies:** signals/desired exposure only; no vendor/network calls.
- **Backtesting:** historical clock/information set, fills, costs and accounting.
- **Portfolio:** aggregate strategy intent and capital allocation.
- **Risk:** independent limits on exposure/sizing/leverage/drawdown.
- **Execution:** translate approved intent into broker-neutral order requests.
- **Attribution:** tag financial events by environment, bot, strategy version and asset.
- **Bot runtime:** independent configured strategy instances with lifecycle/health.

## Research acceleration without changing semantics

Quant Lab may use **vectorized/batched research paths** for feature computation, cross-sectional work and large experiment grids, but these are research accelerators. Any strategy promoted toward paper trading must be reproducible under the canonical event/order semantics. This prevents a fast research-only implementation from silently defining different trading behavior.

## Performance and benchmarking

Correctness comes first, but mature quant systems also measure performance. Add benchmarks only when a hot path exists, for example data normalization, feature calculation, parameter sweeps, event replay or attribution. Track representative dataset size, runtime and memory so optimization work is evidence-driven.

## Testing architecture

Use a trading-specific test pyramid:

```text
many        Unit tests
            - returns/features/statistics/domain invariants
            - deterministic and no network

fewer       Deterministic strategy/backtest tests
            - known fixtures
            - clock/timing/leakage edge cases

fewer       Connector contract/integration tests
            - IBKR / QuantConnect adapters
            - vendor behavior isolated from domain tests

few         End-to-end tests
            - application -> bot -> paper execution/reconciliation
```

Normal unit tests must not require external platforms, credentials or network access.

Use deterministic **synthetic market fixtures** for timing, fills, corporate-action/data-quality edge cases and regression tests. Connector tests verify translation to/from those canonical contracts. CI should eventually gate merges on unit/quantitative tests and critical static/security checks.

## Target repository structure

```text
quant-lab/
├── course/
├── notebooks/
├── experiments/
├── src/quant_lab/
│   ├── domain/
│   │   ├── instruments/
│   │   ├── market_data/
│   │   ├── signals/
│   │   ├── orders/
│   │   ├── portfolio/
│   │   └── events/
│   ├── research/
│   │   ├── features/
│   │   ├── statistics/
│   │   ├── backtesting/
│   │   └── experiments/
│   ├── strategies/
│   ├── risk/
│   ├── attribution/
│   ├── runtime/
│   │   ├── bots/
│   │   └── clock/
│   ├── application/
│   └── infrastructure/
│       ├── ibkr/
│       ├── quantconnect/
│       ├── persistence/
│       └── telemetry/
├── api/
├── frontend/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── contract/
│   └── e2e/
├── docs/
├── ROADMAP.md
├── REFERENCES.md
└── AGENTS.md
```

This is the destination, **not Lesson 1 scaffolding**. Create directories/modules only when a lesson uses them.

## CI, packaging and reproducible environments

As implementation matures, repository engineering should include:
- pinned/locked dependencies and supported Python/runtime versions;
- CI for tests, lint/type checks and critical security/dependency checks;
- coverage visibility for important quantitative/domain code;
- reproducible local/container environment when external services make setup non-trivial;
- changelog/migration notes once persisted schemas or public contracts exist;
- performance regression benchmarks only for demonstrated hot paths.

## Safety lifecycle

```text
DRAFT -> RESEARCHED -> VALIDATED -> PAPER_ELIGIBLE -> PAPER_ACTIVE
                                                   -> PAPER_STOPPED

LIVE_ELIGIBLE is a separate explicit promotion.
LIVE execution is disabled by default.
```

## Research-to-live path

```text
lesson/hypothesis
 -> implementation/tests
 -> experiment identity
 -> historical research
 -> realistic costs
 -> out-of-sample/walk-forward
 -> robustness
 -> paper eligible
 -> IBKR paper runtime/reconciliation
 -> observation period
 -> explicit live eligibility
 -> IBKR live read-only
 -> optional controlled live execution
```

## Technology

Python domain/research/API/connectors; FastAPI candidate; TypeScript + React UI; pytest; Jupyter exploration. WebSockets/SSE, database and production telemetry are selected only when their requirements arrive.

## Incremental implementation rule

Architecture should guide implementation without creating speculative enterprise scaffolding. Lesson 1 introduces only what it genuinely needs: initial instrument/data/time concepts, provider ports, return calculations, tests, research environment and minimal Learn UI. Later lessons grow events, experiments, persistence, bots and operations when their use cases become concrete.

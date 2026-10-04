# Quant Lab Architecture

## Architectural goals

Quant Lab must support three very different workloads without coupling them:
1. **education/research**;
2. **market observation**;
3. **safe automated execution**.

The architecture therefore separates domain logic from presentation, strategies from execution, and paper from live environments.

## User interface

```text
+------------------------------------------------------------------+
| Learn | Market | Paper Trading | Live Trading | Strategies/Control|
+-------------------------------+----------------------------------+
                                |
                           TypeScript/React
                                |
                              API
                                |
                              Python
```

### Learn
Course navigation, interactive explanations, examples, charts, exercises, progress, paper references, experiments and AI tutoring. This is the first UI to implement.

### Market
Read-only market observation. Historical/real-time data, charts and observable features/signals. **No order commands exist in this surface.**

### Paper Trading
IBKR paper account/engine state: positions, orders/fills, P&L and performance attribution.

### Live Trading
Separate live-account observation. Starts read-only. Any future live control is gated and visually distinct from paper mode.

### Strategies / Control
Strategy catalogue and bot control plane. Each bot references:
- strategy + immutable/versioned strategy code;
- configuration;
- universe/assets;
- environment (backtest/paper/live);
- lifecycle state;
- performance attribution;
- health and last heartbeat.

Controls include per-bot activate/deactivate/stop and a global emergency stop.

## Backend layers

```text
                         Application/API
       +----------------------+------------------------+
       |                      |                        |
   Learning service       Market service         Trading control
       |                      |                        |
       +----------------------+------------------------+
                              |
+----------------------------- Domain ------------------------------+
| Data -> Features -> Strategy Signals -> Portfolio -> Risk         |
|   |         |             |                       |               |
| Research/Backtest          +-> Attribution        +-> Execution   |
+-----------------------------------------------------------+-------+
                                                            |
                                                     Broker interface
                                                   /                  \
                                              IBKR Paper           IBKR Live
```

## Core domain boundaries

### Data
Historical and streaming acquisition, canonical schemas, timestamps/calendars, validation, corporate actions and persistence/cache.

### Features
Pure/time-aware transformations. A feature must not see information beyond its decision timestamp.

### Strategies
Hypotheses producing signals/desired exposure. No network/broker calls.

### Backtesting
Historical clock, information availability, simulated fills, costs and portfolio accounting. The same strategy interface should be usable outside the backtester.

### Portfolio
Combines strategy intents and allocates capital subject to constraints.

### Risk
Independent controls over exposure, sizing, leverage, drawdown and later operational limits. Risk can reject/reduce strategy intent.

### Execution
Converts approved targets into orders and manages order lifecycle without exposing broker SDK details upward.

### Brokers
Adapters. IBKR paper and live share concepts but **must be separate runtime configurations/connections**.

### Attribution
Every position/order/fill/P&L event should be attributable to environment, bot, strategy version and asset. This enables per-bot/per-asset/aggregate historical performance.

### Bot runtime
Runs strategy instances independently, tracks lifecycle/health and provides safe stop semantics. A bot is not synonymous with a strategy: multiple bots may run different configurations/universes of the same strategy.

## Safety state model

Suggested lifecycle:

```text
DRAFT -> RESEARCHED -> VALIDATED -> PAPER_ELIGIBLE -> PAPER_ACTIVE
                                             |
                                             v
                                        PAPER_STOPPED

LIVE_ELIGIBLE is a separate explicit promotion after paper validation.
LIVE execution is disabled by default.
```

Bot runtime states should distinguish at least STOPPED, STARTING, ACTIVE, STOPPING, ERROR and KILLED.

A stop action must define whether it only prevents new orders, cancels open orders, and/or liquidates positions. These are **different operations** and must never be conflated.

## Data/control flow

```text
market data
   -> canonical event
   -> feature state
   -> strategy/bot
   -> signal/target
   -> portfolio aggregation
   -> risk checks
   -> execution intent
   -> broker adapter
   -> order/fill events
   -> positions + attribution + UI
```

The Market tab taps the data/features side only. Learn can use historical/replay data. Paper/Live consume account/execution state. Control sends lifecycle commands, not arbitrary broker SDK calls.

## Frontend/backend choice

- **Python:** domain, research, statistics, ML, APIs and broker adapters.
- **FastAPI:** preferred API candidate when implementation begins.
- **TypeScript + React:** frontend.
- **pytest:** tests.
- **Jupyter:** exploration only; reusable logic moves into `src/quant_lab/`.

For real-time UI updates, evaluate WebSockets/SSE when Market/Paper stages require them rather than adding infrastructure during Lesson 1.

## Research-to-live promotion

```text
hypothesis
 -> evidence/lesson
 -> implementation/tests
 -> historical experiment
 -> realistic costs
 -> out-of-sample/walk-forward
 -> robustness
 -> paper eligible
 -> paper runtime/reconciliation
 -> paper observation period
 -> explicit live eligibility decision
 -> live read-only integration
 -> optional controlled live execution
```

Promotion is recorded state, not an automatic consequence of a metric threshold.

## Security/operations

- secrets never enter Git;
- paper/live credentials and runtime configs are isolated;
- least privilege;
- audit lifecycle/control actions;
- idempotent/recoverable order handling;
- broker reconciliation is authoritative for actual account state;
- stale market/account data is visible and can inhibit trading;
- global kill switch is independent of individual strategy logic;
- deterministic risk controls are not delegated to an LLM.

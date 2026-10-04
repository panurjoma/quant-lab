# Quant Lab Architecture

## Goals

Quant Lab separates education/research, market observation and automated execution. It also deliberately limits v1 integration complexity to **two external financial-platform connectors: Interactive Brokers and QuantConnect**.

## Progressive UI

```text
Stage 1+          later                 execution stage        final gated stage
 Learn  ------>  Market  ---------->  Paper + Control  ----->  Live
(always grows)   (read-only)           (IBKR paper)            (read-only first)
```

The five conceptual tabs are:
- **Learn** — first and continuously expanding.
- **Market** — historical first; real-time later; never sends orders.
- **Paper Trading** — unlocked after broker/execution + IBKR paper integration.
- **Live Trading** — unlocked after paper validation; observation first.
- **Strategies / Control** — strategy catalogue grows with lessons; runtime controls unlock with bots.

Locked means the underlying capability is not yet part of the supported product, rather than presenting a misleading empty/unsafe control.

## Exactly two v1 connectors

### Interactive Brokers connector

IBKR has two architectural roles:

```text
IBKR
├── Market/account data adapter
└── Broker/execution adapter
    ├── Paper
    └── Live (later, gated)
```

Paper and live use separate runtime configuration/connections. IBKR vendor objects cannot leak into strategy/domain interfaces.

### QuantConnect connector

QuantConnect is a **research/data/backtesting integration**, not the v1 execution broker:

```text
QuantConnect
└── Research/data adapter
    ├── historical/research data
    └── comparative research/backtest workflows
```

Where QuantConnect workflows do not map cleanly to local streaming semantics, we expose only the capabilities actually supported rather than forcing a fake universal interface.

### Provider capability interfaces

Prefer capability-specific boundaries such as:

```text
HistoricalDataProvider
SnapshotDataProvider
StreamingDataProvider
ResearchBacktestProvider
Broker
AccountProvider
```

Adapters implement only relevant capabilities. This avoids assuming that a research platform and an execution broker behave identically.

All vendor data is normalized into Quant Lab models before reaching features/strategies.

**No third external market-data connector is planned for v1.**

## User interface

```text
+-------------------------------------------------------------------+
| Learn | Market | Paper Trading | Live Trading | Strategies/Control |
+-------------------------------+-----------------------------------+
                                |
                           TypeScript/React
                                |
                              API
                                |
                              Python
```

### Learn
Course navigation, explanations, charts, exercises, progress, references, experiments and AI tutoring.

### Market
Read-only historical/real-time observation. It consumes normalized data from supported provider capabilities and exposes source/freshness metadata. It has no execution commands.

### Paper Trading
IBKR paper state: account, positions, orders/fills, P&L and attribution.

### Live Trading
Separate live account view; initially read-only. Live execution remains independently gated.

### Strategies / Control
Catalogue + bot control plane. Each bot references strategy version, configuration, universe, environment, lifecycle, attribution and health. Controls include per-bot lifecycle commands and global emergency stop.

## Backend

```text
                         Application/API
        +---------------------+-----------------------+
        |                     |                       |
     Learning              Market                Trading control
        +---------------------+-----------------------+
                              |
+----------------------------- Domain -----------------------------+
| canonical data -> features -> strategy -> portfolio -> risk      |
|       |                         |                      |          |
| research/backtest              +-> attribution       execution   |
+-------+--------------------------------------------------+-------+
        |                                                  |
 Provider capabilities                               Broker interface
   /             \                                         |
IBKR          QuantConnect                                 IBKR
data/account  research/data                         paper / gated live
```

## Core boundaries

### Data
Canonical schemas, time, validation, corporate actions and persistence/cache. External data is translated at the edge.

### Features
Pure/time-aware transformations with no future information.

### Strategies
Signals/desired exposure only; no vendor or network calls.

### Backtesting
Historical clock/information set, fills, costs and accounting. QuantConnect may be used as an independent comparative research environment, while Quant Lab retains its own testable domain contracts.

### Portfolio / Risk
Aggregate strategy intent, allocate capital and independently constrain exposure/sizing.

### Execution / Broker
Convert approved intent to orders. **IBKR is the only v1 execution broker.**

### Attribution
Tag position/order/fill/P&L events by environment, bot, strategy version and asset.

### Bot runtime
Independent strategy instances with configuration/universe/lifecycle/health.

## Safety lifecycle

```text
DRAFT -> RESEARCHED -> VALIDATED -> PAPER_ELIGIBLE -> PAPER_ACTIVE
                                                   -> PAPER_STOPPED

LIVE_ELIGIBLE is a separate explicit promotion.
LIVE execution is disabled by default.
```

A stop action must explicitly distinguish:
- prevent new orders;
- cancel open orders;
- liquidate positions.

They are not interchangeable.

## Research-to-live path

```text
lesson/hypothesis
 -> implementation/tests
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

Python domain/API/connectors; FastAPI candidate; TypeScript + React UI; pytest; Jupyter for exploration. WebSockets/SSE are evaluated only when real-time UI requirements arrive.

## Security/operations

Secrets never enter Git; paper/live configs are isolated; broker state is reconciled; stale data is visible and may inhibit trading; lifecycle actions are auditable; kill switch is independent of strategy logic; deterministic risk controls are never delegated to an LLM.

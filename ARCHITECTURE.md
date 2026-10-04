# Architecture

## Principles

Quant Lab uses a layered architecture so research code can mature into execution code without strategies becoming coupled to data vendors, web frameworks or brokers.

### Core rule

```text
strategy != broker
strategy != UI
backtest != strategy
```

A strategy consumes well-defined market/features/state and produces an intent or signal. Portfolio, risk and execution layers decide how that intent becomes an order.

## Logical components

### Data
Acquisition, canonical schemas, calendars/timezones, validation, corporate-action handling and persistence/caching.

### Features
Deterministic transformations and indicators. Features must encode their timing assumptions and never leak future information.

### Strategies
Trading hypotheses and signal generation. Strategies should be testable against in-memory data without network access.

### Backtesting
Clock/event semantics, portfolio state, execution simulation, costs/slippage and performance accounting.

### Portfolio
Combines signals, determines target weights/exposures and handles constraints.

### Risk
Pre-trade and portfolio-level limits, sizing, drawdown/exposure controls and later operational kill switches.

### Execution
Converts approved targets/orders into broker-neutral execution requests; handles lifecycle, idempotency and reconciliation.

### Brokers
Adapters such as PaperBroker and eventually IBKRBroker. Broker-specific SDK objects should not escape this boundary.

### API
A Python application/API layer exposes research and operational capabilities without contaminating the domain model.

### Frontend
TypeScript + React. It consumes APIs for experiments, strategy diagnostics, portfolio/risk and execution monitoring. The frontend is deliberately replaceable.

### AI/Agents
AI is an optional orchestration/research layer, not the mathematical foundation of the system. Agents may help analyze experiments or select among already-defined tools/strategies, but deterministic controls remain outside LLM authority.

## Dependency direction

```text
UI -> API -> application/domain
                |
                +-> data
                +-> features
                +-> strategies
                +-> portfolio/risk
                +-> execution -> broker adapters
```

External dependencies point inward through interfaces/adapters wherever practical.

## Research-to-live path

```text
hypothesis
  -> notebook/exploration
  -> reusable implementation
  -> unit tests
  -> historical backtest
  -> out-of-sample/walk-forward
  -> paper trading
  -> operational validation
  -> controlled live deployment
```

Promotion between stages requires evidence; it is not automatic.

## Initial technology choices

- Python for domain, research, statistics, ML, API and broker integration.
- pytest for automated tests.
- Jupyter for exploratory analysis, with reusable logic moved into `src/`.
- TypeScript + React for the future web UI.
- GitHub issues/PRs for learning milestones and engineering review.

Specific data/backtesting/frontend frameworks are intentionally deferred until a lesson gives us enough requirements to compare them instead of selecting by fashion.

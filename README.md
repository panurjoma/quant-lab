# Quant Lab

Quant Lab is an **AI-assisted systematic trading learning environment, research laboratory and trading-control platform**. The repository grows from first principles into a tested, broker-independent system that can progress from historical research to Interactive Brokers paper trading and, only after explicit validation, live execution.

The project has two equally important outcomes:

1. **Understanding** — learn why systematic strategies exist, their mathematics/statistics, evidence, assumptions and failure modes.
2. **Engineering** — turn that understanding into a reusable Python platform with a modern web interface.

Backtest performance is not evidence of future returns. Quant Lab is designed to make it difficult to fool ourselves.

## Product vision: five tabs

The application evolves around five top-level interfaces. They share one backend/domain model, but each has a different safety level.

### 1. Learn — first priority

The first product surface we build. It is an interactive course rather than a static collection of Markdown files.

It should eventually provide:
- ordered lessons from market basics to advanced statistical/ML strategies;
- explanations at intuition, mathematical and implementation levels;
- worked examples and visualizations using real/historical market data;
- exercises, quizzes and coding tasks;
- progress tracking;
- links to the papers/references motivating each strategy;
- embedded experiment/backtest results;
- an AI tutor that explains results and challenges assumptions;
- a path from each lesson to the exact code, strategy and experiment it created.

The learning experience is the **spine of the product**: capabilities appear in the other tabs as the corresponding lesson is completed.

### 2. Market — observation only

A real-time/read-only market dashboard:
- watchlists and instruments;
- price/return charts;
- OHLCV and selected indicators/features;
- market/session status and timestamps;
- strategy signals as observations where useful.

This tab **cannot place orders**. Its purpose is to understand the market state and the data consumed by strategies.

### 3. Paper Trading

An operational dashboard connected to the **Interactive Brokers paper account**:
- paper account equity/cash;
- positions and orders;
- realized/unrealized P&L;
- performance by asset, strategy/bot and total portfolio;
- historical equity/P&L curves;
- fills, costs and execution diagnostics;
- reconciliation between internal state and broker state.

Paper execution is a required stage before live trading.

### 4. Live Trading — initially observation-first

A separate live-account surface, introduced only after the research and paper-trading pipeline is mature.

Initial scope is **observation of live performance and state**, not casual order placement. Any later live-control capability requires explicit safeguards, authentication, confirmations, risk limits and kill switches.

Paper and live environments must be visually and technically distinguishable to reduce accidental actions.

### 5. Strategies / Control

The control plane for independent strategy bots:
- strategy catalogue with hypothesis, rules, evidence and version;
- active/inactive state;
- bot health/status;
- assets/universe assigned to each bot;
- P&L per strategy, per asset and total;
- historical performance;
- current exposure and risk;
- activate/deactivate a bot;
- cancel/stop a strategy safely;
- **global stop / kill switch** for automated trading.

Each bot runs a defined strategy configuration. Strategy identity and P&L attribution must survive from backtest through paper/live execution.

## Technology direction

### Quantitative/backend — Python

Python is the primary language for market data, statistics, research, strategies, backtesting, portfolio/risk, execution, broker integration, ML and APIs.

Expected ecosystem is introduced only when needed: NumPy, pandas/Polars, SciPy/statsmodels, scikit-learn, pytest, Jupyter and an evaluated backtesting engine.

### API/application layer — Python

FastAPI is the leading choice for the application boundary when the interactive UI needs it. Domain code does not depend on HTTP.

### Frontend — TypeScript + React

The UI will use **TypeScript + React**: modern, strongly typed, widely maintained and suitable for interactive dashboards. Framework/tooling will be selected when we implement the Learn UI rather than prematurely locking the architecture.

The frontend consumes APIs; trading logic stays in Python.

## System shape

```text
                     +---------------- Web UI ----------------+
                     | Learn | Market | Paper | Live | Control|
                     +-------------------+---------------------+
                                         |
                                      Python API
                                         |
       +---------------- Quant / Trading Domain ----------------+
       | data -> features -> strategies -> portfolio -> risk    |
       |                         |                    -> execution|
       | backtesting/research    |                         |     |
       +-------------------------+-------------------------+-----+
                                 |                         |
                           attribution/state         Broker abstraction
                                                           |
                                             +-------------+-----------+
                                             |                         |
                                         IBKR Paper                 IBKR Live
```

A strategy produces signals/intent. It **never calls a broker directly**.

## Learning philosophy

Every concept follows:

```text
question -> intuition -> mathematics -> evidence/paper
 -> worked example -> hypothesis -> implementation
 -> tests -> backtest/experiment -> interpretation
 -> failure modes -> challenge -> reusable platform capability
```

We learn research hygiene early. A moving average is easy to code; knowing whether its apparent profit is meaningful is the harder skill.

AI roles:
- **ChatGPT:** tutor, research synthesizer, quant critic and examiner.
- **Codex in VS Code:** implementation agent following explicit issue/lesson specifications.
- **GitHub:** source of truth for lessons, papers, decisions, experiments, issues and PRs.
- **Learner:** architect/researcher responsible for understanding assumptions and evidence.

## Curriculum

See [ROADMAP.md](ROADMAP.md) for the detailed prerequisite-driven sequence and [REFERENCES.md](REFERENCES.md) for literature and technical references.

The high-level progression is:

1. markets, data, returns and time;
2. Python research environment and data contracts;
3. performance/risk metrics and a minimal honest backtester;
4. simple trend/momentum and mean-reversion hypotheses;
5. relative value, stationarity, pairs and cointegration;
6. cross-sectional factors and portfolio/risk construction;
7. robust validation, costs, overfitting and walk-forward research;
8. advanced statistical arbitrage;
9. regime detection and ML;
10. broker/execution engineering;
11. IBKR paper trading;
12. live observation/controlled deployment;
13. multi-strategy orchestration and AI-assisted analysis.

## Development workflow

```text
Issue / learning objective
 -> lesson + references
 -> branch
 -> implementation + tests
 -> experiment
 -> learner interpretation/challenge
 -> PR review
 -> merge
 -> capability appears in the application
```

## Repository direction

```text
quant-lab/
├── course/             # Interactive-course source material
├── references/         # Optional deeper notes derived from papers
├── notebooks/          # Exploration; reusable logic moves to src/
├── src/quant_lab/
│   ├── data/
│   ├── features/
│   ├── strategies/
│   ├── backtesting/
│   ├── portfolio/
│   ├── risk/
│   ├── execution/
│   ├── brokers/
│   ├── attribution/
│   └── application/
├── tests/
├── experiments/
├── frontend/           # TypeScript/React application
├── ROADMAP.md
├── ARCHITECTURE.md
├── REFERENCES.md
└── AGENTS.md
```

Directories are added when a real lesson/use case requires them.

## Non-negotiables

- no look-ahead bias or future leakage;
- timestamps/timezones and decision timing are explicit;
- costs/slippage are incorporated before performance claims;
- research tracks trials/parameters to expose overfitting risk;
- train/validation/test periods respect time;
- risk is reported alongside return;
- strategy, portfolio, risk and execution are separate;
- broker-specific code is isolated;
- P&L is attributable by bot/strategy and asset;
- paper trading precedes live trading;
- live and paper modes cannot be confused;
- all automated trading has per-bot stop controls and a global kill switch;
- live-order capability is disabled by default.

## First implementation

**Lesson 1 — Market Data, Returns & Research Environment** remains the correct first coding milestone.

It establishes the Python package, tests, canonical OHLCV/time model, simple/log returns, validation, provider abstraction and a first research notebook. The first UI increment should be a minimal **Learn** shell that can render the lesson structure; trading controls come much later.

The measure of success is not the number of bots or historical Sharpe ratios. It is whether Quant Lab can teach, test and operate a hypothesis without hiding the assumptions that make the result possible.

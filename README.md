# Quant Lab

Quant Lab is an **AI-assisted systematic trading laboratory and learning platform**. Its purpose is not to collect disconnected trading scripts: the repository grows lesson by lesson into a tested, broker-independent quantitative trading system that can progress from research and backtesting to paper trading and, only after validation, live execution.

## Objectives

1. Learn systematic and quantitative trading from first principles.
2. Translate every important concept into mathematics, Python, tests and experiments.
3. Build reusable infrastructure instead of throwaway tutorial code.
4. Learn how strategies fail: regime changes, overfitting, leakage, costs, slippage and execution.
5. Add ML/AI only where it improves a clearly defined component.
6. Finish with a multi-strategy platform with portfolio/risk management, paper trading and broker adapters.

This project is educational and research-oriented. Backtest performance is not evidence of future returns.

## Technology direction

### Quantitative/backend layer — Python

Python is the primary language because of its quantitative ecosystem and suitability for research, statistics, ML, optimization and broker integration. The core domain will remain usable independently of any UI.

Expected ecosystem: NumPy, pandas/Polars as appropriate, SciPy/statsmodels, scikit-learn when justified, pytest, Jupyter and one or more backtesting engines evaluated during the course.

### Application/API layer — Python

The platform will expose stable application interfaces, likely through FastAPI once an interactive application is useful. Strategies never depend directly on HTTP or frontend code.

### Frontend — TypeScript + React

The eventual dashboard/research UI will use **TypeScript + React**, a modern, strongly typed and broadly maintained web stack. A lightweight React framework/toolchain will be selected when the UI milestone arrives rather than prematurely coupling the repository to one framework.

The frontend will consume APIs and should be replaceable without changing quantitative logic.

## Target architecture

```text
Market / Alternative Data
          |
          v
      Data Layer
          |
          v
 Feature & Indicator Layer
          |
          +-------------------+
          |                   |
          v                   v
     Strategies        Regime Models
          |                   |
          +---------+---------+
                    v
              Signal Layer
                    |
                    v
          Portfolio Construction
                    |
                    v
             Risk Management
                    |
                    v
             Execution Layer
                    |
                    v
           Broker Abstraction
          /        |         \
   PaperBroker  IBKRBroker  other adapters
                    |
                    v
                 Market

        Python API <----> TypeScript/React UI
```

A strategy produces decisions/signals. It **must not call a broker directly**. This separation lets the same strategy run in research, backtests, paper trading and live execution.

## Learning methodology

Each topic follows a consistent loop:

```text
Problem
  -> intuition
  -> mathematics/statistics
  -> worked example
  -> trading hypothesis
  -> implementation specification
  -> Python implementation
  -> tests
  -> backtest/experiment
  -> interpretation
  -> failure modes
  -> challenge
```

AI is used in distinct roles:

- **ChatGPT:** teacher, quant mentor, research synthesizer, experiment critic and examiner.
- **Codex in VS Code:** implementation agent working from explicit lesson/issue specifications.
- **GitHub:** persistent source of truth for lessons, decisions, issues, code, experiments and reviews.
- **The learner:** architect and quantitative researcher who must understand and defend every assumption.

AI should remove mechanical work, not hide the reasoning.

## Course roadmap

The detailed sequence lives in [ROADMAP.md](ROADMAP.md). The progression is approximately:

1. Market data, returns and research environment
2. Moving averages and basic features
3. Momentum
4. Breakouts
5. Mean reversion
6. Bollinger Bands, RSI and Z-scores
7. Pairs trading
8. Cointegration
9. Statistical arbitrage
10. Factor investing: momentum, value, quality, size and volatility
11. Portfolio construction
12. Risk management
13. Correct backtesting
14. Overfitting and multiple testing
15. Walk-forward/out-of-sample validation
16. Regime detection
17. Machine learning for trading
18. Strategy selection / meta-models
19. Broker APIs and execution architecture
20. Paper trading
21. Live execution and operational safety
22. Multi-strategy and AI-assisted orchestration

The order may evolve as experiments reveal prerequisites.

## Development workflow

Every meaningful milestone should normally follow:

```text
GitHub Issue
   -> lesson/specification
   -> feature branch
   -> implementation + tests
   -> experiment/backtest
   -> interpretation
   -> Pull Request
   -> review
   -> merge
```

Lessons are not considered complete merely because code runs. We should be able to explain the hypothesis, assumptions, statistical validity, costs, risks and conditions under which it is expected to fail.

## Repository direction

```text
quant-lab/
├── course/          # Lessons and exercises
├── notebooks/       # Exploratory research (introduced incrementally)
├── src/quant_lab/   # Reusable production-quality Python package
│   ├── data/
│   ├── features/
│   ├── strategies/
│   ├── backtesting/
│   ├── portfolio/
│   ├── risk/
│   ├── execution/
│   ├── brokers/
│   └── agents/
├── tests/
├── experiments/
├── frontend/        # TypeScript/React UI when needed
├── ROADMAP.md
├── ARCHITECTURE.md
└── AGENTS.md
```

Directories are introduced when their first real use case arrives; we avoid empty architecture for architecture's sake.

## Quantitative non-negotiables

- No look-ahead bias.
- No use of future information in feature construction or training.
- Backtests must model relevant transaction costs and eventually slippage.
- Training, validation and test periods must respect time ordering.
- Strategy rules and execution are separate concerns.
- Risk is evaluated alongside return.
- Parameter optimization must not become historical curve fitting.
- Reproducibility matters: assumptions, data ranges and configurations should be recorded.
- Paper trading precedes live trading.
- Live capital is never deployed merely because a backtest looks attractive.

See [AGENTS.md](AGENTS.md) for coding-agent rules.

## First implementation milestone

After this bootstrap PR, the first implementation issue/PR should be:

**Lesson 1 — Market Data, Returns & Research Environment**

It will establish the Python project, testing/research environment, a canonical OHLCV representation, simple and log returns, data validation, an initial data-provider abstraction, and a small research notebook. The objective is to understand exactly what information a trading system receives before writing the first strategy.

## Long-term outcome

Quant Lab should ultimately support:

- reproducible quantitative research;
- multiple systematic strategies;
- robust backtesting and walk-forward validation;
- statistical and ML models;
- regime detection;
- portfolio construction and risk controls;
- broker-independent execution;
- IBKR paper/live integration;
- monitoring and a modern web interface;
- AI-assisted research/strategy selection where justified.

The measure of success is not the number of strategies implemented. It is whether the platform can test a hypothesis honestly and explain why a result should—or should not—be trusted.

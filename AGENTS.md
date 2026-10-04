# AGENTS.md — Quant Lab Coding Rules

These instructions apply to Codex and other coding agents working in this repository.

## Prime directive

Do not optimize for impressive historical returns. Optimize for **correctness, testability, reproducibility and honest experiments**.

## Quantitative safety rules

1. Never introduce look-ahead bias.
2. Never construct a feature using information unavailable at the simulated decision timestamp.
3. Never shuffle time-series train/test data unless a lesson explicitly demonstrates why it is valid.
4. Include transaction costs when a backtest reaches the stage where trading frequency/performance is evaluated.
5. Model slippage/fill assumptions explicitly once execution realism is relevant.
6. Report risk metrics alongside returns; do not present return alone as success.
7. Do not tune parameters solely to improve the same historical sample used for evaluation.
8. Keep an untouched/out-of-sample evaluation path.
9. Make timezones, bar timestamps and ordering explicit.
10. Treat missing/duplicate data as errors or explicit policies, never silently as convenient values.

## Architecture rules

1. Strategies must not call broker APIs directly.
2. Broker-specific types remain inside broker adapters.
3. Signal generation, portfolio construction, risk and execution are separate responsibilities.
4. Core strategy tests must not require network access.
5. Notebooks are for exploration; reusable business/quant logic belongs in `src/quant_lab/`.
6. The TypeScript/React frontend communicates through stable APIs and must not implement trading rules.
7. Prefer the smallest abstraction that satisfies the current lesson; avoid speculative frameworks.
8. Every strategy and material quantitative transformation requires tests.
9. Domain/runtime code must use explicit time/clock abstractions when behavior depends on “now”; do not hide wall-clock access inside strategy logic.
10. External vendor identifiers/types are mapped at infrastructure boundaries; core logic uses canonical Quant Lab instruments/models.
11. Strategy parameters, universes and risk settings belong in explicit configuration rather than unexplained constants.
12. Preserve strategy, bot, run and experiment identity so results remain attributable and reproducible.
13. Do not create target-architecture directories/modules until the current lesson has a concrete use for them.

## Agent behavior

- Read the relevant issue/lesson before coding.
- Do not silently change trading rules or thresholds.
- If a requirement is statistically ambiguous, surface the ambiguity rather than inventing a convention.
- Explain any assumption that can materially alter a backtest.
- Keep commits/PRs focused on the issue.
- Do not add dependencies without a concrete reason.
- Run the relevant tests before declaring work complete.
- Never add credentials, API keys, account identifiers or secrets to the repository.
- Live-order capability must remain disabled by default and must require explicit configuration.

## Experiment discipline

Each meaningful experiment should record enough information to reproduce:
- data source and date range;
- universe/instruments;
- timeframe;
- strategy/configuration parameters;
- cost/slippage assumptions;
- evaluation period;
- relevant software/config version;
- metrics and benchmark.

## Human responsibility

AI can implement, explain and critique. The human remains responsible for accepting financial assumptions, interpreting evidence and deciding whether anything progresses toward paper or live trading.

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
14. Preserve strategy semantics across backtest/replay/paper/live; environment-specific behavior belongs in clocks, data and execution adapters.
15. Record data lineage/quality assumptions when they can affect a result.
16. Optimization/parameter sweeps must record the search space and trials; never present the best trial alone as validation.
17. Keep trade-level metrics distinct from period-return metrics.
18. Prefer deterministic synthetic fixtures for timing/fill/data-quality edge cases before connector-dependent tests.

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


## Open-source benchmark check for every implementation

Before implementing or materially changing a Quant Lab capability, inspect the relevant implementation patterns in these established public projects:

1. `QuantConnect/Lean`
2. `nautechsystems/nautilus_trader`
3. `quantopian/zipline`
4. `polakowo/vectorbt`
5. `kernc/backtesting.py`

Use `ranaroussi/quantstats` as an additional specialist reference when the work concerns performance analytics, risk metrics or tear sheets.

### Required workflow

1. Identify which parts of the current issue/lesson have analogues in the benchmark repositories.
2. Inspect their current public implementation and documentation, not only their README.
3. Extract useful domain concepts, invariants, API boundaries, testing patterns and failure cases.
4. Compare those findings with the current Quant Lab design before coding.
5. Add a missing concept only when it materially improves correctness, reproducibility, safety, testability or the learning objective.
6. Implement the **smallest Quant Lab-specific version** that satisfies the current lesson. Do not copy framework complexity merely because a mature project contains it.
7. Keep Quant Lab's existing architectural rules authoritative: canonical internal models, explicit time, vendor isolation, deterministic tests, experiment identity and gated execution.
8. Record meaningful borrowed design ideas or deviations in the issue/PR when they affect architecture or behavior.
9. Never copy source code blindly. Understand the pattern, implement it for Quant Lab, and respect upstream licenses/attribution requirements.
10. If the five projects disagree, prefer the simplest approach that preserves correctness for the current milestone; document a consequential trade-off.

The benchmark check is a **design review gate, not a dependency requirement**. Quant Lab should remain intentionally smaller and easier to understand than these frameworks.


## LEAN integration and lesson trace rule

LEAN is an external engine dependency, not source to paste into Quant Lab. The authoritative pin is `integrations/lean/lean.lock.json`.

For every lesson that maps to LEAN:

1. Inspect the pinned commit, not moving `master`.
2. Trace the relevant public algorithm API into the engine/framework implementation, tests and example algorithms.
3. Record the financial meaning, information timing, state transitions, assumptions and failure modes—not merely class names.
4. Build the smallest original Quant Lab example that demonstrates the concept.
5. Compare the hand-checkable Quant Lab result with LEAN behavior before paper eligibility.
6. Explain differences in fills, fees, slippage, warm-up, normalization, portfolio accounting or statistics.
7. Link exact upstream paths at the pinned SHA so lesson evidence remains reproducible.
8. Do not copy community/forum algorithms unless their licence is independently verified.
9. If LEAN code is copied or modified, preserve headers, mark modifications, and update `THIRD_PARTY_NOTICES.md` and the vendored Apache licence material.
10. Treat QuantConnect data, cloud services, names and marks as separate from the Apache-licensed engine.

Changing the LEAN pin requires reviewing upstream changes, running adapter/contract tests and recording migration notes.

# Lesson 1 lab — a reproducible information audit

The Learn application now contains five chapters: the information set, return measurement, a backtest audit, a knowledge checkpoint, and sources. The audit is a small educational preview of later backtesting lessons, not a production execution engine or a strategy recommendation.

## Observe and calculate

Select each interval in the bar inspector. Record its start, end, OHLCV and earliest assumed availability. Chart labels are interval ends. A decision before the end cannot use the final close. The fixture assumes zero publication delay; real feeds need an availability policy as well as event timestamps.

Use the return examples to explain why 100 → 110 → 99 produces a −1% compounded result despite simple returns that sum to zero. Check `1.1 × 0.9 − 1 = −0.01`. The sum of log returns is `ln(0.99)`; exponentiating it gives the same total price return. The first observed bar has no preceding close, so its return is undefined.

A 2-for-1 split does not itself halve holding value: one share at 100 becomes two at 50. Raw price changes, adjusted price changes and investor total returns answer different questions. This lesson introduces that distinction without implementing a corporate-action engine.

## Audit the experiment

Experiment identity: `lesson-01 / SMA-3 / DEMO.SYNTH`. The series has twelve invented consecutive hourly intervals beginning at midnight UTC on January 3, 2026. It is not a historical market sample or an exchange-calendar model. No strategy parameter search is performed.

The causal rule uses the preceding three completed closes. After warm-up, it targets stock when the most recent completed close is above their mean, otherwise cash. It trades at the current interval's open under an explicit zero-latency assumption. All-in stock allocation uses fractional shares with no leverage or shorting. Cash earns zero interest. A benchmark buys at the first open and holds under the same cost convention.

The deliberately invalid rule instead reads the current interval's future close before deciding whether to buy at that interval's open. Reveal its curve and explain the information violation before comparing results. A higher equity curve cannot validate an impossible decision rule.

The cost settings are 0, 10 and 30 basis points per order, split equally between an adverse fill adjustment and a fee on fill notional. At 10 bps, a buy at reference open 100 fills at 100.05, with a 0.05% fee. Shares purchased from $1,000 are `1000 / (100.05 × 1.0005)`. A sale receives the adverse adjusted price minus its fee. Costs are charged only when holdings change.

Equity is cash plus shares times close. The end of the experiment marks holdings to the final close without liquidation. Maximum drawdown uses the initial $1,000 and subsequent close marks; it cannot measure an unobserved intrabar trough. Cost totals measure fees and adverse fill differences, not the entire counterfactual performance gap caused by costs.

Compare all three settings; do not select the best. This fixture has no untouched holdout and cannot support an annualized Sharpe, live-performance claim or generalization conclusion. Volume limits, spreads that change over time, impact, borrow, taxes and execution latency are omitted and stated in the interface.

## Exercises and answer rubric

1. **Timing:** Can a 15:29 decision use a 14:30–15:30 bar's final close? No. Identify the first assumed availability and explain real publication delay.
2. **Compounding:** Explain the −1% round trip without adding percentage returns. The answer must use successive investment bases or growth-factor multiplication.
3. **Leakage:** Identify the exact future observation used by the orange curve. It is the current close used to decide a current-open order. Adding fees does not fix it.
4. **Missing data:** Before filling a gap, check session schedules and source quality. A gap does not establish a zero return or zero volume.
5. **Adjustment:** Explain split economics using both quantity and price. Price alone is insufficient.

The checkpoint stores answers under a lesson-specific browser key. Correct answers determine progress; merely opening a page does not. Reset clears only this lesson's key. Storage failures preserve the current session and display a notice.

## Regenerate and verify

Install the project's existing development dependencies, then run from the repository root:

```bash
PYTHONPATH=src python -m quant_lab.research.lesson_one
PYTHONPATH=src python -m quant_lab.research.lesson_one --check
PYTHONPATH=src pytest
cd frontend
npm run build
```

On PowerShell, set `$env:PYTHONPATH = 'src'` before invoking Python. The generator produces the versioned `frontend/src/lesson-one.generated.json` contract. React selects and formats its precomputed results; the quantitative calculations remain canonical in Python. No server, provider connection or new dependency is needed for the lesson.

Tests cover hand-calculated fills, cost reconciliation, compounding, warm-up, invalid configurations and causality under altered current/future prices. The generated-data check detects stale or manually edited results.

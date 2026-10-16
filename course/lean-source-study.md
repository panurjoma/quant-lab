# LEAN source-study method

Pinned source: [QuantConnect/Lean@`80e7843f645673bcbeaab963049f76f20f6785e1`](https://github.com/QuantConnect/Lean/tree/80e7843f645673bcbeaab963049f76f20f6785e1)

This method turns a mature engine into an understandable finance curriculum without treating implementation as a black box or presenting example strategies as profitable.

## Component map

| Finance question | LEAN area to inspect | Interpretation target |
|---|---|---|
| What data existed at decision time? | `Common/Data`, `Engine/DataFeeds`, subscriptions/consolidators | event time, resolution, normalization, warm-up, missing data |
| How is a signal created? | `Algorithm/Framework/Alphas`, indicators | hypothesis, lookback, state, information boundary |
| How is exposure chosen? | `Algorithm/Framework/Portfolio` | sizing, rebalance, cash and portfolio constraints |
| What can veto or reduce risk? | `Algorithm/Framework/Risk`, buying-power models | exposure, drawdown, leverage, liquidation behavior |
| When and how does an order fill? | `Common/Orders`, fill/slippage/fee models, transaction handlers | order state, price assumption, friction, partial fills |
| How does money move? | `Common/Securities`, portfolio/cash/settlement models | holdings, realized/unrealized P&L, currency conversion |
| How does live differ? | `Engine/TransactionHandlers`, brokerage interfaces/plugins | reconciliation, rejects, reconnects, broker capability |
| How is performance reported? | `Engine/Results`, `Common/Statistics` | sampling, benchmark, drawdown, trade vs period metrics |

## Per-lesson trace

1. State the financial question and falsifiable hypothesis.
2. Identify the public LEAN API used by an algorithm.
3. Follow the call path into implementation, tests and a minimal official example.
4. Write the timing/state/accounting invariants in plain language.
5. Reproduce one tiny scenario with checkable numbers in Quant Lab.
6. Express the equivalent strategy/configuration for pinned LEAN.
7. Compare decision, order, fill, cash, holdings, costs and final equity.
8. Explain discrepancies financially.
9. Document realistic failure modes and invalidation conditions.
10. Add an exercise that changes one assumption and predicts the outcome before running it.

## Interpretability requirements

Every strategy lesson separates:

- **economic story:** why the behavior might exist;
- **observable inputs:** exact information available at the decision time;
- **transformation:** indicators/features and their units;
- **decision rule:** how observations become desired exposure;
- **portfolio rule:** how capital and competing signals are combined;
- **risk rule:** what constrains or overrides the target;
- **execution rule:** how the target becomes orders/fills;
- **accounting:** how costs, cash, holdings and P&L change;
- **evidence:** benchmark, validation split, sensitivity and failure regimes.

LEAN examples are engineering demonstrations, not proof of edge.

## Source and licence discipline

Link exact paths at the pinned SHA. Prefer original explanation and small original examples. Code copied from LEAN must retain applicable notices and be recorded in `THIRD_PARTY_NOTICES.md`. QuantConnect community/forum material and datasets are not assumed to share the engine licence.

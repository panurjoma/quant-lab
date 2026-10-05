# Initial Research & Technical References

This is a living bibliography for the course. A reference appearing here is **not an endorsement that a strategy remains profitable**. Papers are evidence to understand, reproduce, challenge and retest under current data/costs.

## Research methodology and backtesting

- Bailey, Borwein, López de Prado & Zhu — *The Probability of Backtest Overfitting* (2015). Core warning on strategy selection after repeated historical trials. https://escholarship.org/uc/item/4w1110bb
- Bailey & López de Prado — *The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality* (2014). https://doi.org/10.3905/jpm.2014.40.5.094
- QuantConnect — Research Guide: hypothesis-driven research, parameter/trial discipline and backtest-overfitting guidance. https://www.quantconnect.com/docs/v2/cloud-platform/backtesting/research-guide
- QuantConnect — Backtesting documentation and customizable transaction/fill/slippage concepts. https://www.quantconnect.com/docs/v2/cloud-platform/backtesting

## Momentum / trend

- Moskowitz, Ooi & Pedersen — *Time Series Momentum*, Journal of Financial Economics 104(2), 2012. Documents return persistence across equity-index, currency, commodity and bond futures at intermediate horizons. https://doi.org/10.1016/j.jfineco.2011.11.003
- Carhart — *On Persistence in Mutual Fund Performance*, Journal of Finance 52(1), 1997. Useful for momentum/factor and transaction-cost context. https://doi.org/10.1111/j.1540-6261.1997.tb03808.x

## Relative value / statistical arbitrage

- Gatev, Goetzmann & Rouwenhorst — *Pairs Trading: Performance of a Relative-Value Arbitrage Rule*. NBER Working Paper 7032 / Review of Financial Studies. https://www.nber.org/papers/w7032
- Avellaneda & Lee — *Statistical Arbitrage in the U.S. Equities Market* (2008/2010). PCA- and sector-factor residual approaches with mean-reverting signals and transaction-cost analysis. https://doi.org/10.2139/ssrn.1153505

## Factors

- Fama & French — *A Five-Factor Asset Pricing Model*, Journal of Financial Economics 116(1), 2015. Size, value, profitability and investment factor framework. https://doi.org/10.1016/j.jfineco.2014.10.010
- Carhart (above) provides the classic four-factor extension including momentum.

## Platform / execution references

- Interactive Brokers Campus — official API education/documentation should be the primary source when IBKR integration begins. https://www.interactivebrokers.com/campus/ibkr-api-page/
- QuantConnect Learning Center — useful comparison for an interactive learn → code → backtest workflow. https://www.quantconnect.com/docs/v2/cloud-platform/learning-center
- QuantConnect historical-data/backtest docs — useful implementation references for warm-up, historical requests and realistic research workflow. https://www.quantconnect.com/docs/v2/writing-algorithms/historical-data/getting-started

## How references enter a lesson

For each strategy we should capture:
- original/important evidence;
- universe and period studied;
- exact signal/rule where reproducible;
- costs and assumptions;
- what later evidence or current tests say;
- implementation differences in Quant Lab;
- failure modes.

We reproduce ideas and results, not copyrighted paper text. Lessons should paraphrase and cite sources.


## Open-source architecture benchmarks

These repositories are **design references, not dependencies and not endorsements of profitability**. They were reviewed because they are among the most established public projects overlapping Quant Lab's research/backtest/execution goals.

- QuantConnect/LEAN — modular event-driven research/backtest/live engine; especially relevant to pluggable models, environment parity and our planned QuantConnect integration. https://github.com/QuantConnect/Lean
- NautilusTrader — production-oriented event-driven architecture emphasizing deterministic simulation/live strategy parity, normalized domain models, adapters, reconciliation and high-resolution multi-asset data. https://github.com/nautechsystems/nautilus_trader
- Zipline — influential Python event-driven backtesting architecture with data ingestion, asset handling and reproducible algorithm runs. The original Quantopian repository is historical rather than our implementation dependency. https://github.com/quantopian/zipline
- VectorBT — vectorized/batched research, parameter sweeps, portfolio analytics, walk-forward tooling and interactive visualization; useful as a reference for fast research workflows without replacing canonical execution semantics. https://github.com/polakowo/vectorbt
- backtesting.py — intentionally compact strategy/backtest API, explicit commissions, optimization, detailed trade outputs and interactive visualization; useful reference for keeping early lessons simple. https://github.com/kernc/backtesting.py
- QuantStats — portfolio/risk analytics, tear sheets, drawdown/rolling metrics and Monte Carlo risk analysis; useful reference for standardized experiment reporting. https://github.com/ranaroussi/quantstats

### Ideas deliberately adopted into the roadmap

- preserve strategy/event semantics across backtest, replay, paper and live;
- deterministic synthetic fixtures before dependence on external data;
- explicit data lineage/quality metadata;
- standardized research tear sheets and benchmark comparisons;
- parameter-surface/sensitivity analysis rather than reporting only the best optimization result;
- vectorized/batched research as an acceleration path, separate from execution semantics;
- tail-risk and Monte Carlo/bootstrap stress analysis;
- realistic order/time-in-force/fill-model contracts;
- CI, coverage, reproducible environments and performance regression benchmarks as the project matures.

We intentionally **did not** copy their large framework scope, add more brokers/data vendors, or adopt implementation complexity before a Quant Lab lesson requires it.

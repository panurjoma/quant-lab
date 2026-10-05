# Quant Lab: GitHub research review

Research date: 5 October 2026. Prepared for the Learn material in the current Lesson 1 pull request.

## What this review establishes

At the start of this review, the frontend contained a six-point historical sample chart, a short list of objectives and two return formulas. The repository roadmap is substantially richer: 36 lessons, ordered by prerequisites, with paper and live execution gated separately. Lesson 1 now turns the foundational concepts into five interactive chapters; later lessons remain roadmap work.

This is a source-based curriculum review, not an exhaustive audit of all GitHub code, an investment recommendation or a claim that any project proves a profitable strategy. Selected primary source files, tests, notebooks and documentation were inspected. External engines and their complete test suites were not installed or executed. Every recommendation below is our adaptation of inspected concepts, not an upstream endorsement of Quant Lab.

## Ranking method and scope

Searched GitHub for repositories tagged algorithmic-trading, quantitative-finance, quantitative-trading, backtesting and trading-bot, requesting the first 20 results for each query with sort:stars. Deduplicated the resulting candidates, fetched their repository metadata and sorted by their current star count. The following are the top ten **within that explicit discovery universe**. This is not a universal ranking of every finance repository: projects with different or absent topic tags can be missed. Stars are a popularity signal; teaching depth, validity, maintenance and relevance are evaluated separately.

| Rank | Repository | Stars at lookup | Role | Latest push date |
|---|---|---:|---|---|
| 1 | [openbq-org/OpenBB](https://github.com/openbq-org/OpenBB) | 73,872 | Data platform | 2026-10-02 |
| 2 | [ZhuLinsen/daily_stock_analysis](https://github.com/ZhuLinsen/daily_stock_analysis) | 65,922 | AI stock analysis | 2026-10-05 |
| 3 | [freqtrade/freqtrade](https://github.com/freqtrade/freqtrade) | 55,049 | Crypto trading framework | 2026-10-05 |
| 4 | [microsoft/qlib](https://github.com/microsoft/qlib) | 49,156 | Quant research / ML | 2026-10-05 |
| 5 | [HKUDS/Vibe-Trading](https://github.com/HKUDS/Vibe-Trading) | 34,783 | Agent-assisted trading | 2026-10-05 |
| 6 | [Fincept-Corporation/FinceptTerminal](https://github.com/Fincept-Corporation/FinceptTerminal) | 32,209 | Finance terminal | 2026-10-01 |
| 7 | [wilsonfreitas/awesome-quant](https://github.com/wilsonfreitas/awesome-quant) | 29,964 | Resource index | 2026-10-05 |
| 8 | [mementum/backtrader](https://github.com/mementum/backtrader) | 23,400 | Event-based backtesting | 2024-08-19 |
| 9 | [QuantConnect/Lean](https://github.com/QuantConnect/Lean) | 21,864 | Research / trading engine | 2026-10-05 |
| 10 | [stefan-jansen/machine-learning-for-trading](https://github.com/stefan-jansen/machine-learning-for-trading) | 21,235 | Educational research notebooks | 2026-10-04 |

Repository metadata is a dated snapshot. Counts and branches will change. Code-source links below are pinned to the inspected revision.

## Detailed extraction and adaptation

### 1. openbq-org/OpenBB

**Useful concept.** Normalize provider data before research and expose the same typed records to notebooks and the UI.

**Inspected evidence.** The historical-equity model defines date, OHLC, optional volume and VWAP. The Fetcher separates query transformation, extraction and record transformation.

**Quant Lab adaptation.** Add a visible data dictionary and provenance panel to each exercise. Use Quant Lab's existing canonical models rather than importing OpenBB's provider catalogue.

**Limits and corrections.** This is data infrastructure, not a complete trading curriculum. An optional field is not evidence that missing volume can safely be treated as zero. The inspected model accepts dates as well as datetimes, whereas intraday Quant Lab exercises require explicit timezone and interval semantics.

**Primary sources:** [equity_historical.py](https://github.com/openbq-org/OpenBB/blob/ae0268771f761b036996d81bd21522ce79d95415/openbb_platform/core/openbb_core/provider/standard_models/equity_historical.py), [fetcher.py](https://github.com/openbq-org/OpenBB/blob/ae0268771f761b036996d81bd21522ce79d95415/openbb_platform/core/openbb_core/provider/abstract/fetcher.py).

### 2. ZhuLinsen/daily_stock_analysis

**Useful concept.** Distinguish valid strategy evidence, invalid opinions, diagnostics and subsequent outcomes.

**Inspected evidence.** The multi-strategy contract separates individual opinions from consensus, rejects invalid confidence values and describes immutable outcome records with explicit horizons and engine versions.

**Quant Lab adaptation.** Teach evidence provenance and disagreement. Show a strategy's own result separately from aggregate portfolio results; distinguish insufficient evidence from failure.

**Limits and corrections.** Agent consensus is not an independent statistical test. Its documented sample threshold is a project-specific reporting rule, not a universal minimum sample size for proving an edge. The reviewed file is a contract document; it does not independently establish that all corresponding runtime behavior is correct.

**Primary sources:** [multi-strategy-contract.md](https://github.com/ZhuLinsen/daily_stock_analysis/blob/ce364e457aab288863a5707e7b3df79786ad07f2/docs/multi-strategy-contract.md).

### 3. freqtrade/freqtrade

**Useful concept.** Turn leakage and indicator initialization into inspectable experiments.

**Inspected evidence.** Lookahead analysis compares baseline and altered runs. Its test strategy deliberately contrasts past shifts with future shifts. Recursive analysis varies the amount of startup history.

**Quant Lab adaptation.** Build a 'what was knowable then?' exercise and a warm-up comparison. Explain why precomputing a full dataframe is safe only when every feature uses information available at its decision time.

**Limits and corrections.** The diagnostics explicitly document false positives and false negatives; untriggered signals remain unchecked. Warm-up analysis compares the final indicator row and does not directly prove entry/exit stability. Crypto-specific defaults and exchange limits do not transfer to IBKR.

**Primary sources:** [lookahead-analysis.md](https://github.com/freqtrade/freqtrade/blob/a859a8f6e02133be0e291db685a5cb92438fb505/docs/lookahead-analysis.md), [recursive-analysis.md](https://github.com/freqtrade/freqtrade/blob/a859a8f6e02133be0e291db685a5cb92438fb505/docs/recursive-analysis.md), [strategy_test_v3_with_lookahead_bias.py](https://github.com/freqtrade/freqtrade/blob/a859a8f6e02133be0e291db685a5cb92438fb505/tests/strategy/strats/lookahead_bias/strategy_test_v3_with_lookahead_bias.py).

### 4. microsoft/qlib

**Useful concept.** Represent research as a reproducible sequence of data processing, training, inference and portfolio evaluation.

**Inspected evidence.** Workflow documentation and the LightGBM configuration declare separate fit, train, validation and test ranges, a benchmark, transaction costs, and signal/portfolio reporting records.

**Quant Lab adaptation.** Give every experiment a manifest. Display fit dates separately from evaluation dates and compare prediction quality with costed portfolio results.

**Limits and corrections.** A configuration file is not proof that every custom processor avoids leakage. The benchmark is market-specific and its cost/price assumptions must be reconsidered for the instrument and decision clock. Predictive accuracy alone is not trading profitability.

**Primary sources:** [workflow.rst](https://github.com/microsoft/qlib/blob/be725493eb1a6bbb42bf11b37aa7669f59610ff1/docs/component/workflow.rst), [workflow_config_lightgbm_Alpha158.yaml](https://github.com/microsoft/qlib/blob/be725493eb1a6bbb42bf11b37aa7669f59610ff1/examples/benchmarks/LightGBM/workflow_config_lightgbm_Alpha158.yaml).

### 5. HKUDS/Vibe-Trading

**Useful concept.** Teach the difference between proposed allocations and allocations that satisfy portfolio constraints.

**Inspected evidence.** The constraint layer works on magnitudes of signed weights, preserves signs, applies constraints in configuration order, and includes tests for infeasible caps, redistribution and group exposure.

**Quant Lab adaptation.** Add worked examples for long/short gross exposure, sector caps, feasibility and final invariant checks. Compare a proposed portfolio with its risk-adjusted portfolio.

**Limits and corrections.** Do not treat the presence of agents as evidence of profitable automation. Sequential constraints can interact: a later redistribution can undo an earlier group cap. Check the final portfolio against every invariant rather than assuming each local adjustment guarantees the whole system.

**Primary sources:** [constraints.py](https://github.com/HKUDS/Vibe-Trading/blob/7f6908b7e1b95d971f4151bfaf2382e2ce9485cf/agent/backtest/constraints.py), [test_constraints.py](https://github.com/HKUDS/Vibe-Trading/blob/7f6908b7e1b95d971f4151bfaf2382e2ce9485cf/agent/tests/test_constraints.py), [correlation.py](https://github.com/HKUDS/Vibe-Trading/blob/7f6908b7e1b95d971f4151bfaf2382e2ce9485cf/agent/backtest/correlation.py).

### 6. Fincept-Corporation/FinceptTerminal

**Useful concept.** Use consistent result contracts to compare experiments across engines.

**Inspected evidence.** The base provider defines separate performance, trades, equity, fees, slippage, logs and execution status. Its integration document checks that frontend identifiers and parameters match the Python provider.

**Quant Lab adaptation.** Create one research-result vocabulary: equity, drawdown, turnover, costs and trade records. Display which metrics are unavailable rather than substituting invented values.

**Limits and corrections.** A broad terminal is not a beginner learning sequence. Similar field names do not guarantee identical metric definitions across engines. Some fields are non-optional in the inspected dataclasses; Quant Lab should explicitly represent undefined metrics. GitHub's license metadata is inconclusive, so reuse requires inspecting the applicable license.

**Primary sources:** [base_provider.py](https://github.com/Fincept-Corporation/FinceptTerminal/blob/3f444cb7ab712d85a57d270d5edd6e7a2ef50d55/fincept-qt/scripts/Analytics/backtesting/base/base_provider.py), [backtesting-provider-process.md](https://github.com/Fincept-Corporation/FinceptTerminal/blob/3f444cb7ab712d85a57d270d5edd6e7a2ef50d55/fincept-qt/docs/backtesting-provider-process.md).

### 7. wilsonfreitas/awesome-quant

**Useful concept.** Use a classified index to discover specialist tools and references.

**Inspected evidence.** The README is a catalogue spanning quantitative libraries and resources, rather than one trading engine or tutorial application.

**Quant Lab adaptation.** Maintain a small reference library organized by learning objective, prerequisite and evidence type. Link a library only when the learner has a concrete task for it.

**Limits and corrections.** A directory entry is a lead, not validation. Inspect the primary project before adopting its methods, and avoid a dependency list that overwhelms the curriculum. This repository does not provide a single runnable learning platform to copy.

**Primary sources:** [README.md](https://github.com/wilsonfreitas/awesome-quant/blob/48e48a76b2054b5fe6eede6852ffef7783b992ce/README.md).

### 8. mementum/backtrader

**Useful concept.** Expose event flow, multi-feed timing and order state in worked examples.

**Inspected evidence.** The unaligned multi-data sample prints feed timestamps and lengths, uses one feed for a signal and another for trading, and handles submitted, completed, cancelled, expired and margin-related order states.

**Quant Lab adaptation.** Teach a signal/order/fill timeline and a two-feed alignment exercise before adding multi-asset strategies. Explain that an order request is not a completed trade.

**Limits and corrections.** Different feed lengths are not automatically an error or alignment proof. The sample is illustrative; it does not establish that an economically meaningful correlation or usable edge exists. The repository's latest push is much older than several other ranked projects; verify environment compatibility before adopting runtime code.

**Primary sources:** [multidata-strategy-unaligned.py](https://github.com/mementum/backtrader/blob/b853d7c90b6721476eb5a5ea3135224e33db1f14/samples/multidata-strategy/multidata-strategy-unaligned.py).

### 9. QuantConnect/Lean

**Useful concept.** Preserve bar interval semantics, strategy attribution and distinct risk layers.

**Inspected evidence.** TradeBar derives its end time from start time plus period. CompositeAlphaModel preserves or assigns each insight's source model. CompositeRiskManagementModel applies models sequentially to portfolio targets.

**Quant Lab adaptation.** Build data-availability exercises and a multi-strategy attribution table. Teach alpha generation, capital allocation, risk adjustment and execution as separate stages.

**Limits and corrections.** Combining alpha outputs does not automatically resolve capital conflicts or prove diversification. Sequential risk models need final invariant checks. Use concepts that fit the current lesson; do not import the entire engine into a small teaching app.

**Primary sources:** [TradeBar.cs](https://github.com/QuantConnect/Lean/blob/705b9551be1aaa821c7f77896a7eb8fcd07b92ee/Common/Data/Market/TradeBar.cs), [CompositeAlphaModel.cs](https://github.com/QuantConnect/Lean/blob/705b9551be1aaa821c7f77896a7eb8fcd07b92ee/Algorithm/Alphas/CompositeAlphaModel.cs), [CompositeRiskManagementModel.py](https://github.com/QuantConnect/Lean/blob/705b9551be1aaa821c7f77896a7eb8fcd07b92ee/Algorithm/Risk/CompositeRiskManagementModel.py).

### 10. stefan-jansen/machine-learning-for-trading

**Useful concept.** Make the research protocol the curriculum spine and investigate why a result fails.

**Inspected evidence.** The cross-validation notebook distinguishes decision-time admissibility, chronological splits, overlapping labels and different buffers. The cost-sensitivity notebook varies per-leg cost while holding the strategy and protocol fixed.

**Quant Lab adaptation.** Teach one reproducible baseline from data through costed evaluation. Add split timelines, cost sensitivity and a written interpretation of each experiment.

**Limits and corrections.** This review uses the current third-edition revision; older links may describe the second edition. Advanced libraries, large datasets and complex case studies should remain optional. Purging and embargo must follow actual sample information intervals, not an arbitrary universal number of days.

**Primary sources:** [02_cv_foundations.py](https://github.com/stefan-jansen/machine-learning-for-trading/blob/07a170d957fa602ae27d0590e738b88a52ba94cd/06_strategy_definition/02_cv_foundations.py), [14_cost_sensitivity.py](https://github.com/stefan-jansen/machine-learning-for-trading/blob/07a170d957fa602ae27d0590e738b88a52ba94cd/16_strategy_simulation/14_cost_sensitivity.py).

## User-supplied reference: Quantum Trader by Zohar Babin

[Quantum Trader](https://github.com/zoharbabin/quantum-trader) has 55 stars at lookup. It is included for relevance, independently of the popularity ranking.

Its course configuration separates levels, tutorial pages, quizzes and practical exercises. Topic-level checkpoints provide a simple, useful content model. Its progress engine stores checked items in the browser. These are good references for navigation, course organization and continuity between visits.

The content still needs critical review. The basic-risk tutorial recommends fixed percentage ranges and minimum reward/risk ratios without establishing their suitability for a particular strategy. Treat those as illustrative settings, never universal rules. Risk expressed as planned stop distance is not a guaranteed realized loss: gaps, slippage and inability to exit can increase it.

A technical-analysis quiz treats crossing a Bollinger Band as primarily establishing increased volatility. A crossing can occur because of a large move, a narrow band or both; the crossing alone does not establish that estimated volatility rose, nor that reversal is imminent. The revised materials ask the learner to distinguish an observation from a forecast.

The inspected portfolio-exposure helper divides the proposed trade's notional by portfolio value. It does not include existing holdings in that helper. That is a useful counterexample: naming a check 'portfolio exposure' does not prove that it constrains aggregate portfolio exposure. A teaching exercise should calculate existing positions plus proposed orders, use gross and net exposure separately, and recheck the result.

Reading-progress checkboxes are not evidence of quantitative competence. Keep 'read' separate from 'exercise verified'. Store only the course's own keys, tolerate unavailable browser storage and version progress when a lesson changes. The inspected reset function clears all browser local storage, a behavior Quant Lab should avoid.

Primary sources: [course.json](https://github.com/zoharbabin/quantum-trader/blob/3b2e37a02313e82ce9de67e33d518b3705d327d4/training/courses/quantum-trading/course.json), [progress.js](https://github.com/zoharbabin/quantum-trader/blob/3b2e37a02313e82ce9de67e33d518b3705d327d4/training/src/engine/progress.js), [basic-risk.md](https://github.com/zoharbabin/quantum-trader/blob/3b2e37a02313e82ce9de67e33d518b3705d327d4/training/courses/quantum-trading/content/tutorials/basic-risk.md), [technical-analysis-quiz.json](https://github.com/zoharbabin/quantum-trader/blob/3b2e37a02313e82ce9de67e33d518b3705d327d4/training/courses/quantum-trading/content/exercises/technical-analysis-quiz.json), [risk_validator.py](https://github.com/zoharbabin/quantum-trader/blob/3b2e37a02313e82ce9de67e33d518b3705d327d4/src/trading/agents/risk_validator.py), [test_risk_validator.py](https://github.com/zoharbabin/quantum-trader/blob/3b2e37a02313e82ce9de67e33d518b3705d327d4/tests/test_risk_validator.py).

## Additional teaching and correctness references

These sources complement the top ten because they address concrete gaps. They are not silently substituted into the popularity ranking.

| Reference | Inspected material | What to retain | What to qualify |
|---|---|---|---|
| [NautilusTrader](https://github.com/nautechsystems/nautilus_trader/blob/aef5cbe8fee4ea0ffe7dfc57dbce19e1a8eb3082/docs/concepts/backtesting/bar-execution.md) | Bar execution documentation | Distinguish event time from availability; explain unknown intrabar path | Synthetic OHLC paths are simulator assumptions, not recovered historical trade order |
| [Zipline](https://github.com/quantopian/zipline/blob/014f1fc339dc8b7671d29be2d85ce57d3daec343/zipline/finance/slippage.py) | Slippage model source | Volume limits, partial fills, impact and limit-price checks | OHLCV alone cannot guarantee a fill; market-specific assumptions matter |
| [VectorBT](https://github.com/polakowo/vectorbt/blob/ceffc501f2d37033a79dd86a9f883e69ec6977bd/examples/WalkForwardOptimization.ipynb) | Walk-forward notebook | Separate rolling training and test windows; compare baselines | The example selects parameters by Sharpe and uses external data; replicate the idea offline and retain all trials |
| [backtesting.py](https://github.com/kernc/backtesting.py/blob/ca2e2611621e472542ba90f7243a1fa06a7d7108/backtesting/backtesting.py) | Strategy and broker source | Gradual visibility, warm-up, orders and fee assumptions | Different indicator lookbacks can change the start date, making comparisons unfair |
| [QuantStats](https://github.com/ranaroussi/quantstats/blob/9ef4c6d0a4ffe7831f6ebba6a5824fd33a90c05a/quantstats/stats.py) | Return, Sharpe and pairing functions | Compounding, matching observations, explicit frequency and risk-free convention | A convenience equity-curve function fills missing returns with zero; that policy must not silently become a data-quality rule |
| [Quantopian lectures](https://github.com/quantopian/research_public/blob/e183ecd093efbebce9b0febdc7d0253159c04061/notebooks/lectures/Hypothesis_Testing/notebook.ipynb) | Hypothesis-testing notebook | Explanation, experiment and interpretation as a lesson pattern | Update old environment/API assumptions and correct any wording that turns a p-value into the probability the hypothesis is true |
| [QuantConnect tutorials](https://github.com/QuantConnect/Tutorials/blob/4a341890296f7e79e095508f06170c72ccaa629c/05%20Introduction%20to%20Financial%20Python%5B%5D/05%20Pandas-Resampling%20and%20DataFrame/03%20Resampling.html) | Resampling lesson | Explain aggregation with small examples | Rewrite legacy syntax and compare consecutive period-end prices; an within-month endpoint ratio is not the previous-close-to-current-close return |
| [Nick McCullum course](https://github.com/nickmccullum/algorithmic-trading-python/blob/e1e3c2e586188a9222d3de61849cfeef29d3d28a/finished_files/002_quantitative_momentum_strategy.ipynb) | Momentum notebook | Small end-to-end ranking and allocation exercise | It uses an IEX sandbox API and old pandas calls; a ranking/trade worksheet is not a historical validation of momentum |

## Design decisions for Learn

1. Each lesson starts with a specific question, then intuition, a precise definition, a tiny worked example, a falsifiable experiment and an explanation of failure cases.
2. Keep the first labs offline and deterministic. They teach measurement and mechanics without external accounts or market-data entitlements. Clearly label synthetic data.
3. Show the raw rows behind a chart. Include instrument identity, currency, interval, timezone, adjustment policy, source and availability assumptions.
4. Put a reference next to the relevant concept; avoid a giant undifferentiated resource list. Keep primary sources and original explanations distinguishable.
5. Use quizzes to detect misconceptions, not memorization of indicator defaults. Give an explanation for wrong answers and ask for a small calculation or reasoning step.
6. Reading and quiz completion are learning progress. They do not unlock broker connectivity, paper execution or live orders. Operational capabilities depend on tested implementation milestones.
7. Record every research trial, including failures. A best historical parameter is a selected result, not validation.
8. Multi-strategy lessons must show common exposure, shared capital, conflicts, gross/net exposure and attribution. More strategies or agents does not imply more independent evidence.
9. The initial material should teach the existing data contract before adding frameworks. Keep vendor objects outside domain and strategy code.
10. Use browser interaction for inspection and learning. Canonical quantitative transformations and trading rules stay in Python, as required by the repository's architecture.

## Content delivery and next implementation slice

The implemented slice is Lesson 1: original explanations, worked return examples, a deterministic Python-generated experiment, explicit cost comparisons, a flawed backtest to critique, and explained checkpoint answers. Correct answers determine saved progress. It requires no external LLM API, broker setup or new financial-data provider. The [lab guide](../lesson-01-lab-guide.md) describes regeneration and limitations.

The video recommendations were recovered. Selected QuantInsti workshop transcript sections informed the cost discussion; a full visual/code audit of all recommended videos is still pending. Inspection depth is recorded in the [Lesson 1 source review](../lesson-01-source-review.md).

## Broader specialist inspection

Discovery extended beyond the popularity ranking and Quantum Trader using algo-trading and quantitative-investment topics and text searches for learning, multi-strategy trading and portfolio/risk management. Eight further specialist repositories were inspected at the scope described below. This stage brought the inventory to 27 repositories and 43 selected files; TradeMaster and the Lesson 1 LEAN trace subsequently brought it to 28 repositories and 54 selected files. These counts do not mean every file or capability has been audited.

- [pst-group/pysystemtrade](https://github.com/pst-group/pysystemtrade/blob/326b5d402c2825cc8561cabb899d1454e593bda9/docs/backtesting.md): Inspectable stages from forecasts to sizing and portfolio construction; use its worked research flow as a later multi-strategy reference.
- [PyPortfolio/PyPortfolioOpt](https://github.com/PyPortfolio/PyPortfolioOpt/blob/a6638d2e06dae6f444fd022cfd4b3c528902a85b/docs/RiskModels.rst): Covariance estimation, shrinkage and estimation uncertainty; compare equal weights with constrained alternatives rather than treating optimizer output as truth.
- [dcajasn/Riskfolio-Lib](https://github.com/dcajasn/Riskfolio-Lib/blob/7b1b26ac9760974c12ecefe290a9d3bd37b66b7a/docs/source/riskfoliolib/risk.rst): A specialist risk-function documentation entry point. This page delegates to generated API documentation; detailed risk-formula implementation has not yet been inspected.
- [AI4Finance-Foundation/FinRL](https://github.com/AI4Finance-Foundation/FinRL/blob/e60e26e4870f00fbc704c6297edfd9d81816b3d3/finrl/applications/stock_trading/ensemble_stock_trading.py): Declared training/evaluation windows, costs and ensemble setup. The example fills missing/infinite values with zero; do not transfer that convenience into Quant Lab's data-quality policy.
- [hummingbot/hummingbot](https://github.com/hummingbot/hummingbot/blob/9af100d6822da7d2d0291a906c730ef172284ee2/hummingbot/strategy_v2/models/executor_actions.py): Explicit controller identity and create/stop/store executor actions; stopping an executor and keeping a position are separate choices.
- [vnpy/vnpy](https://github.com/vnpy/vnpy/blob/2ae433660477f9f6a10b0683603879e59072659f/docs/community/app/risk_manager.md): Pre-trade operational checks for order flow, single orders, active orders and cancellations. This is documentation inspection, not a test of the installed risk module.
- [nkaz001/hftbacktest](https://github.com/nkaz001/hftbacktest/blob/5f3ec40b2afb764e0fea112f941ed85523ef4e88/docs/order_fill.rst): Queue position and partial-fill assumptions; replay cannot change historical liquidity and therefore does not by itself model market impact.
- [stefan-jansen/alphalens-reloaded](https://github.com/stefan-jansen/alphalens-reloaded/blob/f0a07c22d554e4b4036983cc80320b432714fe7e/src/alphalens/performance.py): Spearman rank information coefficients by date and group. Factor prediction diagnostics need separate portfolio/cost analysis before economic claims.


## Added reference: TradeMaster (28th repository)

Selected portfolio environment and PRUDEX documentation inspected at revision 1747cc18db3fe2639af12defc80e138c51a625c0. The environment maps actions through softmax to cash plus long-only asset weights, uses separate train/validation/test paths, applies price-driven weight drift and a transaction fee. Useful teaching examples: drift-aware turnover and explicit action constraints. Audit caveats: fee turnover includes cash changes (cash-to-one-stock yields L1 distance 2); metrics hard-code 252 in Sharpe while displayed volatility is unannualized; risky-asset vectors rely on consistent row ordering. These require declared conventions and numerical verification before adoption. PRUDEX documentation says the evaluation tool is independent and not integrated in that pipeline; avoid treating a plotted evaluation dashboard as an automatically enforced protocol. No external test suite or profitability replication was run.

[Portfolio environment](https://github.com/TradeMaster-NTU/TradeMaster/blob/1747cc18db3fe2639af12defc80e138c51a625c0/trademaster/environments/portfolio_management/environment.py)
[Evaluation documentation](https://github.com/TradeMaster-NTU/TradeMaster/blob/1747cc18db3fe2639af12defc80e138c51a625c0/trademaster/evaluation/market_dynamics_labeling/PRUDEX_README.MD)

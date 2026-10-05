# Academic review — working evidence map

Research date: 5 October 2026. This is a developing literature review, not an exhaustive systematic review or a finding of a universally best trading strategy. Google Scholar's direct search page failed to load through the web tool; discovery continued through primary journal, author, NBER and arXiv sources. Do not describe this as a completed Scholar review. Full-text examination, replication and video review remain incomplete.

## What the evidence changes for Learn

Teach the entire decision process: information available at the decision time, estimation uncertainty, portfolio constraints, execution assumptions, costs, and honest evaluation. Separate a predictive indicator from an executable strategy. A higher forecast score does not automatically yield a better portfolio.

### Cost-aware portfolio learning

Jensen, Kelly, Malamud and Pedersen's **Machine Learning and the Implementable Efficient Frontier**, published in the Review of Financial Studies in 2026, connects flexible return prediction with portfolio choice incorporating trading costs. The relevant teaching target is out-of-sample risk and return after costs. Its empirical gains are conditional on its data and cost assumptions; its large-stock-universe infrastructure is demanding for a small investor. The journal search result supplied substantial model and conclusion excerpts, but the direct full-page retrieval failed. Full methods and replication inspection are pending. [Journal article](https://academic.oup.com/rfs/article/39/10/3035/8524346); [authors' replication repository](https://github.com/theisij/ml-and-the-implementable-efficient-frontier).

Gârleanu and Pedersen's published 2013 work provides an earlier foundation: costly trading and signal persistence affect how quickly a portfolio should move toward its target. This motivates a lesson comparing immediate rebalancing with gradual adjustment, using explicitly declared assumptions. The NBER abstract and publication record were inspected. [Primary record](https://www.nber.org/papers/w15205).

### Covariance estimation and portfolio risk

Ledoit and Wolf explain how estimation error in sample covariance can distort optimization and propose shrinkage. Teach sample covariance alongside shrinkage, concentration limits and a simple equal-weight baseline; compare realized held-out risk rather than presenting an estimated frontier as certain. The author-hosted abstract was inspected; a complete methods review remains pending. [Author paper](https://www.ledoit.net/honey.pdf).

Risk lessons should separately specify volatility, drawdown, tail losses, leverage, liquidity, and exposure aggregation. A stop distance or per-trade percentage is insufficient to describe an entire portfolio. These are curriculum design recommendations; they are not claims that the reviewed papers settle all risk definitions.

### Selection bias and replication

Bailey and López de Prado's 2014 **Deflated Sharpe Ratio** adjusts statistical assessment for selection among multiple trials and non-normal returns. The author-hosted PDF was inspected through its methods and example sections. Track unsuccessful experiments as well as the winning backtest. Applying an adjustment requires assumptions about the effective number and dependence of trials; it cannot repair bad data or an unrealistic simulator. [Author PDF](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf).

Chen and Zimmermann's 2022 **Open Source Cross-Sectional Asset Pricing** supplies reproducible predictor constructions and reports substantial replication of published findings. This is a useful counterweight to blanket claims that financial findings cannot replicate. Reproducing a historical statistical relationship still does not establish net tradability for this project's instruments and costs. The journal abstract and companion repository overview were inspected. [Journal](https://doi.org/10.1561/104.00000112); [companion code](https://github.com/OpenSourceAP/CrossSection).

### Recent research: retain as experiments

**Benchmarking Deep Time Series Models for Equity Portfolios** (June 2026) compares 15 architectures and reports preference-, market- and cost-sensitive rankings. Its baseline constrained portfolio comparison had negative net Sharpe at its 20-basis-point assumption. It is an arXiv preprint; only the abstract has been inspected. Teach it as a model-selection case study, not a consensus or a profitable strategy. [Preprint](https://arxiv.org/abs/2606.09420).

**From Knowing to Doing** (May 2026) studies historical-memory contamination in LLM trading evaluations and separates market/style exposure from stock-selection returns. Its reported results concern its CSI300 experiment. It is an arXiv preprint, inspected at abstract level; masking does not prove that every source of leakage has been removed. [Preprint](https://arxiv.org/abs/2605.28359).

**Intraday trading strategy selection under transaction costs with machine learning** appeared on 1 October 2026. The full article is accessible and confirms peer review; detailed examination of its methods, tables and selection protocol remains pending. Its novelty is a reason to investigate, not sufficient evidence to replace established validation practices. [Journal article](https://www.frontiersin.org/journals/applied-mathematics-and-statistics/articles/10.3389/fams.2026.1888767/full).

## Recommended conversion into learning material

1. Build source cards recording evidence level, actual inspection depth, data dates, universe, decision timing, costs, baselines, validation, limitations and companion code.
2. Create short lessons with one worked numerical example, a deliberate failure case, an exercise and an answer explanation. Separate established foundations from experimental methods.
3. Use one common research protocol across trend, momentum, mean reversion, pairs and factor strategies. Record parameters and failed trials; reserve final evaluation data.
4. Add portfolio labs comparing equal-weight, constrained optimization, shrinkage and strategy combinations under common costs. Evaluate shared exposures and stressed correlations rather than counting strategy names.
5. Introduce ML and reinforcement learning after learners can audit a conventional backtest. Require simple baselines, repeated seeds, cost sensitivity and attribution.

These are original curriculum recommendations. The academic evidence map is saved; expanded lessons, academic replication and a complete video review have not yet been completed.

# Kronos integration plan

Status: planned research and learning capability; no runtime integration implemented by this change.

## Immutable upstream reference

- Official repository: https://github.com/shiyu-coder/Kronos
- Source snapshot: [67b630e67f6a18c9e9be918d9b4337c960db1e9a](https://github.com/shiyu-coder/Kronos/tree/67b630e67f6a18c9e9be918d9b4337c960db1e9a)
- Default branch: `master`, not `main`.
- Latest default-branch commit checked on 2026-10-07: 67b630e67f6a18c9e9be918d9b4337c960db1e9a.
- Author and committer timestamp: 2026-04-13T12:38:49Z (14:38:49 Europe/Amsterdam).
- Commit: merge PR #243, preserving the batch dimension in tokenizer and predictor training.
- GitHub releases collection was empty when checked. This is a source snapshot, not a numbered release or a claim of tested compatibility.
- Code licence: MIT. Preserve upstream copyright and licence if code is redistributed. Model/tokenizer weights and datasets require separate licence/provenance verification.

Code and checkpoint versions are different. Before runnable experiments, record immutable Hugging Face revisions and file hashes for both model and tokenizer, plus dependency/runtime versions. Do not silently download moving weight revisions or automatically update the source pin.

## Placement and prerequisites

Add an advanced case study after Lesson 23, without renumbering existing lessons: Learn -> AI / Foundation Models -> Kronos. Require Lessons 1–3, 14–18 and 23: bar timing, costs, risk, chronological validation and experiment identity. Lesson 22 connects regime diagnostics; Lesson 24 can later study selection among validated signals.

Start with one instrument, one timeframe, a bounded horizon and Kronos-small (24.7M parameters, 512 context, matching base tokenizer). Mini (4.1M, 2048 context, 2k tokenizer) is an optional smaller comparison; base (102.3M) follows only if measurement justifies it. Large weights are not listed as open in the inspected model zoo. Measure latency/memory on actual CPU/GPU hardware; parameter count does not establish a hardware requirement or runtime SLA.

## Smallest architecture

Canonical historical bars -> isolated Python inference job -> versioned forecast artifact -> original signal rule -> portfolio/risk -> pinned LEAN backtest -> normalized Quant Lab report.

Kronos is a research model dependency, not a third financial-platform connector. IBKR and QuantConnect remain the two v1 connectors; LEAN remains the execution engine. React renders results and explanations; forecasting and financial transformations stay in Python. Begin with an optional separate environment/process and offline artifacts rather than a new always-running microservice. Model loading is outside LEAN's event callback.

The planned adapter accepts canonical instrument, available-at cutoff, completed OHLC bars, volume/amount policy, exchange calendar/timezone, forecast timestamps, lookback, horizon, sampler configuration and seed. It returns individual paths with path IDs and provenance, not vendor objects. The manifest includes source SHA, model/tokenizer revisions, data hash/range, decision time, input cutoff, seed, temperature/top-p/top-k, context/horizon, path count, runtime/device and elapsed inference time. Reject unsupported context sizes rather than relying on silent truncation.

OHLC is required; volume/amount are optional upstream. Inspect and expose the exact policy: absent volume is zero-filled; absent amount with volume is approximated as volume times mean OHLC. This approximation is not observed traded turnover. No future prices or volumes enter preprocessing; only calendar-known future timestamps are admissible. Validate finite values, ordering, session gaps, adjustment consistency, nonnegative volume and OHLC inequalities. Flag invalid generated bars and record any correction policy; never silently repair outcomes.

## Preserve uncertainty correctly

The pinned [predictor source](https://github.com/shiyu-coder/Kronos/blob/67b630e67f6a18c9e9be918d9b4337c960db1e9a/model/kronos.py) averages samples internally when sample_count > 1. Its returned DataFrame is not a collection of independent paths and cannot recover forecast percentiles.

Initial implementation should call predict with sample_count=1 repeatedly under recorded independent seeds, retaining each entire path. Later batching may optimize this only after equivalence checks. Compute terminal return per path, empirical probability of negative return, mean/median, quantiles and sampled tail loss. Pointwise fan-chart quantiles are not executable trajectories. Sampling probabilities are model-implied estimates, not calibrated guarantees; distinguish sampling dispersion from uncertainty about model correctness.

## Delivery slices and acceptance criteria

1. **Learning/source study:** original explanation of tokenization, autoregression and financial interpretation; tiny OHLC example; links to pinned README, model/kronos.py and examples/prediction_example.py. Show the difference between a forecast, a signal and a filled trade. The early lesson can use clearly labelled illustrative fixtures; never present them as real Kronos inference.
2. **Offline inference:** optional pinned environment and separately versioned weights; validated input adapter; seeded retained paths; saved manifest/artifacts. Verify cutoff causality by perturbing future data, timestamp alignment, missing fields, context rejection and seed behavior. Unit CI uses deterministic fixtures and a fake predictor; actual-weight smoke tests are explicit and optional.
3. **Forecast evaluation:** chronological walk-forward runs against last-close/random-walk and simple historical-return bootstrap baselines on identical data/cutoffs/horizons. Report price/return error, directional diagnostics, interval coverage/width and a proper probabilistic score such as CRPS; stratify by regime and timeframe. Account for overlapping horizons in splits and inference about results.
4. **LEAN experiment:** freeze an original long/flat rule with cost-aware thresholds selected only on training/validation, capped sizing and independent risk controls. Persist timestamped forecasts and consume them only after their information cutoff plus declared latency. Execute at the next admissible event with fees, spread/slippage and explicit fill assumptions. Compare against buy-and-hold, no-trade and simple strategies; report turnover, net returns, drawdown and exposure.
5. **Promotion review:** require untouched holdout, cost/parameter sensitivity, regime failure analysis and latency budget before paper eligibility. Fine-tuning is a separate later experiment with train-only fitting and distinct checkpoint lineage. Paper/live permissions do not follow from lesson completion.

Pretraining overlap is a specific limitation: chronological splits in Quant Lab do not prove the pretrained model never saw those dates/assets. Establish the checkpoint training cutoff/provenance where possible; otherwise label contamination unknown and favor prospective evaluation. Record all trials and failures rather than showing only a selected winning curve.

## Learning UI

A historical chart shows the decision cutoff, retained sample paths and p10/p50/p90 fan; controls expose horizon, lookback and seed/path count within bounded presets. Reveal realized outcomes only after the learner commits an interpretation. A second view connects forecast -> fixed signal -> LEAN order/fill -> costs/P&L. Display model provenance and empirical coverage alongside return metrics.

## Scope of this planning change

Only roadmap and design documentation are changed. No weights, datasets, upstream code, dependencies, broker connectivity or trading behavior are added. Existing lesson delivery and LEAN integration milestones retain priority. The five-repository benchmark review in AGENTS.md must run before the actual adapter/backtest implementation; the existing review is context, not a substitute for that future implementation gate.

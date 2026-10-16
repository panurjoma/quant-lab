# ADR 0001: Use LEAN as Quant Lab's external execution engine

- Status: Accepted
- Date: 2026-10-06
- Initial pin: `80e7843f645673bcbeaab963049f76f20f6785e1`

## Context

Building a credible trading engine requires correct event timing, security models, portfolio accounting, order state, brokerage behavior, fees, fills, slippage, corporate actions, statistics and live recovery. Reimplementing all of this would displace Quant Lab's learning and product goals.

LEAN already provides an open-source engine and a modular Algorithm Framework. Quant Lab additionally needs a simple teaching surface where every number can be checked by hand.

## Decision

Quant Lab remains an MIT-licensed control plane, course and research product. It integrates the Apache-2.0 LEAN engine behind a process/container adapter pinned by full commit SHA.

The early Python simulator remains an educational oracle, not a second production engine. It is used to expose causality, fills and accounting with tiny fixtures. LEAN becomes the execution reference used for scalable backtests and the route toward paper/live trading.

Quant Lab owns:

- finance-first lessons and source interpretation;
- hypotheses, strategies and versions;
- experiment/run specifications and provenance;
- orchestration, persistence, promotion and safety policy;
- normalized result contracts and UI.

LEAN owns, inside its boundary:

- algorithm event scheduling and data subscriptions;
- securities, cash, holdings and portfolio accounting;
- transaction/order processing;
- fee, fill, slippage, buying-power and settlement models;
- engine statistics and brokerage plugins.

## Integration style

The first integration is a pinned source/runtime contract, not a fork and not copied source. A separate Quant Lab fork is created only if an engine-level patch is unavoidable. Generic fixes should be proposed upstream.

QuantConnect Cloud is optional. Quant Lab's domain may not depend on a paid CLI/cloud tier, proprietary data or QuantConnect-specific UI state.

## Consequences

Benefits:

- mature execution semantics without hiding them from the learner;
- one route from research to IBKR paper/live;
- reproducible engine upgrades;
- clear licensing and vendor boundary.

Costs:

- C#/.NET and Python interop must be tested;
- engine output needs normalization;
- a pinned snapshot needs security and compatibility updates;
- differences between the teaching simulator and LEAN must be explained.

## Validation gate

Before a strategy becomes paper-eligible, run a golden scenario through the Python teaching oracle and pinned LEAN engine. Reconcile decision timestamps, orders, fills, fees, cash, holdings, equity and drawdown. Any difference must be expected, documented and financially interpreted.

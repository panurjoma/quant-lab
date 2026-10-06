# LEAN integration contract

Quant Lab pins the open-source QuantConnect LEAN engine at `80e7843f645673bcbeaab963049f76f20f6785e1` (captured 2026-10-06).

## Why a commit pin instead of “latest”

GitHub's latest LEAN release object is `v2.4.0.1` from 2017, while development continues on `master`. A full commit SHA is therefore the reproducible representation of the current engine state. Runtime tooling must read `lean.lock.json`; it must not silently pull moving `master` or an unpinned `latest` image.

## Boundary

Quant Lab will invoke LEAN as a supervised external process/container. The adapter will:

1. accept a versioned Quant Lab run specification;
2. materialize a LEAN project/configuration;
3. start the pinned engine;
4. stream structured status/log information;
5. collect orders, fills, holdings, equity, costs and statistics;
6. normalize them into Quant Lab result contracts;
7. attach engine commit, strategy version, data identity and configuration to the experiment manifest.

Credentials and account identifiers are runtime secrets and must never enter the repository or result artifacts.

## Initial run contract

Inputs eventually include strategy/version, environment, dates, instruments/universe, resolution, starting cash, parameters, data/provider selection, brokerage model and explicit fee/slippage/fill assumptions.

Outputs include lifecycle status, engine version, normalized orders/fills, holdings/cash/equity timeline, costs, drawdown/statistics, logs/warnings and artifact identities.

## Update policy

Updating the pin requires a dedicated PR that:

- reviews upstream changes since the previous SHA;
- checks licence/notice changes;
- rebuilds the engine image or checkout;
- runs adapter contract tests and golden strategies;
- compares order/fill/accounting/statistics behavior;
- documents migrations and intentional result changes.

The open-source engine is distinct from QuantConnect Cloud, LEAN CLI subscriptions and separately licensed datasets.

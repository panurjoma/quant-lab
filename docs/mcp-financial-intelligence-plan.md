# MCP financial intelligence — architecture and roadmap

**Status:** proposal only. No new runtime connector, credentials, paid service, or execution permission.

MCP (Model Context Protocol) is open-source tooling/protocol; **LSEG datasets are not thereby free**. Before selecting an LSEG MCP server verify its official status, source license, supported products, authentication, pricing, entitlements, caching and redistribution terms. Keep LSEG optional and disabled unless explicitly approved. Quant Lab v1 still has exactly two financial-platform connectors: IBKR and QuantConnect.

## Pre-decision architecture

```text
IBKR / QuantConnect market data       optional licensed news / fundamentals
              |                                      |
      Historical/Snapshot ports              News/Fundamentals ports
              |                                      |
              +---------- ingest + normalize --------+
                                   |
                 canonical instrument IDs + point-in-time metadata
                                   |
                 validate, deduplicate, freshness, provenance
                                   |
                     immutable intelligence snapshot
                                   |
                   features / AI research (advisory)
                                   |
                     strategy -> portfolio -> risk
                                   |
                       LEAN backtest / IBKR paper
                                   |
                     live only by separate approval
```

MCP is a read-only **infrastructure adapter** to approved tools, not a strategy dependency or an order-execution path. Use explicit `NewsProvider` and `FundamentalsProvider` interfaces alongside existing market-data ports. Normalize articles/events with source, URL, instrument IDs, publication, first-seen and **available-at** timestamps, revisions, hashes and licensing. Fundamentals require fiscal period, announcement/availability time, revision vintage and units. Decisions consume an immutable `FinancialIntelligenceSnapshot` containing provider IDs, as-of time, data quality and feature/model versions.

## Safety and research requirements

- In backtests require `available_at <= decision_time`; publication time alone does not prevent look-ahead bias.
- Quarantine stale, duplicated, malformed, ambiguous or unauthorized data; record missing coverage and fallback policy.
- Treat news text and MCP tool output as untrusted data, not instructions. Allowlist read-only tools; set timeouts, rate limits, retries and audit trails.
- No LLM/MCP direct broker orders; independent deterministic risk and kill-switch controls remain mandatory.
- No proprietary payloads, credentials or redistributable assumptions committed to Git.
- Evaluate news/fundamental features against price-only baselines using chronological splits, realistic costs, ablations and provenance.

## Prerequisite-driven plan

1. **Data foundations:** specify ports, availability timestamps and synthetic offline news/fundamentals fixtures without adding a third v1 provider.
2. **Research:** mock local MCP client/server contract, deterministic ingestion, point-in-time snapshots, tests for revisions, leakage, missing entitlements and outages.
3. **AI research:** optional evidence-linked news summarization and feature generation; measure whether it adds predictive value; advisory only.
4. **Observation:** optional read-only MCP source behind feature flag with source licensing, entitlement checks and health telemetry.
5. **LSEG evaluation gate:** verify actual MCP server implementation and license plus LSEG dataset commercial terms; use only after explicit approval. Prefer free, properly licensed alternatives where feasible.
6. **Paper:** feed validated snapshots into existing strategy, LEAN research and IBKR paper workflows. No automatic live promotion.

Acceptance: offline CI without credentials/network; canonical timestamps and provenance on every decision; deterministic replay and leakage tests; provider failure cannot silently introduce stale news; existing lessons unaffected.

# Lesson 1 — Market Data, Returns & Research Environment

## Why this exists
A strategy cannot be more trustworthy than the information it consumes. Before predicting anything, Quant Lab needs a precise vocabulary for instruments, prices and time.

## Learning objectives
By the end of this lesson you should be able to explain an OHLCV bar, distinguish a vendor ticker from canonical instrument identity, explain why timestamps must be explicit, calculate simple/log returns, and reject malformed time series.

## Core ideas
An OHLCV bar summarizes **open, high, low, close and volume** over a stated interval. It is an aggregation, not the complete sequence of trades inside the interval.

A ticker such as `AAPL` is not enough as durable identity: venue, asset class and currency can matter. Quant Lab therefore maps vendor identifiers into its own canonical `Instrument`.

Time is part of the data. A timestamp without timezone is ambiguous. Later, decision-time rules will also determine whether a bar was actually knowable when a strategy acted.

## Returns
For consecutive prices `P[t-1]` and `P[t]`:

- simple return: `r[t] = P[t] / P[t-1] - 1`
- log return: `g[t] = ln(P[t] / P[t-1])`

Example: 100 → 110 gives a simple return of 10% and log return of about 9.53%.

## Data-quality checks
Quant Lab rejects non-finite/non-positive prices, negative volume, impossible OHLC relationships, duplicate bars and out-of-order bars. Missing bars require an explicit policy rather than silent invention.

## Raw vs adjusted prices
Splits and distributions can make raw historical prices jump even when investor economics did not change by the same amount. We introduce the distinction here; corporate-action processing is expanded when real providers are connected.

## Experiment
Use `data/lesson-01/sample_bars.csv`. Inspect the close series, calculate both return definitions, and verify the 100 → 110 example manually before trusting the function.

## Challenge
1. Why is a timestamp without timezone dangerous?
2. If a daily bar closes at 16:00, can a strategy placing an order at 15:59 use that close?
3. Why can two providers legitimately return different-looking historical price series around a stock split?

## Capability unlocked
The application can now represent, validate and visualize deterministic historical bars and calculate returns. Real-time data, external connectors and execution remain locked.

# Lesson 1 — Market Data, Returns & Research Environment

## Why this exists
A strategy cannot be more trustworthy than the information it consumes. Before predicting anything, Quant Lab needs a precise vocabulary for instruments, prices and time.

## Learning objectives
By the end of this lesson you should be able to explain an OHLCV bar, distinguish a vendor ticker from canonical instrument identity, explain why timestamps must be explicit, calculate simple/log returns, and reject malformed time series.

## Core ideas
An OHLCV bar summarizes **open, high, low, close and volume** over a stated interval. It is an aggregation, not the complete sequence of trades inside the interval. Quant Lab stores the bar's start timestamp **and duration**, so the interval end is explicit; the full bar is not knowable until that end.

A ticker such as `AAPL` is not enough as durable identity: venue, asset class and currency can matter. Quant Lab therefore maps vendor identifiers into its own canonical `Instrument`.

Time is part of the data. A timestamp without timezone is ambiguous. Later, decision-time rules will also determine whether a bar was actually knowable when a strategy acted.

## Returns
For consecutive prices `P[t-1]` and `P[t]`:

- simple return: `r[t] = P[t] / P[t-1] - 1`
- log return: `g[t] = ln(P[t] / P[t-1])`

Example: 100 → 110 gives a simple return of 10% and log return of about 9.53%.

## Missing-data policy
A gap is not automatically zero activity and must not be silently forward-filled. Mature research systems make alignment/fill policy explicit. Quant Lab starts conservatively: validation detects structural problems and later provider/session-aware lessons will decide whether a timestamp is actually missing.

## Data-quality checks
Quant Lab rejects non-finite/non-positive prices, negative volume, impossible OHLC relationships, duplicate bars and out-of-order bars. Missing bars require an explicit policy rather than silent invention.

## Raw vs adjusted prices
Splits and distributions can make raw historical prices jump even when investor economics did not change by the same amount. We introduce the distinction here; corporate-action processing is expanded when real providers are connected.

## Experiment
Use `data/lesson-01/sample_bars.csv`. Inspect the close series, calculate both return definitions, and verify the 100 → 110 example manually before trusting the function.

The Learn interface provides five navigable chapters, an interval/availability inspector, three compounding examples, a cost-sensitive causal-versus-biased experiment, and five questions with answer feedback. See the [worked lab guide and answer rubric](lesson-01-lab-guide.md) and [source review with an end-to-end LEAN trace](lesson-01-source-review.md).

This small experiment is a didactic preview of later statistics/backtesting lessons. It uses invented bars and does not establish a validated trading strategy. Python generates the results; React presents them through a versioned offline data contract.

## Challenge
1. Why is a timestamp without timezone dangerous?
2. If a daily bar closes at 16:00, can a strategy placing an order at 15:59 use that close?
3. Why can two providers legitimately return different-looking historical price series around a stock split?

## Capability unlocked
The application can now represent, validate and visualize deterministic historical bars and calculate returns. Real-time data, external connectors and execution remain locked.


## Open-source implementation review
Before finalizing this lesson we compared the relevant market-data implementations in QuantConnect LEAN, NautilusTrader, Zipline, VectorBT and backtesting.py. The useful concepts retained for this small milestone were: persistent instrument identity rather than ticker-only identity; timezone-aware time-series; explicit bar interval/end semantics; explicit missing-data policy; immutable canonical domain records; and separation of provider data from strategy/research code.

We deliberately deferred exchange calendars, corporate-action engines, tick/quote hierarchies, symbol mapping histories and high-performance array/event machinery because Lesson 1 does not yet need them.
